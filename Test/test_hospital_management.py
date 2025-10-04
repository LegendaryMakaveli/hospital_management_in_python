from  unittest import TestCase
from doctors import Doctor
from patient import Patient
from queue import Queue


class TestDoctor(TestCase):

    def setUp(self):
        Doctor.clear_registry()

    def test_doctor_creation_and_getters(self):
        doc = Doctor("Dr. Smith", 1234567890)
        doc.set_department("Cardiology")
        doc.set_contact_info("123-456-7890")

        self.assertEqual(doc.get_name(), "Dr. Smith")
        self.assertEqual(doc.get_id(), "1234567890")
        self.assertEqual(doc.get_department(), "Cardiology")
        self.assertEqual(doc.get_contact_info(), "123-456-7890")
        self.assertTrue(doc.get_is_available())

    def test_invalid_doctor_id(self):
        with self.assertRaises(ValueError):
            Doctor("Dr. Smith", 12345)

    def test_invalid_department(self):
        doc = Doctor("Dr. Jones", 1234567890)
        with self.assertRaises(ValueError):
            doc.set_department("Astrology")

    def test_register_and_count_registry(self):
        doc = Doctor("Dr. Smith", 1234567890)
        doc.set_department("Cardiology")
        doc.register()

        self.assertEqual(Doctor.count_registry(), 1)
        self.assertIn("1234567890", Doctor.registry)

    def test_duplicate_doctor_registration(self):
        doc = Doctor("Dr. Smith", 1234567890)
        doc.set_department("Cardiology")
        doc.register()

        duplicate = Doctor("Dr. Clone", 1234567890)
        duplicate.set_department("Cardiology")
        with self.assertRaises(ValueError):
            duplicate.register()

    def test_doctor_availability_methods(self):
        doc = Doctor("Dr. Smith", 1234567890)
        doc.set_department("Cardiology")
        doc.register()

        self.assertTrue(doc.doctor_availability())
        Doctor.registry["1234567890"]["is_available"] = False
        self.assertFalse(Doctor.get_doctor_availability_by_id("1234567890"))

    def test_clear_registry(self):
        d1 = Doctor("Dr. Adria", 1111111111)
        d1.set_department("General")
        d1.register()
        Doctor.clear_registry()
        self.assertEqual(Doctor.count_registry(), 0)


class TestPatient(TestCase):

    def setUp(self):
        Patient.clear_patients()

    def test_valid_patient_creation(self):
        patient = Patient("Alice", 25, "alice@example.com", "heart pain")
        self.assertEqual(patient.get_name(), "Alice")
        self.assertEqual(patient.get_age(), 25)
        self.assertEqual(patient.get_email(), "alice@example.com")
        self.assertEqual(patient.get_problem(), "Heart pain")

    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            Patient("", 25, "a@b.com", "fever")

    def test_invalid_age(self):
        with self.assertRaises(ValueError):
            Patient("Alice", -5, "a@b.com", "fever")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            Patient("Alice", 25, "invalidemail", "fever")

    def test_invalid_problem(self):
        with self.assertRaises(ValueError):
            Patient("Alice", 25, "alice@example.com", "")

    def test_patient_tracking(self):
        self.assertEqual(Patient.count_patients(), 0)
        p = Patient("Bob", 30, "bob@example.com", "cold")
        self.assertEqual(Patient.count_patients(), 1)
        self.assertIn(p, Patient.patients)
        Patient.clear_patients()
        self.assertEqual(Patient.count_patients(), 0)


class TestQueue(TestCase):

    def setUp(self):
        Doctor.clear_registry()
        Patient.clear_patients()
        self.queue = Queue()


        doctor1 = Doctor("Dr. Smith", 1234567890)
        doctor1.set_department("Cardiology")
        doctor1.register()

        doctor2 = Doctor("Dr. Jones", 9876543210)
        doctor2.set_department("ENT")
        doctor2.register()

    def test_enqueue_and_peek(self):
        patient = Patient("Alice", 25, "alice@gmail.com", "heart pain")
        self.queue.enqueue(patient)
        self.assertEqual(self.queue.peek(), patient)
        self.assertEqual(self.queue.size(), 1)

    def test_enqueue_invalid_type(self):
        with self.assertRaises(TypeError):
            self.queue.enqueue("not a patient")

    def test_dequeue_order(self):
        patient1 = Patient("Alice", 25, "a@gmail.com", "heart pain")
        patient2 = Patient("Bob", 30, "b@gmail.com", "ear ache")
        self.queue.enqueue(patient1)
        self.queue.enqueue(patient2)
        first = self.queue.dequeue()
        self.assertEqual(first, patient1)
        self.assertEqual(self.queue.peek(), patient2)

    def test_assign_doctor_success(self):
        patient = Patient("Alice", 25, "a@gmail.com", "heart pain")
        self.queue.enqueue(patient)
        result = self.queue.assign_doctor()

        self.assertIn("doctor", result)
        self.assertIn("patient", result)
        self.assertEqual(result["assigned_department"], "Cardiology")

        doc_id = result["doctor"]["id"]
        self.assertFalse(Doctor.registry[doc_id]["is_available"])

    def test_assign_doctor_no_available(self):
        for doc in Doctor.registry.values():
            doc["is_available"] = False

        p = Patient("Alice", 25, "a@gmail.com", "heart pain")
        self.queue.enqueue(p)
        with self.assertRaises(LookupError):
            self.queue.assign_doctor()

    def test_assign_doctor_unknown_problem(self):
        patient = Patient("Alice", 25, "a@gmail.com", "unknown disease")
        self.queue.enqueue(patient)
        with self.assertRaises(LookupError):
            self.queue.assign_doctor()

    def test_clear_queue(self):
        patient = Patient("Alice", 25, "a@gmail.com", "heart pain")
        self.queue.enqueue(patient)
        self.queue.clear()
        self.assertTrue(self.queue.is_empty())

    def test_department_mapping(self):
        self.assertEqual(self.queue.get_department_for_problem("heart pain"), "Cardiology")
        self.assertIsNone(self.queue.get_department_for_problem("mystery illness"))


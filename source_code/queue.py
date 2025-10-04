from doctors import Doctor
from patient import Patient


class Queue:
    problem_to_department = {
        "heart pain": "Cardiology",
        "chest pain": "Cardiology",
        "ear ache": "ENT",
        "sore throat": "ENT",
        "broken bone": "Orthopedics",
        "joint pain": "Orthopedics",
        "skin rash": "Dermatology",
        "eczema": "Dermatology",
        "fever": "Pediatrics",
        "cold": "General",
        "headache": "General",
    }

    def __init__(self):
        self.queue = []

    def enqueue(self, patient):
        if not isinstance(patient, Patient):
            raise TypeError("Only Patient instances can be added to the queue")

        self.queue.append(patient)

    def dequeue(self):
        if not self.queue:
            return None
        return self.queue.pop(0)

    def peek(self):
        return self.queue[0] if self.queue else None

    def size(self):
        return len(self.queue)

    def is_empty(self):
        return len(self.queue) == 0

    def clear(self):
        self.queue = []

    def get_department_for_problem(self, problem):
        key = problem.strip().lower()
        return Queue.problem_to_department.get(key, None)

    def assign_doctor(self):
        if self.is_empty():
            raise ValueError("No patients in queue")

        patient = self.peek()
        department = self.get_department_for_problem(patient.get_problem())

        if department is None:
            raise LookupError(
                f"No department found for problem: {patient.get_problem()}"
            )

        for doc_id, doc_data in Doctor.registry.items():
            if (
                doc_data["department"] == department
                and doc_data["is_available"]
            ):

                Doctor.registry[doc_id]["is_available"] = False
                assigned_doctor = doc_data
                self.dequeue()
                return {
                    "doctor": assigned_doctor,
                    "patient": patient.to_dict(),
                    "assigned_department": department,
                }

        raise LookupError(f"No available doctor in department: {department}")

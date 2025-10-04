class Doctor:
    registry = {}
    departments = {"Cardiology", "ENT", "Orthopedics", "Pediatrics", "General", "Dermatology"}

    def __init__(self, name, id=None):
        self.id = None
        self.name = None
        self.department = None
        self.contact_info = None
        self.is_available = True

        self.set_name(name)
        if id is not None:
            self.set_id(id)

    def set_id(self, id_value):
        id_to_string = str(id_value)
        if not id_to_string.isdigit() or len(id_to_string) != 10:
            raise ValueError("Id must be a 10-digit number")
        self.id = id_to_string

    def get_id(self):
        return self.id


    def set_name(self, name):
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")
        self.name = name

    def get_name(self):
        return self.name


    def set_department(self, department):
        if not Doctor.is_valid_department(department):
            raise ValueError(
                f"Invalid department. Valid departments: {', '.join(Doctor.departments)}"
            )
        self.department = department

    def get_department(self):
        return self.department


    def set_contact_info(self, contact_info):
        self.contact_info = contact_info

    def get_contact_info(self):
        return self.contact_info

    def set_is_available(self, is_available):
        if not isinstance(is_available, bool):
            raise ValueError("isAvailable must be a boolean")
        self.is_available = is_available

    def get_is_available(self):
        return self.is_available

    def to_dict(self):
        return {
            "id": self.get_id(),
            "name": self.get_name(),
            "department": self.get_department(),
            "contact_info": self.get_contact_info(),
            "is_available": self.get_is_available(),
        }

    def register(self):
        if not self.id:
            raise ValueError("Doctor id is required to register")
        if self.id in Doctor.registry:
            raise ValueError(f"Doctor with id {self.id} is already registered")
        if not Doctor.is_valid_department(self.department):
            raise ValueError(
                "Doctor department must be one of the allowed departments before registering"
            )
        Doctor.registry[self.id] = self.to_dict()

    def get_profile(self):
        return self.to_dict()


    def doctor_availability(self):
        if self.id:
            entry = Doctor.registry.get(self.id)
            if entry is not None:
                return entry.get("is_available", None)
        return self.get_is_available()


    @staticmethod
    def get_doctor_availability_by_id(id_value):
        if not id_value:
            return None
        entry = Doctor.registry.get(str(id_value))
        if entry is None:
            return None
        return entry.get("is_available", None)

    @staticmethod
    def get_registered_doctor_by_id(id_value):
        if not id_value:
            return None
        return Doctor.registry.get(str(id_value))

    @staticmethod
    def register_doctor(new_doctor):
        if isinstance(new_doctor, Doctor):
            if not new_doctor.id:
                raise ValueError("Doctor id is required to register")
            if new_doctor.id in Doctor.registry:
                raise ValueError(f"Doctor with id {new_doctor.id} is already registered")
            if not Doctor.is_valid_department(new_doctor.get_department()):
                raise ValueError(
                    "Doctor department must be one of the allowed departments before registering"
                )
            Doctor.registry[new_doctor.id] = new_doctor.to_dict()
            return


        if not new_doctor or "id" not in new_doctor:
            raise ValueError("newDoctor must have an id to register")

        id_number = str(new_doctor["id"])
        if not id_number.isdigit() or len(id_number) != 10:
            raise ValueError("Id must be a 10-digit number")
        if not Doctor.is_valid_department(new_doctor.get("department")):
            raise ValueError(
                "Doctor department must be one of the allowed departments before registering"
            )
        if id_number in Doctor.registry:
            raise ValueError(f"Doctor with id {id_number} is already registered")

        Doctor.registry[id_number] = dict(new_doctor)

    @staticmethod
    def clear_registry():
        Doctor.registry = {}

    @staticmethod
    def count_registry():
        return len(Doctor.registry)

    @staticmethod
    def is_valid_department(dept):
        return isinstance(dept, str) and dept in Doctor.departments

class Patient:
    patients = []

    def __init__(self, name, age, email, problem):
        self.name = None
        self.age = None
        self.email = None
        self.problem = None

        self.set_name(name)
        self.set_age(age)
        self.set_email(email)
        self.set_problem(problem)

        Patient.patients.append(self)

    def set_name(self, name):
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")
        self.name = name

    def get_name(self):
        return self.name


    def set_age(self, age):
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive integer")
        self.age = age

    def get_age(self):
        return self.age


    def set_email(self, email):
        if not isinstance(email, str) or "@" not in email:
            raise ValueError("Invalid email format")
        self.email = email

    def get_email(self):
        return self.email


    def set_problem(self, problem):
        if not problem or not isinstance(problem, str):
            raise ValueError("Problem must be a non-empty string")
        self.problem = problem.strip().capitalize()

    def get_problem(self):
        return self.problem


    def to_dict(self):
        return {
            "name": self.get_name(),
            "age": self.get_age(),
            "email": self.get_email(),
            "problem": self.get_problem(),
        }


    @staticmethod
    def clear_patients():
        Patient.patients = []

    @staticmethod
    def count_patients():
        return len(Patient.patients)

    @staticmethod
    def get_all_patients():
        return [patient.to_dict() for patient in Patient.patients]

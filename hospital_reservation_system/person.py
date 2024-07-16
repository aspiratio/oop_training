class Human:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class Patient(Human):
    def __init__(self, name, patient_id, symptom):
        super().__init__(name)
        self._patient_id = patient_id
        self._symptom = symptom

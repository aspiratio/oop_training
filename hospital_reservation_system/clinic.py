class Clinic:
    def __init__(self):
        self._patient_list = []

    def show_waiting_count(self):
        waiting_count = len(self._patient_list)
        print(f"現在の待ち人数は{waiting_count}人です")

    def reserve(self, patient):
        if self._check_reserved(patient):
            print(f"{patient.name}さんは予約済です")
        else:
            self._patient_list.append(patient)
            print(f"{patient.name}さんの予約が完了しました")

    def diagnosis(self, patient_id=None):
        # 引数で患者が指定されたときは、その患者を優先して診察。指定がない時は、予約の早い患者を順に診察。
        if len(self._patient_list) == 0:
            print("患者がいません")

        if patient_id:
            for p in self._patient_list:
                if p._patient_id == patient_id:
                    self._patient_list.remove(p)
                    print(f"{p.name}さんを診察しました")
        else:
            patient = self._patient_list.pop(0)
            print(f"{patient.name}さんを診察します")

    def _check_reserved(self, patient):
        return patient in self._patient_list

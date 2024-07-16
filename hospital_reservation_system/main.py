from clinic import Clinic
from person import Patient

# インスタンスを作成する
myclinic = Clinic()

patient1 = Patient("佐藤", "111", "咳")
patient2 = Patient("田中", "222", "腹痛")
patient3 = Patient("鈴木", "333", "鼻水")
patient4 = Patient("山田", "444", "倦怠感")
patient5 = Patient("伊藤", "555", "下痢")

patients = [patient1, patient2, patient3, patient4, patient5]

# 患者を予約リストに追加する
for patient in patients:
    myclinic.reserve(patient)

# 予約人数を表示する
myclinic.show_waiting_count()

# 重複する一人を予約して「予約済です」のメッセージを確認する
myclinic.reserve(patient1)

# 診察メソッドを実行し、待ち人数が減ったことを確認する
myclinic.diagnosis()
myclinic.show_waiting_count()

# 診察メソッドに患者のIDを引数に与えて実行し、待ち人数が減ったことを確認する
myclinic.diagnosis("444")
myclinic.show_waiting_count()

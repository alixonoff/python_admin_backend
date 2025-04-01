import json
import os

ADMIN_FAYL = "admins.json"
USER_FAYL = "users.json"


# Ma'lumotlarni yuklash
def yuklash(fayl_nomi):
    if os.path.exists(fayl_nomi) and os.stat(fayl_nomi).st_size > 0:
        with open(fayl_nomi, "r", encoding="utf-8") as fayl:
            return json.load(fayl)
    return []


# Ma'lumotlarni saqlash
def saqlash(fayl_nomi, malumotlar):
    with open(fayl_nomi, "w", encoding="utf-8") as fayl:
        json.dump(malumotlar, fayl, ensure_ascii=False, indent=4)


# Parolni tekshirish
def parolni_tekshir():
    while True:
        parol = input("Parolni kiriting (8-16 belgi, harf va son bo‘lishi shart): ").strip()
        uzunlik = 8 <= len(parol) <= 16
        son_bor = any(i.isdigit() for i in parol)
        harf_bor = any(i.isalpha() for i in parol)

        if uzunlik and son_bor and harf_bor:
            return parol
        else:
            print("Xato! Parol 8-16 belgidan iborat bo‘lishi va harflar ham, sonlar ham bo‘lishi kerak!")


admins = yuklash(ADMIN_FAYL)
users = yuklash(USER_FAYL)

Super_admin = {
    "login": "admin2025",
    "parol": "parol2025"
}


def super_admin_menyu():
    while True:
        buyruq = input(
            "\n[Super Admin Menyu]\n"
            "1. Admin yaratish\n"
            "2. Admin sifatida kirish\n"
            "3. Foydalanuvchi sifatida kirish\n"
            "4. Chiqish\n"
            "Buyruqni tanlang: "
        ).strip()

        if buyruq == "1":
            admin = {
                "name": input("Adminning ismini kiriting: ").title(),
                "username": input("Admin username kiriting: ").strip(),
                "type": input("Admin turi (super/oddiy): ").strip(),
                "parol": parolni_tekshir()
            }

            if any(a["username"] == admin["username"] for a in admins):
                print("Bu username band! Boshqa tanlang.")
            else:
                admins.append(admin)
                saqlash(ADMIN_FAYL, admins)
                print(f"Admin muvaffaqiyatli yaratildi: {admin['name']}!")

        elif buyruq == "2":
            admin_menyu()

        elif buyruq == "3":
            user_menyu()

        elif buyruq == "4":
            print("Tizimdan chiqildi.")
            break

        else:
            print("Noto‘g‘ri buyruq!")


def admin_menyu():
    username = input("Admin username-ni kiriting: ").strip()
    admin = next((a for a in admins if a["username"] == username), None)

    if not admin:
        print("Bunday admin mavjud emas!")
        return

    parol = input("Parolni kiriting: ").strip()
    if admin["parol"] != parol:
        print("Xato! Parol noto‘g‘ri.")
        return

    print(f"Tizimga kirdingiz! Xush kelibsiz, {admin['name']}!")

    while True:
        buyruq = input(
            "\n[Admin Menyu]\n"
            "1. Foydalanuvchi yaratish\n"
            "2. Foydalanuvchi sifatida kirish\n"
            "3. Super admin sifatida kirish\n"
            "4. Chiqish\n"
            "Buyruqni tanlang: "
        ).strip()

        if buyruq == "1":
            user = {
                "name": input("Foydalanuvchi ismini kiriting: ").title(),
                "username": input("Foydalanuvchi username kiriting: ").strip(),
                "type": "user",
                "parol": parolni_tekshir()
            }

            if any(u["username"] == user["username"] for u in users):
                print("Bu username band! Boshqa nom tanlang.")
            else:
                users.append(user)
                saqlash(USER_FAYL, users)
                print(f"Foydalanuvchi muvaffaqiyatli yaratildi: {user['name']}!")

        elif buyruq == "2":
            user_menyu()

        elif buyruq == "3":
            super_admin_menyu()

        elif buyruq == "4":
            print("Admin menyudan chiqildi.")
            break

        else:
            print("Noto‘g‘ri buyruq!")


def user_menyu():
    username = input("Foydalanuvchi username-ni kiriting: ").strip()
    user = next((u for u in users if u["username"] == username), None)

    if not user:
        print("Bunday foydalanuvchi mavjud emas!")
        return

    parol = input("Parolni kiriting: ").strip()
    if user["parol"] != parol:
        print("Xato! Parol noto‘g‘ri.")
        return

    print(f"Tizimga kirdingiz! Xush kelibsiz, {user['name']}!")

    while True:
        buyruq = input(
            "\n[Foydalanuvchi Menyu]\n"
            "1. Super admin sifatida kirish\n"
            "2. Admin sifatida kirish\n"
            "3. Chiqish\n"
            "Buyruqni tanlang: "
        ).strip()

        if buyruq == "1":
            super_admin_menyu()

        elif buyruq == "2":
            admin_menyu()

        elif buyruq == "3":
            print("Foydalanuvchi menyudan chiqildi.")
            break

        else:
            print("Noto‘g‘ri buyruq!")


# Super admin login
while True:
    login = input("Super admin loginini kiriting: ").strip()
    if login != Super_admin["login"]:
        print("Xato! Login noto‘g‘ri!")
        continue

    parol = input("Parolni kiriting: ").strip()
    if parol != Super_admin["parol"]:
        print("Parol noto‘g‘ri!")
        continue

    print("\nSuper admin sifatida tizimga kirdingiz!")
    super_admin_menyu()
    break

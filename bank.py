import json
import random
import string
from pathlib import Path

class Bank:
    database = 'data.json'
    data = []

    @classmethod
    def load_data(cls):
        """Loads account data from the JSON file into memory."""
        try:
            db_path = Path(cls.database)
            if db_path.exists():
                with open(cls.database, 'r') as fs:
                    content = fs.read().strip()
                    cls.data = json.loads(content) if content else []
            else:
                cls.data = []
                cls._save_data()
        except Exception as err:
            cls.data = []

    @classmethod
    def _save_data(cls):
        """Saves current memory data back to data.json."""
        with open(cls.database, 'w') as fs:
            json.dump(cls.data, fs, indent=4)

    @classmethod
    def account_generator(cls):
        """Generates a random 7-character mixed string account ID."""
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)
        account_id = alpha + num + spchar
        random.shuffle(account_id)
        return "".join(account_id)

    @classmethod
    def create_account(cls, name, age, email, pin):
        if age < 18:
            return False, "Account creation failed: You must be at least 18 years old."
        if len(str(pin)) != 4:
            return False, "Account creation failed: PIN must be exactly 4 digits."

        account_no = cls.account_generator()
        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo": account_no,
            "Balance": 0
        }
        
        cls.data.append(info)
        cls._save_data()
        return True, info

    @classmethod
    def authenticate(cls, acc_number, pin):
        """Finds user data matching account number and PIN."""
        for user in cls.data:
            if user['accountNo'] == acc_number and user['pin'] == pin:
                return user
        return None

    @classmethod
    def deposit_money(cls, acc_number, pin, amount):
        user = cls.authenticate(acc_number, pin)
        if not user:
            return False, "Authentication failed. Invalid Account Number or PIN."
        
        if amount <= 0 or amount > 10000:
            return False, "Deposit failed: Amount must be between $1 and $10,000 per transaction."

        user['Balance'] += amount
        cls._save_data()
        return True, f"Successfully deposited ${amount}. New Balance: ${user['Balance']}"

    @classmethod
    def withdraw_money(cls, acc_number, pin, amount):
        user = cls.authenticate(acc_number, pin)
        if not user:
            return False, "Authentication failed. Invalid Account Number or PIN."

        if amount <= 0:
            return False, "Withdrawal failed: Enter a valid positive amount."

        if user['Balance'] < amount:
            return False, f"Insufficient funds. Current balance is ${user['Balance']}."

        user['Balance'] -= amount
        cls._save_data()
        return True, f"Successfully withdrew ${amount}. New Balance: ${user['Balance']}"

    @classmethod
    def update_details(cls, acc_number, pin, new_name, new_email, new_pin):
        user = cls.authenticate(acc_number, pin)
        if not user:
            return False, "Authentication failed. Invalid Account Number or PIN."

        if new_name.strip():
            user['name'] = new_name.strip()
        if new_email.strip():
            user['email'] = new_email.strip()
        if new_pin and len(str(new_pin)) == 4:
            user['pin'] = new_pin

        cls._save_data()
        return True, "Account details updated successfully!"

    @classmethod
    def delete_account(cls, acc_number, pin):
        user = cls.authenticate(acc_number, pin)
        if not user:
            return False, "Authentication failed. Invalid Account Number or PIN."

        cls.data.remove(user)
        cls._save_data()
        return True, "Account deleted successfully."
import json
import random
import string
from pathlib import Path

class Bank:
    database = 'data.json'
    data = []
    try:
        if Path(database).exists:
           with open(database) as fs:
              data = json.loads(fs.read())
        else:
          print("no such file exists")
    except Exception as err:
        print(f"The exception has occured as{err}")

    @classmethod
    def __update(cls):
       with open(cls.database , 'w') as fs:
           fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgenertor(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits , k=3)
        spchar = random.choices("!@#$%^&*" , k=1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)


    def Createaccount(self):
        info = {
            "name": input("Tell your name:- "),
            "age": int(input("Enter your age:- ")),
            "email": input("Tell your emailid:- "),
            "pin": int(input("enter your 4 digit pin:- ")),
            "accountNo":Bank.__accountgenertor(),
            "Balance": 0
        }
        if info['age'] < 18 or len(str(info['pin'])) !=4 :
            print("Sorry u can't create your account")

        else:
            print("Your account is successfully created")

            for i in info:
                print(f"{i} : {info[i]}")
            print("Please note down your account number")
            
            Bank.data.append(info)
            Bank.__update()

    def Depositmoney(self):
        accnumber = input("Enter your accountNo:")
        pin = int(input("Enter correct pin as well"))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("Soorrry no data found")
        else:
            amount = int(input("Enter the amount for deposit:"))
            if amount > 10000 or amount < 0:
                print("this is exceeding our bank policy")
            else:
                
                userdata[0]['Balance'] += amount
                Bank.__update()   

    def withdrawalMoney(self):
        accnumber = input("Enter your accountNo:")
        pin = int(input("Enter correct pin as well"))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if userdata == False:
            print("Soorrry no data found")
        else:
            amount = int(input("Enter the amount for withdrawal:"))
            if userdata[0]['Balance'] < amount:
                print("You donot have enough balance to withdraw")
            else:
                
                userdata[0]['Balance'] -= amount
                Bank.__update()     


    def showDetails(self):
        accnumber = input("Enter your accountNo:")
        pin = int(input("Enter correct pin as well"))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]
        print("Your details are as follows \n\n\n:")

        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")


    def updateDetails(self):
        accnumber = input("Enter your accountNo:")
        pin = int(input("Enter correct pin as well"))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]
        if userdata == False:
            print("Sorry no such data found")

        else:
            print("You can't change the age ,accountNo and Balance of the user")
            newData = {
                "name" : input("Please enter new name or press enter:"),
                "email":input("Please enter the new email"),
                "pin": input("Please enter new pin or press enter")

            }
            if newData["name"] == "":
                newData["name"] = userdata[0]["name"]

            if newData["email"] == "":
                newData["email"] = userdata[0]["email"]

            if newData["pin"] == "":
                newData["pin"] = userdata[0]["pin"]
            
            newData["age"] = userdata[0]["age"]

            newData["accountNo"] = userdata[0]["accountNo"]
            newData["Balance"] = userdata[0]["Balance"]

            if type(newData["pin"]) == str:
                newData["pin"] = int(newData["pin"])

            for i in newData:
                if newData[i] == userdata[0][i]:
                   continue
                else:
                    userdata[0][i] = newData[i]
            
            print("Details updated successfully")
            Bank.__update()
            


    def Delete(self):
        accnumber = input("Enter your accountNo:")
        pin = int(input("Enter correct pin as well"))

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]
        if userdata == False:
            print("no such data exists")

        else:
            check = input("press y if u really want to delete the account or press n")
            if check == 'n' or check == 'N':
                print("bypassed")
            else:
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("Account deleted successfully")
                Bank.__update()

        
user = Bank()

print("Press 1 for creating new account")
print("Press 2 to deposit money to account")
print("Press 3 for withdrawing the money ")
print("Press 4 for details")
print("Press 5 for updating the details")
print("Press 6 to delete the account")

check = int(input("tell your response :-"))

if check == 1:
    user.Createaccount()

if check == 2:
    user.Depositmoney()

if check == 3:
    user.withdrawalMoney()

if check == 4:
    user.showDetails()

if check == 5:
    user.updateDetails()

if check == 6:
    user.Delete()



from collections import UserDict
from datetime import datetime, timedelta
import re
# КЛАСИ ПРОЕКТУ

 
class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
		pass

class Phone(Field):
           
    def __init__(self, value):
        mask = r'\d{10}'
        if re.match(mask, value):
            super().__init__(value)
        else:
            raise ValueError ("Invalid phone number format. Use XXXXXXXXXX ")
        

class Birthday(Field):
    def __init__(self, value):
        try:
            mask = r'^\d{2}\.\d{2}\.\d{4}$'
            if re.match(mask, value):
                super().__init__(value)
            else:
                print ("Invalid date format. Use DD.MM.YYYY.")
               
            # та перетворіть? рядок на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")   

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_birthday(self):
        pass
    
    def edit_phone(self, old_phone, new_phone):
          for phone in self.phones:
            if phone.value==old_phone:
                phone.value=new_phone
    
    def find_phone(self, find_phone):
        for phone in self.phones:
            if phone.value==find_phone:
                return phone
        
    def remove_phone(self, rem_phone):
         for phone in self.phones:
            if phone.value==rem_phone:
                self.phones.remove(phone)          

    def add_phone(self, phone):
        self.phones.append(Phone (phone))
    
    def add_bithday (self, birthday):
        self.birthday=Birthday (birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def __init__(self):
        self.data={}
    
    def add_record(self, record):
           self.data[record.name.value]=record
    
    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None
    
    def delete(self, name):
          del self.data[name]
    def __str__(self):
        list=""
        for name in self.data:
            list = list+ f"Contact name: {name}, phones: {'; '.join(p.value for p in self.data[name].phones)} \n"
        return list

# ФУНКЦІЇ ПРОЕКТУ

# ОБРОБКА ПОМИЛОК
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please, or name and two phone - old and new."
        except KeyError:
            return "Нажаль такого абонента не існує, спробуйте точніше вказати імя"
        except IndexError:
            return "Нема такого заведи спочатку"
        except AttributeError:
            return "Даних не знайдено"

    return inner



def parse_input(user_input): # Парсер введених даних
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not find"
    else:
        record.add_bithday(birthday)
        if record.birthday.value:
            return "birthday added"
        else:
            return "Tru again"
@input_error
def show_birthday(args, book):
    name, *_ = args
    return book.find(name).birthday.value
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Блок коду що відображає дні народження на тиждень вперед за запросом.

def get_list_of_week(): # формуємо список дат днів на найближчі 7 днів від поточної дати
    week=[]
    delta = timedelta(days=1)
    week.append(datetime.now().strftime("%d.%m."))
    for i in range (1,7):
        week.append((datetime.now()+delta*i).strftime("%d.%m."))
        
    return week

def get_list_of_weekend_and_monday(): # В цьому блоці формуємо списки для дат суботи та неділі на поточному тижні, а також вираховуємо дату найближчого понеділка, нвіть якщо він не на поточному тижні.
    weekend=[]
    monday=[]
    delta = timedelta(days=1)
    for i in range (8):
        if ((datetime.now()+delta*i).weekday())>=5:
            weekend.append((datetime.now()+delta*i).strftime("%d.%m."))
        if len(weekend)==2 and ((datetime.now()+delta*i).weekday())==0:
            monday.append((datetime.now()+delta*i).strftime("%d.%m."))
    return weekend, monday

def we_hawe_birthday_in_weekend(data, weekend): # Перевіряємо чи не на вихідний припадає дата
    if str(data[:6]) in weekend:
        return True
    else:
        print("data:", data)
        print("weekend:", weekend)
        return False

def we_have_birthday(data, week): # Перевіряємо чи на цьому тижні є іменинники просто порівнюючи певну дату із списком.
    if str(data[:6]) in week:
        return True
    else:
        print ("data:", str(data[:6]))
        print ("week:", week)
        return False
    
# Основна функція
@input_error
# Сюди звертаємось коли хочемо отримати список поздоровлень
def birthdays(book):  # Основна функція  - з неї робим виклики відповідних блоків коду, формуємо список словників з датами поздоровлень
    week=get_list_of_week()
    weekend, monday=get_list_of_weekend_and_monday()
    congratulations=[]
    for name in book.data.keys():
        user = {}
        if we_have_birthday(book.find(name).birthday.value, week):
            if we_hawe_birthday_in_weekend(book.find(name).birthday.value, weekend ):
                user["name"]=name
                user["congratulations_date"]=(datetime.now().strftime("%Y")) + monday[0]
                congratulations.append(user)
            else:
                user["name"]=name
                user["congratulations_date"]= book.find(name).birthday.value[:6]+(datetime.now().strftime("%Y")) 
                congratulations.append(user)
    return congratulations

# # # # # # # # # # # # # # # # # # # # # # 


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, contacts):
    name, old_phone, new_phone, *_ = args
    contacts.find(name).edit_phone(old_phone, new_phone)
    return "Contact changed"

@input_error
def show_phone(contacts):
    return f"Contacts list:\n{contacts}"

@input_error
def find_phone(name, contacts):
    name, *_=name
    return contacts[name]

def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(find_phone(args, contacts))
        elif command == "all":
            print(show_phone(contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print (birthdays(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
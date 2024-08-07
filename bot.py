from collections import UserDict
from datetime import datetime, timedelta
import pickle
import re

def save_data(book, filename="./addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="./addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def input_error(func):
  def inner(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except ValueError:
      return "Give me name and phone please."
    except IndexError:
      return "Give me name please."
    except KeyError:
      return "Contact not found."

  return inner

class Field:
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return str(self.value)

class Name(Field):
  def __init__(self, value):
    if not value:
      print("Name is required")
    else:
      self.value = value

class Phone(Field):

  def __init__(self, value):
    if(self.validate_phone(value)):
      self.value = value

  def validate_phone(self, value):
    if re.match(r'^\d{10}$', value):
      return True
    print("Phone number must be 10 digits")
    return False
  
class Birthday(Field):
  def __init__(self, value):
    try:
      self.value = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
  def __init__(self, name):
    self.name = Name(name)
    self.phones = []
    self.birthday = None

  def __str__(self):
    return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
  
  def add_phone(self, phone):
    phone_obj = Phone(phone)
    self.phones.append(phone_obj)

  def add_birthday(self, date):
    birthday_obj = Birthday(date)
    self.birthday = birthday_obj

  def remove_phone(self, phone):
    for p in self.phones:
      if p.value == phone:
        self.phones.remove(p)

  def edit_phone(self, old_phone, new_phone):
    for phone in self.phones:
      if phone.value == old_phone:
        phone.value = new_phone

  def find_phone(self, phone):
    for p in self.phones:
      if p.value == phone:
        return p
    return None

class AddressBook(UserDict):
  def add_record(self, record):
    self.data[record.name.value] = record

  def find(self, name):
    return self.data.get(name, None)
  
  def delete(self, name):
    if name in self.data:
      del self.data[name]
  
  def get_upcoming_birthdays(self):
    upcoming_birthdays = []
    today = datetime.today().date()
    next_week = today + timedelta(days=7)
    
    for record in self.data.values():
      if record.birthday:
        birthday_this_year = record.birthday.value.replace(year=today.year)
        if today <= birthday_this_year <= next_week:
          upcoming_birthdays.append({
            "name": record.name.value,
            "congratulation_date": birthday_this_year.strftime("%Y.%m.%d")
          })
    
    return upcoming_birthdays
  
def parse_input(user_input):
  cmd, *args = user_input.split()
  cmd = cmd.strip().lower()
  return cmd, *args

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
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone  = args
    contact_record = book.find(name)
    if contact_record is None:
      return "Contact not found."
    else:
      contact_record.edit_phone(old_phone, new_phone)
      return "Contact changed."

@input_error
def show_phone(args, book: AddressBook):
  name = args[0]
  contact_record = book.find(name)
  if contact_record is None:
    return "Contact not found."
  else:
    return contact_record

@input_error
def show_birthday(args, book: AddressBook):
  name = args[0]
  contact_record = book.find(name)
  if contact_record is None:
    return "Contact not found."
  else:
    return contact_record.birthday

@input_error
def add_birthday(args, book: AddressBook):
  name, birthday = args
  contact_record = book.find(name)
  if contact_record is None:
    new_contact = Record(name)
    new_contact.add_birthday(birthday)
    book.add_record(new_contact)
    return f"New contact {name} with birthday {birthday} added."
  else:
    contact_record.add_birthday(birthday)
    return "Contact changed."

@input_error
def show_upcoming_birthdays(args, book: AddressBook):
  return book.get_upcoming_birthdays()
  

def main():
  book = load_data()
  # john_record = Record("John")
  # john_record.add_phone("1234567890")
  # john_record.add_phone("5555555555")
  # john_record.add_birthday("1985-07-30")
  # book.add_record(john_record)

  # jane_record = Record("Jane")
  # jane_record.add_phone("9876543210")
  # jane_record.add_birthday("1990-08-09")
  # book.add_record(jane_record)
  print("Welcome to the assistant bot!")
  while True:
    user_input = input("Enter a command: ")
    command, *args = parse_input(user_input)

    if command in ["close", "exit"]:
      save_data(book)
      print("Good bye!")
      break

    elif command == "hello":
      print("How can I help you?")

    elif command == "add":
      print(add_contact(args, book))

    elif command == "change":
      print(change_contact(args, book))

    elif command == "phone":
     print(show_phone(args, book))

    elif command == "all":
      for name, record in book.data.items():
        print(record)

    elif command == "add-birthday":
      print(add_birthday(args, book))

    elif command == "show-birthday":
      print(show_birthday(args, book))

    elif command == "birthdays":
      print(show_upcoming_birthdays(args, book))

    else:
      print("Invalid command.")
      pass

if __name__ == "__main__":
  main()
  # book = AddressBook()

  # john_record = Record("John")
  # john_record.add_phone("1234567890")
  # john_record.add_phone("5555555555")
  # john_record.add_birthday("1985-07-30")
  # book.add_record(john_record)

  # jane_record = Record("Jane")
  # jane_record.add_phone("9876543210")
  # jane_record.add_birthday("1990-08-09")
  # book.add_record(jane_record)

  # for name, record in book.data.items():
  #   print(record)

  # john = book.find("John")
  # john.edit_phone("1234567890", "1112223333")

  # print(john)

  # found_phone = john.find_phone("5555555555")
  # print(f"{john.name}: {found_phone}")

  # upcoming_birthdays = book.get_upcoming_birthdays()
  # print("Upcoming birthdays:", upcoming_birthdays)

  # book.delete("Jane")
  # print(book.find("Jane"))
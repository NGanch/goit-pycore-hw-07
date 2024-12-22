from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must consist of 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY.")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for idx, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return
        raise ValueError("Old phone not found.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

class AddressBook:
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[record.name.value] = record

    def find(self, name):
        return self.records.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.now()
        upcoming = []
        for record in self.records.values():
            if record.birthday:
                days = record.days_to_birthday()
                if days is not None and 0 <= days <= 7:
                    upcoming.append((record.name.value, record.birthday.value.strftime("%d.%m.%Y")))
        return upcoming

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, ValueError, KeyError) as e:
            return str(e)
    return wrapper

@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.add_birthday(birthday)
    return f"Birthday added for {name}."

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    if record.birthday is None:
        return "No birthday set for this contact."
    return f"{name}'s birthday is {record.birthday.value.strftime('%d.%m.%Y')}"

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the upcoming week."
    return "\n".join([f"{name}: {date}" for name, date in upcoming])

@input_error
def add_contact(args, book):
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
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    record.change_phone(old_phone, new_phone)
    return f"Phone number updated for {name}."

@input_error
def show_contact(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    phones = ", ".join([phone.value for phone in record.phones])
    return f"{name}: {phones}"

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.strip().split(" ", 1)
        args = args[0].split(" ") if args else []

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_contact(args, book))

        elif command == "all":
            for record in book.records.values():
                phones = ", ".join([phone.value for phone in record.phones])
                print(f"{record.name.value}: {phones}")

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
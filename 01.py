from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) < 10:
            raise ValueError("Phone number must contain only digits and be at least 10 characters long.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if not isinstance(phone, Phone):
            raise ValueError("Invalid phone object.")
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone.value]

    def add_birthday(self, birthday):
        if not isinstance(birthday, Birthday):
            raise ValueError("Invalid birthday object.")
        self.birthday = birthday

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
        if not isinstance(record, Record):
            raise ValueError("Invalid record object.")
        self.records[record.name.value] = record

    def get_upcoming_birthdays(self, days=7):
        today = datetime.now()
        upcoming_birthdays = []

        for record in self.records.values():
            if record.birthday:
                next_birthday = record.birthday.value.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)

                if 0 <= (next_birthday - today).days < days:
                    upcoming_birthdays.append((record.name.value, next_birthday.strftime("%d.%m.%Y")))

        return sorted(upcoming_birthdays, key=lambda x: datetime.strptime(x[1], "%d.%m.%Y"))

# Example Usage
if __name__ == "__main__":
    book = AddressBook()

    record1 = Record("John Doe")
    record1.add_phone(Phone("1234567890"))
    record1.add_birthday(Birthday("25.12.1990"))

    record2 = Record("Jane Smith")
    record2.add_phone(Phone("0987654321"))
    record2.add_birthday(Birthday("22.12.1985"))

    book.add_record(record1)
    book.add_record(record2)

    print("Upcoming birthdays:", book.get_upcoming_birthdays())

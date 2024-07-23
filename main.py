from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value


class Birthday(Field):
    def __init__(self, value):
        try:
            super().__init__(datetime.strptime(value, "%d.%m.%Y"))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


class AddressBook:
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[record.name.value] = record

    def find(self, name):
        return self.records.get(name, None)

    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming_birthdays = []

        for record in self.records.values():
            if record.birthday:
                birthday_date = record.birthday.value.replace(year=today.year)
                if today <= birthday_date <= today + timedelta(days=7):
                    if birthday_date.weekday() >= 5:  # If birthday falls on weekend
                        # Move to next Monday
                        birthday_date = birthday_date + timedelta(days=(7 - birthday_date.weekday()))
                    upcoming_birthdays.append(
                        {"name": record.name.value, "birthday": birthday_date.strftime("%d.%m.%Y")})

        return upcoming_birthdays


def input_error(handler):
    def wrapper(*args):
        try:
            return handler(*args)
        except IndexError:
            return "Not enough arguments."
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)

    return wrapper


@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise IndexError
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
    if len(args) < 3:
        raise IndexError
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        for phone in record.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return "Phone number updated."
        return "Old phone number not found."
    return "Contact not found."


@input_error
def phone_contact(args, book):
    if len(args) < 1:
        raise IndexError
    name, *_ = args
    record = book.find(name)
    if record:
        return ", ".join(phone.value for phone in record.phones)
    return "Contact not found."


@input_error
def show_all_contacts(book):
    return "\n".join(
        f"{record.name.value}: {', '.join(phone.value for phone in record.phones)}" for record in book.records.values())


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        raise IndexError
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."


@input_error
def show_birthday(args, book):
    if len(args) < 1:
        raise IndexError
    name, *_ = args
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    return "Birthday not found for the contact."


@input_error
def birthdays(book):
    return "\n".join(f"{record['name']}: {record['birthday']}" for record in book.get_upcoming_birthdays())


def parse_input(user_input):
    return user_input.strip().split()


def main():
    book = AddressBook()
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
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(phone_contact(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

from functools import wraps


def input_error(func):
    """Перехоплює помилки введення в обробниках команд.

    Замість того щоб падати, бот повертає користувачеві підказку,
    і цикл запит-відповідь у main() продовжує працювати.
    """

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
        except KeyError:
            return "Contact not found."

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts):
    # Менше або більше двох аргументів -> ValueError при розпакуванні
    name, phone = args
    contacts[name.capitalize()] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, phone = args
    name = name.capitalize()
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    # Немає аргументів -> IndexError, немає такого контакту -> KeyError
    name = args[0].capitalize()
    return contacts[name]


@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts saved."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("Enter a command: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGood bye!")
            break

        if not user_input.strip():
            print("Invalid command.")
            continue

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
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

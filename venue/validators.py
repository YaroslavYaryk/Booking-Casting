import phonenumbers
from email_validator import validate_email, EmailNotValidError


def validate_phone(string):
    try:
        my_number = phonenumbers.parse(string)
        return phonenumbers.is_possible_number(my_number), "no error"
    except Exception as e:
        return False, e


def validate_email(string):
    try:
        print("no_error")
        return validate_email(string)
    except EmailNotValidError as e:
        print(e, "here")
        return False

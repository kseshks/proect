import secrets
import string


def generate_password(length = 12, use_letters = True, use_digits = True, use_special_chars = True):
    chars = ""
    if use_letters:
        chars += string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_special_chars:
        chars += string.punctuation

    if not chars:
        raise ValueError("Должен быть выбран хотя бы один тип символов")

    password_chars = []
    if use_letters:
        password_chars.append(secrets.choice(string.ascii_letters))
    if use_digits:
        password_chars.append(secrets.choice(string.digits))
    if use_special_chars:
        password_chars.append(secrets.choice(string.punctuation))


    for _ in range(length - len(password_chars)):
        password_chars.append(secrets.choice(chars))

    secrets.SystemRandom().shuffle(password_chars)

    return ''.join(password_chars)

def generate_login():
    random_digits = ''.join(secrets.choice(string.digits) for _ in range(6))
    return f"student_{random_digits}"

def generate_student_number():
    return int(''.join(secrets.choice(string.digits) for _ in range(8)))


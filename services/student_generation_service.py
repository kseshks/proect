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



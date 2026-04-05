import secrets
import string


def generate_password(length: int = 10) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def generate_teacher_login() -> str:
    return f"teacher_{''.join(secrets.choice(string.digits) for _ in range(6))}"


def generate_student_number(length: int = 8) -> str:
    return "".join(secrets.choice(string.digits) for _ in range(length))
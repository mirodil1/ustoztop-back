import secrets


def generate_security_code(length):
    return "".join(str(secrets.randbelow(10) for i in range(length)))

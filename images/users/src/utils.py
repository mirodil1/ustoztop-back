import secrets


def generate_security_code():
    return "".join(str(secrets.choice(range(100000, 999999))))

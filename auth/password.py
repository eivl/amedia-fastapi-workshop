from auth.context import pwd_context


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    :param plain_password: string of the plain password.
    :param hashed_password: string of the hashed password.
    :return: boolean of whether the password matches the hash.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Helper function to hash a password.
    :param password: string as plaintext password.
    :return: hashed password.
    """
    return pwd_context.hash(password)

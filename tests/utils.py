import random
import string


def randon_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=12))


def randon_email() -> str:
    return f"{randon_string()}@{randon_string()}.com"

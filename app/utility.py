import secrets


def generate_random_hex():
    return secrets.token_hex(32)


# Example usage:
random_hex = generate_random_hex()
print(f"Generated 32-character hex string: {random_hex}")

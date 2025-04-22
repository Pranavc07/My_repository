from cryptography.fernet import Fernet

def generate_key():
    """Generate a new Fernet key."""
    return Fernet.generate_key()

def save_key(key, filename):
    """Save the generated key to a file."""
    with open(filename, 'wb') as key_file:
        key_file.write(key)
        

def load_key(filename):
    """Load the key from a file."""
    with open(filename, 'rb') as key_file:
        return key_file.read()


def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data)  # <- no .encode()


def decrypt_data(encrypted_data, key):
    """Decrypt the data using the provided key."""
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data


if __name__ == "__main__":
    key = generate_key()
    save_key(key, "key.key")
    
    loaded_key = load_key("key.key")
    
    data = "Hello, World!"
    encrypted_data = encrypt_data(data, loaded_key)
    
    print(f"Encrypted: {encrypted_data}")
    
    decrypted_data = decrypt_data(encrypted_data, loaded_key)
    print(f"Decrypted: {decrypted_data}")
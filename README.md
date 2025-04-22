🛡️ Simulated Ransomware Framework


This project is a simulated ransomware attack chain developed purely for educational and research purposes.
It models real-world ransomware behavior, including:

File encryption with secure key generation

Dynamic file renaming using Base64 encoding

Ransom note and encrypted file list generation

Command and Control (C2) communication for remote key management

Persistence mechanisms via startup registry modifications

Script stealth by relocating payload into hidden Windows directories

The focus is on demonstrating the full ransomware lifecycle — from initial compromise to encryption and persistence — without causing any real harm or risk outside the controlled environment.

⚙️ Key Features
File Encryption: Encrypts .txt, .docx, and similar files with a symmetric key (Fernet AES-based encryption).

File Renaming: Encodes filenames using Base64 and appends a custom .enc extension.

Ransom Note Creation: Automatically drops an HTML ransom note onto the user's Desktop.

Encrypted Files List: Generates a complete list of encrypted files.

Persistence Mechanism: Copies the executable to a hidden directory and adds it to Windows startup using Registry modifications.

C2 Server Communication: Sends the encryption key to a remote HTTP server securely using POST requests (basic authentication supported).

🖥️ Technologies Used
Python 3.x

Cryptography library (Fernet)

Base64 encoding/decoding

Windows Registry access (winreg)

HTTP Requests (for C2 communication)

🚀 How to Set Up & Run
Clone the repository:

git clone https://github.com/yourusername/simulated-ransomware.git
cd simulated-ransomware

Install dependencies:
pip install cryptography requests

Configure settings (optional):
Edit TARGET_DIR to specify the folder to encrypt.
Set your C2 server URL in the code (optional, for testing key retrieval).

Run the script (ONLY IN A SAFE TEST ENVIRONMENT!):
python ransomware_simulation.py

Simulation Flowchart: 
 ┌────────────────────┐
 │ Start Execution     │
 └─────────┬───────────┘
           ↓
 ┌────────────────────┐
 │ Generate Encryption │
 │ Key (Fernet AES)    │
 └─────────┬───────────┘
           ↓
 ┌────────────────────┐
 │ Scan Target Folder  │
 └─────────┬───────────┘
           ↓
 ┌────────────────────┐
 │ For Each File:      │
 │ - Check extension   │
 │ - Check size        │
 └─────────┬───────────┘
           ↓
 ┌────────────────────┐
 │ Encrypt File Data   │
 └─────────┬───────────┘
           ↓
 ┌────────────────────┐
 │ Rename File (Base64 │
 │ encoding + .enc)    │
 └─────────┬───────────┘
           ↓
 ┌────────────────────┐
 │ Create Ransom Note  │
 │ and Encrypted Files │
 │ List on Desktop     │
 └─────────┬───────────┘
           ↓
 ┌────────────────────┐
 │ Send Key to Remote  │
 │ Server (C2 Upload)  │
 └─────────┬───────────┘
           ↓
 ┌────────────────────┐
 │ Copy Script to     │
 │ Hidden Location     │
 │ (AppData\Windows)    │
 └─────────┬───────────┘
           ↓
 ┌────────────────────┐
 │ Add Persistence via │
 │ Windows Registry    │
 │ (Startup Entry)      │
 └─────────┬───────────┘
           ↓
 ┌────────────────────┐
 │ End Execution       │
 └────────────────────┘


🧪 Testing Notes
Test inside virtual machines (VMs) or sandbox environments like VMware, VirtualBox, or AWS EC2 Windows instances.

Use test documents (NOT real sensitive data).

Host a simple HTTP server locally or remotely (e.g., using Flask or FastAPI) for receiving the encryption key.

⚠️ Important Disclaimer
This project is intended strictly for educational, research, and ethical hacking practice only.
Running ransomware code against unauthorized systems is illegal and unethical.
The author is not responsible for any misuse or damages caused by improper deployment of this project.
Always ensure you have explicit permission before using these tools.

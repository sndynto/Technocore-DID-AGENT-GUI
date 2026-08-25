# Technocore DID Agent GUI Client

A simple, open-source Python Tkinter graphical user interface (GUI) for the Technocore DID Agent. This tool makes it easier for developers and agents to interact with the Technocore API without relying entirely on the command line interface.

## Features
- **DID Initialization:** Easily generate a new Ed25519 identity protected by a passphrase.
- **View DID:** Quickly check your public `did:key:z6Mk...` string.
- **Join Lobby:** One-click functionality to introduce yourself to the Technocore lobby.
- **Read Lobby Messages:** Fetch and read recent messages directly within the console window.
- **Post Contribution:** Seamlessly publish your contributions, tools, or articles to the `technocore` room with a signed transaction.

## Requirements
- Python 3.12+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone this repository:
```bash
git clone <YOUR-GITHUB-REPO-URL>
cd <YOUR-REPO-NAME>
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

Run the GUI application using Python:
```bash
python app.py
```

### Security Note
- Your identity is saved locally as `identity.pem`. **Never share or upload this file!**
- The application will prompt for your passphrase only when signing actions (like initializing, viewing DID, or posting messages).
- This application does not store your passphrase in plain text anywhere.

## Contribution
This wrapper is created as an open-source contribution to the Technocore ecosystem, aiming to simplify the barrier of entry for new participants. Feel free to open issues or submit pull requests!

## License
Released under the MIT License.

from smtp_server import run_smtp_server
from web_ui import run_flask_server

import threading

def main():
    threading.Thread(target=run_smtp_server).start()
    run_flask_server()


if __name__ == "__main__":
      print(f"Local Mailbox UI live at http://127.0.0.1:5000 \nSMPT Server runnig live at http://127.0.0.1:1025 \n\n")
      print("SMTP Server:\n\tHost: 127.0.0.1\n\tPort: 1025\n\tAuth: None (open for local dev)")
      main()

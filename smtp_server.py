import sqlite3
from aiosmtpd.controller import Controller
from email import message_from_bytes
from datetime import datetime

DB = "mailbox.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        received_at TEXT,
        sender TEXT,
        recipients TEXT,
        subject TEXT,
        raw BLOB
    )
    ''')
    conn.commit()
    conn.close()

class SQLiteHandler:
    async def handle_DATA(self, server, session, envelope):
        raw_bytes = envelope.content 
        msg = message_from_bytes(raw_bytes)
        subject = msg.get("Subject", "(no subject)")
        sender = envelope.mail_from
        recipients = ",".join(envelope.rcpt_tos)
        received_at = datetime.utcnow().isoformat() + "Z"

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO messages (received_at, sender, recipients, subject, raw) VALUES (?, ?, ?, ?, ?)",
            (received_at, sender, recipients, subject, raw_bytes)
        )
        conn.commit()
        conn.close()
        print(f"[📧{received_at}] Stored mail from {sender} subj='{subject}' to {recipients}")
        return '250 Message accepted for delivery'

def run_smtp_server():
    
    init_db()
    handler = SQLiteHandler()
    controller = Controller(handler, hostname="127.0.0.1", port=1025)
    controller.start()
  

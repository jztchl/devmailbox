
from flask import Flask, g, render_template_string, send_file, abort,request, redirect, url_for
import sqlite3
import io
from email import message_from_bytes, policy
import smtplib
from email.message import EmailMessage
import logging
import flask.cli




DB = "mailbox.db"
app = Flask(__name__)

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

INDEX_HTML = '''<!doctype html>
<title>Local Mailbox</title>
<h1>Local Mailbox</h1>
<p><a href="/send">Send sample test email (Python)</a></p>
<table border=1 cellpadding=6>
<tr><th>ID</th><th>Received At (UTC)</th><th>From</th><th>To</th><th>Subject</th><th>Actions</th></tr>
{% for m in messages %}
  <tr>
    <td>{{m["id"]}}</td>
    <td>{{m["received_at"]}}</td>
    <td>{{m["sender"]}}</td>
    <td>{{m["recipients"]}}</td>
    <td>{{m["subject"]}}</td>
    <td>
      <a href="/msg/{{m['id']}}">view</a> |
      <a href="/raw/{{m['id']}}">raw</a>
    </td>
  </tr>
{% endfor %}
</table>
'''

MSG_HTML = '''<!doctype html>
<title>Message {{msg['id']}}</title>
<h1>Message {{msg['id']}}</h1>
<p><b>Received:</b> {{msg['received_at']}}</p>
<p><b>From:</b> {{msg['sender']}}</p>
<p><b>To:</b> {{msg['recipients']}}</p>
<p><b>Subject:</b> {{msg['subject']}}</p>
<hr>
<h3>Parsed</h3>
<pre>{{parsed}}</pre>
<hr>
<a href="/">Back</a> | <a href="/raw/{{msg['id']}}">Download raw</a>
'''

@app.route("/")
def index():
    db = get_db()
    cur = db.execute("SELECT id, received_at, sender, recipients, subject FROM messages ORDER BY id DESC")
    messages = cur.fetchall()
    return render_template_string(INDEX_HTML, messages=messages)

@app.route("/msg/<int:mid>")
def view_msg(mid):
    db = get_db()
    cur = db.execute("SELECT * FROM messages WHERE id = ?", (mid,))
    row = cur.fetchone()
    if not row:
        abort(404)
    raw = row["raw"]
    msg = message_from_bytes(raw, policy=policy.default)
    parsed = []
    for k, v in msg.items():
        parsed.append(f"{k}: {v}")
    parsed.append("\n--- Body preview ---\n")
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain":
                parsed.append(part.get_content().strip()[:10000])
                break
    else:
        parsed.append(msg.get_content().strip()[:10000])
    return render_template_string(MSG_HTML, msg=row, parsed="\n".join(parsed))

@app.route("/raw/<int:mid>")
def raw(mid):
    db = get_db()
    cur = db.execute("SELECT raw FROM messages WHERE id = ?", (mid,))
    row = cur.fetchone()
    if not row:
        abort(404)
    raw = row["raw"]
    return send_file(io.BytesIO(raw), mimetype="message/rfc822", as_attachment=True, download_name=f"message-{mid}.eml")

SEND_HTML = '''<!doctype html>
<title>Send Email</title>
<h1>Send an Email</h1>
<form method="POST">
  <p>From: <input type="email" name="from_addr" required></p>
  <p>To: <input type="email" name="to_addr" required></p>
  <p>Subject: <input type="text" name="subject" required></p>
  <p>Body:<br><textarea name="body" rows="8" cols="50" required></textarea></p>
  <p><button type="submit">Send</button></p>
</form>
<a href="/">Back</a>
'''

@app.route("/send", methods=["GET", "POST"])
def send_mail():
    if request.method == "POST":
        from_addr = request.form["from_addr"]
        to_addr = request.form["to_addr"]
        subject = request.form["subject"]
        body = request.form["body"]

        msg = EmailMessage()
        msg["From"] = from_addr
        msg["To"] = to_addr
        msg["Subject"] = subject
        msg.set_content(body)

        try:
            with smtplib.SMTP("127.0.0.1", 1025) as smtp:
                smtp.send_message(msg)
            return redirect(url_for("index"))
        except Exception as e:
            return f"<p>Error sending email: {e}</p><a href='/'>Back</a>"

    return render_template_string(SEND_HTML)
def run_flask_server():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR) 
    flask.cli.show_server_banner = lambda *args: None
    app.run(host="127.0.0.1", port=5000, use_reloader=False)

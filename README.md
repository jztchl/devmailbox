<p align="center">
  <img src="/logo.png" alt="Dev Mail Box" width="200">
</p>
<h1 align="center">Dev Mail Box</h1>
A lightweight local SMTP server with a clean Flask-based web UI for viewing and sending test emails — perfect for development environments.

---

## 🚀 Features

* **Local SMTP Server** – Captures all outgoing mail on `127.0.0.1:1025`
* **Web UI** – Browse messages, view raw source, send new messages
* **No External SMTP** – No username/password required
* **Cross-Platform** – Runs on Windows, macOS, and Linux
* **Packagable** – Build to `.exe` with PyInstaller for easy sharing on Windows

---

## 📦 Installation

### Option 1 – Using [uv](https://github.com/astral-sh/uv) (Recommended)

```bash
uv sync
```

> Installs all dependencies from `pyproject.toml` or `requirements.txt`.

---

### Option 2 – Using pip

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
python main.py
```

You’ll see output like:

```
📨 SMTP server running on 127.0.0.1:1025
🌐 Web UI available at http://127.0.0.1:5000
```

---

## 🌍 Usage

1. **Point your app’s SMTP settings to:**

   * **Host:** `127.0.0.1`
   * **Port:** `1025`
   * **Username / Password:** *(Leave blank)*

2. **Access the Web UI:**
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

3. **View Messages:**
   Browse captured messages, read full content, or view raw email source.

4. **Send a Test Email:**
   Use the **Send** page in the UI to send a new message to the SMTP server.

---

## 🛠 Building to EXE (Optional)

Using PyInstaller:

```bash
pyinstaller --onefile main.py
```

The compiled executable will be inside the `dist/` folder.

---

## 📥 Download Release

Get the latest Windows executable here:
[https://github.com/jztchl/devmailbox/releases/tag/v1](https://github.com/jztchl/devmailbox/releases/tag/v1)

*(Replace the URL above with your actual GitHub release link.)*

---

## 📄 Requirements

Minimal dependencies:

```
Flask>=3.0.0
aiosmtpd>=1.4.5
```

---

## 📜 License

MIT License — use freely for development purposes.

---

This keeps it sharp and user-friendly. When you push releases, just drop the EXE there and folks can grab it without fuss.




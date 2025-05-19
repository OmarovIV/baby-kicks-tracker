# 🧰 Mac User Setup — Baby Kicks Tracker

This guide helps you run the Baby Kicks Tracker on macOS.

---

## 1. Requirements

- Python 3 installed (pre-installed on macOS)
- Recommended: Homebrew + virtualenv

---

## 2. Setup

### Option A: Quick start without virtualenv

```bash
cd path/to/project
pip3 install -r requirements.txt
python3 main.py
```

### Option B: Using virtualenv (recommended)

```bash
cd path/to/project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 3. 🚀 Run without Terminal (recommended)

You can run the app by double-clicking a script:

### ✅ Steps:

1. Double-click the `run.command` file in the project folder.
2. If macOS prompts security warnings, click **Open**.
3. The app will launch.

If the script doesn’t run:
```bash
chmod +x run.command
```

That’s it 🎉


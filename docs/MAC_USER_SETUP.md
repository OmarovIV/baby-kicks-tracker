# 👩‍🍼 Baby Kicks Tracker — Setup on macOS

This guide helps you run the app on macOS without being a developer.

## ✅ Requirements

- macOS with internet access
- Python 3.11+ installed (https://www.python.org/downloads/mac-osx/)

---

## 🔧 Step-by-Step Installation

### 1. Download the App

- Get the zipped project folder from your partner or GitHub.
- Unzip it to your Desktop or Documents.

### 2. Open Terminal

- Use Spotlight (Cmd + Space) → search for **Terminal** and open it.

### 3. Navigate to the project folder

```bash
cd ~/Desktop/baby-kicks-tracker   # Or wherever you unzipped it
```

### 4. Create a virtual environment

```bash
python3 -m venv venv
```

### 5. Activate the environment

```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your Terminal prompt.

### 6. Install dependencies

```bash
pip install -r requirements.txt
```

### 7. Run the App 🎉

```bash
python3 main.py
```

---

## 📲 (Optional) Create a Mac App (.app)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "BabyKicks" main.py
```

- After a few seconds, you’ll find `dist/BabyKicks.app`
- Move it to `Applications/` or Desktop, and launch by double-clicking

---

## ❗ Common Issues

- "Permission denied": use `chmod +x` on script or `.app`
- "Python not found": try `python3` instead of `python`
- App won't launch: check security settings under System Preferences → Security → Allow from Anywhere

---

## 🙋 Need Help?

Ask your partner or open an issue on GitHub.

---

Enjoy using Baby Kicks Tracker! ❤️

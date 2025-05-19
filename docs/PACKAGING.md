# 📦 Packaging Guide — Baby Kicks Tracker

This guide explains how to build distributable versions of the app:

- ✅ Windows `.exe` file
- ✅ macOS `.app` bundle

---

## 🖥 Windows — EXE Build

### 1. Install PyInstaller (inside virtualenv)

```bash
pip install pyinstaller
```

### 2. Run the build

```bash
pyinstaller --onefile --windowed --name BabyKicksTracker main.py
```

- `--onefile`: package into a single `.exe`
- `--windowed`: no console window appears
- `--name`: output file name

### 3. Result

Your `.exe` will be in the `dist/` folder:

```
dist/BabyKicksTracker.exe
```

### 4. Optional — Include extra files (e.g., database, tkcalendar)

```bash
pyinstaller \
  --onefile \
  --windowed \
  --name BabyKicksTracker \
  --add-data "baby_kicks.db;." \
  --add-data "venv/Lib/site-packages/tkcalendar;tkcalendar" \
  main.py
```

---

## 🍏 macOS — App Bundle (.app)

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build the app

```bash
pyinstaller --onefile --windowed --name "BabyKicks" main.py
```

### 3. Locate the app bundle

```
dist/BabyKicks.app
```

Move it to `Applications/` or zip it to share.

### 4. Gatekeeper (security)

If macOS blocks the app:

- Go to `System Preferences → Security & Privacy → Allow Anyway`
- Or sign the app with:

```bash
codesign --force --deep --sign - dist/BabyKicks.app
```

---

## 💡 .gitignore Recommendations

Add this to avoid committing build artifacts:

```
build/
dist/
*.spec
.vscode/
__pycache__/
*.pyc
```

---

## 🚀 GitHub Actions (optional CI build)

You can automate building `.exe` or `.app` with GitHub Actions and publish in Releases. See `.github/workflows/build.yml`.

---

## 🧪 Test Before Sharing

Always test the output:

- Open app
- Try Add → View → Chart → Heatmap
- Run it without Python installed (pure executable)

---

## ✅ Result

Distribute the `.exe` or `.app` via GitHub Releases, Drive, or manually.

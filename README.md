# Baby Kicks Tracker

Simple desktop app to log and visualize your baby’s kicks.

## Features

- Add kick records with date, time, count and comment
- Automatic calculation of pregnancy weeks
- View, filter and delete records
- Daily overview chart & hourly heatmap
- Anomaly alerts if no kicks today
- Cross-platform (Windows, macOS, Linux)

## Prerequisites

- **Python 3.8+**
- **pip**

On **macOS** you may need to install and link `tkinter`:

```bash
brew install tcl-tk
# then when installing Python, point it at Homebrew’s tcl-tk, e.g.:
# export LDFLAGS="-L/usr/local/opt/tcl-tk/lib"
# export CPPFLAGS="-I/usr/local/opt/tcl-tk/include"
# pyenv install 3.x.x
```

## Installation

```bash
git clone <your-repo-url>
cd baby_kicks_app

### Create virtual env

python3 -m venv venv
source venv/bin/activate # on Windows: venv\Scripts\activate

### Install dependencies

pip install --upgrade pip
pip install -r requirements.txt

### Run

python main.py
```

## Packaging

### Standalone executable (Windows/macOS/Linux)

Using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

The app bundle will appear in dist/.

## Usage

- Add Record: enter Date, Time, optional Kicks count & Comment
- View Records: filter by date, delete, show chart or heatmap
- Settings: adjust pregnancy start date
- Alerts: see if today’s activity is missing

# 📶 Speed Meter

**A lightweight network speed monitor for the Windows taskbar**
Displays real-time upload/download speeds — simple, minimal, and effective.

---

## 🛠 Requirements

* Windows 10 or 11
* Python 3.7 or later (if running from source)

---

## 🚀 Installation

### ✅ Option 1: Run from Source

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Benojir/Networx-Alternative-Python.git
   cd Networx-Alternative-Python
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   python speedmeter.py
   ```

---

### 🧱 Option 2: Build Executable Yourself

1. **Install PyInstaller:**

   ```bash
   pip install pyinstaller
   ```

2. **Build the executable:**

   ```bash
   pyinstaller --onefile --windowed --noconsole --clean --upx-exclude=vcruntime140.dll --add-data "speedmeter.ico;." speedmeter.py
   ```

3. **Create Setup File:**

   * Download & Install `Inno Setup Compiler`
   * Open `Inno Setup Compiler` and choose `speedmeter.iss`

---

### 📦 Option 3: Download Prebuilt Installer

1. **Download** the installer from the [Releases](https://github.com/Benojir/Networx-Alternative-Python/releases) page.
2. **Double-click** the setup file to install.

---

## ⚠️ Note

Some antivirus software may flag the executable as a false positive. This happens because it was built using **PyInstaller**, a common tool that can trigger such warnings.

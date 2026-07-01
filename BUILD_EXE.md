# Build Instructions for Token Scanner .exe

## Prerequisites

1. **Python 3.12+** installed and in PATH
2. **Git** for version control
3. **pip** package manager (usually comes with Python)

## Automatic Build (Recommended)

### Windows

```bash
# 1. Open Command Prompt in project directory
# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install PyInstaller
pip install pyinstaller

# 5. Run build script
python build.py
```

### Mac/Linux

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install PyInstaller
pip install pyinstaller

# 4. Run build script
python build.py
```

## Manual Build

### Windows Command Line

```batch
REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt
pip install pyinstaller

REM Build executable
pyinstaller --onefile --windowed --name TokenScanner --icon assets/icon.ico gui_app.py
```

### Build with more options

```bash
pyinstaller --onefile \
  --windowed \
  --name TokenScanner \
  --icon assets/icon.ico \
  --add-data "assets:assets" \
  --add-data ".env.example:." \
  --hidden-import=PySide6 \
  --hidden-import=axiomtradeapi \
  --hidden-import=sqlalchemy \
  --hidden-import=pydantic \
  --hidden-import=loguru \
  --hidden-import=plyer \
  --hidden-import=playwright \
  --hidden-import=aiohttp \
  gui_app.py
```

## Output

After successful build, you'll find:

```
token-scanner/
├── dist/
│   └── TokenScanner.exe       # Main executable
├── build/                      # Build artifacts (can be deleted)
└── TokenScanner.spec          # Build specification
```

## Running the .exe

### First Time Setup

```bash
# 1. Create .env file from template
copy .env.example .env

# 2. Edit .env and add your Axiom Trade tokens
# AXIOM_ACCESS_TOKEN=your_token
# AXIOM_REFRESH_TOKEN=your_token

# 3. Run the executable
TokenScanner.exe
```

### Subsequent Runs

Double-click `TokenScanner.exe` to run the application.

## Troubleshooting

### Build Fails

1. **Check Python version**: `python --version` (must be 3.12+)
2. **Verify dependencies**: `pip list`
3. **Update pip**: `python -m pip install --upgrade pip`
4. **Clean rebuild**: Delete `build/`, `dist/`, `*.spec` and try again

### .exe Won't Start

1. **Check .env file**: Must be in same directory as .exe
2. **Verify tokens**: Check AXIOM_ACCESS_TOKEN and AXIOM_REFRESH_TOKEN
3. **Check logs**: Look in `logs/` directory for errors
4. **Run in console**: `TokenScanner.exe` from command prompt to see errors

### Missing Modules Error

Add to PyInstaller command:
```bash
--hidden-import=module_name
```

### Large File Size

The .exe is large (300-500MB) because it bundles:
- Python runtime
- PySide6 GUI framework
- All dependencies
- Playwright browser binaries

This is normal. You can reduce size:
```bash
pyinstaller --onefile --windowed --strip gui_app.py
```

## Distribution

### Create Portable Version

1. Build the .exe
2. Copy to external drive or zip file
3. Requires:
   - `.env.example` (template)
   - Instructions for setup

### Share with Others

```bash
# Create distribution package
mkdir TokenScanner-dist
cd TokenScanner-dist
copy ..\dist\TokenScanner.exe .
copy ..\requirements.txt .
copy ..\.env.example .
copy ..\README.md .

# Zip it
# Users extract and run TokenScanner.exe
```

## Advanced Options

### Include Desktop Shortcut

Add to build script:
```python
from pathlib import Path
desktop = Path.home() / "Desktop"
shortcut = desktop / "TokenScanner.lnk"
```

### Auto-Update Capability

Add version checking in `gui_app.py`:
```python
if check_for_updates():
    download_and_install_update()
```

### Signed Executable

For distribution:
```bash
signtool sign /f cert.pfx /p password TokenScanner.exe
```

## Size Optimization

### Reduce to ~200MB

```bash
pyinstaller \
  --onefile \
  --windowed \
  --strip \
  --exclude-module numpy \
  --exclude-module pandas \
  gui_app.py
```

### Use UPX Compression

```bash
# Download UPX from upx.github.io
pyinstaller --onefile --upx-dir=path/to/upx gui_app.py
```

## Security

### Code Obfuscation

For sensitive code:
```bash
pip install pyarmor
pyarmor obfuscate gui_app.py
```

### Certificate Signing

Recommended for distribution:
```bash
pip install certifi
```

## Deployment

### GitHub Releases

1. Build .exe
2. Create GitHub release
3. Upload TokenScanner.exe
4. Users download directly

### Windows Store

1. Create MSIX package
2. Submit for certification
3. Users install from Store

## Support

If build fails:
1. Check `build.py` for errors
2. Review PyInstaller documentation
3. Check GitHub issues
4. Verify all dependencies installed

---

**Next Steps**:
1. Run `python build.py`
2. Find `.exe` in `dist/` folder
3. Distribute to users
4. Users run TokenScanner.exe

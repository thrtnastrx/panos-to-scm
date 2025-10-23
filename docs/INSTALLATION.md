# Installation Guide

Quick installation guide for the PAN-OS to Strata Cloud Manager Migration Tool.

---

## Requirements

- **Python 3.7+** (Python 3.9 or higher recommended)
- **Operating System**: macOS, Linux, or Windows

---

## Installation Steps

### 1. Install Python

**Check if Python is installed:**
```bash
python3 --version
```

**If not installed:**
- **macOS**: `brew install python3`
- **Linux**: `sudo apt install python3 python3-pip`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

### 2. Install Dependencies

```bash
# Navigate to the application directory
cd /path/to/migration-tool

# Install required packages
pip3 install -r requirements.txt
```

**Manual installation (if requirements.txt not available):**
```bash
pip3 install customtkinter PyYAML requests urllib3 cryptography
```

### 3. Verify Installation

```bash
# Check installed packages
pip3 list | grep -E "customtkinter|PyYAML|requests"
```

---

## Running the Application

### Launch the GUI

```bash
python3 complete_migration_gui.py
```

**Or make it executable:**
```bash
chmod +x complete_migration_gui.py
./complete_migration_gui.py
```

---

## Quick Setup

1. **Launch the application**: `python3 complete_migration_gui.py`
2. **Go to Configuration tab**
3. **Enter your credentials**:
   - SCM: Client ID, Client Secret, TSG ID
   - Panorama: URL, Username, Password
4. **Click "Save Configuration"**
5. **Click "Test Connection"** to verify

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'customtkinter'"
```bash
pip3 install customtkinter
```

### "Permission denied"
```bash
chmod +x complete_migration_gui.py
```

### SSL Certificate Errors
- Enable "Accept untrusted certificate" checkbox in the Migration tab
- Built-in SSL bypass is already included in the application

### GUI won't launch
- Ensure you're in a graphical environment (not SSH terminal)
- Check Python version is 3.7 or higher
- Verify all dependencies are installed

---

## File Locations

- **Configuration**: `~/.panapi/config.yml`
- **Logs**: `~/.panapi/logs/`

---

## System Requirements

| Component | Requirement |
|-----------|------------|
| Python | 3.7+ (3.9+ recommended) |
| RAM | 4 GB minimum |
| Disk Space | 500 MB |
| Display | 1400x900 or higher |
| Network | HTTPS access to Panorama and SCM |

---

## Next Steps

After installation:
1. Read the [USER_GUIDE.md](USER_GUIDE.md) for detailed usage instructions
2. Configure your credentials in the Configuration tab
3. Start with a small test migration

---

**That's it! You're ready to migrate.**

*For detailed usage instructions, see USER_GUIDE.md*

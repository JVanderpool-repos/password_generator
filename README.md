# Password Generator

A secure, customizable password generator written in Python with both graphical (GUI) and command-line interfaces.

## Features

- **🖥️ Graphical Interface**: User-friendly GUI with real-time password strength visualization
- **⌨️ Command-Line Interface**: Full-featured CLI for automation and scripting
- **🔒 Secure Generation**: Uses Python's `secrets` module for cryptographically secure random number generation
- **⚙️ Customizable Options**: Configure password length, character sets, and exclusions
- **📝 Multiple Passwords**: Generate multiple passwords at once
- **💪 Password Strength Checker**: Real-time evaluation with color-coded feedback
- **📋 Clipboard Integration**: One-click copy functionality in GUI
- **🔧 Character Set Control**: Include/exclude lowercase, uppercase, digits, and symbols
- **🚫 Character Exclusion**: Exclude specific characters (useful for avoiding confusing characters like 0, O, 1, l)
- **🎨 Modern UI**: Clean, intuitive interface with progress bars and visual feedback

## GitHub Installation (Recommended)

This repository includes **automatic fixes** for common cross-platform issues. Here's how to get started:

### One-Command Setup

```bash
git clone https://github.com/YourUsername/password_generator.git
cd password_generator
python -m venv venv
# Windows:
venv\Scripts\activate && pip install -r requirements.txt && python setup.py
# macOS/Linux:
source venv/bin/activate && pip install -r requirements.txt && python setup.py
```

### What's Included

✅ **Cross-platform compatibility** (Windows, macOS, Linux)  
✅ **Automatic Tkinter fixes** for virtual environments  
✅ **Comprehensive diagnostics** (`python setup.py`)  
✅ **Multiple interface options** (GUI, CLI, Web demo)  
✅ **Zero-configuration** for most systems  
✅ **Fallback options** if GUI doesn't work  

### Tested Environments

| Platform | Python Version | Status |
|----------|---------------|--------|
| Windows 10/11 | 3.8+ | ✅ Fully Supported |
| macOS Big Sur+ | 3.8+ | ✅ Fully Supported |
| Ubuntu 20.04+ | 3.8+ | ✅ Fully Supported |
| CentOS 8+ | 3.8+ | ✅ Fully Supported |
| Virtual Environments | All | ✅ Auto-fixed |
| Conda Environments | All | ✅ Auto-detected |

## Quick Start

### GUI Version (Recommended)
```bash
python launcher.py
# or
python launcher.py --gui
# or directly
python password_generator_gui.py
```

### CLI Version
```bash
python launcher.py --cli
# or directly  
python password_generator.py
```

## GUI Interface

The GUI provides an intuitive interface with the following sections:

### 🎛️ Password Options
- **Length Slider**: Adjust password length from 4 to 64 characters
- **Count**: Generate 1-20 passwords at once
- **Character Types**: Toggle lowercase, uppercase, digits, and symbols
- **Exclusion Field**: Exclude specific characters with quick-select buttons

### 🔐 Generation Controls
- **Generate Button**: Create passwords with current settings
- **Clear Results**: Reset the results area
- **Copy All**: Copy all generated passwords to clipboard

### 📊 Results Display
- **Password List**: Shows generated passwords with strength scores
- **Right-Click Menu**: Copy individual selections
- **Strength Indicators**: Color-coded strength ratings

### 💪 Strength Checker
- **Real-time Analysis**: Check any password as you type
- **Progress Bar**: Visual strength indicator (0-100)
- **Detailed Metrics**: Shows character type usage
- **Show/Hide**: Toggle password visibility

## Command Line Usage

### Basic Usage

Generate a default 12-character password:
```bash
python password_generator.py
```

### Command Line Options

```bash
python password_generator.py [options]
```

**Options:**
- `-l, --length LENGTH`: Set password length (default: 12)
- `-c, --count COUNT`: Number of passwords to generate (default: 1)
- `--no-lowercase`: Exclude lowercase letters
- `--no-uppercase`: Exclude uppercase letters
- `--no-digits`: Exclude digits
- `--no-symbols`: Exclude symbols
- `-e, --exclude CHARS`: Exclude specific characters
- `--check PASSWORD`: Check the strength of a given password
- `-q, --quiet`: Only output passwords, no additional text

### Examples

Generate a 16-character password:
```bash
python password_generator.py -l 16
```

Generate 5 passwords:
```bash
python password_generator.py -c 5
```

Generate a password without symbols:
```bash
python password_generator.py --no-symbols
```

Generate a password excluding confusing characters:
```bash
python password_generator.py -e "0O1l"
```

Generate a digits-only PIN:
```bash
python password_generator.py -l 6 --no-lowercase --no-uppercase --no-symbols
```

Check password strength:
```bash
python password_generator.py --check "MyPassword123!"
```

Quiet mode (only output the password):
```bash
python password_generator.py -q
```

### Using as a Python Module

```python
from password_generator import PasswordGenerator

# Create generator instance
generator = PasswordGenerator()

# Generate a simple password
password = generator.generate_password()
print(password)

# Generate a custom password
custom_password = generator.generate_password(
    length=16,
    use_symbols=False,
    exclude_chars="0O1l"
)
print(custom_password)

# Generate multiple passwords
passwords = generator.generate_multiple_passwords(count=5, length=14)
for pwd in passwords:
    print(pwd)

# Check password strength
strength = generator.check_password_strength("MyPassword123!")
print(f"Password strength: {strength['score']}/100")
```

## GUI Screenshots and Features

### Main Interface
The GUI features a clean, modern design with:
- **Intuitive Controls**: All options clearly organized in labeled sections
- **Real-time Feedback**: Instant strength checking and visual indicators  
- **Responsive Design**: Resizable window that adapts to your needs
- **Keyboard Shortcuts**: Standard copy/paste and selection operations

### Advanced Features
- **Batch Generation**: Create up to 20 passwords simultaneously
- **Smart Exclusion**: Quick buttons for common exclusions (ambiguous characters)
- **Clipboard Integration**: Seamless copying with system clipboard
- **Error Handling**: Graceful handling of invalid configurations
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Troubleshooting

### GUI Issues
If the GUI doesn't start:

1. **Run diagnostics first:**
   ```bash
   python setup.py
   ```

2. **Common Solutions:**
   
   **Windows:**
   - Reinstall Python from [python.org](https://python.org) (not Microsoft Store)
   - During installation, check "tcl/tk and IDLE" option
   - Or install Anaconda/Miniconda
   
   **Linux:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # CentOS/RHEL
   sudo yum install tkinter
   
   # Arch Linux
   sudo pacman -S tk
   ```
   
   **macOS:**
   - Install Python from [python.org](https://python.org) (recommended)
   - Avoid using system Python for GUI apps
   - Or: `brew install python-tk`

3. **Test tkinter separately:**
   ```bash
   python -c "import tkinter; tkinter.Tk().mainloop()"
   ```

4. **Use CLI as fallback:**
   ```bash
   python launcher.py --cli
   python password_generator.py
   ```

### Virtual Environment Issues

If you encounter tkinter issues in virtual environments:

1. **The application includes automatic fixes** for common venv+tkinter issues
2. **Manual fix:** Set environment variables:
   ```bash
   # Find your Python installation
   python -c "import sys; print(sys.base_prefix)"
   
   # Set variables (adjust path as needed)
   export TCL_LIBRARY="/path/to/python/tcl/tcl8.6"
   export TK_LIBRARY="/path/to/python/tcl/tk8.6"
   ```

### Dependency Issues

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Or install individually
pip install pyperclip
```

### Permission Issues

**Linux/macOS:**
```bash
chmod +x start_gui.sh
chmod +x *.py
```

**Windows:** Run as Administrator if needed

### Still Having Issues?

1. **Check the setup diagnostic:** `python setup.py`
2. **Use the test utilities:** `python tkinter_setup.py`
3. **Try the web demo:** `python web_demo.py`
4. **Use CLI version:** `python password_generator.py --help`

## Password Strength Evaluation

The password strength checker evaluates passwords based on:

- **Length**: Longer passwords get higher scores
- **Character Diversity**: Using different character types (lowercase, uppercase, digits, symbols)
- **Score Range**: 0-100, where:
  - 80-100: Strong
  - 60-79: Medium
  - Below 60: Weak

## Security Features

- Uses Python's `secrets` module for cryptographically secure randomness
- No predictable patterns in generated passwords
- Secure by default with reasonable character set choices
- Option to exclude visually confusing characters

## Requirements

- Python 3.6 or higher
- **GUI Version**: `pyperclip` for clipboard functionality  
- **CLI Version**: No external dependencies (uses only Python standard library)

### Dependencies
- `tkinter`: GUI framework (included with Python)
- `pyperclip`: Clipboard integration (installed via pip)

## File Structure

```
password_generator/
├── 🖥️ password_generator_gui.py  # Main GUI application
├── ⌨️ password_generator.py       # CLI application  
├── 🚀 launcher.py                # Universal launcher (GUI/CLI)
├── 🔧 setup.py                   # System diagnostics & auto-fix
├── 🪟 start_gui.bat              # Windows quick-start
├── 🐧 start_gui.sh               # Unix/Linux quick-start
├── ✅ test_password_generator.py  # Test suite
├── 📋 requirements.txt           # Dependencies
├── 📚 README.md                  # This documentation
├── 🗂️ .gitignore                 # Git ignore rules
└── 🔗 venv/                      # Virtual environment
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security Notes

- Generated passwords are displayed in the terminal, which may be logged in shell history
- For maximum security, consider using the quiet mode (`-q`) and redirect output appropriately
- The password strength checker is a basic implementation and should not be the sole method for evaluating password security
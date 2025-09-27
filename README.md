# Password Generator

A secure, customizable password generator written in Python with a command-line interface.

## Features

- **Secure Generation**: Uses Python's `secrets` module for cryptographically secure random number generation
- **Customizable Options**: Configure password length, character sets, and exclusions
- **Multiple Passwords**: Generate multiple passwords at once
- **Password Strength Checker**: Evaluate the strength of existing passwords
- **CLI Interface**: Easy-to-use command-line interface with various options
- **Character Set Control**: Include/exclude lowercase, uppercase, digits, and symbols
- **Character Exclusion**: Exclude specific characters (useful for avoiding confusing characters like 0, O, 1, l)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd password_generator
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Install dependencies (if any):
```bash
pip install -r requirements.txt
```

## Usage

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
- No external dependencies (uses only Python standard library)

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
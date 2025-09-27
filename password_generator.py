#!/usr/bin/env python3
"""
Password Generator - A secure password generation utility
Author: Your Name
Date: September 27, 2025
"""

import random
import string
import secrets
import argparse
import sys


class PasswordGenerator:
    """A secure password generator with customizable options."""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
    def generate_password(self, length=12, use_lowercase=True, use_uppercase=True, 
                         use_digits=True, use_symbols=True, exclude_chars=""):
        """
        Generate a secure password with specified criteria.
        
        Args:
            length (int): Length of the password (default: 12)
            use_lowercase (bool): Include lowercase letters (default: True)
            use_uppercase (bool): Include uppercase letters (default: True)
            use_digits (bool): Include digits (default: True)
            use_symbols (bool): Include symbols (default: True)
            exclude_chars (str): Characters to exclude from password
            
        Returns:
            str: Generated password
            
        Raises:
            ValueError: If no character sets are selected or length is invalid
        """
        if length < 1:
            raise ValueError("Password length must be at least 1")
            
        # Build character set
        charset = ""
        if use_lowercase:
            charset += self.lowercase
        if use_uppercase:
            charset += self.uppercase
        if use_digits:
            charset += self.digits
        if use_symbols:
            charset += self.symbols
            
        if not charset:
            raise ValueError("At least one character set must be enabled")
            
        # Remove excluded characters
        if exclude_chars:
            charset = ''.join(c for c in charset if c not in exclude_chars)
            
        if not charset:
            raise ValueError("No valid characters available after exclusions")
            
        # Generate password using cryptographically secure random
        password = ''.join(secrets.choice(charset) for _ in range(length))
        
        return password
    
    def generate_multiple_passwords(self, count=5, **kwargs):
        """
        Generate multiple passwords with the same criteria.
        
        Args:
            count (int): Number of passwords to generate
            **kwargs: Arguments to pass to generate_password()
            
        Returns:
            list: List of generated passwords
        """
        return [self.generate_password(**kwargs) for _ in range(count)]
    
    def check_password_strength(self, password):
        """
        Evaluate password strength based on common criteria.
        
        Args:
            password (str): Password to evaluate
            
        Returns:
            dict: Dictionary with strength metrics
        """
        strength = {
            'length': len(password),
            'has_lowercase': any(c.islower() for c in password),
            'has_uppercase': any(c.isupper() for c in password),
            'has_digits': any(c.isdigit() for c in password),
            'has_symbols': any(c in self.symbols for c in password),
            'score': 0
        }
        
        # Calculate strength score (0-100)
        if strength['length'] >= 8:
            strength['score'] += 25
        if strength['length'] >= 12:
            strength['score'] += 10
        if strength['length'] >= 16:
            strength['score'] += 5
            
        if strength['has_lowercase']:
            strength['score'] += 15
        if strength['has_uppercase']:
            strength['score'] += 15
        if strength['has_digits']:
            strength['score'] += 15
        if strength['has_symbols']:
            strength['score'] += 15
            
        return strength


def main():
    """Main CLI interface for the password generator."""
    parser = argparse.ArgumentParser(
        description="Generate secure passwords with customizable options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  password_generator.py                    # Generate a 12-character password
  password_generator.py -l 16             # Generate a 16-character password
  password_generator.py -c 5              # Generate 5 passwords
  password_generator.py --no-symbols      # Generate without symbols
  password_generator.py -e "0O1l"         # Exclude confusing characters
        """
    )
    
    parser.add_argument(
        "-l", "--length", 
        type=int, 
        default=12,
        help="Password length (default: 12)"
    )
    
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=1,
        help="Number of passwords to generate (default: 1)"
    )
    
    parser.add_argument(
        "--no-lowercase",
        action="store_true",
        help="Exclude lowercase letters"
    )
    
    parser.add_argument(
        "--no-uppercase",
        action="store_true",
        help="Exclude uppercase letters"
    )
    
    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Exclude digits"
    )
    
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude symbols"
    )
    
    parser.add_argument(
        "-e", "--exclude",
        default="",
        help="Characters to exclude from password"
    )
    
    parser.add_argument(
        "--check",
        metavar="PASSWORD",
        help="Check the strength of a given password"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only output the password(s), no additional text"
    )
    
    args = parser.parse_args()
    
    generator = PasswordGenerator()
    
    # If checking password strength
    if args.check:
        strength = generator.check_password_strength(args.check)
        if not args.quiet:
            print(f"Password: {args.check}")
            print(f"Length: {strength['length']}")
            print(f"Has lowercase: {strength['has_lowercase']}")
            print(f"Has uppercase: {strength['has_uppercase']}")
            print(f"Has digits: {strength['has_digits']}")
            print(f"Has symbols: {strength['has_symbols']}")
            print(f"Strength score: {strength['score']}/100")
            
            if strength['score'] >= 80:
                print("Strength: Strong")
            elif strength['score'] >= 60:
                print("Strength: Medium")
            else:
                print("Strength: Weak")
        else:
            print(strength['score'])
        return
    
    try:
        # Generate passwords
        passwords = generator.generate_multiple_passwords(
            count=args.count,
            length=args.length,
            use_lowercase=not args.no_lowercase,
            use_uppercase=not args.no_uppercase,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            exclude_chars=args.exclude
        )
        
        if args.quiet:
            for password in passwords:
                print(password)
        else:
            if args.count == 1:
                print(f"Generated password: {passwords[0]}")
            else:
                print(f"Generated {args.count} passwords:")
                for i, password in enumerate(passwords, 1):
                    print(f"  {i}: {password}")
                    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
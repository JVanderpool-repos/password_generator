#!/usr/bin/env python3
"""
Test script for the password generator
"""

from password_generator import PasswordGenerator
import re


def test_basic_generation():
    """Test basic password generation functionality."""
    generator = PasswordGenerator()
    
    # Test default password generation
    password = generator.generate_password()
    assert len(password) == 12
    print(f"✓ Default password generated: {password}")
    
    # Test custom length
    password_16 = generator.generate_password(length=16)
    assert len(password_16) == 16
    print(f"✓ 16-character password generated: {password_16}")
    
    # Test multiple passwords
    passwords = generator.generate_multiple_passwords(count=3, length=8)
    assert len(passwords) == 3
    assert all(len(p) == 8 for p in passwords)
    print(f"✓ Multiple passwords generated: {passwords}")


def test_character_sets():
    """Test character set inclusion/exclusion."""
    generator = PasswordGenerator()
    
    # Test digits only
    digits_only = generator.generate_password(
        length=10,
        use_lowercase=False,
        use_uppercase=False,
        use_symbols=False
    )
    assert digits_only.isdigit()
    print(f"✓ Digits-only password: {digits_only}")
    
    # Test no symbols
    no_symbols = generator.generate_password(
        length=12,
        use_symbols=False
    )
    # Should only contain letters and digits
    assert re.match(r'^[a-zA-Z0-9]+$', no_symbols)
    print(f"✓ No symbols password: {no_symbols}")
    
    # Test character exclusion
    excluded = generator.generate_password(
        length=20,
        exclude_chars="0O1l"
    )
    assert not any(c in "0O1l" for c in excluded)
    print(f"✓ Password excluding confusing chars: {excluded}")


def test_strength_checker():
    """Test password strength evaluation."""
    generator = PasswordGenerator()
    
    # Test weak password
    weak_strength = generator.check_password_strength("abc")
    print(f"✓ Weak password 'abc' score: {weak_strength['score']}")
    
    # Test strong password
    strong_strength = generator.check_password_strength("MyStr0ng!P@ssw0rd")
    print(f"✓ Strong password score: {strong_strength['score']}")
    
    assert strong_strength['score'] > weak_strength['score']


def test_error_handling():
    """Test error handling for invalid inputs."""
    generator = PasswordGenerator()
    
    try:
        # Test invalid length
        generator.generate_password(length=0)
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Invalid length properly handled")
    
    try:
        # Test no character sets
        generator.generate_password(
            use_lowercase=False,
            use_uppercase=False,
            use_digits=False,
            use_symbols=False
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ No character sets properly handled")


def main():
    """Run all tests."""
    print("Running Password Generator Tests...")
    print("=" * 50)
    
    test_basic_generation()
    print()
    
    test_character_sets()
    print()
    
    test_strength_checker()
    print()
    
    test_error_handling()
    print()
    
    print("=" * 50)
    print("✓ All tests passed!")


if __name__ == "__main__":
    main()
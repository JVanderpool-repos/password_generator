#!/usr/bin/env python3
"""
Password Generator Launcher - Launch GUI or CLI version
"""

import sys
import argparse
import os
from pathlib import Path


def setup_tcl_environment():
    """Set up Tcl/Tk environment variables to fix tkinter issues in virtual environments."""
    if 'TCL_LIBRARY' in os.environ and 'TK_LIBRARY' in os.environ:
        return True  # Already set up
    
    # Get the base Python directory (handles virtual environments)
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        base_python_dir = Path(sys.base_prefix)
    else:
        base_python_dir = Path(sys.executable).parent
    
    tcl_dir = base_python_dir / "tcl"
    if tcl_dir.exists():
        # Use version-flexible patterns and validate directories
        tcl_version_dirs = [d for d in tcl_dir.glob("tcl*") if d.is_dir() and (d / "init.tcl").exists()]
        tk_version_dirs = [d for d in tcl_dir.glob("tk*") if d.is_dir() and (d / "tk.tcl").exists()]
        
        if tcl_version_dirs and tk_version_dirs:
            # Sort by version (newest first) for forward compatibility
            tcl_version_dirs.sort(reverse=True)
            tk_version_dirs.sort(reverse=True)
            os.environ['TCL_LIBRARY'] = str(tcl_version_dirs[0])
            os.environ['TK_LIBRARY'] = str(tk_version_dirs[0])
            return True
    
    return False


def launch_gui():
    """Launch the GUI version with error handling."""
    try:
        print("Starting Password Generator GUI...")
        
        # Set up Tcl/Tk environment first with comprehensive fix
        if not setup_tcl_environment():
            print("Warning: Could not set up Tcl/Tk environment automatically")
            print("If GUI fails, try: python setup.py")
        
        # Test tkinter availability
        import tkinter as tk
        
        # Quick test to ensure tkinter works
        try:
            root = tk.Tk()
            root.withdraw()
            root.destroy()
        except Exception as e:
            if "init.tcl" in str(e):
                print("Attempting comprehensive Tcl/Tk fix...")
                # Try the comprehensive fix using integrated solution
                try:
                    # Integrated Tcl/Tk fix
                    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
                        base_python_dir = Path(sys.base_prefix)
                    else:
                        base_python_dir = Path(sys.executable).parent
                    
                    tcl_dir = base_python_dir / "tcl"
                    if tcl_dir.exists():
                        # Find valid Tcl/Tk directories with version-flexible matching
                        tcl_version_dirs = [d for d in tcl_dir.glob("tcl*") if d.is_dir() and (d / "init.tcl").exists()]
                        tk_version_dirs = [d for d in tcl_dir.glob("tk*") if d.is_dir() and (d / "tk.tcl").exists()]
                        
                        if tcl_version_dirs and tk_version_dirs:
                            # Sort by version (newest first)
                            tcl_version_dirs.sort(reverse=True)
                            tk_version_dirs.sort(reverse=True)
                            os.environ['TCL_LIBRARY'] = str(tcl_version_dirs[0])
                            os.environ['TK_LIBRARY'] = str(tk_version_dirs[0])
                            print("✅ Comprehensive fix applied, retrying...")
                            # Test again
                            root = tk.Tk()
                            root.withdraw()
                            root.destroy()
                        else:
                            raise e
                    else:
                        raise e
                except:
                    raise e
            else:
                raise e
        
        # If tkinter works, import and run the GUI
        from password_generator_gui import main as gui_main
        gui_main()
        
    except ImportError as e:
        print(f"Error: GUI dependencies not available: {e}")
        print("\nThe GUI version requires tkinter, which should come with Python.")
        print("Please ensure you have a complete Python installation.")
        print("\nAlternatively, you can use the command-line version:")
        print("  python password_generator.py --help")
        return False
        
    except Exception as e:
        print(f"Error launching GUI: {e}")
        print("\nTrying to provide more information...")
        
        # Provide troubleshooting info
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()  # Hide the window
            print("✓ Tkinter is available")
            root.destroy()
        except Exception as tk_error:
            print(f"✗ Tkinter issue: {tk_error}")
            print("\nTroubleshooting suggestions:")
            print("1. Ensure you have a complete Python installation")
            print("2. On Linux, install python3-tk: sudo apt-get install python3-tk")
            print("3. On Windows, reinstall Python with 'tcl/tk and IDLE' option")
            print("4. Use the CLI version: python password_generator.py")
            
        return False
    
    return True


def launch_cli():
    """Launch the CLI version."""
    print("Starting Password Generator CLI...")
    from password_generator import main as cli_main
    cli_main()


def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(
        description="Password Generator - Launch GUI or CLI version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage Examples:
  launcher.py                    # Launch GUI (default)
  launcher.py --gui              # Launch GUI explicitly  
  launcher.py --cli              # Launch CLI version
  launcher.py --cli -l 16        # CLI with 16-char password
  launcher.py --test             # Test components
        """
    )
    
    parser.add_argument('--gui', action='store_true', default=True,
                       help='Launch GUI version (default)')
    parser.add_argument('--cli', action='store_true', 
                       help='Launch CLI version')
    parser.add_argument('--test', action='store_true',
                       help='Test GUI components')
    
    # If --cli is specified, pass remaining args to CLI
    if '--cli' in sys.argv:
        # Remove launcher-specific args and pass the rest to CLI
        cli_args = [arg for arg in sys.argv[1:] if arg != '--cli']
        sys.argv = [sys.argv[0]] + cli_args
        launch_cli()
        return
        
    args, remaining = parser.parse_known_args()
    
    if args.test:
        print("Running component tests...")
        # Run basic component tests inline
        try:
            from password_generator import PasswordGenerator
            generator = PasswordGenerator()
            
            print("✓ Testing basic password generation...")
            password = generator.generate_password(length=12)
            print(f"  Generated: {password} (length: {len(password)})")
            
            print("✓ Testing multiple password generation...")
            passwords = generator.generate_multiple_passwords(count=3, length=10)
            for i, pwd in enumerate(passwords, 1):
                print(f"  Password {i}: {pwd}")
            
            print("✓ Testing password strength checker...")
            strength = generator.check_password_strength("MyStr0ng!P@ssw0rd")
            print(f"  Test password score: {strength['score']}/100")
            
            print("✓ All components tested successfully!")
            
        except Exception as e:
            print(f"❌ Component test failed: {e}")
        return
        
    # Default behavior: try GUI first, fall back to CLI
    if not args.cli:
        if not launch_gui():
            print("\nFalling back to CLI version...")
            launch_cli()
    else:
        launch_cli()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Password Generator Setup - Diagnose and fix common installation issues
Run this before using the GUI version
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


class PasswordGeneratorSetup:
    """Setup and diagnostic tool for the Password Generator."""
    
    def __init__(self):
        self.system = platform.system()
        self.python_version = sys.version_info
        self.issues_found = []
        self.fixes_applied = []
    
    def run_diagnostics(self):
        """Run comprehensive diagnostics."""
        print("🔍 Password Generator - System Diagnostics")
        print("=" * 60)
        
        self.check_python_version()
        self.check_virtual_environment()
        self.check_tkinter_availability()
        self.check_dependencies()
        self.check_tcl_tk_libraries()
        
        self.show_summary()
        
        if self.issues_found:
            self.offer_fixes()
    
    def check_python_version(self):
        """Check Python version compatibility."""
        print(f"🐍 Python Version: {sys.version}")
        
        if self.python_version < (3, 6):
            self.issues_found.append("Python version too old (need 3.6+)")
        else:
            print("✅ Python version compatible")
    
    def check_virtual_environment(self):
        """Check virtual environment setup."""
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print(f"🔗 Virtual Environment: Active ({sys.prefix})")
            print(f"📁 Base Python: {sys.base_prefix}")
        else:
            print("🐍 Using system Python installation")
    
    def check_tkinter_availability(self):
        """Check if tkinter is available."""
        print("\n🧪 Testing Tkinter...")
        
        try:
            import tkinter as tk
            print("✅ Tkinter module import successful")
            
            # Try creating a root window
            try:
                root = tk.Tk()
                root.withdraw()
                root.destroy()
                print("✅ Tkinter GUI creation successful")
                return True
                
            except Exception as e:
                print(f"❌ Tkinter GUI creation failed: {e}")
                
                if "init.tcl" in str(e):
                    self.issues_found.append("Tcl/Tk libraries not found")
                else:
                    self.issues_found.append(f"Tkinter error: {e}")
                
                return False
                
        except ImportError:
            print("❌ Tkinter not available")
            self.issues_found.append("Tkinter not installed")
            return False
    
    def check_dependencies(self):
        """Check required dependencies."""
        print("\n📦 Checking Dependencies...")
        
        # Check pyperclip
        try:
            import pyperclip
            print("✅ pyperclip available")
        except ImportError:
            print("❌ pyperclip not installed")
            self.issues_found.append("pyperclip not installed")
        
        # Check password_generator module
        try:
            from password_generator import PasswordGenerator
            print("✅ password_generator module available")
        except ImportError:
            print("❌ password_generator module not found")
            self.issues_found.append("password_generator module missing")
    
    def check_tcl_tk_libraries(self):
        """Check Tcl/Tk library availability."""
        print("\n🔍 Searching for Tcl/Tk Libraries...")
        
        # Basic Tcl/Tk path detection
        try:
            # Get base Python directory
            if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
                base_python = Path(sys.base_prefix)
            else:
                base_python = Path(sys.executable).parent
            
            # Common search paths
            search_paths = [
                base_python / "tcl",
                base_python / "Library" / "lib",
            ]
            
            tcl_found = False
            tk_found = False
            
            for search_path in search_paths:
                if search_path.exists():
                    tcl_dirs = list(search_path.glob("tcl*"))
                    tk_dirs = list(search_path.glob("tk*"))
                    
                    if tcl_dirs:
                        print(f"✅ TCL libraries found: {tcl_dirs[0]}")
                        tcl_found = True
                    if tk_dirs:
                        print(f"✅ TK libraries found: {tk_dirs[0]}")
                        tk_found = True
                    
                    if tcl_found and tk_found:
                        break
            
            if not (tcl_found and tk_found):
                print("❌ Could not locate Tcl/Tk libraries")
                self.issues_found.append("Tcl/Tk libraries not found")
                
        except Exception as e:
            print(f"❌ Error checking Tcl/Tk libraries: {e}")
    
    def show_summary(self):
        """Show diagnostic summary."""
        print("\n" + "=" * 60)
        print("📊 DIAGNOSTIC SUMMARY")
        print("=" * 60)
        
        if not self.issues_found:
            print("🎉 No issues found! Your setup should work perfectly.")
            print("\n🚀 You can run the GUI with:")
            print("   python password_generator_gui.py")
            print("   python launcher.py")
            print("   .\\start_gui.bat  (Windows)")
        else:
            print(f"⚠️  Found {len(self.issues_found)} issues:")
            for issue in self.issues_found:
                print(f"   • {issue}")
    
    def offer_fixes(self):
        """Offer to fix common issues."""
        print("\n🔧 AVAILABLE FIXES")
        print("=" * 60)
        
        if "pyperclip not installed" in self.issues_found:
            if self.ask_yes_no("Install pyperclip for clipboard functionality?"):
                self.fix_pyperclip()
        
        if "Tkinter not installed" in self.issues_found:
            self.suggest_tkinter_installation()
        
        if "Tcl/Tk libraries not found" in self.issues_found:
            if self.ask_yes_no("Try to set up Tcl/Tk environment automatically?"):
                self.fix_tcl_tk_environment()
    
    def fix_pyperclip(self):
        """Install pyperclip."""
        try:
            print("📦 Installing pyperclip...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
            print("✅ pyperclip installed successfully")
            self.fixes_applied.append("Installed pyperclip")
        except subprocess.CalledProcessError:
            print("❌ Failed to install pyperclip")
            print("💡 Try manually: pip install pyperclip")
    
    def suggest_tkinter_installation(self):
        """Provide tkinter installation suggestions."""
        print("💡 Tkinter Installation Suggestions:")
        
        if self.system == "Windows":
            print("   1. Reinstall Python from python.org")
            print("   2. During installation, check 'tcl/tk and IDLE'")
            print("   3. Or install Anaconda/Miniconda")
        elif self.system == "Linux":
            print("   • Ubuntu/Debian: sudo apt-get install python3-tk")
            print("   • CentOS/RHEL: sudo yum install tkinter")
            print("   • Arch: sudo pacman -S tk")
        elif self.system == "Darwin":  # macOS
            print("   • Install Python from python.org (recommended)")
            print("   • Or: brew install python-tk")
            print("   • Avoid using system Python for GUI applications")
    
    def fix_tcl_tk_environment(self):
        """Attempt to fix Tcl/Tk environment."""
        try:
            # Integrated Tcl/Tk environment setup
            if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
                base_python = Path(sys.base_prefix)
            else:
                base_python = Path(sys.executable).parent
            
            tcl_dir = base_python / "tcl"
            if tcl_dir.exists():
                tcl_version_dirs = list(tcl_dir.glob("tcl*"))
                tk_version_dirs = list(tcl_dir.glob("tk*"))
                
                if tcl_version_dirs and tk_version_dirs:
                    os.environ['TCL_LIBRARY'] = str(tcl_version_dirs[0])
                    os.environ['TK_LIBRARY'] = str(tk_version_dirs[0])
                    print("✅ Tcl/Tk environment configured")
                    self.fixes_applied.append("Configured Tcl/Tk environment")
                    
                    # Test again
                    if self.check_tkinter_availability():
                        print("🎉 Tkinter now working!")
                    return True
            
            print("❌ Could not configure Tcl/Tk environment automatically")
            return False
                
        except Exception as e:
            print(f"❌ Error configuring Tcl/Tk: {e}")
            return False
    
    def ask_yes_no(self, question):
        """Ask a yes/no question."""
        while True:
            answer = input(f"{question} (y/n): ").lower().strip()
            if answer in ['y', 'yes']:
                return True
            elif answer in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'")
    
    def create_launcher_scripts(self):
        """Create convenient launcher scripts."""
        if self.ask_yes_no("Create desktop shortcuts/launchers?"):
            self.create_desktop_shortcuts()
    
    def create_desktop_shortcuts(self):
        """Create platform-specific desktop shortcuts."""
        if self.system == "Windows":
            self.create_windows_shortcut()
        elif self.system == "Linux":
            self.create_linux_desktop_file()
        elif self.system == "Darwin":
            print("💡 macOS: You can drag the .py file to your Dock")
    
    def create_windows_shortcut(self):
        """Create Windows shortcut."""
        # This would require additional Windows-specific code
        print("💡 Windows: You can create a shortcut to start_gui.bat")
    
    def create_linux_desktop_file(self):
        """Create Linux .desktop file."""
        desktop_file_content = f"""[Desktop Entry]
Name=Password Generator
Comment=Secure Password Generator
Exec={sys.executable} {Path.cwd() / 'launcher.py'}
Icon=applications-utilities
Terminal=false
Type=Application
Categories=Utility;
"""
        
        desktop_dir = Path.home() / "Desktop"
        if desktop_dir.exists():
            desktop_file = desktop_dir / "password_generator.desktop"
            try:
                desktop_file.write_text(desktop_file_content)
                desktop_file.chmod(0o755)
                print(f"✅ Created desktop shortcut: {desktop_file}")
            except Exception as e:
                print(f"❌ Could not create desktop file: {e}")


def main():
    """Main setup function."""
    setup = PasswordGeneratorSetup()
    setup.run_diagnostics()
    
    if setup.fixes_applied:
        print(f"\n✅ Applied {len(setup.fixes_applied)} fixes:")
        for fix in setup.fixes_applied:
            print(f"   • {fix}")
    
    print("\n🔒 Setup complete! You can now use the Password Generator.")
    print("\n📖 Usage:")
    print("   GUI: python password_generator_gui.py")
    print("   CLI: python password_generator.py")
    print("   Universal: python launcher.py")


if __name__ == "__main__":
    main()
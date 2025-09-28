#!/usr/bin/env python3
"""
Password Generator GUI - A user-friendly graphical interface for secure password generation
Author: Your Name
Date: September 27, 2025
"""

# Universal Tkinter setup - works across different systems and Python installations
import os
import sys
from pathlib import Path
import platform

def setup_universal_tkinter():
    """Universal Tkinter setup that works across systems and Python installations."""
    if os.environ.get('TCL_LIBRARY') and os.environ.get('TK_LIBRARY'):
        return True  # Already configured
    
    # Determine base Python directory
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        base_python = Path(sys.base_prefix)
    else:
        base_python = Path(sys.executable).parent
    
    system = platform.system()
    
    # System-specific Tcl/Tk search paths
    search_paths = []
    
    if system == "Windows":
        search_paths = [
            base_python / "tcl",
            base_python / "Library" / "lib",
            Path(os.environ.get('CONDA_PREFIX', '')) / "Library" / "lib" if os.environ.get('CONDA_PREFIX') else None
        ]
    elif system == "Darwin":  # macOS
        search_paths = [
            base_python / "lib",
            Path("/usr/local/lib"),
            Path("/opt/homebrew/lib")
        ]
    elif system == "Linux":
        search_paths = [
            base_python / "lib",
            Path("/usr/lib"),
            Path("/usr/local/lib")
        ]
    
    # Find and set Tcl/Tk libraries
    for search_path in [p for p in search_paths if p and p.exists()]:
        tcl_dirs = list(search_path.glob("tcl*"))
        tk_dirs = list(search_path.glob("tk*"))
        
        if tcl_dirs and tk_dirs:
            # Use the first valid match
            tcl_dir = next((d for d in tcl_dirs if d.is_dir()), None)
            tk_dir = next((d for d in tk_dirs if d.is_dir()), None)
            
            if tcl_dir and tk_dir:
                os.environ['TCL_LIBRARY'] = str(tcl_dir)
                os.environ['TK_LIBRARY'] = str(tk_dir)
                return True
    
    return False  # Could not set up automatically

# Set up Tkinter environment before importing
setup_universal_tkinter()

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyperclip
from password_generator import PasswordGenerator
import threading


class PasswordGeneratorGUI:
    """Graphical user interface for the password generator."""
    
    def __init__(self, root):
        self.root = root
        self.generator = PasswordGenerator()
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the user interface."""
        # Configure the main window
        self.root.title("Secure Password Generator")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔒 Secure Password Generator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Create sections
        self.create_options_section(main_frame, row=1)
        self.create_generation_section(main_frame, row=2)
        self.create_results_section(main_frame, row=3)
        self.create_strength_section(main_frame, row=4)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to generate passwords")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def create_options_section(self, parent, row):
        """Create the password options section."""
        options_frame = ttk.LabelFrame(parent, text="Password Options", padding="10")
        options_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        
        # Length setting
        ttk.Label(options_frame, text="Length:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.length_var = tk.IntVar(value=12)
        length_frame = ttk.Frame(options_frame)
        length_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.length_scale = ttk.Scale(length_frame, from_=4, to=64, orient=tk.HORIZONTAL,
                                     variable=self.length_var, command=self.update_length_label)
        self.length_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.length_label = ttk.Label(length_frame, text="12")
        self.length_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Count setting
        ttk.Label(options_frame, text="Count:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        count_frame = ttk.Frame(options_frame)
        count_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.count_var = tk.IntVar(value=1)
        count_spinbox = ttk.Spinbox(count_frame, from_=1, to=20, width=10,
                                   textvariable=self.count_var)
        count_spinbox.pack(side=tk.LEFT)
        
        # Character set options
        char_frame = ttk.Frame(options_frame)
        char_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(char_frame, text="Include Character Types:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        # Checkboxes for character sets
        checkbox_frame = ttk.Frame(char_frame)
        checkbox_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(checkbox_frame, text="Lowercase (a-z)", 
                       variable=self.use_lowercase).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Checkbutton(checkbox_frame, text="Uppercase (A-Z)", 
                       variable=self.use_uppercase).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Checkbutton(checkbox_frame, text="Digits (0-9)", 
                       variable=self.use_digits).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Checkbutton(checkbox_frame, text="Symbols (!@#$%)", 
                       variable=self.use_symbols).pack(side=tk.LEFT)
        
        # Exclude characters
        exclude_frame = ttk.Frame(char_frame)
        exclude_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(exclude_frame, text="Exclude Characters:").pack(side=tk.LEFT)
        self.exclude_var = tk.StringVar()
        exclude_entry = ttk.Entry(exclude_frame, textvariable=self.exclude_var, width=20)
        exclude_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Quick exclude buttons
        quick_exclude_frame = ttk.Frame(exclude_frame)
        quick_exclude_frame.pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(quick_exclude_frame, text="Ambiguous (0O1l)", 
                  command=lambda: self.exclude_var.set("0O1l")).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_exclude_frame, text="Clear", 
                  command=lambda: self.exclude_var.set("")).pack(side=tk.LEFT)
        
    def create_generation_section(self, parent, row):
        """Create the generation controls section."""
        gen_frame = ttk.Frame(parent)
        gen_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        gen_frame.columnconfigure(0, weight=1)
        
        button_frame = ttk.Frame(gen_frame)
        button_frame.pack()
        
        # Generate button
        self.generate_btn = ttk.Button(button_frame, text="🔐 Generate Password(s)", 
                                      command=self.generate_passwords, style="Accent.TButton")
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        clear_btn = ttk.Button(button_frame, text="🗑️ Clear Results", 
                              command=self.clear_results)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Copy all button
        self.copy_all_btn = ttk.Button(button_frame, text="📋 Copy All", 
                                      command=self.copy_all_passwords, state=tk.DISABLED)
        self.copy_all_btn.pack(side=tk.LEFT)
        
    def create_results_section(self, parent, row):
        """Create the results display section."""
        results_frame = ttk.LabelFrame(parent, text="Generated Passwords", padding="10")
        results_frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results text area with scrollbar
        self.results_text = scrolledtext.ScrolledText(results_frame, height=8, width=70,
                                                     font=("Courier", 10), state=tk.DISABLED)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for styling
        self.results_text.tag_configure("password", font=("Courier", 12, "bold"))
        self.results_text.tag_configure("info", foreground="gray")
        
    def create_strength_section(self, parent, row):
        """Create the password strength checker section."""
        strength_frame = ttk.LabelFrame(parent, text="Password Strength Checker", padding="10")
        strength_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        strength_frame.columnconfigure(1, weight=1)
        
        # Password input
        ttk.Label(strength_frame, text="Check Password:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        check_frame = ttk.Frame(strength_frame)
        check_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        check_frame.columnconfigure(0, weight=1)
        
        self.check_var = tk.StringVar()
        self.check_entry = ttk.Entry(check_frame, textvariable=self.check_var, show="*")
        self.check_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.check_entry.bind('<KeyRelease>', self.on_check_password_change)
        
        # Show/hide password button
        self.show_password = tk.BooleanVar()
        show_btn = ttk.Checkbutton(check_frame, text="Show", variable=self.show_password,
                                  command=self.toggle_password_visibility)
        show_btn.grid(row=0, column=1)
        
        # Strength display
        self.strength_frame = ttk.Frame(strength_frame)
        self.strength_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        self.strength_frame.columnconfigure(0, weight=1)
        
        # Progress bar for strength
        self.strength_var = tk.DoubleVar()
        self.strength_progress = ttk.Progressbar(self.strength_frame, variable=self.strength_var,
                                               maximum=100, length=300)
        self.strength_progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Strength label
        self.strength_label = ttk.Label(self.strength_frame, text="Enter a password to check its strength")
        self.strength_label.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Strength details
        self.strength_details = ttk.Label(self.strength_frame, text="", foreground="gray")
        self.strength_details.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
    def update_length_label(self, value):
        """Update the length label when scale changes."""
        length = int(float(value))
        self.length_label.config(text=str(length))
        
    def generate_passwords(self):
        """Generate passwords based on current settings."""
        try:
            # Validate settings
            if not any([self.use_lowercase.get(), self.use_uppercase.get(), 
                       self.use_digits.get(), self.use_symbols.get()]):
                messagebox.showerror("Error", "Please select at least one character type!")
                return
                
            # Update status
            self.status_var.set("Generating passwords...")
            self.generate_btn.config(state=tk.DISABLED)
            self.root.update()
            
            # Generate passwords
            passwords = self.generator.generate_multiple_passwords(
                count=self.count_var.get(),
                length=self.length_var.get(),
                use_lowercase=self.use_lowercase.get(),
                use_uppercase=self.use_uppercase.get(),
                use_digits=self.use_digits.get(),
                use_symbols=self.use_symbols.get(),
                exclude_chars=self.exclude_var.get()
            )
            
            # Display results
            self.display_passwords(passwords)
            
            # Update status
            count = len(passwords)
            self.status_var.set(f"Generated {count} password{'s' if count > 1 else ''}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate passwords: {str(e)}")
            self.status_var.set("Error generating passwords")
            
        finally:
            self.generate_btn.config(state=tk.NORMAL)
            
    def display_passwords(self, passwords):
        """Display generated passwords in the results area."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        for i, password in enumerate(passwords, 1):
            # Add password with copy button functionality
            self.results_text.insert(tk.END, f"Password {i}: ", "info")
            self.results_text.insert(tk.END, f"{password}\n", "password")
            
            # Add strength info
            strength = self.generator.check_password_strength(password)
            strength_text = self.get_strength_text(strength['score'])
            self.results_text.insert(tk.END, f"            Strength: {strength['score']}/100 ({strength_text})\n\n", "info")
            
        # Add copy instructions
        if passwords:
            self.results_text.insert(tk.END, "💡 Tip: Select text and right-click to copy, or use 'Copy All' button\n", "info")
            
        self.results_text.config(state=tk.DISABLED)
        self.copy_all_btn.config(state=tk.NORMAL)
        
        # Store passwords for copying
        self.current_passwords = passwords
        
    def get_strength_text(self, score):
        """Get strength description from score."""
        if score >= 80:
            return "Strong"
        elif score >= 60:
            return "Medium"
        else:
            return "Weak"
            
    def get_strength_color(self, score):
        """Get color for strength score."""
        if score >= 80:
            return "green"
        elif score >= 60:
            return "orange"
        else:
            return "red"
            
    def clear_results(self):
        """Clear the results area."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.copy_all_btn.config(state=tk.DISABLED)
        self.current_passwords = []
        self.status_var.set("Results cleared")
        
    def copy_all_passwords(self):
        """Copy all generated passwords to clipboard."""
        if hasattr(self, 'current_passwords') and self.current_passwords:
            passwords_text = '\n'.join(self.current_passwords)
            pyperclip.copy(passwords_text)
            self.status_var.set(f"Copied {len(self.current_passwords)} passwords to clipboard")
        else:
            messagebox.showwarning("Warning", "No passwords to copy!")
            
    def toggle_password_visibility(self):
        """Toggle password visibility in strength checker."""
        if self.show_password.get():
            self.check_entry.config(show="")
        else:
            self.check_entry.config(show="*")
            
    def on_check_password_change(self, event=None):
        """Handle password change in strength checker."""
        password = self.check_var.get()
        
        if not password:
            self.strength_var.set(0)
            self.strength_label.config(text="Enter a password to check its strength")
            self.strength_details.config(text="")
            return
            
        # Check strength
        strength = self.generator.check_password_strength(password)
        score = strength['score']
        
        # Update progress bar
        self.strength_var.set(score)
        
        # Update label with color
        strength_text = self.get_strength_text(score)
        color = self.get_strength_color(score)
        self.strength_label.config(text=f"Strength: {score}/100 ({strength_text})", 
                                  foreground=color)
        
        # Update details
        details = []
        if strength['has_lowercase']:
            details.append("✓ Lowercase")
        if strength['has_uppercase']:
            details.append("✓ Uppercase")
        if strength['has_digits']:
            details.append("✓ Digits")
        if strength['has_symbols']:
            details.append("✓ Symbols")
            
        details_text = f"Length: {strength['length']} | " + " | ".join(details)
        self.strength_details.config(text=details_text)


def main():
    """Main function to run the GUI application."""
    # Check if pyperclip is available
    try:
        import pyperclip
    except ImportError:
        print("Warning: pyperclip not available. Copy functionality will be limited.")
        # Create a mock pyperclip for basic functionality
        class MockPyperclip:
            @staticmethod
            def copy(text):
                print(f"Would copy to clipboard: {text[:50]}...")
        import sys
        sys.modules['pyperclip'] = MockPyperclip()
    
    # Create and run the application
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Add right-click context menu to results
    def create_context_menu():
        context_menu = tk.Menu(root, tearoff=0)
        context_menu.add_command(label="Copy Selection", 
                               command=lambda: copy_selection(app.results_text))
        context_menu.add_command(label="Select All", 
                               command=lambda: select_all(app.results_text))
        return context_menu
    
    def copy_selection(text_widget):
        try:
            selected_text = text_widget.selection_get()
            pyperclip.copy(selected_text)
            app.status_var.set("Selection copied to clipboard")
        except tk.TclError:
            pass  # No selection
            
    def select_all(text_widget):
        text_widget.tag_add(tk.SEL, "1.0", tk.END)
        
    def show_context_menu(event):
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    context_menu = create_context_menu()
    app.results_text.bind("<Button-3>", show_context_menu)  # Right-click
    
    # Run the application
    root.mainloop()


if __name__ == "__main__":
    main()
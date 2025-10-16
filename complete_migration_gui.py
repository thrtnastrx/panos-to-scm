#!/usr/bin/env python3
"""
PAN-OS to SCM Migration - Complete GUI Application
Includes configuration, object selection, live output, and results
"""

import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import yaml
from pathlib import Path
import threading
import subprocess
import queue
import sys
import os
import ssl
import urllib3
from datetime import datetime

# Disable SSL warnings
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MigrationGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("PAN-OS to Strata Cloud Manager Migration")
        self.root.geometry("1400x900")
        
        # Configuration
        self.config_path = Path.home() / ".panapi" / "config.yml"
        self.config = {}
        
        # Migration state
        self.selected_objects = []
        self.migration_process = None
        self.output_queue = queue.Queue()
        self.is_migrating = False
        
        # Object categories
        self.object_categories = {
            'Network Objects': {
                'Tag': 'Tags for objects',
                'Address': 'Address objects',
                'AddressGroup': 'Address groups',
                'Service': 'Service objects',
                'ServiceGroup': 'Service groups',
            },
            'Application Objects': {
                'Application': 'Custom application objects',
                'ApplicationFilter': 'Application filters',
                'ApplicationGroup': 'Application groups',
            },
            'Security Profiles': {
                'URLFilterProfile': 'URL filtering profiles',
                'VulnerabilityProfile': 'Vulnerability protection profiles',
                'AntiSpywareProfile': 'Anti-spyware profiles',
                'DNSSecurityProfile': 'DNS security profiles',
                'FileBlockingProfile': 'File blocking profiles',
                'DecryptionProfile': 'Decryption profiles',
                'ProfileGroup': 'Security profile groups',
            },
            'Other Objects': {
                'ExternalDynamicList': 'External dynamic lists',
                'CustomURLCategory': 'Custom URL categories',
                'HIPObject': 'Host Information Profile objects',
                'HIPProfile': 'HIP profiles',
            },
            'Security Policies': {
                'SecurityRules': 'Security policy rules',
                'NATRules': 'NAT policy rules',
                'AppOverrideRules': 'Application override rules',
                'DecryptionRules': 'Decryption policy rules',
            }
        }
        
        self.setup_ui()
        self.load_config()
        
    def setup_ui(self):
        """Setup the main UI"""
        
        # Main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            main_container,
            text="PAN-OS to Strata Cloud Manager Migration Tool",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 10))
        
        # Create tab view
        self.tabview = ctk.CTkTabview(main_container)
        self.tabview.pack(fill="both", expand=True)
        
        # Add tabs
        self.tabview.add("Configuration")
        self.tabview.add("Select Objects")
        self.tabview.add("Migration")
        
        self.setup_config_tab()
        self.setup_selection_tab()
        self.setup_migration_tab()
        
    def setup_config_tab(self):
        """Setup configuration tab"""
        tab = self.tabview.tab("Configuration")
        
        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # SCM Section
        scm_frame = ctk.CTkFrame(scroll_frame)
        scm_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            scm_frame,
            text="Strata Cloud Manager Credentials",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10, padx=20, anchor="w")
        
        # Client ID
        self.client_id_var = ctk.StringVar()
        self.create_config_field(scm_frame, "Client ID:", self.client_id_var)
        
        # Client Secret
        self.client_secret_var = ctk.StringVar()
        self.create_config_field(scm_frame, "Client Secret:", self.client_secret_var, show="*")
        
        # TSG ID
        self.tsg_id_var = ctk.StringVar()
        self.create_config_field(scm_frame, "TSG ID:", self.tsg_id_var)
        
        # PAN-OS Section
        panos_frame = ctk.CTkFrame(scroll_frame)
        panos_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            panos_frame,
            text="PAN-OS/Panorama Credentials",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10, padx=20, anchor="w")
        
        # URL
        self.panos_url_var = ctk.StringVar()
        self.create_config_field(panos_frame, "Panorama URL:", self.panos_url_var)
        
        # Username
        self.panos_user_var = ctk.StringVar()
        self.create_config_field(panos_frame, "Username:", self.panos_user_var)
        
        # Password
        self.panos_pass_var = ctk.StringVar()
        self.create_config_field(panos_frame, "Password:", self.panos_pass_var, show="*")
        
        # Buttons
        button_frame = ctk.CTkFrame(scroll_frame)
        button_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Save Configuration",
            command=self.save_config,
            height=40,
            width=200
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Test Connection",
            command=self.test_connection,
            height=40,
            width=200
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Load Configuration",
            command=self.load_config,
            height=40,
            width=200
        ).pack(side="left", padx=5)
        
    def setup_selection_tab(self):
        """Setup object selection tab"""
        tab = self.tabview.tab("Select Objects")
        
        # Top controls
        control_frame = ctk.CTkFrame(tab)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            control_frame,
            text="Select Configuration Objects to Migrate",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            control_frame,
            text="Select All",
            command=lambda: self.toggle_all_selections(True),
            width=120
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            control_frame,
            text="Clear All",
            command=lambda: self.toggle_all_selections(False),
            width=120
        ).pack(side="right", padx=5)
        
        # Presets
        preset_frame = ctk.CTkFrame(tab)
        preset_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(
            preset_frame,
            text="Quick Presets:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=10)
        
        presets = [
            ("Basic Network", ['Tag', 'Address', 'AddressGroup', 'Service', 'ServiceGroup']),
            ("Security Profiles", ['URLFilterProfile', 'VulnerabilityProfile', 'AntiSpywareProfile', 'ProfileGroup']),
            ("Security Rules", ['SecurityRules']),
            ("All Policies", ['SecurityRules', 'NATRules', 'AppOverrideRules', 'DecryptionRules'])
        ]
        
        for name, objects in presets:
            ctk.CTkButton(
                preset_frame,
                text=name,
                command=lambda objs=objects: self.apply_preset(objs),
                width=120
            ).pack(side="left", padx=5)
        
        # Scrollable selection area
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.checkboxes = {}
        
        for category, objects in self.object_categories.items():
            # Category header
            category_frame = ctk.CTkFrame(scroll_frame)
            category_frame.pack(fill="x", pady=(15, 5))
            
            ctk.CTkLabel(
                category_frame,
                text=category,
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(side="left", padx=10)
            
            # Select/Deselect category buttons
            ctk.CTkButton(
                category_frame,
                text="Select All",
                command=lambda cat=category: self.toggle_category(cat, True),
                width=80,
                height=25
            ).pack(side="right", padx=2)
            
            ctk.CTkButton(
                category_frame,
                text="Clear",
                command=lambda cat=category: self.toggle_category(cat, False),
                width=80,
                height=25
            ).pack(side="right", padx=2)
            
            # Object checkboxes
            for obj_type, description in objects.items():
                var = ctk.BooleanVar(value=False)
                self.checkboxes[obj_type] = var
                
                cb_frame = ctk.CTkFrame(scroll_frame)
                cb_frame.pack(fill="x", padx=20, pady=2)
                
                ctk.CTkCheckBox(
                    cb_frame,
                    text=f"{obj_type}",
                    variable=var,
                    font=ctk.CTkFont(size=12, weight="bold")
                ).pack(side="left")
                
                ctk.CTkLabel(
                    cb_frame,
                    text=f"- {description}",
                    font=ctk.CTkFont(size=11),
                    text_color="gray"
                ).pack(side="left", padx=5)
        
        # Selection summary
        self.selection_summary = ctk.CTkLabel(
            tab,
            text="Selected: 0 object types",
            font=ctk.CTkFont(size=12)
        )
        self.selection_summary.pack(pady=10)
        
        # Update summary button
        ctk.CTkButton(
            tab,
            text="Update Selection Count",
            command=self.update_selection_summary,
            width=200
        ).pack(pady=5)
        
    def setup_migration_tab(self):
        """Setup migration tab with live output"""
        tab = self.tabview.tab("Migration")
        
        # Migration Configuration Section
        config_frame = ctk.CTkFrame(tab)
        config_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            config_frame,
            text="Migration Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Source Type
        source_frame = ctk.CTkFrame(config_frame)
        source_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(
            source_frame,
            text="Configuration Source:",
            width=180,
            anchor="w"
        ).pack(side="left", padx=10)
        
        self.source_type_var = ctk.StringVar(value="shared")
        source_menu = ctk.CTkOptionMenu(
            source_frame,
            values=["shared", "device-group"],
            variable=self.source_type_var,
            width=200
        )
        source_menu.pack(side="left", padx=10)
        
        ctk.CTkLabel(
            source_frame,
            text="(Source device-group or 'shared' from Panorama or Firewall)",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        ).pack(side="left", padx=5)
        
        # Device Group Name (only if device-group selected)
        dg_frame = ctk.CTkFrame(config_frame)
        dg_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(
            dg_frame,
            text="Device Group Name:",
            width=180,
            anchor="w"
        ).pack(side="left", padx=10)
        
        self.device_group_var = ctk.StringVar()
        self.device_group_entry = ctk.CTkEntry(
            dg_frame,
            textvariable=self.device_group_var,
            width=200,
            placeholder_text="Required if source is device-group"
        )
        self.device_group_entry.pack(side="left", padx=10)
        
        ctk.CTkLabel(
            dg_frame,
            text="(Name of device-group in Panorama)",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        ).pack(side="left", padx=5)
        
        # Destination Type
        dest_frame = ctk.CTkFrame(config_frame)
        dest_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(
            dest_frame,
            text="SCM Destination Type:",
            width=180,
            anchor="w"
        ).pack(side="left", padx=10)
        
        self.dest_type_var = ctk.StringVar(value="folder")
        dest_menu = ctk.CTkOptionMenu(
            dest_frame,
            values=["folder", "snippet"],
            variable=self.dest_type_var,
            width=200
        )
        dest_menu.pack(side="left", padx=10)
        
        ctk.CTkLabel(
            dest_frame,
            text="(Destination folder or snippet in SCM)",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        ).pack(side="left", padx=5)
        
        # Destination Name
        dest_name_frame = ctk.CTkFrame(config_frame)
        dest_name_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(
            dest_name_frame,
            text="Destination Name:",
            width=180,
            anchor="w"
        ).pack(side="left", padx=10)
        
        self.dest_name_var = ctk.StringVar(value="")
        self.dest_name_entry = ctk.CTkEntry(
            dest_name_frame,
            textvariable=self.dest_name_var,
            width=200,
            placeholder_text="Enter folder or snippet name"
        )
        self.dest_name_entry.pack(side="left", padx=10)
        
        ctk.CTkLabel(
            dest_name_frame,
            text="(Name of destination folder or snippet in SCM)",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        ).pack(side="left", padx=5)
        
        # Fetch new config option
        fetch_frame = ctk.CTkFrame(config_frame)
        fetch_frame.pack(fill="x", padx=20, pady=10)
        
        self.fetch_config_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            fetch_frame,
            text="Fetch new configuration from Panorama (recommended)",
            variable=self.fetch_config_var,
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=10)
        
        # Accept untrusted certificate
        cert_frame = ctk.CTkFrame(config_frame)
        cert_frame.pack(fill="x", padx=20, pady=5)
        
        self.accept_cert_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            cert_frame,
            text="Accept untrusted certificate (self-signed)",
            variable=self.accept_cert_var,
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=10)
        
        # Separator
        separator = ctk.CTkFrame(tab, height=2)
        separator.pack(fill="x", padx=20, pady=15)
        
        # Status info
        info_frame = ctk.CTkFrame(tab)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text="Migration Status",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        self.status_label = ctk.CTkLabel(
            info_frame,
            text="Ready to migrate",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=5)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(tab)
        self.progress_bar.pack(fill="x", padx=20, pady=10)
        self.progress_bar.set(0)
        
        # Output window
        output_frame = ctk.CTkFrame(tab)
        output_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            output_frame,
            text="Migration Output (Live)",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        # Create text widget for output
        self.output_text = ctk.CTkTextbox(output_frame, wrap="word")
        self.output_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Control buttons
        button_frame = ctk.CTkFrame(tab)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        self.start_button = ctk.CTkButton(
            button_frame,
            text="Start Migration",
            command=self.start_migration,
            height=50,
            width=200,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green"
        )
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="Stop Migration",
            command=self.stop_migration,
            height=50,
            width=200,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="red",
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Clear Output",
            command=self.clear_output,
            height=50,
            width=200
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Save Log",
            command=self.save_log,
            height=50,
            width=200
        ).pack(side="left", padx=5)
        
    def create_config_field(self, parent, label_text, variable, show=None):
        """Create a configuration input field"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(
            frame,
            text=label_text,
            width=150,
            anchor="w"
        ).pack(side="left", padx=10)
        
        ctk.CTkEntry(
            frame,
            textvariable=variable,
            show=show
        ).pack(side="left", fill="x", expand=True, padx=10)
        
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    self.config = yaml.safe_load(f) or {}
                
                self.client_id_var.set(self.config.get('client_id', ''))
                self.client_secret_var.set(self.config.get('client_secret', ''))
                self.tsg_id_var.set(str(self.config.get('tsg_id', '')))
                self.panos_url_var.set(self.config.get('palo_alto_ngfw_url', ''))
                self.panos_user_var.set(self.config.get('palo_alto_username', ''))
                self.panos_pass_var.set(self.config.get('palo_alto_password', ''))
                
                messagebox.showinfo("Success", "Configuration loaded successfully!")
            else:
                messagebox.showwarning("Not Found", f"Configuration file not found:\n{self.config_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration:\n{str(e)}")
            
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                'client_id': self.client_id_var.get(),
                'client_secret': self.client_secret_var.get(),
                'tsg_id': self.tsg_id_var.get(),
                'palo_alto_ngfw_url': self.panos_url_var.get(),
                'palo_alto_username': self.panos_user_var.get(),
                'palo_alto_password': self.panos_pass_var.get(),
            }
            
            # Create directory if needed
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            # Set file permissions
            os.chmod(self.config_path, 0o600)
            
            messagebox.showinfo("Success", "Configuration saved successfully!")
            self.config = config
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")
            
    def test_connection(self):
        """Test connection to Panorama"""
        self.add_output("Testing connection to Panorama...\n")
        
        def test():
            try:
                import requests
                
                url = self.panos_url_var.get()
                username = self.panos_user_var.get()
                password = self.panos_pass_var.get()
                
                from urllib.parse import quote
                keygen_url = f"{url}?type=keygen&user={quote(username)}&password={quote(password)}"
                
                response = requests.get(keygen_url, verify=False, timeout=10)
                
                if response.status_code == 200:
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(response.text)
                    if root.get('status') == 'success':
                        self.add_output("✓ Connection successful!\n")
                        messagebox.showinfo("Success", "Connection to Panorama successful!")
                    else:
                        error = root.find('.//msg')
                        msg = error.text if error is not None else "Unknown error"
                        self.add_output(f"✗ Authentication failed: {msg}\n")
                        messagebox.showerror("Failed", f"Authentication failed:\n{msg}")
                else:
                    self.add_output(f"✗ HTTP Error: {response.status_code}\n")
                    messagebox.showerror("Failed", f"HTTP Error: {response.status_code}")
                    
            except Exception as e:
                self.add_output(f"✗ Connection failed: {str(e)}\n")
                messagebox.showerror("Error", f"Connection failed:\n{str(e)}")
        
        threading.Thread(target=test, daemon=True).start()
        
    def toggle_all_selections(self, state):
        """Select or deselect all checkboxes"""
        for var in self.checkboxes.values():
            var.set(state)
        self.update_selection_summary()
        
    def toggle_category(self, category, state):
        """Toggle all items in a category"""
        objects = self.object_categories[category]
        for obj_type in objects.keys():
            if obj_type in self.checkboxes:
                self.checkboxes[obj_type].set(state)
        self.update_selection_summary()
        
    def apply_preset(self, objects):
        """Apply a preset selection"""
        # Clear all first
        for var in self.checkboxes.values():
            var.set(False)
        # Set preset
        for obj_type in objects:
            if obj_type in self.checkboxes:
                self.checkboxes[obj_type].set(True)
        self.update_selection_summary()
        
    def update_selection_summary(self):
        """Update the selection count"""
        count = sum(1 for var in self.checkboxes.values() if var.get())
        self.selection_summary.configure(text=f"Selected: {count} object types")
        
    def add_output(self, text):
        """Add text to output window"""
        self.output_text.insert("end", text)
        self.output_text.see("end")
        self.root.update_idletasks()
        
    def clear_output(self):
        """Clear output window"""
        self.output_text.delete("1.0", "end")
        
    def save_log(self):
        """Save output to file"""
        try:
            log_dir = Path.home() / ".panapi" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = log_dir / f"migration_{timestamp}.log"
            
            with open(log_file, 'w') as f:
                f.write(self.output_text.get("1.0", "end"))
            
            messagebox.showinfo("Saved", f"Log saved to:\n{log_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save log:\n{str(e)}")
            
    def start_migration(self):
        """Start the migration process"""
        # Get selected objects
        selected = [name for name, var in self.checkboxes.items() if var.get()]
        
        if not selected:
            messagebox.showwarning("No Selection", "Please select at least one object type to migrate")
            return
        
        # Validate migration configuration
        dest_name = self.dest_name_var.get().strip()
        if not dest_name:
            messagebox.showerror("Missing Configuration", "Please enter a destination name (folder or snippet name in SCM)")
            self.tabview.set("Migration")
            self.dest_name_entry.focus()
            return
        
        # If device-group selected, require device group name
        if self.source_type_var.get() == "device-group":
            dg_name = self.device_group_var.get().strip()
            if not dg_name:
                messagebox.showerror("Missing Configuration", "Please enter a device group name or select 'shared' as source")
                self.tabview.set("Migration")
                self.device_group_entry.focus()
                return
        
        # Build command
        cmd = self.build_migration_command(selected)
        
        if not cmd:
            return
        
        # Build summary
        summary = "Migration Configuration:\n"
        summary += "="*50 + "\n\n"
        summary += f"Source: {self.source_type_var.get()}"
        if self.source_type_var.get() == "device-group":
            summary += f" ({self.device_group_var.get()})"
        summary += f"\n"
        summary += f"Destination: {self.dest_type_var.get()} - '{dest_name}'\n"
        summary += f"Fetch new config: {'Yes' if self.fetch_config_var.get() else 'No'}\n"
        summary += f"Accept cert: {'Yes' if self.accept_cert_var.get() else 'No'}\n\n"
        summary += f"Objects to migrate ({len(selected)}):\n"
        summary += "\n".join(f"  • {obj}" for obj in selected[:15])
        if len(selected) > 15:
            summary += f"\n  ... and {len(selected) - 15} more"
        
        if not messagebox.askyesno("Confirm Migration", summary):
            return
        
        self.is_migrating = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text="Migration in progress...")
        self.progress_bar.set(0.3)
        
        self.clear_output()
        self.add_output("="*80 + "\n")
        self.add_output("MIGRATION STARTED\n")
        self.add_output(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.add_output("="*80 + "\n\n")
        self.add_output(f"Source: {self.source_type_var.get()}\n")
        if self.source_type_var.get() == "device-group":
            self.add_output(f"Device Group: {self.device_group_var.get()}\n")
        self.add_output(f"Destination: {self.dest_type_var.get()} - '{dest_name}'\n")
        self.add_output(f"Command: {' '.join(cmd)}\n\n")
        
        # Run migration in thread
        threading.Thread(target=self.run_migration, args=(cmd,), daemon=True).start()
        
    def build_migration_command(self, selected):
        """Build the migration command with all configuration parameters"""
        # Use Python pexpect wrapper that handles prompts properly
        cmd = ['python3', 'auto_migrate.py']
        
        # Add configuration parameters
        cmd.append(self.source_type_var.get())  # shared or device-group
        cmd.append(self.device_group_var.get() if self.source_type_var.get() == "device-group" else "")  # DG name
        cmd.append(self.dest_type_var.get())  # folder or snippet
        cmd.append(self.dest_name_var.get())  # destination name
        cmd.append('yes' if self.fetch_config_var.get() else 'no')  # fetch config
        cmd.append('yes' if self.accept_cert_var.get() else 'no')  # accept cert
        
        # Separate policies from objects
        policy_types = ['SecurityRules', 'NATRules', 'AppOverrideRules', 'DecryptionRules']
        selected_policies = [obj for obj in selected if obj in policy_types]
        selected_objects = [obj for obj in selected if obj not in policy_types]
        
        if selected_objects:
            cmd.extend(['-o', ','.join(selected_objects)])
        
        if 'SecurityRules' in selected_policies:
            cmd.append('-s')
        if 'NATRules' in selected_policies:
            cmd.append('-n')
        if 'DecryptionRules' in selected_policies:
            cmd.append('-d')
        if 'AppOverrideRules' in selected_policies:
            cmd.append('-p')
        
        return cmd
        
    def run_migration(self, cmd):
        """Run the migration process"""
        try:
            self.migration_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Read output line by line
            for line in self.migration_process.stdout:
                if not self.is_migrating:
                    break
                self.add_output(line)
            
            # Wait for process to complete
            return_code = self.migration_process.wait()
            
            self.add_output("\n" + "="*80 + "\n")
            if return_code == 0:
                self.add_output("✓ MIGRATION COMPLETED SUCCESSFULLY\n")
                result_text = "Migration completed successfully!"
                result_type = "success"
            else:
                self.add_output(f"✗ MIGRATION COMPLETED WITH ERRORS (code: {return_code})\n")
                result_text = f"Migration completed with errors.\nReturn code: {return_code}"
                result_type = "error"
            self.add_output("="*80 + "\n")
            
            # Show results popup
            self.show_migration_results(result_text, result_type)
            
        except Exception as e:
            self.add_output(f"\n✗ ERROR: {str(e)}\n")
            self.show_migration_results(f"Migration failed:\n{str(e)}", "error")
        finally:
            self.is_migrating = False
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.status_label.configure(text="Migration complete")
            self.progress_bar.set(1.0)
            
    def stop_migration(self):
        """Stop the migration process"""
        if self.migration_process and self.migration_process.poll() is None:
            self.migration_process.terminate()
            self.is_migrating = False
            self.add_output("\n✗ MIGRATION CANCELLED BY USER\n")
            self.status_label.configure(text="Migration cancelled")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            
    def show_migration_results(self, message, result_type):
        """Show migration results in a popup with formatted errors"""
        # Create popup window
        popup = ctk.CTkToplevel(self.root)
        popup.title("Migration Results")
        popup.geometry("800x600")
        popup.transient(self.root)
        popup.grab_set()
        
        # Icon and message
        icon_frame = ctk.CTkFrame(popup)
        icon_frame.pack(fill="x", padx=20, pady=20)
        
        if result_type == "success":
            icon_text = "✓"
            icon_color = "green"
        else:
            icon_text = "✗"
            icon_color = "red"
        
        ctk.CTkLabel(
            icon_frame,
            text=icon_text,
            font=ctk.CTkFont(size=48),
            text_color=icon_color
        ).pack(side="left", padx=20)
        
        ctk.CTkLabel(
            icon_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=600
        ).pack(side="left", padx=10)
        
        # Details frame with tabs
        details_frame = ctk.CTkFrame(popup)
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create tabs for summary and errors
        tab_view = ctk.CTkTabview(details_frame)
        tab_view.pack(fill="both", expand=True)
        
        tab_view.add("Summary")
        tab_view.add("Errors")
        tab_view.add("Full Output")
        
        # Parse output
        output_text = self.output_text.get("1.0", "end")
        
        # Summary Tab
        summary_text = ctk.CTkTextbox(tab_view.tab("Summary"), wrap="word")
        summary_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Extract summary statistics
        success_count = output_text.count("created successfully")
        error_count = output_text.count("ERROR")
        existed_count = output_text.count("already existed")
        
        summary_text.insert("end", "Migration Summary\n")
        summary_text.insert("end", "="*60 + "\n\n")
        summary_text.insert("end", f"✓ Successfully Created: {success_count}\n")
        summary_text.insert("end", f"⊙ Already Existed: {existed_count}\n")
        summary_text.insert("end", f"✗ Errors: {error_count}\n\n")
        
        # Extract completion messages
        for line in output_text.split('\n'):
            if 'Summary:' in line or 'created,' in line or 'already existed' in line:
                summary_text.insert("end", line + "\n")
        
        summary_text.configure(state="disabled")
        
        # Errors Tab - Format errors nicely
        errors_text = ctk.CTkTextbox(tab_view.tab("Errors"), wrap="word")
        errors_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        if error_count > 0:
            errors_text.insert("end", "Migration Errors (Detailed)\n")
            errors_text.insert("end", "="*60 + "\n\n")
            
            # Parse and format errors
            import re
            error_lines = []
            for line in output_text.split('\n'):
                if 'ERROR' in line and 'API Error' in line:
                    error_lines.append(line)
            
            for i, error_line in enumerate(error_lines, 1):
                # Extract object name
                obj_match = re.search(r"'([^']+)':", error_line)
                obj_name = obj_match.group(1) if obj_match else "Unknown"
                
                errors_text.insert("end", f"{i}. Object: {obj_name}\n")
                errors_text.insert("end", "-"*60 + "\n")
                
                # Extract error details from JSON
                json_match = re.search(r'\{.*\}', error_line)
                if json_match:
                    try:
                        import json
                        error_json = json.loads(json_match.group(0))
                        
                        if '_errors' in error_json and error_json['_errors']:
                            error_info = error_json['_errors'][0]
                            
                            # Main error message
                            if 'message' in error_info:
                                errors_text.insert("end", f"   Error: {error_info['message']}\n")
                            
                            # Details
                            if 'details' in error_info:
                                details = error_info['details']
                                
                                if 'errorType' in details:
                                    errors_text.insert("end", f"   Type: {details['errorType']}\n")
                                
                                # Parse message array or string
                                if 'message' in details:
                                    msg = details['message']
                                    if isinstance(msg, list):
                                        errors_text.insert("end", "   Issues:\n")
                                        for issue in msg:
                                            cleaned_issue = issue.strip()
                                            if cleaned_issue:
                                                errors_text.insert("end", f"      • {cleaned_issue}\n")
                                    elif isinstance(msg, str):
                                        errors_text.insert("end", f"   Details: {msg}\n")
                                
                                # Parse specific error types
                                if 'errors' in details:
                                    for err in details['errors']:
                                        if 'type' in err:
                                            errors_text.insert("end", f"   • {err['type']}: {err.get('message', 'N/A')}\n")
                    except:
                        # If JSON parsing fails, show raw error
                        errors_text.insert("end", f"   Raw: {error_line}\n")
                else:
                    errors_text.insert("end", f"   {error_line}\n")
                
                errors_text.insert("end", "\n")
        else:
            errors_text.insert("end", "No errors detected! ✓\n\n")
            errors_text.insert("end", "All objects were migrated successfully.")
        
        errors_text.configure(state="disabled")
        
        # Full Output Tab
        full_text = ctk.CTkTextbox(tab_view.tab("Full Output"), wrap="word")
        full_text.pack(fill="both", expand=True, padx=10, pady=10)
        full_text.insert("1.0", output_text)
        full_text.configure(state="disabled")
        
        # Button frame
        button_frame = ctk.CTkFrame(popup)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        # Copy to Clipboard button
        def copy_to_clipboard():
            # Get the current tab content
            current_tab = tab_view.get()
            if current_tab == "Summary":
                content = summary_text.get("1.0", "end")
            elif current_tab == "Errors":
                content = errors_text.get("1.0", "end")
            else:
                content = full_text.get("1.0", "end")
            
            popup.clipboard_clear()
            popup.clipboard_append(content)
            
            # Show feedback
            copy_btn.configure(text="✓ Copied!")
            popup.after(2000, lambda: copy_btn.configure(text="Copy to Clipboard"))
        
        copy_btn = ctk.CTkButton(
            button_frame,
            text="Copy to Clipboard",
            command=copy_to_clipboard,
            width=200,
            height=40
        )
        copy_btn.pack(side="left", padx=5)
        
        # Export to File button
        def export_to_file():
            from tkinter import filedialog
            from datetime import datetime
            
            default_name = f"migration_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=default_name
            )
            
            if filename:
                with open(filename, 'w') as f:
                    f.write("="*80 + "\n")
                    f.write("MIGRATION RESULTS\n")
                    f.write("="*80 + "\n\n")
                    f.write(f"Time: {datetime.now()}\n\n")
                    f.write("SUMMARY\n")
                    f.write("-"*80 + "\n")
                    f.write(summary_text.get("1.0", "end"))
                    f.write("\n\nERRORS\n")
                    f.write("-"*80 + "\n")
                    f.write(errors_text.get("1.0", "end"))
                    f.write("\n\nFULL OUTPUT\n")
                    f.write("-"*80 + "\n")
                    f.write(full_text.get("1.0", "end"))
                
                messagebox.showinfo("Saved", f"Results exported to:\n{filename}")
        
        export_btn = ctk.CTkButton(
            button_frame,
            text="Export to File",
            command=export_to_file,
            width=200,
            height=40
        )
        export_btn.pack(side="left", padx=5)
        
        # Close button
        ctk.CTkButton(
            button_frame,
            text="Close",
            command=popup.destroy,
            width=200,
            height=40
        ).pack(side="right", padx=5)
        
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MigrationGUI()
    app.run()

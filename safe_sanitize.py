#!/usr/bin/env python3
"""
Safe sanitization script - Only sanitizes documentation and config examples
Does NOT touch Python code to avoid breaking functionality
"""

import re
from pathlib import Path
import shutil

class SafeSanitizer:
    def __init__(self):
        # Only these specific replacements in documentation
        self.replacements = [
            # Your specific domain
            (r'panorama\.thrtnastrx\.com', 'panorama.example.com'),
            (r'thrtnastrx\.com', 'example.com'),
            
            # Your specific device groups
            (r'aa-home', 'your-device-group'),
            (r'aa-strict', 'your-profile-group'),
            
            # Your username (in examples only)
            (r'aa-admin', 'admin'),
            
            # Your user ID (in paths only)
            (r'206788335', 'username'),
            
            # Specific real IPs in examples (keep 10.x.x.x format)
            (r'192\.168\.\d+\.\d+', '10.1.1.1'),
        ]
        
        # Only sanitize these file types (documentation only)
        self.files_to_sanitize = [
            'README.md',
            'INSTALLATION.md',
            'USER_GUIDE.md',
            'TROUBLESHOOTING.md',
            'PUBLISHING_CHECKLIST.md',
            '*.example',
            'example_*.txt',
        ]
        
        # Files that should be deleted (contain real data)
        self.files_to_delete = [
            'running_config.xml',
            'cisco_config.txt',
            '*.log',
            'sanitization_report.txt',
        ]
        
        # Directories to clean
        self.dirs_to_clean = [
            '__pycache__',
            '.pytest_cache',
            'build',
            'dist',
            '*.egg-info',
        ]

    def sanitize_file(self, file_path: Path) -> int:
        """Sanitize a documentation file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Apply replacements
            for pattern, replacement in self.replacements:
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            # Write back if changed
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                return 1
            
            return 0
            
        except Exception as e:
            print(f"  ⚠️  Error sanitizing {file_path}: {e}")
            return 0

    def run(self, directory: Path = Path.cwd(), dry_run: bool = False):
        """Run safe sanitization"""
        print("="*70)
        print("Safe Sanitization for Publishing")
        print("="*70)
        print()
        
        if dry_run:
            print("🔍 DRY RUN MODE - No files will be modified\n")
        
        # Step 1: Delete sensitive files
        print("Step 1: Removing files with real configuration data...")
        deleted_count = 0
        for pattern in self.files_to_delete:
            for file_path in directory.rglob(pattern):
                if file_path.is_file():
                    print(f"  🗑️  Deleting: {file_path.relative_to(directory)}")
                    if not dry_run:
                        file_path.unlink()
                    deleted_count += 1
        
        if deleted_count == 0:
            print("  ✓ No sensitive files found")
        print()
        
        # Step 2: Clean build directories
        print("Step 2: Cleaning build artifacts...")
        cleaned_count = 0
        for pattern in self.dirs_to_clean:
            for dir_path in directory.rglob(pattern):
                if dir_path.is_dir():
                    print(f"  🗑️  Removing: {dir_path.relative_to(directory)}/")
                    if not dry_run:
                        shutil.rmtree(dir_path)
                    cleaned_count += 1
        
        if cleaned_count == 0:
            print("  ✓ No build artifacts found")
        print()
        
        # Step 3: Sanitize documentation files
        print("Step 3: Sanitizing documentation files...")
        sanitized_count = 0
        
        for pattern in self.files_to_sanitize:
            for file_path in directory.rglob(pattern):
                if not file_path.is_file():
                    continue
                
                # Skip if in venv or build dirs
                if any(skip in str(file_path) for skip in ['venv', 'build', 'dist', '.git']):
                    continue
                
                if not dry_run:
                    count = self.sanitize_file(file_path)
                    if count > 0:
                        print(f"  ✓ Sanitized: {file_path.relative_to(directory)}")
                        sanitized_count += 1
                else:
                    print(f"  Would sanitize: {file_path.relative_to(directory)}")
        
        if sanitized_count == 0 and not dry_run:
            print("  ✓ No documentation files needed sanitization")
        print()
        
        # Step 4: Check for .panapi config
        print("Step 4: Checking for credentials in home directory...")
        home_config = Path.home() / ".panapi" / "config.yml"
        if home_config.exists():
            print(f"  ⚠️  Found: {home_config}")
            print(f"     This file contains your real credentials")
            print(f"     It will NOT be included in the repository")
        else:
            print("  ✓ No .panapi/config.yml found in home directory")
        print()
        
        # Summary
        print("="*70)
        print("Summary")
        print("="*70)
        print(f"Files deleted: {deleted_count}")
        print(f"Directories cleaned: {cleaned_count}")
        print(f"Documentation files sanitized: {sanitized_count}")
        print()
        
        if not dry_run:
            print("✅ Safe sanitization complete!")
            print()
            print("Next steps:")
            print("  1. Review changes: git diff")
            print("  2. Test the app: python3 complete_migration_gui.py")
            print("  3. Create example config: python3 safe_sanitize.py --create-example")
            print("  4. Review PUBLISHING_CHECKLIST.md")
        else:
            print("Run without --dry-run to apply changes")
        print()

    def create_example_config(self):
        """Create example configuration file"""
        example_config = Path.cwd() / "config.yml.example"
        
        config_content = """# PAN-OS to SCM Migration Tool - Configuration Example
# Copy this file to ~/.panapi/config.yml and fill in your values

# Strata Cloud Manager Credentials
# Get these from: https://apps.paloaltonetworks.com
# Settings → Identity & Access → Service Accounts
client_id: your-client-id@12345.iam.panserviceaccount.com
client_secret: your-client-secret-here
tsg_id: 1234567890

# PAN-OS/Panorama Credentials
palo_alto_ngfw_url: https://panorama.example.com/api/
palo_alto_username: admin
palo_alto_password: your-password-here

# Optional: Use API token instead of username/password
# palo_api_token: your-api-token-here

# Optional: Migration Settings
migration:
  conflict_strategy: prompt  # prompt, merge, replace, append, ignore
  dry_run: true
  parallel_workers: 4
  timeout: 30
  retry_attempts: 3

# Optional: Logging Settings
logging:
  level: INFO
  file: ~/.panapi/migration.log
"""
        
        example_config.write_text(config_content)
        print(f"✓ Created example configuration: {example_config}")
        print()
        print("Users should:")
        print("  1. Copy this to ~/.panapi/config.yml")
        print("  2. Fill in their real credentials")
        print("  3. Never commit ~/.panapi/config.yml to git")

    def create_gitignore(self):
        """Create comprehensive .gitignore"""
        gitignore_path = Path.cwd() / ".gitignore"
        
        gitignore_content = """# PAN-OS to SCM Migration Tool - Git Ignore

# Credentials and sensitive data (CRITICAL - NEVER COMMIT THESE)
config.yml
.panapi/
*.log
running_config.xml
cisco_config.txt
*.backup
*.original

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
*.egg
*.egg-info/
dist/
build/
*.spec

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Testing
.pytest_cache/
.coverage
htmlcov/

# Build artifacts
*.dmg
*.app/

# Temporary files
*.tmp
.~*
"""
        
        if gitignore_path.exists():
            print("⚠️  .gitignore already exists")
            response = input("Overwrite? (y/n): ")
            if response.lower() != 'y':
                print("Skipped .gitignore creation")
                return
        
        gitignore_path.write_text(gitignore_content)
        print(f"✓ Created .gitignore: {gitignore_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Safe sanitization - only touches documentation and examples"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )
    parser.add_argument(
        '--create-example',
        action='store_true',
        help='Create config.yml.example file'
    )
    parser.add_argument(
        '--create-gitignore',
        action='store_true',
        help='Create .gitignore file'
    )
    
    args = parser.parse_args()
    
    sanitizer = SafeSanitizer()
    
    if args.create_example:
        sanitizer.create_example_config()
    elif args.create_gitignore:
        sanitizer.create_gitignore()
    else:
        sanitizer.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()

# User Guide: PAN-OS to Strata Cloud Manager Migration Tool (GUI)

## Overview

The **PAN-OS to Strata Cloud Manager Migration Tool** is a graphical user interface (GUI) application that simplifies the process of migrating configurations from Palo Alto Networks firewalls or Panorama to Strata Cloud Manager (SCM). The tool provides an intuitive interface for configuration management, object selection, and real-time migration monitoring.

**Application File:** `complete_migration_gui.py`

---

## Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Quick Start Guide](#quick-start-guide)
- [Detailed User Guide](#detailed-user-guide)
  - [Configuration Tab](#configuration-tab)
  - [Select Objects Tab](#select-objects-tab)
  - [Migration Tab](#migration-tab)
- [Migration Workflow](#migration-workflow)
- [Understanding Object Types](#understanding-object-types)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [FAQ](#faq)

---

## Features

### Core Capabilities

- **Intuitive GUI** - No command-line experience required
- **Configuration Management** - Save and load credentials securely
- **Flexible Object Selection** - Choose specific objects or use quick presets
- **Live Migration Monitoring** - Real-time output and progress tracking
- **Detailed Results** - Formatted summary, error analysis, and full logs
- **SSL Support** - Built-in support for self-signed certificates
- **Export Capabilities** - Save logs and results to files

### Migration Options

- **Source Types**: Panorama shared config or device-groups, standalone firewalls
- **Destination Types**: SCM folders or snippets
- **Object Categories**: Network objects, applications, security profiles, policies
- **Policy Types**: Security rules, NAT rules, decryption rules, application override rules

---

## System Requirements

### Operating System
- **macOS** 10.14 (Mojave) or later
- **Linux** (Ubuntu 18.04+, CentOS 7+, or equivalent)
- **Windows** 10 or later (with Python 3.7+)

### Software Dependencies
- **Python** 3.7 or higher (3.9+ recommended)
- **Required Python Packages**:
  - customtkinter (GUI framework)
  - PyYAML (configuration management)
  - requests (API communication)
  - urllib3 (HTTP handling)

### Network Requirements
- Network access to PAN-OS/Panorama management interface
- Internet access for Strata Cloud Manager API
- HTTPS (443) outbound access

### Minimum Hardware
- **CPU**: Dual-core processor
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB free space
- **Display**: 1400x900 resolution or higher

---

## Installation

### Step 1: Install Python

**macOS:**
```bash
# Check if Python is installed
python3 --version

# Install via Homebrew if needed
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- Check "Add Python to PATH" during installation

### Step 2: Install Required Packages

```bash
# Navigate to the application directory
cd /path/to/migration-tool

# Install dependencies
pip3 install -r requirements.txt

# Or install manually:
pip3 install customtkinter PyYAML requests urllib3
```

### Step 3: Verify Installation

```bash
# Check that all packages are installed
pip3 list | grep -E "customtkinter|PyYAML|requests|urllib3"
```

### Step 4: Make the Script Executable (Optional)

```bash
chmod +x complete_migration_gui.py
```

---

## Quick Start Guide

### Launch the Application

```bash
# From the application directory
python3 complete_migration_gui.py

# Or if made executable:
./complete_migration_gui.py
```

### Basic Migration in 5 Steps

1. **Configure Credentials** (Configuration tab)
   - Enter SCM credentials (Client ID, Secret, TSG ID)
   - Enter PAN-OS/Panorama credentials (URL, Username, Password)
   - Click "Save Configuration"

2. **Test Connection** (Configuration tab)
   - Click "Test Connection" to verify Panorama access
   - Ensure you see "✓ Connection successful!"

3. **Select Objects** (Select Objects tab)
   - Choose individual objects or use Quick Presets
   - Click "Update Selection Count" to verify your choices

4. **Configure Migration** (Migration tab)
   - Set source type (shared or device-group)
   - Set destination (folder or snippet name)
   - Enable "Fetch new configuration" (recommended)

5. **Start Migration** (Migration tab)
   - Click "Start Migration"
   - Monitor progress in real-time
   - Review results when complete

---

## Detailed User Guide

## Configuration Tab

The Configuration tab manages your connection credentials for both SCM and PAN-OS/Panorama.

### Strata Cloud Manager Credentials

**Client ID**
- Your SCM service account Client ID
- Format: UUID-style string (e.g., `12345678-abcd-1234-efgh-123456789abc`)
- Obtained from SCM → Settings → Service Accounts

**Client Secret**
- Your SCM service account Client Secret
- Displayed only once during service account creation
- Store securely; cannot be retrieved later

**TSG ID**
- Tenant Service Group ID
- Obtained from SCM → Settings → TSG Information
- Format: Numeric ID (e.g., `1234567890`)

### PAN-OS/Panorama Credentials

**Panorama URL**
- Full URL to your Panorama or firewall management interface
- Format: `https://panorama.example.com` or `https://10.0.1.1`
- Must include `https://`
- Do not include trailing slash

**Username**
- Administrative username with API access
- Must have sufficient permissions to read configuration
- Recommended: Create dedicated API user

**Password**
- Password for the administrative account
- Stored securely in `~/.panapi/config.yml`
- File permissions automatically set to 600 (owner read/write only)

### Configuration Actions

**Save Configuration**
- Saves credentials to `~/.panapi/config.yml`
- Creates directory structure if needed
- Sets secure file permissions automatically
- Credentials persist between sessions

**Test Connection**
- Validates connection to Panorama
- Generates API key using provided credentials
- Shows success/failure message
- Recommended before starting migration

**Load Configuration**
- Loads previously saved credentials
- Useful after application restart
- Automatically loads on startup if config exists

---

## Select Objects Tab

Choose which configuration objects to migrate from PAN-OS to SCM.

### Object Categories

The tool organizes objects into logical categories:

#### 1. Network Objects
- **Tag** - Object tags/labels
- **Address** - Address objects (IPs, FQDNs, IP ranges)
- **AddressGroup** - Groups of address objects
- **Service** - Service/port definitions
- **ServiceGroup** - Groups of services

#### 2. Application Objects
- **Application** - Custom application definitions
- **ApplicationFilter** - Application filters
- **ApplicationGroup** - Groups of applications

#### 3. Security Profiles
- **URLFilterProfile** - URL filtering profiles
- **VulnerabilityProfile** - IPS/vulnerability protection
- **AntiSpywareProfile** - Anti-spyware profiles
- **DNSSecurityProfile** - DNS security profiles
- **FileBlockingProfile** - File blocking profiles
- **DecryptionProfile** - SSL/TLS decryption profiles
- **ProfileGroup** - Security profile groups

#### 4. Other Objects
- **ExternalDynamicList** - External dynamic lists (EDLs)
- **CustomURLCategory** - Custom URL categories
- **HIPObject** - Host Information Profile objects
- **HIPProfile** - HIP profiles

#### 5. Security Policies
- **SecurityRules** - Security policy rules
- **NATRules** - NAT policy rules
- **AppOverrideRules** - Application override rules
- **DecryptionRules** - SSL/TLS decryption rules

### Selection Methods

#### Manual Selection
1. Click individual checkboxes for each object type
2. Click "Update Selection Count" to see total selected

#### Quick Presets
Pre-configured selections for common use cases:

- **Basic Network** - Tags, addresses, address groups, services, service groups
- **Security Profiles** - URL filtering, vulnerability, anti-spyware, profile groups
- **Security Rules** - Security policy rules only
- **All Policies** - All policy rule types

#### Category Controls
Each category has quick buttons:
- **Select All** - Select all objects in that category
- **Clear** - Deselect all objects in that category

#### Global Controls
- **Select All** - Select every object type
- **Clear All** - Deselect every object type

### Selection Tips

**Start Small**
- For first migration, start with basic network objects
- Test with non-critical objects before migrating policies

**Dependencies Matter**
- Address objects should be migrated before address groups
- Services should be migrated before service groups
- Objects should be migrated before policies that reference them

**Recommended Order**
1. Tags
2. Address objects and services
3. Address groups and service groups
4. Applications and application groups
5. Security profiles
6. Security policies

---

## Migration Tab

Configure and execute the migration, monitor progress, and view results.

### Migration Configuration

#### Source Configuration

**Configuration Source**
- **shared** - Migrate from Panorama shared configuration or standalone firewall
- **device-group** - Migrate from a specific Panorama device group

**Device Group Name** (required if device-group selected)
- Exact name of the device group in Panorama
- Case-sensitive
- Must exist in Panorama

#### Destination Configuration

**SCM Destination Type**
- **folder** - Migrate to an SCM folder (recommended for most use cases)
- **snippet** - Migrate to an SCM snippet (for reusable configurations)

**Destination Name** (required)
- Name of the destination folder or snippet in SCM
- Will be created if it doesn't exist
- Examples: `Production`, `Branch-Offices`, `Security-Baseline`

#### Migration Options

**Fetch new configuration from Panorama**
- ✅ **Enabled (recommended)**: Downloads fresh configuration from Panorama before migration
- ❌ **Disabled**: Uses previously cached configuration (if available)

**Accept untrusted certificate**
- ✅ **Enabled**: Accepts self-signed SSL certificates (common in lab environments)
- ❌ **Disabled**: Requires valid SSL certificate (recommended for production)

### Migration Execution

#### Starting Migration

1. **Review Configuration**
   - Verify source and destination settings
   - Check selected objects count
   - Ensure credentials are configured

2. **Click "Start Migration"**
   - Confirmation dialog shows full migration summary
   - Review carefully before confirming

3. **Monitor Progress**
   - Watch live output in real-time
   - Progress bar shows migration status
   - Status label updates as migration proceeds

#### During Migration

**Live Output Window**
- Real-time display of migration activities
- Shows API calls, object creation, errors
- Auto-scrolls to latest output

**Control Buttons**
- **Stop Migration** - Cancels running migration
- **Clear Output** - Clears output window
- **Save Log** - Saves current output to file

#### Migration Results

When migration completes, a detailed results window displays:

**Summary Tab**
- Success count (objects created)
- Already existed count (objects skipped)
- Error count (failed objects)
- Quick overview statistics

**Errors Tab**
- Detailed breakdown of each error
- Object names and error messages
- Specific validation issues
- Formatted for easy reading

**Full Output Tab**
- Complete migration log
- All API interactions
- Detailed object processing information

### Results Window Actions

**Copy to Clipboard**
- Copies current tab content to clipboard
- Paste into documentation or tickets

**Export to File**
- Saves all tabs to a text file
- Includes timestamp in filename
- Useful for record-keeping and audits

**Close**
- Closes results window
- Returns to main application

---

## Migration Workflow

### Pre-Migration Checklist

- [ ] SCM service account created and credentials obtained
- [ ] PAN-OS/Panorama accessible and credentials validated
- [ ] Network connectivity verified (can reach both systems)
- [ ] Destination folder/snippet planned (naming convention decided)
- [ ] Objects to migrate identified and prioritized
- [ ] Dependencies understood (e.g., objects before groups before policies)

### Migration Steps

#### Phase 1: Preparation
1. Launch the GUI application: `python3 complete_migration_gui.py`
2. Configure credentials in Configuration tab
3. Test connection to Panorama
4. Save configuration for future use

#### Phase 2: Planning
1. Navigate to Select Objects tab
2. Review available object types
3. Choose objects based on migration scope
4. Consider using presets for common scenarios
5. Update selection count to verify

#### Phase 3: Configuration
1. Navigate to Migration tab
2. Set source type (shared or device-group)
3. Enter device group name if applicable
4. Choose destination type (folder or snippet)
5. Enter destination name in SCM
6. Enable "Fetch new configuration" (recommended)
7. Enable "Accept untrusted certificate" if needed

#### Phase 4: Execution
1. Click "Start Migration"
2. Review confirmation dialog carefully
3. Confirm to begin migration
4. Monitor live output for issues
5. Wait for completion

#### Phase 5: Validation
1. Review results window
2. Check Summary tab for statistics
3. Investigate any errors in Errors tab
4. Export results for documentation
5. Verify objects in SCM web interface

#### Phase 6: Post-Migration
1. Save migration log
2. Document any errors or issues
3. Plan remediation for failed objects
4. Schedule next migration phase if needed

---

## Understanding Object Types

### Network Objects

**Address Objects**
- IP addresses (e.g., `192.168.1.10`)
- IP ranges (e.g., `10.0.0.1-10.0.0.254`)
- IP subnets (e.g., `172.16.0.0/16`)
- FQDNs (e.g., `www.example.com`)

**Address Groups**
- Static groups (predefined list of addresses)
- Dynamic groups (based on tags/attributes)
- Used to simplify security policies

**Service Objects**
- TCP/UDP port definitions
- Protocol specifications
- Used in security rules to control traffic by port

**Tags**
- Labels for organizing objects
- Used in dynamic groups
- Color-coded for visual identification

### Security Profiles

**URL Filtering**
- Block/allow access to websites by category
- Custom URL categories
- Credential submission policies

**Vulnerability Protection**
- IPS signatures
- Exploit protection
- Protocol decoder vulnerabilities

**Anti-Spyware**
- Spyware signatures
- DNS sinkhole configuration
- Botnet protection

**Profile Groups**
- Bundles of security profiles
- Simplifies policy application
- Ensures consistent protection

### Security Policies

**Security Rules**
- Control traffic between zones
- Specify allowed/denied applications
- Apply security profiles
- Most common rule type

**NAT Rules**
- Source NAT (hide internal IPs)
- Destination NAT (port forwarding)
- Static NAT (1:1 translations)

**Decryption Rules**
- SSL/TLS inspection policies
- Certificate requirements
- Exclude rules for sensitive traffic

---

## Troubleshooting

### Connection Issues

#### Problem: "Connection refused" or timeout errors

**Possible Causes:**
- Panorama is unreachable
- Incorrect URL format
- Firewall blocking connection
- Management interface not accessible

**Solutions:**
1. Verify Panorama URL is correct and includes `https://`
2. Test network connectivity: `ping <panorama-ip>`
3. Ensure Panorama management interface is enabled
4. Check firewall rules allow outbound HTTPS (port 443)
5. Verify DNS resolution if using hostname

#### Problem: "Authentication failed" errors

**Possible Causes:**
- Incorrect username or password
- Account lacks API permissions
- Account is locked or disabled

**Solutions:**
1. Verify credentials in Panorama web interface
2. Check user has "XML API" permission
3. Try logging into Panorama web UI with same credentials
4. Check if account requires password reset
5. Ensure no special characters are causing parsing issues

### SSL Certificate Issues

#### Problem: SSL certificate verification errors

**Solutions:**
1. Enable "Accept untrusted certificate" checkbox in Migration tab
2. Application has built-in SSL bypass for self-signed certificates
3. For production, install proper certificates on Panorama

### Migration Errors

#### Problem: "Object already exists" errors

**Explanation:**
- Object with same name already exists in SCM destination
- Not necessarily an error; indicates object was already migrated

**Solutions:**
- Review existing objects in SCM
- Decide whether to skip (safe) or manually rename conflicting objects
- These are typically counted as "already existed" not "errors"

#### Problem: API validation errors

**Common Causes:**
- Object name contains invalid characters
- Required fields missing in object definition
- Dependency objects not yet migrated
- Object configuration not supported in SCM

**Solutions:**
1. Check Errors tab for specific validation messages
2. Review object configuration in PAN-OS
3. Migrate dependency objects first (e.g., addresses before groups)
4. Consult SCM API documentation for supported configurations
5. Manually create problematic objects in SCM if needed

#### Problem: "TSG ID not found" errors

**Solutions:**
1. Verify TSG ID is numeric and correct
2. Check service account has access to the TSG
3. Verify service account is not expired or disabled
4. Try retrieving TSG list from SCM API to confirm access

### Application Issues

#### Problem: GUI window is too small or elements are cut off

**Solutions:**
```bash
# The application requires minimum 1400x900 resolution
# Check your display settings:

# macOS:
# System Preferences → Displays → Resolution

# Linux:
xrandr

# Resize the window manually by dragging corners
```

#### Problem: "ModuleNotFoundError: No module named 'customtkinter'"

**Solution:**
```bash
# Reinstall dependencies
pip3 install customtkinter

# Or install all requirements
pip3 install -r requirements.txt

# Verify installation
python3 -c "import customtkinter; print('OK')"
```

#### Problem: Application crashes immediately on launch

**Solutions:**
1. Check Python version: `python3 --version` (must be 3.7+)
2. Verify all dependencies installed: `pip3 list`
3. Check for error messages in terminal
4. Try running with verbose output: `python3 -v complete_migration_gui.py`
5. Check display settings (GUI requires graphical environment)

### Configuration Issues

#### Problem: "Configuration file not found" warning

**Explanation:**
- Normal on first run
- Configuration file doesn't exist yet

**Solution:**
- Enter credentials and click "Save Configuration"
- File will be created at `~/.panapi/config.yml`

#### Problem: Cannot save configuration

**Solutions:**
1. Check write permissions: `ls -la ~/.panapi/`
2. Manually create directory: `mkdir -p ~/.panapi`
3. Check disk space: `df -h ~`
4. Ensure no file is locking the config file

---

## Best Practices

### Security

**Credential Management**
- Use dedicated service accounts with minimal required permissions
- Rotate credentials regularly
- Store configuration file securely (automatic 600 permissions)
- Never share credentials in logs or screenshots

**SSL/TLS**
- Use proper certificates in production environments
- Only use "Accept untrusted certificate" in lab/dev environments
- Monitor for man-in-the-middle attacks in sensitive environments

### Migration Planning

**Test First**
- Start with non-production environments
- Test with small object sets before full migration
- Validate migrated objects before relying on them

**Incremental Approach**
- Migrate objects in phases (network objects → profiles → policies)
- Validate each phase before proceeding
- Keep detailed notes of what was migrated when

**Documentation**
- Export and save all migration logs
- Document any errors and resolutions
- Maintain inventory of migrated objects
- Track migration progress in project management tool

### Performance

**Large Migrations**
- For 1000+ objects, consider breaking into batches
- Monitor network bandwidth during migration
- Schedule migrations during maintenance windows
- Consider API rate limits

**Optimization**
- Fetch configuration once and reuse for multiple migrations
- Disable unnecessary object types to speed up selection
- Clear output window periodically during long migrations

### Error Handling

**When Errors Occur**
- Don't panic - most errors are validation issues
- Review Errors tab carefully for specific messages
- Check if objects already exist (not really an error)
- Document errors for trend analysis
- Re-migrate failed objects individually after fixing issues

**Common Non-Critical Errors**
- "Already existed" - Object already in SCM, safe to ignore
- "Invalid character in name" - Rename object in PAN-OS
- "Missing dependency" - Migrate referenced objects first

---

## FAQ

### General Questions

**Q: Do I need command-line experience to use this tool?**

A: No! The GUI is designed for users who prefer graphical interfaces. All functionality is accessible through menus, buttons, and forms.

**Q: What is the correct file to run?**

A: Run `python3 complete_migration_gui.py` from the application directory.

**Q: Can I migrate from multiple Panorama device groups?**

A: Yes, but you need to run separate migrations for each device group. Configure source as "device-group" and specify each group name in turn.

**Q: What happens if migration is interrupted?**

A: SCM API is transactional. Objects already created will remain, but incomplete objects won't be saved. You can safely re-run the migration; existing objects will be skipped.

**Q: How long does a migration take?**

A: Depends on object count and network speed. Typical rates:
- Small (< 100 objects): 2-5 minutes
- Medium (100-500 objects): 5-15 minutes
- Large (500-2000 objects): 15-45 minutes
- Very large (2000+ objects): 1+ hours

**Q: Can I run multiple migrations simultaneously?**

A: Not recommended. Run migrations sequentially to avoid conflicts and make troubleshooting easier.

### Technical Questions

**Q: Where is my configuration stored?**

A: `~/.panapi/config.yml` with 600 permissions (owner read/write only)

**Q: Where are migration logs saved?**

A: `~/.panapi/logs/migration_YYYYMMDD_HHMMSS.log` when using "Save Log" button

**Q: Does this tool modify my PAN-OS configuration?**

A: No. The tool only reads from PAN-OS/Panorama. All writes go to SCM. Your source configuration is never modified.

**Q: What if an object fails to migrate?**

A: The migration continues with remaining objects. Failed objects are listed in the Errors tab. You can manually fix the issue and re-migrate just those objects.

**Q: Can I undo a migration?**

A: No automatic undo. You must manually delete objects from SCM if needed. Always test in non-production first.

**Q: Does this support Panorama templates?**

A: No. This tool migrates policy objects and security policies. Network and device settings from templates are not migrated.

### Migration-Specific Questions

**Q: Should I migrate "shared" or "device-group" configuration?**

A: Depends on your deployment:
- **Shared**: Common objects used across all device groups
- **Device-group**: Specific to certain managed devices
- Typically migrate shared first, then device groups

**Q: What's the difference between "folder" and "snippet" in SCM?**

A: 
- **Folder**: Full configuration container, like a device group
- **Snippet**: Reusable configuration block that can be referenced by folders
- Use folder for most migrations

**Q: Can I migrate policies without migrating objects first?**

A: Not recommended. Policies reference objects (addresses, services, profiles). Migrate objects first to avoid broken references.

**Q: What if I have custom applications or URL categories?**

A: Custom objects are supported. The tool migrates:
- Custom applications
- Custom URL categories
- Custom security profiles
- All custom objects you select

**Q: How do I verify the migration was successful?**

A:
1. Review the Summary tab for success count
2. Check Errors tab for any failures
3. Log into SCM web interface
4. Navigate to your destination folder/snippet
5. Verify objects appear correctly
6. Check object counts match expected values

---

## Advanced Features

### Configuration File Format

The configuration is stored in YAML format at `~/.panapi/config.yml`:

```yaml
client_id: "your-scm-client-id"
client_secret: "your-scm-client-secret"
tsg_id: "your-tsg-id"
palo_alto_ngfw_url: "https://panorama.example.com"
palo_alto_username: "admin"
palo_alto_password: "your-password"
```

You can manually edit this file if needed (ensure permissions remain 600).

### Log File Locations

Logs are automatically saved with timestamps:
- **Configuration file**: `~/.panapi/config.yml`
- **Migration logs**: `~/.panapi/logs/migration_YYYYMMDD_HHMMSS.log`

### Command-Line Options

While the GUI is the primary interface, you can customize launch behavior:

```bash
# Standard launch
python3 complete_migration_gui.py

# Launch with specific Python version
python3.9 complete_migration_gui.py

# Run with verbose debugging (if needed for troubleshooting)
python3 -v complete_migration_gui.py
```

---

## Getting Help

### Self-Help Resources

1. **This User Guide** - Comprehensive documentation
2. **Troubleshooting Section** - Common issues and solutions
3. **FAQ** - Frequently asked questions
4. **Migration Logs** - Review output for specific errors

### Support Channels

1. **Error Messages** - Read carefully; they often indicate the exact issue
2. **Results Window** - Errors tab provides detailed breakdown
3. **Export Logs** - Save and share logs with support team
4. **SCM Documentation** - For API and object configuration details
5. **PAN-OS Documentation** - For source configuration questions

### Reporting Issues

When reporting issues, include:
1. Application version and file name (`complete_migration_gui.py`)
2. Python version (`python3 --version`)
3. Operating system and version
4. Exported migration log
5. Screenshots of error messages
6. Steps to reproduce the issue
7. Number and types of objects being migrated

---

## Appendix

### Keyboard Shortcuts

- **Cmd/Ctrl + Tab** - Switch between tabs (some systems)
- **Cmd/Ctrl + C** - Copy selected text
- **Cmd/Ctrl + V** - Paste text
- **Cmd/Ctrl + A** - Select all text in output window

### File Permissions

The application automatically sets secure permissions:
- Configuration file: `600` (owner read/write only)
- Log files: `644` (owner read/write, others read)

### Supported Object Types Summary

| Category | Object Type | PAN-OS Name | SCM Support |
|----------|------------|-------------|-------------|
| Network | Address | address | ✓ |
| Network | AddressGroup | address-group | ✓ |
| Network | Service | service | ✓ |
| Network | ServiceGroup | service-group | ✓ |
| Network | Tag | tag | ✓ |
| Application | Application | application | ✓ |
| Application | ApplicationGroup | application-group | ✓ |
| Application | ApplicationFilter | application-filter | ✓ |
| Security | URLFilterProfile | profiles/url-filtering | ✓ |
| Security | VulnerabilityProfile | profiles/vulnerability | ✓ |
| Security | AntiSpywareProfile | profiles/spyware | ✓ |
| Security | DNSSecurityProfile | profiles/dns-security | ✓ |
| Security | FileBlockingProfile | profiles/file-blocking | ✓ |
| Security | DecryptionProfile | profiles/decryption | ✓ |
| Security | ProfileGroup | profile-group | ✓ |
| Policy | SecurityRules | security/rules | ✓ |
| Policy | NATRules | nat/rules | ✓ |
| Policy | DecryptionRules | decryption/rules | ✓ |
| Policy | AppOverrideRules | app-override/rules | ✓ |

---

## Summary

The PAN-OS to Strata Cloud Manager Migration Tool provides a user-friendly graphical interface for migrating firewall configurations. Key points to remember:

✅ **Run with**: `python3 complete_migration_gui.py`

✅ **Three main tabs**: Configuration → Select Objects → Migration

✅ **Built-in SSL support**: Works with self-signed certificates

✅ **Real-time monitoring**: Watch migration progress live

✅ **Detailed results**: Summary, errors, and full output

✅ **Safe operation**: Only reads from PAN-OS, writes to SCM

✅ **Best practice**: Test in non-production first

---

**Ready to begin your migration? Start with the [Quick Start Guide](#quick-start-guide)!**

*Last Updated: October 2025*

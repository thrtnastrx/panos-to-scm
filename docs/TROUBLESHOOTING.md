# Troubleshooting Guide: PAN-OS to SCM Migration

## App Won't Open (Icon Bounces and Stops)

If the app icon bounces in the dock a few times but won't open, this is typically caused by macOS Gatekeeper blocking the app.

### Error Message
```
Apple could not verify "PAN-OS to SCM Migration" is free of malware 
that may harm your Mac or compromise your privacy.
```

## Solutions

### Option 1: Override Gatekeeper (Recommended)
1. Right-click (or Control-click) the app icon
2. Select "Open" from the context menu
3. Click "Open" in the warning dialog that appears
4. If needed, repeat - the first attempt shows the warning, the second provides an "Open" button

### Option 2: Remove Quarantine Flag (Most Reliable)
Open Terminal and run:
```bash
xattr -cr /path/to/PAN-OS\ to\ SCM\ Migration.app
```

Replace `/path/to/` with the actual location of your app. This removes the quarantine attribute that triggers Gatekeeper.

### Option 3: System Settings
1. Open System Settings → Privacy & Security
2. Scroll down to the Security section
3. Look for a message about the blocked app
4. Click "Open Anyway"

## Why This Happens

- The app is not notarized by Apple (common for internal/enterprise tools)
- macOS Gatekeeper security may block the app after system restarts or updates
- The quarantine flag can be reapplied by macOS security checks

## Additional Troubleshooting

### Check Console Logs
If the app still won't open after trying the above:
1. Open Console.app (Applications/Utilities)
2. Try launching the app
3. Look for crash reports or error messages related to "PAN-OS to SCM Migration"

### Launch from Terminal
See detailed error output by running:
```bash
/path/to/PAN-OS\ to\ SCM\ Migration.app/Contents/MacOS/PAN-OS\ to\ SCM\ Migration
```

### Clear App Preferences/Cache
If issues persist, try removing:
- `~/Library/Preferences/[app-identifier].plist`
- `~/Library/Caches/[app-bundle-id]`

### Verify Code Signature
Check if the app's signature is valid:
```bash
codesign --verify --deep --strict /path/to/PAN-OS\ to\ SCM\ Migration.app
```

## Security Note

These solutions allow you to run apps that aren't notarized by Apple. Only use these methods for apps from trusted sources that you control or know are safe.

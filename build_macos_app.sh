#!/bin/bash
# Build PAN-OS to SCM Migration Tool as macOS .app
# Run this script from your project directory

set -e  # Exit on error

echo "=========================================="
echo "Building PAN-OS to SCM Migration Tool"
echo "=========================================="
echo ""

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Not in a virtual environment"
    echo "   Activating venv..."
    source venv/bin/activate
fi

# Install PyInstaller if not already installed
echo "1. Checking PyInstaller..."
pip install pyinstaller pillow > /dev/null 2>&1
echo "   ✓ PyInstaller ready"

# Prepare app icon
echo ""
echo "2. Preparing app icon..."

# Check for pan-logo-1.png
if [ -f "pan-logo-1.png" ]; then
    echo "   ✓ Found pan-logo-1.png"
    
    # Convert PNG to ICNS for macOS
    echo "   Converting to .icns format..."
    
    # Create iconset directory
    mkdir -p app_icon.iconset
    
    # Generate multiple sizes from the source image
    sips -z 16 16     pan-logo-1.png --out app_icon.iconset/icon_16x16.png > /dev/null 2>&1
    sips -z 32 32     pan-logo-1.png --out app_icon.iconset/icon_16x16@2x.png > /dev/null 2>&1
    sips -z 32 32     pan-logo-1.png --out app_icon.iconset/icon_32x32.png > /dev/null 2>&1
    sips -z 64 64     pan-logo-1.png --out app_icon.iconset/icon_32x32@2x.png > /dev/null 2>&1
    sips -z 128 128   pan-logo-1.png --out app_icon.iconset/icon_128x128.png > /dev/null 2>&1
    sips -z 256 256   pan-logo-1.png --out app_icon.iconset/icon_128x128@2x.png > /dev/null 2>&1
    sips -z 256 256   pan-logo-1.png --out app_icon.iconset/icon_256x256.png > /dev/null 2>&1
    sips -z 512 512   pan-logo-1.png --out app_icon.iconset/icon_256x256@2x.png > /dev/null 2>&1
    sips -z 512 512   pan-logo-1.png --out app_icon.iconset/icon_512x512.png > /dev/null 2>&1
    sips -z 1024 1024 pan-logo-1.png --out app_icon.iconset/icon_512x512@2x.png > /dev/null 2>&1
    
    # Convert to icns
    iconutil -c icns app_icon.iconset -o app_icon.icns
    rm -rf app_icon.iconset
    
    echo "   ✓ Created app_icon.icns from pan-logo-1.png"
    ICON_OPTION="--icon=app_icon.icns"
else
    echo "   ⚠️  pan-logo-1.png not found, using default icon"
    ICON_OPTION=""
fi

# Clean previous builds
echo "   Cleaning old builds..."
rm -rf build dist *.spec

echo "   ✓ Resources ready"

# Build the application
echo ""
echo "3. Building application..."
echo "   This may take a few minutes..."

pyinstaller \
    --name="PAN-OS to SCM Migration" \
    --windowed \
    --onefile \
    --noconfirm \
    --clean \
    $ICON_OPTION \
    --add-data="auto_migrate.py:." \
    --add-data="fix_ssl_comprehensive.py:." \
    --hidden-import=customtkinter \
    --hidden-import=pexpect \
    --hidden-import=yaml \
    --hidden-import=urllib3 \
    --hidden-import=ssl \
    --collect-all=customtkinter \
    complete_migration_gui.py

echo "   ✓ Build complete!"

# Check if build was successful
if [ -d "dist/PAN-OS to SCM Migration.app" ]; then
    echo ""
    echo "=========================================="
    echo "✅ SUCCESS!"
    echo "=========================================="
    echo ""
    echo "Your application is ready at:"
    echo "  📦 dist/PAN-OS to SCM Migration.app"
    echo ""
    echo "To install:"
    echo "  1. Open Finder"
    echo "  2. Navigate to the 'dist' folder"
    echo "  3. Drag 'PAN-OS to SCM Migration.app' to Applications"
    echo ""
    echo "Note: On first launch, you may need to:"
    echo "  - Right-click → Open (to bypass Gatekeeper)"
    echo "  - Allow in System Preferences → Security & Privacy"
    echo ""
    
    # Get app size
    APP_SIZE=$(du -sh "dist/PAN-OS to SCM Migration.app" | cut -f1)
    echo "Application size: $APP_SIZE"
    echo ""
else
    echo ""
    echo "❌ Build failed! Check the output above for errors."
    exit 1
fi

# Optional: Create DMG
read -p "Create installer DMG? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "4. Creating DMG installer..."
    
    # Install create-dmg if needed
    if ! command -v create-dmg &> /dev/null; then
        echo "   Installing create-dmg..."
        brew install create-dmg
    fi
    
    DMG_NAME="PAN-OS-to-SCM-Migration-Installer.dmg"
    
    create-dmg \
        --volname "PAN-OS to SCM Migration" \
        --window-pos 200 120 \
        --window-size 600 400 \
        --icon-size 100 \
        --app-drop-link 425 120 \
        "$DMG_NAME" \
        "dist/PAN-OS to SCM Migration.app"
    
    echo "   ✓ DMG created: $DMG_NAME"
    echo ""
    echo "You can now distribute: $DMG_NAME"
fi

echo ""
echo "=========================================="
echo "Build complete!"
echo "=========================================="

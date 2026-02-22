#!/bin/bash
# Test character creation script

echo "Creating test character"
mkdir -p "/mnt/z/Turdbot/Turd History/characters/minor-characters/associates/test-character"
echo "Test character directory created at /mnt/z/Turdbot/Turd History/characters/minor-characters/associates/test-character"

# Create a simple file
cat > "/mnt/z/Turdbot/Turd History/characters/minor-characters/associates/test-character/test-file.md" << EOF
# Test Character File
This is a test file to verify directory creation.
EOF

echo "Test file created"
ls -la "/mnt/z/Turdbot/Turd History/characters/minor-characters/associates/test-character"
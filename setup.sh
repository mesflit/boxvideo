#!/bin/bash

# Define MESFLITDIR variable
MESFLITDIR="$HOME/.local/share/mesflit"

# Create mesflit directory if it doesn't exist
if [ ! -d "$MESFLITDIR" ]; then
    mkdir -p "$MESFLITDIR"
    echo "Mesflit directory created successfully."
else
    echo "Mesflit directory already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r installer.txt

# Build the application using PyInstaller
echo "Building the application..."
pyinstaller --onefile boxvideo.py

# Add mesflit directory to PATH if not already added
if ! echo "$PATH" | grep -q "$MESFLITDIR"; then
    if [[ "$SHELL" == "/bin/bash" || "$SHELL" == "/usr/bin/bash" ]]; then
        echo 'export PATH="$PATH:'"$MESFLITDIR"'"' >> ~/.bashrc
        source ~/.bashrc
    elif [[ "$SHELL" == "/bin/zsh" || "$SHELL" == "/usr/bin/zsh" ]]; then
        echo 'export PATH="$PATH:'"$MESFLITDIR"'"' >> ~/.zshrc
        source ~/.zshrc
    elif [[ "$SHELL" == "/usr/bin/fish" || "$SHELL" == "/bin/fish" ]]; then
        echo 'set PATH $PATH '"$MESFLITDIR" >> ~/.config/fish/config.fish
        source ~/.config/fish/config.fish
    else
        echo "Unsupported shell: $SHELL"
    fi
fi


mv dist/boxvideo "$MESFLITDIR/boxvideo"

# Set permissions for the executable
chmod +x "$MESFLITDIR/boxvideo"

# Clean up empty directories
rm -rf build/ dist/ __pycache__/ *.spec venv

echo "Boxvideo application has been installed successfully!"

# Function to check if a substring exists in a string
contains() {
    [[ $1 =~ (^|:)$2(:|$) ]] && return 0 || return 1
}

# Installation Guide - Project "Litter"

Follow these steps to set up the project on your Windows machine, even if you don't have Python installed yet.

## Step 1: Install Python
If you don't have Python installed:
1. Go to [python.org](https://www.python.org/downloads/windows/).
2. Download the latest **Windows Installer (64-bit)**.
3. **CRITICAL**: During installation, check the box that says **"Add Python to PATH"**.
4. Complete the installation and restart your computer.

## Step 2: Download the Project
Ensure all files are in a folder named `litter`.

## Step 3: Run the Setup Script
Double-click `setup.bat`. This will:
- Check for Python.
- Create a virtual environment (`venv`).
- Install all necessary libraries: `ultralytics`, `roboflow`, `yt-dlp`, etc.

## Step 4: Configure (Optional)
Open `config.py` to update your Roboflow API Key or project settings if needed.

## Step 5: Start Detection
Double-click `start.bat`.

### Troubleshooting
- **Script Blocked**: If Windows SmartScreen blocks the `.bat` files, click "More info" and "Run anyway".
- **Path Error**: Ensure you checked "Add Python to PATH" in Step 1.

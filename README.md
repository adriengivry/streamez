# Streamez
Streamez is a lightweight system tray application designed to simplify your livestreaming and meeting lighting setups. With Streamez, you can effortlessly control your Philips Hue and Elgato lights and open or close OBS Studio with a single click.

# Features
Includes 3 services:
  - **Elgato**:
    - Define lights to toggle ON/OFF
  - **Philips Hue**:
    - Define lights to toggle ON/OFF
    - Define lights colors
  - **OBS Studio**:
    - Start & Stop OBS Studio with custom arguments

Easy to expand to include your own services!

# Roadmap
- Implement a proper configuration system that wouldn't require to edit Python files directly
- Add a profile system to switch between different configurations (example: meeting mode, streaming mode)

# Installation
```bash
git clone https://github.com/adriengivry/streamez
cd streamez/
python -m pip install .
```

# Configuration
Open `streamez/settings.py` and edit it to adapt *streamez* to your setup!

You might want to:
- Define the IP address of your own Philips Hue bridge
- Define the name and desired settings for your Philips Hue lights
- Define the IP address of your Elgato lights
- Define the IP address and desired settings for your Elgato lights
- Adjust OBS Studio path and command line arguments to meet your requirements

# Creating a Shortcut (Windows)
To create a shortcut for streamez that can be accessed by typing "streamez" in the Windows search menu, follow these steps:

1. Open Windows PowerShell as an Administrator.
2. Navigate to the streamez repository (`cd path/to/streamez/`)
3. Copy and execute the following code:
```powershell
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Streamez.lnk")
$Shortcut.TargetPath = "pythonw.exe"
$Shortcut.Arguments = "-m streamez"
$Shortcut.IconLocation = Join-Path -Path $pwd.Path -ChildPath "icon.ico"
$Shortcut.Save()
```

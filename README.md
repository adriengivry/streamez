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
- Add a profile system to switch between different configurations (example: meeting mode, streaming mode)

# Installation
```bash
git clone https://github.com/adriengivry/streamez
cd streamez/
python -m pip install .
```

# Running
```bash
python -m streamez
```

# Configuration
1. Start the application
2. Locate Streamez's REC icon (red circle) in your system tray
3. Right-click on the icon
4. Select "Open Settings"
5. Add your settings based on your use case

**Note: If no setting override is provided for a particular entry (example: "hue_bridge_address"), the default settings will be used!**

**Example settings:** *Turn on 2 Elgato lights and update the settings of 2 Philips Hue lights, and start OBS Studio minimized with the virtual camera option:*
```json
{
    "elgato_lights": [
        {"address": "192.168.2.38", "state": true},
        {"address": "192.168.2.21", "state": true}
    ],
    "hue_lights": [
        {"name": "Office Floor", "on": true, "brightness": 254, "hue": 38146, "saturation": 7},
        {"name": "Hue go", "on": true, "brightness": 254, "hue": 38146, "saturation": 7}
    ],
    "hue_bridge_address": "192.168.2.14",
    "obs_args": [
        "--startvirtualcam", "--scene", "Default", "--minimize-to-tray", "--disable-shutdown-check", "--disable-updater"
    ]
}
```

**Default settings:**
```json
{
  "auto_reload_settings_on_initialization": true,
  "auto_initialize_on_service_start": true,
  "show_message_box_on_error": true,
  "obs_folder": "C:\\Program Files\\obs-studio\\bin\\64bit",
  "obs_executable_name": "obs64.exe",
  "obs_args": [],
  "elgato_lights": [],
  "hue_bridge_address": null,
  "hue_lights": []
}
```


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

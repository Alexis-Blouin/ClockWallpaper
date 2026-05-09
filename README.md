# WallpaperSwitch
A Python utility that displays the current time directly on your desktop wallpaper and updates it automatically through Windows Task Scheduler.

## Features
- Displays the current time on the wallpaper
- Automatic scheduled updates
- Simple PowerShell setup scripts
- Easy install and removal

## Requirements
Before running the project, install the Python dependencies:
```PowerShell
pip install -r requirements.txt
```
You will also need:
- Windows
- Python 3 installed and added to PATH
- Administrator privileges (required for task creation/removal)

## Setup
1. Clone the repository
```PowerShell
git clone https://github.com/Alexis-Blouin/ClockWallpaper
cd WallpaperSwitch
```
2. Install dependencies
```PowerShell
pip install -r requirements.txt
```
3. Create the scheduled tasks
Run PowerShell as Administrator, then execute:
```PowerShell
.\power_shell\create_tasks.ps1
```
This script creates the Windows scheduled tasks required for the wallpaper updates.

## Removing the Scheduled Tasks
To remove the scheduled tasks, run PowerShell as Administrator and execute:
```PowerShell
.\power_shell\remove_tasks.ps1
```
## Manual Alternative
You can also manually configure Windows Task Scheduler by following this guide: <br />
[AskPython Task Scheduler Tutorial](https://www.askpython.com/python/examples/execute-python-windows-task-scheduler)

## Notes
- The PowerShell scripts must be executed with administrator privileges
- If PowerShell blocks script execution, you may need to allow local scripts temporarily:
```PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
- Depending on your Python installation, you may need to use:
```PowerShell
python -m pip install -r requirements.txt
```
instead of `pip install`

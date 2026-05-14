# Hello World Calculator

A themed, interactive desktop calculator built with Python and Tkinter.

## Features
- Beautiful light and dark themes
- Arithmetic, scientific functions, and constants (`pi`, `e`)
- Memory controls (`MC`, `MR`, `M+`, `M-`)
- Live expression preview
- Calculation history with quick reuse
- Keyboard shortcuts

## Run From Source
```powershell
py -3 Calculator.py
```

## Build Windows Executable (.exe)
```powershell
./build.ps1
```

Single-file exe build (larger startup extraction, easier sharing):
```powershell
./build.ps1 -OneFile
```

After build, run:
- `dist/HelloWorldCalculator/HelloWorldCalculator.exe`

For one-file build, run:
- `dist/HelloWorldCalculator.exe`

## Manual Build Command
```powershell
py -3 -m pip install -r requirements.txt
py -3 -m PyInstaller --noconfirm --clean --windowed --name HelloWorldCalculator Calculator.py
```

## GitHub Actions Build Artifact
This repository now includes an automated Windows build workflow:
- `.github/workflows/master_mikegitpull.yml`

On each push, pull request, or manual run, GitHub Actions builds the exe and uploads it as:
- `HelloWorldCalculator-windows`

## GitHub Release Automation
Tag-based releases are automated via:
- `.github/workflows/release.yml`

When you push a tag like `v1.0.0`, GitHub Actions will create/update a GitHub Release and attach:
- `dist/HelloWorldCalculator.exe` (single-file)
- `dist/HelloWorldCalculator-portable.zip` (portable folder build)

Create and push a tag:
```powershell
git tag v1.0.0
git push origin v1.0.0
```

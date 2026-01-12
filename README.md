# X-COM Soldier Editor

A command-line save-file editor for **X-COM: Enemy Unknown** and **X-COM: Terror From The Deep**.

This tool allows you to:
- View and edit soldier stats
- Batch-edit all soldiers
- Instantly eliminate all enemies in an active tactical mission
- Safely work with both EU and TFTD save formats

---

## ⚠️ Important Warning

**Always make backups of your save files before using this tool.**  
This program directly modifies binary `.DAT` files. Mistakes can permanently corrupt saves.

---

## 📁 Supported Files

The editor works with the following X-COM save files:

### Strategic / Soldier Editing
- `SOLDIERS.DAT`

### Tactical / Mission Editing
- `UNITPOS.DAT`
- `UNITREF.DAT`

Both **Enemy Unknown** and **TFTD** formats are supported.

---

## 🚀 Running the Program

### Option 1: Using the EXE (Recommended)
1. Download the latest `.exe` from the Releases page
2. Double-click to run
3. Follow the on-screen menu instructions

### Option 2: Using Python
Requires **Python 3.10+**

```bash
python main.py

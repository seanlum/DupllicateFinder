# DupllicateFinder - <small>a cli Python utility which finds duplicate files by sha256sum</small>

## This tool is in early stages of development

### Libraries currently used:
- File and directory traversal: (`Python3/Lib/os`)
- File hashing: (`Python3/Lib/hashlib`)
- JSON output: (`Python3/Lib/json`)

### Goals:
- PyQT5 GUI Bindings (`pyqt5`)
- SQLite Database Storage (`Python3/Lib/sqlite3/`)
- JSON as Temp Cache Data (`refactor on using Python3/Lib/json`)
- Regular Expression search capabilities (`Python3/Lib/re`)

### Dependencies
```
python3 - for the cli, library, and GUI
python3-pyqt5 - for the GUI framework
qtwayland5 - (edge-case) for older wayland environments
```

## Installation
```
git clone <http-repo|ssh-repo>
# qtwayland5 is not required on all systems
# sudo apt install qtwayland5
./install.sh
$ GuiDupllicateFinder
$ DupllicateFinder
```


## Milestones
```
Transition from Python to C for easier native dependency management
```


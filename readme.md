# Lily Launcher

Fully customizable launcher for Windows, created with Python and Qt.

Configuration in JSON. Example configuration included.

Flat or hierarchical menu configuration possible.

### Run (delevopment)

```
python -m src.main
```

### Build

```
python -m src.build
```

A portable executable is created with a `lib` folder.
The example config is in the `lib` folder.

## Using icons.

Custom icons can be used. The following folder structure should be used:

```
 LilyLauncher/
  |- lib/
  |   |- icons/             # Default icons included with the launcher
  |
  |- icons/                 # Create 'icons' folder for your own icons
  |
  |- LilyLauncher.exe       # The executable
  |- lily_launcher.json     # Custom configuration
```

You can set an icon in the config file like this:

```
"icon": "my_computer.png"
```

The launcher will first search for `my_computer.png` in `LilyLauncher\lib\icons` and then in `LilyLauncher\icons`.
This will make sure your launcher keeps working after you copy it to another PC.
You can also specify an absolute path (not recommended).

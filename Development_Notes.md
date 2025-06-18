# Development Notes

## project structure:
```
project-root/
│
├── app/
│   ├── win/                    ← Packaged app for Windows users
│   │
│   ├── mac/                    ← Packaged app for MacOS users
│   │
│   └── lin/                    ← Packaged app for Linux users
│
│
│
├── src/
│   └── main/
│       ├── java/               ← Java GUI source
│       │   └── GUI/
│       │       ├── profiles/   ← saved to file location chosen by user, default in this folder
│       │       │   │
│       │       │   └── pi_profile.properties
│       │       │
│       │       ├── BuildGUI.java
│       │       ├── RpiCommandTab.java
│       │       ├── SettingsTab.java
│       │       ├── DataTab.java
│       │       ├── DataTab.java
│       │       ├── HelpTab.java
│       │       ├── SetupWizard.java
│       │       ├── Utility.java
│       │       │
│       │       └── host_config.properties
│       │
│       └── resources/
│           ├── icon/           ← image files for app icons
│           │
│           ├── setup/          ← image files for app icons
│           │   │
│           │   └── installer.iss/
│           │
│           │
│           │
│           ├── python/         ← bundled embedded python
│           │
│           └── python-scripts/ ← Python scripts, profiles/, configs.py
│               ├── modem/
│               │   ├── test.py
│               │   └── ssh.sh
│               │
│               ├── Py3SQM/
│               │
│               ├── ssh/
│               │   ├── auto_setup.py
│               │   ├── configs_ssh.py
│               │   ├── first_time_setup.py
│               │   ├── host_ssh.py
│               │   ├── lora_child_ssh.py
│               │   ├── lora_parent_ssh.py
│               │   ├── rpi_ssh.py
│               │   ├── sensor_ssh.py
│               │   ├── sensor_stream.py
│               │   ├── ui_commands.py
│               │   ├── radio_runner.sh
│               │   ├── rpi_runner.sh
│               │   └── sensor_runner.sh
│               │
│               └── scripts/
│                   ├── runradio.sh
│                   ├── runrpi.sh
│                   ├── runsensor.sh
│                   └── cronjobs.txt
│
├── jre/                       ← Bundled JRE (Java Runtime Environment)
│
│
├── pom.xml                    ← Maven build settings and plugins here
└── target/                    ← Output .jar/.exe
```
### `BuildGUI.java`
Contains the constructor for the full GUI
* calls each of `RPiCommandTab.java`, `SensorCommandTab.java`, `DataTab.java`, etc. to build the tabs of the GUI
* uses JTabbed Pane to separate each of the tabs
* builds one global console where backend information is displayed
* includes methods to minimize and show the console

### `RPiCommandTab.java`
Manage core RPi processes like starting/stopping the listener, checking status, and syncing files with the host, and sensor processes like requesting readings, calibration, etc.
* contains 3 main parts: the built-in commands, the manual command field, and the input field.
    * there are 4 built in commands located at the top of the RPi Command Center Tab to communicate directly with the RPi and a dropdown menu for specific commands to control the sensor.
    * the manual command field located at the bottom of the RPi Command Tab allows you to type in a command.
    * the input field becomes active for commands that require user input: if command requires user input, the input panel will prompt the user to supply more information

**parameters**:
* utility &rarr; one common utility method that is built in GUI.java
    * two main panels: command panel and feedback panel

**return**


### `DataTab.java`
Contains the constructor for the Data Tab
* **parameters**:
    * utility &rarr; one common utility method that is built in GUI.java
* using file chooser to allow user to navigate through their files to see where sqm data is synced to
* opens the user's file explorer to allow them to actually see the data
* **return**

### `SettingsTab.java`
Contains the constructor for the Settings Tab
* **parameters**:
    * utility &rarr; one common utility method that is built in GUI.java
* **other methods**
    * `loadAllProfiles()`
    * `loadProfile(String profileName)`
    * `saveProfile()`
    * `addProfile()`
    * `deleteProfile()`
* **return**
### `HelpTab.java`
This tab goes more in depth on each of the GUI tabs and how to use it.
* dropdown menu to access pages on more specific parts of the help center:
    * General
    * Rpi Command
    * Data Sync
    * Settings
    * SSH Help

**parameters**:
* utility &rarr; one common utility method that is built in GUI.java

**returns**

### `Utility.java`
Contains the utility methods used across all GUI tabs
* `sendCommand(String cmd)`
    * takes in command string and sends that to the python backend
* `append(String txt)`
    *
* `updateConfigsPy(String RpiName, String RpiAddr)`
    *
* `wrapWithRightPanel(JPanel main, JPanel side)`
    *
* `startPythonBackend()`
    *
* `copyToClipboard(String text)`
    *
* Getters:
    * `getProfileSaveDirFromConfig()`
        *
    * `getSQMSaveDirFromConfig()`
        *
    * `getDetectedOSType()`
        *
* Builders:
    * `buildTextArea(JPanel panel, int height)`
        *
    * `buildCopyRow(String command, int height)`
        *

### `SetupWizard.java`
### `setup_linux.java`
### `setup_windows.java`
### `setup_mac.java`

---

## why java?
### cross-platform compatibility
runs on Windows, macOS, and Linux without needing to rewrite the UI code.

ideal when the GUI needs to be used from different machines or OSes to control the Raspberry Pi.

### strong UI toolkit with swing
swing provides a rich set of widgets (buttons, tabs, text areas, dialogs, etc.) that are sufficient for the needs of:
* command buttons
* real-time logs
* file listing and settings forms


### maintainable and modular
GUI logic is separated from backend logic (handled in Python), allowing easier development and debugging on both ends.

### widely known/easy accessible
java is commonly taught and widely used, so it's easier for other developers to maintain or extend.
It avoids forcing the user to install and configure a web server, browser-based interface, and is taught in Smith's CS curriculum so avoids having to learn a new language.

## packaging with maven
This project uses maven as a project/build manager.




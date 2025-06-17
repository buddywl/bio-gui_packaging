; installer.iss — Inno Setup Script for GUIProject

[Setup]
; Metadata about your app
AppName=MPR-Bio-Remote
AppVersion=1.0
AppPublisher=MPR-Lab
DefaultDirName={pf}\MPR-Bio-Remote
DefaultGroupName=MPR-Bio-Remote
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

; Optional: Show a license file
; LicenseFile=license.txt

[Files]
; Recursively include everything in app/
Source: "C:\Users\buddy\Desktop\app2\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
; Desktop shortcut
Name: "{commondesktop}\MPR-Bio-Remote"; Filename: "{app}\MPR-Bio-Remote.exe"; WorkingDir: "{app}"
; Start Menu shortcut
Name: "{group}\MPR-Bio-Remote"; Filename: "{app}\MPR-Bio-Remote.exe"; WorkingDir: "{app}"

[Run]
; Optionally, launch after install
Filename: "{app}\MPR-Bio-Remote.exe"; Description: "Launch MPR-Bio-Remote now"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Optional: remove any extra generated files on uninstall (e.g., logs)
; Example:
; Type: filesandordirs; Name: "{app}\logs"

; Inno Setup script for {{APP_NAME}}
; Download Inno Setup: https://jrsoftware.org/isdl.php

#define MyAppName "{{APP_NAME}}"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "{{APP_PUBLISHER}}"
#define MyAppURL "{{APP_URL}}"
#define MyAppExeName "{{APP_EXE}}"

[Setup]
; AppId uniquely identifies this product across versions. NEVER change it for an existing product.
; NEVER reuse a GUID from another product.
; Inno Setup syntax: {{GUID} — two opening braces (escape for literal `{`), one closing brace.
; Template substitution replaces {{APP_ID_GUID}} with the GUID string, leaving surrounding braces intact.
AppId={{{{APP_ID_GUID}}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Output locally — we copy to the network share after signing. Writing direct to Z: causes file-lock errors.
OutputDir=..\dist\installer
OutputBaseFilename={{APP_SLUG}}_Setup_{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
MinVersion={{MIN_WINDOWS_VERSION}}
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Everything from PyInstaller's COLLECT output
Source: "..\dist\{{APP_SLUG}}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  if not IsWin64 then
  begin
    MsgBox('This application requires a 64-bit version of Windows.', mbError, MB_OK);
    Result := False;
    exit;
  end;
end;

[UninstallDelete]
Type: filesandordirs; Name: "{app}\__pycache__"
Type: filesandordirs; Name: "{app}\*.log"

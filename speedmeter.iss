[Setup]
AppName=Internet Speed Meter
AppVersion=1.0
DefaultDirName={autopf}\InternetSpeedMeter
DefaultGroupName=Internet Speed Meter
OutputDir=output
OutputBaseFilename=setup
SetupIconFile=speedmeter.ico
Compression=lzma2/ultra64
SolidCompression=yes
UninstallDisplayIcon={app}\speedmeter.exe
AppMutex=InternetSpeedMeterMutex

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  if CheckForMutexes('InternetSpeedMeterMutex') then
  begin
    MsgBox('Internet Speed Meter is already running. Please close it before installation.', mbError, MB_OK);
    Result := False;
  end;
end;

[Files]
Source: "dist\speedmeter.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Internet Speed Meter"; Filename: "{app}\speedmeter.exe"
Name: "{userstartup}\Internet Speed Meter"; Filename: "{app}\speedmeter.exe" ; WorkingDir: "{app}"; IconFilename: "{app}\speedmeter.exe"
Name: "{group}\Uninstall Internet Speed Meter"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\speedmeter.exe"; Description: "Launch after install"; Flags: nowait postinstall skipifsilent
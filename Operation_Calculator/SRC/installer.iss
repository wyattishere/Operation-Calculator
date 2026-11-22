[Setup]
AppName=Operation Cost Calculator
AppVersion=1.0.01
AppPublisher=Sight Vector Studios
PrivilegesRequired=lowest
DefaultDirName={localappdata}\Programs\Operation Cost Calculator
DefaultGroupName=Operation Cost Calculator
OutputDir=installer_output
OutputBaseFilename=OperationCostCalculator_Setup
SetupIconFile=moneycalc.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\OperationCostCalculator\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Operation Cost Calculator"; Filename: "{app}\OperationCostCalculator.exe"
Name: "{autodesktop}\Operation Cost Calculator"; Filename: "{app}\OperationCostCalculator.exe"

[Run]
Filename: "{app}\OperationCostCalculator.exe"; Description: "Launch Operation Cost Calculator"; Flags: nowait postinstall skipifsilent

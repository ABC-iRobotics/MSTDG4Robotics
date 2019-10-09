[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$tempFolder="C:/vrep_install_temp_folder"
Write-Host "Checking if $tempFolder directory exists..."
if (!(Test-Path $tempFolder -PathType Container)){
	New-Item -Path $tempFolder -ItemType directory
	Write-Host "Directory created..."
} else{
	Write-Host "Directory existed..."
}
Write-Host "Downloading V-REP 3.6.1..."
Invoke-WebRequest -Uri "http://www.coppeliarobotics.com/files/V-REP_PRO_EDU_V3_6_1_Setup.exe" -OutFile "$tempFolder/V-REP_PRO_EDU_V3_6_1_Setup.exe"

Write-Host "Installing V-REP 3.6.1..."
$fullpath = join-path -path $tempFolder -childpath "V-REP_PRO_EDU_V3_6_1_Setup.exe"
& $fullpath /quiet InstallAllUsers=0 PrependPath=1 Include_test=0

Write-Host "Deleting install file and temp folder..."
Remove-Item -Path $tempFolder -Force
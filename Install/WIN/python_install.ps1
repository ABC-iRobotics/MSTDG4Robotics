[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$tempFolder="C:/python_install_temp_folder"
Write-Host "Checking if $tempFolder directory exists..."
if (!(Test-Path $tempFolder -PathType Container)){
	New-Item -Path $tempFolder -ItemType directory
	Write-Host "Directory created..."
} else{
	Write-Host "Directory existed..."
}
Write-Host "Downloading python 3.7.0..."
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.7.0/python-3.7.0-amd64.exe" -OutFile "$tempFolder/python-3.7.0-amd64.exe"

Write-Host "Installing python 3.7.0..."
$fullpath = join-path -path $tempFolder -childpath "python-3.7.0-amd64.exe"
& $fullpath /quiet InstallAllUsers=0 PrependPath=1 Include_test=0

Write-Host "Adding python to PATH..."
$env:Path += ";$HOME\AppData\Local\Programs\Python\Python37"

cd ../../PythonClient
pip install Pillow
pip install pymongo
cd ../Install/WIN

Write-Host "Deleting install file and temp folder..."
Remove-Item -Path $tempFolder -Force
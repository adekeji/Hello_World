param(
	[switch]$OneFile
)

$ErrorActionPreference = "Stop"

Write-Host "Installing build dependencies..."
py -3 -m pip install -r requirements.txt

Write-Host "Building Hello World Calculator executable..."
$buildArgs = @("-m", "PyInstaller", "--noconfirm", "--clean", "--windowed", "--name", "HelloWorldCalculator")

if ($OneFile) {
	$buildArgs += "--onefile"
}

$buildArgs += "Calculator.py"
py -3 @buildArgs

if ($OneFile) {
	Write-Host "Build complete. Output: dist\HelloWorldCalculator.exe"
}
else {
	Write-Host "Build complete. Output: dist\HelloWorldCalculator\HelloWorldCalculator.exe"
}

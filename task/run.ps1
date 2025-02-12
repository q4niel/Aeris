$task = "$(Split-Path -Parent $MyInvocation.MyCommand.Path)"
$files = Get-ChildItem -Path "$($task)\bin"
$tasks = @()

if (-not (Test-Path $("$task\env") -PathType Container)) {
    py -3 -B -m venv $task\env
    & "$($task)\env\Scripts\Activate.ps1"
    pip install -r $("$task\requirements.txt")
    deactivate
}

for ($i = 0; $i -lt $files.Count; $i++) {
    $tasks += $files[$i].Name
}

for ($i = 0; $i -lt $tasks.Count; $i++) {
    Write-Host "$i | $($tasks[$i])"
}

$input = Read-Host "Run: "

if ($input -ge "0" -and $input -lt $tasks.Count) {
    & "$($task)\env\Scripts\Activate.ps1"
    python -B "$($task)\bin\$($tasks[$input])"
    deactivate
}
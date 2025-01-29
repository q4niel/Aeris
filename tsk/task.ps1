$tsk = Split-Path -Parent $MyInvocation.MyCommand.Path
$files = Get-ChildItem -Path $tsk
$tasks = @()

for ($i = 0; $i -lt $files.Count; $i++) {
    if ($files[$i].Extension -ne ".py") { continue }

    if (Select-String -Path $files[$i].FullName -Pattern 'if __name__ == "__main__": main()') {
        $tasks += $files[$i].Name
    }
}

for ($i = 0; $i -lt $tasks.Count; $i++) {
    Write-Host "$i | $($tasks[$i])"
}

$input = Read-Host "Run: "

if ($input -ge "0" -and $input -lt $tasks.Count) {
    py -3 -B "$($tsk)\$($tasks[$input])"
}
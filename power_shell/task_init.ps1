$LogOnTaskName = "WallPaperTask"
$LoopTaskName = "WallPaperTaskLoop"
# Remove the possible already existing tasks.
# **If you change the task names, make sure to remove the older tasks, as they won't be remove with this specific code.
if (Get-ScheduledTask -TaskName $LogOnTaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $LogOnTaskName -Confirm:$false
    Write-Host "Scheduled task '$LogOnTaskName' removed successfully."
} else {
    Write-Host "Scheduled task '$LoopTaskName' does not exist, skipping removal."
}
if (Get-ScheduledTask -TaskName $LoopTaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $LoopTaskName -Confirm:$false
    Write-Host "Scheduled task '$LoopTaskName' removed successfully."
} else {
    Write-Host "Scheduled task '$LoopTaskName' does not exist, skipping removal."
}

$PythonExePath = "Put here the result of print(sys.executable) after adding w to get pythonw.exe"
$WorkingDirectory = "Put here the root folder of the application"
# Task that runs on log on
$Action = New-ScheduledTaskAction -Execute $PythonExePath `
    -Argument "src\program.pyw" -WorkingDirectory $WorkingDirectory
$UserName = [Environment]::UserName
$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $UserName
$Principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -RunLevel Highest
Register-ScheduledTask -TaskName $LogOnTaskName -Action $Action -Trigger $Trigger -Principal $Principal

# Task that runs every minutes
$Action = New-ScheduledTaskAction -Execute $PythonExePath `
    -Argument "src\program_loop.pyw" -WorkingDirectory $WorkingDirectory
# Define a duration of 1 year which I hope you will have restarted your PC at least once during this time.
$MaxTaskDuration = New-TimeSpan -Days 365
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) `
    -RepetitionInterval (New-TimeSpan -Minutes 1)`
    -RepetitionDuration $MaxTaskDuration
$Principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -RunLevel Highest
Register-ScheduledTask -TaskName $LoopTaskName -Action $Action -Trigger $Trigger -Principal $Principal

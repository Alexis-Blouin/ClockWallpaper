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

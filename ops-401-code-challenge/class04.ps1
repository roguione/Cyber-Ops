# Justin H
# Tm Geneva, Sirra , and Nick A
# Powershell -> Min password / Enabled: Disable driver
# 4/20/23


$currentUsername = $env:USERNAME
$newPassword = Read-Host -Prompt "Enter a new password" -AsSecureString

try {
    Set-LocalUser -Name $currentUsername -Password $newPassword -ErrorAction Stop
    Write-Host "Password has been set for user $currentUsername."
}
catch {
    Write-Host "Failed to set password for user $currentUsername. Error message: $($_.Exception.Message)"
}


# Get the current SMB server configuration
$smbConfig = Get-SmbServerConfiguration

# Check if SMB1 is currently enabled
if ($smbConfig.EnableSMB1Protocol) {
    # Disable SMB1
    Set-SmbServerConfiguration -EnableSMB1Protocol $false

    # Output a message indicating that SMB1 has been disabled
    Write-Host "SMB1 protocol has been disabled."
} else {
    # Output a message indicating that SMB1 is already disabled
    Write-Host "SMB1 protocol is already disabled."
}

import paramiko


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='10.60.190.16', username='940305', password='!Madinah25')
print("SSH connection is successfully established with 10.60.190.16")
import os
import paramiko
import csv
from paramiko import SSHClient, AutoAddPolicy


def ssh_via_bastion(dest_address, dest_key, bast_address, bast_key, dest_user, bast_user):

    bast_ssh_client = SSHClient()
    bast_ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    bast_ssh_client.connect(
        hostname=bast_address,
        username=bast_user,
        pkey=bast_key
    )

    transport = bast_ssh_client.get_transport()
    dest_addr = (dest_address, 22)  
    local_addr = ("localhost", 54321)       
    channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

    dest_client = SSHClient()
    dest_client.set_missing_host_key_policy(AutoAddPolicy())
    dest_client.connect(
        hostname=dest_address,
        username=dest_user,
        pkey=dest_key,
        sock=channel
)
    
    return dest_client

def fetch_file_via_sshclient(sshclient, filename):
    with sshclient.open_sftp() as sftp:
        with sftp.file(filename, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            fetched_csv_data = list(reader)

    return fetched_csv_data
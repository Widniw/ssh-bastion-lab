import csv
from paramiko import SSHClient, AutoAddPolicy
import logging
import time


def ssh_via_bastion(
    dest_address,
    dest_key,
    bast_address,
    bast_key,
    dest_user,
    bast_user,
    max_retries=3,
    retry_delay=10,
):
    for attempt in range(max_retries):
        try:
            bast_ssh_client = SSHClient()
            bast_ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            bast_ssh_client.connect(
                hostname=bast_address, username=bast_user, pkey=bast_key
            )

            transport = bast_ssh_client.get_transport()
            dest_addr = (dest_address, 22)
            local_addr = ("localhost", 0)
            channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

            dest_client = SSHClient()
            dest_client.set_missing_host_key_policy(AutoAddPolicy())
            dest_client.connect(
                hostname=dest_address, username=dest_user, pkey=dest_key, sock=channel
            )
        except Exception as e:
            logging.error(
                f"Connection failed (attempt {attempt+1}/{max_retries}): {str(e)}"
            )
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            logging.critical(
                f"Connection timeout. Failed to connect to {str(bast_address)} -> {str(dest_address)}"
            )
            raise

    return dest_client


def fetch_csv_via_sshclient(sshclient, filename):
    with sshclient.open_sftp() as sftp:
        try:
            with sftp.file(filename, "r") as csv_file:
                reader = csv.DictReader(csv_file)
                fetched_csv_data = {}
                for row in reader:
                    fetched_csv_data[row["hostname"]] = row
        except FileNotFoundError:
            logging.critical(f"File {filename} not found. Test terminated.")
            raise

    return fetched_csv_data

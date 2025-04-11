import paramiko
import os
import csv
import ipaddress
import logging
from datetime import datetime
from paramiko import SSHClient, AutoAddPolicy
from ssh_utils import ssh_via_bastion, fetch_file_via_sshclient

logging.basicConfig(
    filename=f"test_log_{datetime.now()}.log",
    filemode="w",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.WARNING
)

ssh_user = "stauto"
server_a_address = os.getenv("SERVER_A_ADDRESS")
server_b_address = os.getenv("SERVER_B_ADDRESS")
server_a_key = paramiko.RSAKey.from_private_key_file(os.getenv("SERVER_A_KEY"))
server_b_key = paramiko.RSAKey.from_private_key_file(os.getenv("SERVER_B_KEY"))

server_b_client = ssh_via_bastion(server_b_address, server_b_key, server_a_address, server_a_key, ssh_user, ssh_user)

filename = "/home/stauto/network_devices.csv"

fetched_csv_data = fetch_file_via_sshclient(server_b_client, filename)

valid_csv_data = []

for row in fetched_csv_data:
    if row['status'] not in ('online', 'offline'):
        logging.warning(row)
        continue

    try:
        row['device_id'] = int(row["device_id"])
        row['ip_address'] = ipaddress.IPv4Address(row['ip_address'])
    except ipaddress.AddressValueError:
        logging.warning(row)
    except ValueError:
        logging.warning(row)
    else:
        valid_csv_data.append(row)

online_devices_csv = list(filter(lambda x: x['status'] == 'online', valid_csv_data))

print('Checking device`s online status: 1/')




    
    


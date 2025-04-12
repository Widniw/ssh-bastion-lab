import paramiko
import os
import logging
import argparse
import time
import sys
from csv_utils import validate_csv
from ssh_utils import ssh_via_bastion, fetch_csv_via_sshclient
from argparse_utils import check_positive

logging.basicConfig(
    filename="/rem_device_stat_check/test_log.log",
    filemode="w",
    format="{asctime} - {levelname} - {message}",
    style="{",
    level=logging.INFO,
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t",
    "--timeout",
    required=True,
    type=check_positive,
    help="Test duration. The network status check is performed every 20 seconds.",
)
args = parser.parse_args()

test_interval = 20
ssh_user = "stauto"
filename = "/home/stauto/network_devices.csv"
server_a_address = os.getenv("SERVER_A_ADDRESS")
server_b_address = os.getenv("SERVER_B_ADDRESS")
server_a_key = paramiko.RSAKey.from_private_key_file(os.getenv("SERVER_A_KEY"))
server_b_key = paramiko.RSAKey.from_private_key_file(os.getenv("SERVER_B_KEY"))

server_b_client = ssh_via_bastion(
    server_b_address, server_b_key, server_a_address, server_a_key, ssh_user,
    ssh_user, max_retries=3, retry_delay=10
)

fetched_csv_data = fetch_csv_via_sshclient(server_b_client, filename)

valid_csv_data = validate_csv(fetched_csv_data)

if not valid_csv_data:
    logging.critical(f"Filename {filename} is empty. Test terminated")
    sys.exit(1) 

online_devices_csv = {
    k: v for k, v in valid_csv_data.items() if "online" in v["status"]
}

start_time = time.time()
elapsed_time = time.time() - start_time
while elapsed_time < args.timeout:

    print(f"Checking device status. Elapsed time: {elapsed_time}")

    try:

        fetched_csv_data = fetch_csv_via_sshclient(server_b_client, filename)

        for hostname in online_devices_csv:
            if (
                online_devices_csv[hostname]["status"]
                != fetched_csv_data[hostname]["status"]
            ):

                logging.critical(f"Device {hostname} is offline. Test terminated.")
                sys.exit(1)

    except Exception as e:
        logging.error(f"Error during check: {str(e)}")
        server_b_client = ssh_via_bastion(
            server_b_address,
            server_b_key,
            server_a_address,
            server_a_key,
            ssh_user,
            ssh_user,
            max_retries=3,
            retry_delay=10
        )
    else:
        time.sleep(test_interval)
    finally:
        elapsed_time = time.time() - start_time


logging.info(
    f"Test completed. All devices remained online. Elapsed time: {elapsed_time}"
)

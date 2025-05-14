
## Scenario & Program Description

In the following scenario, a script is connecting to the server B via a bastion host (Eg. A firewall is blocking direct access via policy). Once connected the CSV data is fetched and then validated for correct type. Then, every 20 seconds the data is fetched again to check whether there is a device which went offline. The script implements auto-reconnect mechanism to prevent test termination in case of temporary network failure.

## Requirements

- Docker  
- SSH key generation software  

## How To Run The Program

**Step 1.**  
Generate SSH key pair for server A and B:  
```bash
ssh-keygen -t rsa -f server_a_key
ssh-keygen -t rsa -f server_b_key
```
**Step 2.**  
Put `server_a_key.pub` into the `server_a` folder.  
Put `server_b_key.pub` into the `server_b` folder.  

**Step 3.**  
Run the containers from the main directory using:  
```bash
sudo docker compose up -d
```

**Step 4.**
Enter the script_runner container
```bash
sudo docker exec -it hitachi-interview-script_runner-1 /bin/bash
```

**Step 5.**
Run the program
```bash
python /rem_device_stat_check/main.py -t 30
```

The test_log.log should be available in rem_device_stat_check directory.

## Performed tests.

The program was tested manually and automatically, using pytest. Perfmormed tests are listed below:

**Manual tests**
- Check fetching empty CSV file
- Check logging invalid csv entries inside test_log.log
- Modify device's status to ***offline*** on live server B
- Finish test with no device status change
- Disconnect Server A temporarily
- Disconnect Server B temporarily
- Disconnect Server A permanently
- Disconnect Server B permanently

**Automatic tests**

- Unit test for csv_utils and argparse_utils


## Used workarounds

A python dictionary was used for CSV rows instead of list of dynamically generated objects. Dynamically generated attributes for class were
problematic to implement.

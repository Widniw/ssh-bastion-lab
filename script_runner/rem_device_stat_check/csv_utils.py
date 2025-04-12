import logging
import ipaddress


def validate_csv(csv_file):
    valid_csv_data = {}
    
    if not csv_file:
        logging.error("CSV file is empty.")
        return None

    for row in csv_file:
        if csv_file[row]["status"] not in ("online", "offline"):
            logging.warning(f"Invalid CSV data: {csv_file[row]}")
            continue

        try:
            csv_file[row]["device_id"] = int(csv_file[row]["device_id"])
            csv_file[row]["ip_address"] = ipaddress.IPv4Address(
                csv_file[row]["ip_address"]
            )
            csv_file[row]["hostname"] = str(csv_file[row]["hostname"])
            csv_file[row]["vendor"] = str(csv_file[row]["vendor"])
            csv_file[row]["model"] = str(csv_file[row]["model"])
            csv_file[row]["firmware_version"] = str(csv_file[row]["firmware_version"])

        except ipaddress.AddressValueError:
            logging.warning(f"Invalid CSV data: {csv_file[row]}")
        except ValueError:
            logging.warning(f"Invalid CSV data: {csv_file[row]}")
        else:
            valid_csv_data[row] = csv_file[row]

    return valid_csv_data

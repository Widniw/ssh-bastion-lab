import pytest
from script_runner.rem_device_stat_check.csv_utils import validate_csv
from ipaddress import IPv4Address

@pytest.fixture
def sample_data():
    return {
        "string_device_id": {
            "device_id": "abc",
            "hostname": "dnsmasq",
            "ip_address": "192.168.0.1",
            "status": "online",
            "vendor": "Cisco",
            "model": "advanced",
            "firmware_version": "1.2.2"
        },
        "invalid_ip_address": {
            "device_id": "1",
            "hostname": "router1",
            "ip_address": "192.168.1.1/24",
            "status": "online",
            "vendor": "Cisco",
            "model": "advanced",
            "firmware_version": "1.2.2"
        },
        "invalid_status": {
            "device_id": "1",
            "hostname": "router1",
            "ip_address": "192.168.1.1",
            "status": "up",
            "vendor": "Cisco",
            "model": "advanced",
            "firmware_version": "1.2.2"
        },
        "valid_row": {
            "device_id": "1",
            "hostname": "router1",
            "ip_address": "192.168.1.1",
            "status": "online",
            "vendor": "Hitachi",
            "model": "advanced",
            "firmware_version": "1.2.2"
        }
    }

def test_string_device_id(sample_data):
    result = validate_csv(sample_data)
    assert "invalid_device_id" not in result

def test_invalid_ip_address(sample_data):
    result = validate_csv(sample_data)
    assert "invalid_ip_address" not in result

def test_invalid_status(sample_data):
    result = validate_csv(sample_data)
    assert "invalid_status" not in result

def test_valid_row(sample_data):
    result = validate_csv(sample_data)
    assert "valid_row" in result
    assert isinstance(result["valid_row"]["device_id"], int)
    assert isinstance(result["valid_row"]["hostname"], str)
    assert isinstance(result["valid_row"]["ip_address"], IPv4Address)
    assert isinstance(result["valid_row"]["status"], str)
    assert result["valid_row"]["status"] in ("online", "offline")
    assert isinstance(result["valid_row"]["vendor"], str)
    assert isinstance(result["valid_row"]["model"], str)
    assert isinstance(result["valid_row"]["firmware_version"], str)

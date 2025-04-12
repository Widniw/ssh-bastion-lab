import pytest
import argparse
from script_runner.rem_device_stat_check.argparse_utils import check_positive


def test_valid_positive_integer():
    assert check_positive("20") == 20


def test_zero_value():
    with pytest.raises(argparse.ArgumentTypeError):
        check_positive("0")


def test_negative_values():
    with pytest.raises(argparse.ArgumentTypeError):
        check_positive("-5")


def test_string_value():
    with pytest.raises(ValueError):
        check_positive("asdf")


def test_float_value():
    assert check_positive("7.12") == 7

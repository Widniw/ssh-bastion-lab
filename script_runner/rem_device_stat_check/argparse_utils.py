import argparse


def check_positive(value):
    ivalue = int(float(value))
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(
            f"{value} is not a positive int value."
            )
    return ivalue

import argparse
import datetime
import logging
import time
from .radman2 import RadMan2
from .radhaz_standards import *


# Command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "port",
    default="/dev/ttyACM0",
    type=str,
    help=f"RadMan2 Serial Port (Default: /dev/ttyACM0)",
)
parser.add_argument(
    "-l",
    "--log",
    default=False,
    action='store_true',
    help=f"Enable logging output (YYYYMMDD-HHMMSS.log)",
)
parser.add_argument(
    "--frequency",
    default=None,
    type=float,
    help=f"Convert percentage measurements to E/H-field levels for this frequency (MHz).",
)
parser.add_argument(
    "-v", "--verbose", help="Enable debug output.", action="store_true"
)
args = parser.parse_args()

# Set log-level to DEBUG if requested
if args.verbose:
    logging_level = logging.DEBUG
else:
    logging_level = logging.INFO

# Set up logging
logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging_level)


def print_device_info(device_info):
    logging.info(f"Device Information for {device_info['product_name']}")
    logging.info(f"\tProduct Name: {device_info['product_name']}")
    logging.info(f"\tProduction ID: {device_info['production_id']}")
    logging.info(f"\tSerial Number: {device_info['serial_number']}")
    logging.info(f"\tDevice ID: {device_info['device_id']}")
    logging.info(f"\tDevice Type: {device_info['device_type']}")
    logging.info(f"\tFirmware Version: {device_info['firmware_version']}")
    logging.info(f"\tCalibration Date: {device_info['calibration_date']}")
    logging.info(f"\tCalibration Due: {device_info['calibration_due']}")

def print_probe_info(probe_info):
    logging.info(f"Probe Information for {probe_info['product_name']}")
    logging.info(f"\tProduct Name: {probe_info['product_name']}")
    logging.info(f"\tProduction ID: {probe_info['production_id']}")
    logging.info(f"\tSerial Number: {probe_info['serial_number']}")
    logging.info(f"\tCalibration Date: {probe_info['calibration_date']}")
    logging.info(f"\tCalibration Due: {probe_info['calibration_due']}")
    logging.info(f"\tE-Field Range: {probe_info['e_field_lower_frequency_hz']/1e6} - {probe_info['e_field_upper_frequency_hz']/1e6} MHz")
    try:
        logging.info(f"\tH-Field Range: {probe_info['h_field_lower_frequency_hz']/1e6} - {probe_info['h_field_upper_frequency_hz']/1e6} MHz")
    except:
        pass
    logging.info(f"\tShaped Probe: {probe_info['shaped']}")
    logging.info(f"\tShaping Standard: {probe_info['standard_name']}")


# Shaping Standard, for conversion of percentages back to E/H field levels.
standard = None

# Log file
log_file = None

def handle_data(data):

    _timestamp = datetime.datetime.utcnow().isoformat() + 'Z'

    # Convert percentages to E/H-field levels, if we have been provided a frequency.
    if standard and args.frequency:
        data['e_field'] = standard.percentage_to_efield(data['e_field_percentage'], args.frequency)
        data['h_field'] = standard.percentage_to_hfield(data['h_field_percentage'], args.frequency)

        logging.info(f"{_timestamp}: E-Field: {data['e_field']:.3f} V/m ({data['e_field_percentage']:.2f}%), H-Field: {data['h_field']:.3f} A/m ({data['h_field_percentage']:.2f}%)")

    else:
        logging.info(f"{_timestamp}: E-Field: {data['e_field_percentage']:.2f}%, H-Field: {data['h_field_percentage']:.2f}%")

    if log_file:

        if standard and args.frequency:
            _log_line = f"{_timestamp},{data['e_field_percentage']:.2f},{data['h_field_percentage']:.2f},{data['battery_percentage']},{data['e_field']:.3f},{data['h_field']:.3f}\n"
        else:
            _log_line = f"{_timestamp},{data['e_field_percentage']:.2f},{data['h_field_percentage']:.2f},{data['battery_percentage']}\n"

        logging.debug(f"Logged Line: {_log_line.strip()}")
        log_file.write(_log_line)
        log_file.flush()



_radman = RadMan2(args.port, auto=False, callback=handle_data)

print_device_info(_radman.device_info)
print_probe_info(_radman.probe_info)

standard = choose_standard(_radman.probe_info['standard_name'])
if standard and args.frequency:
    logging.info(f"Using RADHAZ Standard '{standard.name}', for {args.frequency} MHz.")
    logging.info(f"Limits: {standard.efield_limit(args.frequency):.3f} V/m, {standard.hfield_limit(args.frequency):.3f} A/m")


if args.log:
    _logfilename = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S.log")

    log_file = open(_logfilename,'w')

    log_file.write(f"# Device Info: {_radman.device_info}\n")
    log_file.write(f"# Probe Info: {_radman.probe_info}\n")
    if standard and args.frequency:
        log_file.write(f"# Using RADHAZ Standard '{standard.name}', for {args.frequency} MHz.\n")
        log_file.write(f"# Limits: {standard.efield_limit(args.frequency):.3f} V/m, {standard.hfield_limit(args.frequency):.3f} A/m\n")
        log_file.write("timestamp,e_field_percent,h_field_percent,battery,e_field,h_field\n")
    else:
        log_file.write("timestamp,e_field_percent,h_field_percent,battery\n")

    logging.info(f"Opened Log File: {_logfilename}")


_radman.start_measurement()


# Just wait for data
try:
    while True:
        time.sleep(1)
except Exception as e:
    _radman.close()
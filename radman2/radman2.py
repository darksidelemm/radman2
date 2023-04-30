import datetime
import logging
import sys
import serial
import time
from threading import Thread, Lock

DEFAULT_RADMAN_PORT = "/dev/ttyACM0"

class RadMan2(object):
    """
    A class to communicate with a Narda RadMan 2XT
    (And possibly other versions)
    """

    def __init__(self, port="/dev/ttyACM0", baud_rate=115200, sample_rate=1, auto=False, callback=None, log=None, timeout=2):
        """
        Create a RadMan2 Communication Object.
        """

        self.measurement_running = False
        self.callback = callback
        self.sample_rate = sample_rate

        # Connect
        logging.info(f"Attempting to connect to RadMan2 on {port}, at {baud_rate} baud...")
        try:
            self.s = serial.Serial(port, baud_rate, timeout=timeout)
        except Exception as e:
            logging.critical("Could not connect to RadMan2 - %s" % str(e))
            sys.exit(1)

        # Get the device information data
        self.device_info = self.get_device_info()

        # Get the device information data
        self.probe_info = self.get_probe_info()

        if auto:
            self.start_measurement()



    def __del__(self):
        try:
            self.s.close()
        except AttributeError:
            # Silently handle errors if self.s does not exist.
            pass


    def get_device_info(self):
        """
        Query a RadMan2 for device information.
        """
        data = self.command("DEVICE_INFO?")

        _fields = data[:-1].split(',')

        if len(_fields) != 10:
            raise ValueError(f"Incorrect number of fields {len(_fields)} from RadMan Device Info response!")

        output = {
            'product_name': _fields[0],
            'production_id': _fields[1],
            'serial_number': _fields[2],
            'device_id': _fields[3],
            'device_type': _fields[4],
            'firmware_version': _fields[5],
            'calibration_date': _fields[6],
            'calibration_due': _fields[7],
            'num_options': _fields[8],
            'options_name': _fields[9]
        }

        return output

    def get_probe_info(self):
        """
        Query a RadMan2 for probe information.
        """
        data = self.command("Probe_INFO?")

        _fields = data[:-1].split(',')

        if len(_fields) != 12:
            raise ValueError(f"Incorrect number of fields {len(_fields)} from RadMan Probe Info response!")

        output = {
            'product_name': _fields[0],
            'production_id': _fields[1],
            'serial_number': _fields[2],
            'calibration_date': _fields[3],
            'calibration_due': _fields[4],
            'field_type': _fields[5]
        }
        try:
            output
            output['e_field_lower_frequency_hz'] = float(_fields[6])
            output['e_field_upper_frequency_hz'] = float(_fields[7])
            output['h_field_lower_frequency_hz'] = float(_fields[8])
            output['h_field_upper_frequency_hz'] = float(_fields[9])
            output['shaped'] = _fields[10]
            output['standard_name'] = _fields[11]
        except Exception as e:
            logging.warning(f"Exception when parsing probe info fields - {str(e)}")

        return output


    def set_remote_mode(self,remote_mode=True):
        """
        Set the RadMan2 into remote mode, allowing enabling of measurements.
        """

        if remote_mode:
            _status = self.command("REMOTE ON")
        else:
            _status = self.command("REMOTE OFF")

        if _status == '0;':
            return True
        else:
            return False


    def measurement_loop(self):
        """
        Continually read lines of measurement from the RadMan2, and attempt to
        parse them.

        Each line is of the format:
        0,8,0,OK,OK,100;
        which appears to be:
        e_field_percentage, h_field_percentage, unknown, e_field_meas_ok, h_field_meas_ok, battery_percentage;

        The E and H-field percentage values are the percentage of the limit standard, multiplied by 100.

        """

        while self.measurement_running:

            _line = self.s.readline().decode().strip()
            
            try:
                # Split into comma separated fields, remove last ; character
                _fields = _line[:-1].split(',')

                if len(_fields) != 6:
                    logging.error(f"Not enough fields in measurement line.")
                    continue
                else:
                    _output = {}
                    _output['e_field_percentage'] = float(_fields[0])/100.0
                    _output['h_field_percentage'] = float(_fields[1])/100.0
                    _output['unknown'] = _fields[2]
                    _output['e_field_ok'] = _fields[3]
                    _output['h_fields_ok'] = _fields[4]
                    _output['battery_percentage'] = float(_fields[5])

                    if self.callback:
                        self.callback(_output)

            except Exception as e:
                logging.error(f"Could not parse measurement line: {str(_line)} - {str(e)}")
        

    def start_measurement(self):
        """
        Configure the RadMan2 into remote mode, then initiate
        a continuous measurement.

        TODO: Allow sample rate adjustment.
        """

        if self.measurement_running:
            return

        self.set_remote_mode(True)

        self.command("MEAS_START_CIB", noreply=True)

        self.measurement_running = True
        self.measurement_thread = Thread(target=self.measurement_loop)
        self.measurement_thread.start()


    def stop_measurement(self):
        """
        Halt a measurement.
        """
        self.command("MEAS_STOP_CIB", noreply=True)


    def command(self, command, noreply = False):
        """
        Send a command and return the result. For human interactive use.
        """

        if self.measurement_running:
            return None

        _command = command.encode() + b';'

        self.s.write(_command)

        if noreply:
            return

        _response = self.s.readline()

        return _response.decode().strip()


    def close(self):
        self.measurement_running = False
        time.sleep(5)
        self.s.close()


if __name__ == "__main__":
    """
    Basic test script. Connect to a RadMan2, query it for some basic info,
    then set it into measurement mode and print out the results.
    """
    import sys

    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG,
    )

    def print_data(data):
        print(data)

    if len(sys.argv) > 1:
        _port = sys.argv[1]
    else:
        _port = DEFAULT_RADMAN_PORT

    _radman = RadMan2(_port, auto=True, callback=print_data)

    print(_radman.device_info)
    print(_radman.probe_info)

    try:
        while True:
            time.sleep(1)
    
    except:
        _radman.close()

    
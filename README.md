# Narda RadMan 2XT Communication Utilities

A very basic python library and utilities for communicating with a Narda Radman 2XT personal non-ionising radiation monitor.

The RadMan 2XT has a USB-C port which appears as a ACM-serial device. The commmunications protocol appears to have a similar message structure as some of Narda's other products, e.g. the [NBM-550](https://www.narda-sts.com/en/wideband-emf/nbm-550/nbme-field-3-ghz-high-power/pd/pdfs/23286/eID/). Further, Narda's RadMan2-TS software displays the commands being sent, giving a good idea as to what needs to be sent.

## Disclaimers
* This library should not be used for making safety-of-life measurements (at least, not until it's been properly validated!)
* Conversions from percentages-of-standards to absolute E/H-field measurements are only valid when measuring single-frequency emitters, and if the frequency has been specified correctly.
* The uncertainty of any results from this library have not been tested. Future work will involve comparing the output of a RadMan 2XT to that of a Narda NBM-550, for both free-space and TEM-cell measurements.

## TODO List:
* Compare measurements from a RadMan 2XT against a Narda NBM-550 or similar.
* Implement more RADHAZ Standards (in particular RPS S-1), and add support to convert between standards.
* Develop plotting GUIs

## Dependencies
* Python3
* pyserial

For the plotting examples, the following dependncies are also needed:
* pyqtgraph
* PyQt5

### System-Level Dependencies
* Python >= 3.6

### Create a Virtual Environment

Create a virtual environment and install dependencies.

```console
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install pip -U       (Optional - this updates pip)
```

Gather packages required for basic communication with:
```
(venv) $ pip install -r requirements.txt
```

Gather packages required for plotting of data with:
```
(venv) $ pip install -r requirements_plotter.txt
```

## Usage
We can start a command-line utility that will print out measurements using:

```shell
% python -m radman2 /dev/tty.usbmodem2101 
2023-04-30 13:58:06,315 INFO: Attempting to connect to RadMan2 on /dev/tty.usbmodem2101, at 115200 baud...
2023-04-30 13:58:06,346 INFO: Device Information for RadMan 2XT
2023-04-30 13:58:06,347 INFO: 	Product Name: RadMan 2XT
2023-04-30 13:58:06,347 INFO: 	Production ID: <removed>
2023-04-30 13:58:06,347 INFO: 	Serial Number: <removed>
2023-04-30 13:58:06,347 INFO: 	Device ID: <removed>
2023-04-30 13:58:06,347 INFO: 	Device Type: <removed>
2023-04-30 13:58:06,347 INFO: 	Firmware Version: <removed>
2023-04-30 13:58:06,347 INFO: 	Calibration Date: <removed>
2023-04-30 13:58:06,347 INFO: 	Calibration Due: <removed>
2023-04-30 13:58:06,347 INFO: Probe Information for RadMan 2XT
2023-04-30 13:58:06,347 INFO: 	Product Name: RadMan 2XT
2023-04-30 13:58:06,347 INFO: 	Production ID: <removed>
2023-04-30 13:58:06,347 INFO: 	Serial Number: <removed>
2023-04-30 13:58:06,347 INFO: 	Calibration Date: <removed>
2023-04-30 13:58:06,348 INFO: 	Calibration Due: <removed>
2023-04-30 13:58:06,348 INFO: 	E-Field Range: 3.0 - 60000.0 MHz
2023-04-30 13:58:06,348 INFO: 	H-Field Range: 3.0 - 1000.0 MHz
2023-04-30 13:58:06,348 INFO: 	Shaped Probe: YES
2023-04-30 13:58:06,348 INFO: 	Shaping Standard: FCC 96-326 / Occupational
2023-04-30 13:58:07,213 INFO: 2023-04-30T04:28:07.212924Z: E-Field: 0.00%, H-Field: 0.00%
2023-04-30 13:58:08,212 INFO: 2023-04-30T04:28:08.212686Z: E-Field: 0.00%, H-Field: 0.00%
2023-04-30 13:58:09,212 INFO: 2023-04-30T04:28:09.212879Z: E-Field: 48.29%, H-Field: 122.52%
2023-04-30 13:58:10,212 INFO: 2023-04-30T04:28:10.212769Z: E-Field: 73.99%, H-Field: 185.87%
2023-04-30 13:58:11,212 INFO: 2023-04-30T04:28:11.212862Z: E-Field: 73.43%, H-Field: 184.23%
2023-04-30 13:58:12,212 INFO: 2023-04-30T04:28:12.212823Z: E-Field: 60.13%, H-Field: 152.65%
```

If you know the frequency of the emitter being measured, add the `--frequency 146.0` option, replacing 146.0 with your frequency in MHz. This will result in the limit percentages being converted to E/H-field levels.

```shell
% python -m radman2 --frequency 146.0 /dev/tty.usbmodem2101
2023-04-30 13:57:49,266 INFO: Attempting to connect to RadMan2 on /dev/tty.usbmodem2101, at 115200 baud...
2023-04-30 13:58:06,346 INFO: Device Information for RadMan 2XT
2023-04-30 13:58:06,347 INFO: 	Product Name: RadMan 2XT
2023-04-30 13:58:06,347 INFO: 	Production ID: <removed>
2023-04-30 13:58:06,347 INFO: 	Serial Number: <removed>
2023-04-30 13:58:06,347 INFO: 	Device ID: <removed>
2023-04-30 13:58:06,347 INFO: 	Device Type: <removed>
2023-04-30 13:58:06,347 INFO: 	Firmware Version: <removed>
2023-04-30 13:58:06,347 INFO: 	Calibration Date: <removed>
2023-04-30 13:58:06,347 INFO: 	Calibration Due: <removed>
2023-04-30 13:58:06,347 INFO: Probe Information for RadMan 2XT
2023-04-30 13:58:06,347 INFO: 	Product Name: RadMan 2XT
2023-04-30 13:58:06,347 INFO: 	Production ID: <removed>
2023-04-30 13:58:06,347 INFO: 	Serial Number: <removed>
2023-04-30 13:58:06,347 INFO: 	Calibration Date: <removed>
2023-04-30 13:58:06,348 INFO: 	Calibration Due: <removed>
2023-04-30 13:58:06,348 INFO: 	E-Field Range: 3.0 - 60000.0 MHz
2023-04-30 13:58:06,348 INFO: 	H-Field Range: 3.0 - 1000.0 MHz
2023-04-30 13:58:06,348 INFO: 	Shaped Probe: YES
2023-04-30 13:58:06,348 INFO: 	Shaping Standard: FCC 96-326 / Occupational
2023-04-30 13:57:49,303 INFO: Using RADHAZ Standard 'FCC 96-326 Controlled Environments (Occupational)', for 146.0 MHz.
2023-04-30 13:57:49,304 INFO: Limits: 61.400 V/m, 0.163 A/m
2023-04-30 13:57:50,157 INFO: 2023-04-30T04:27:50.155045Z: E-Field: 0.000 V/m (0.00%), H-Field: 0.000 A/m (0.00%)
2023-04-30 13:57:51,160 INFO: 2023-04-30T04:27:51.155344Z: E-Field: 14.813 V/m (5.82%), H-Field: 0.066 A/m (16.48%)
2023-04-30 13:57:52,159 INFO: 2023-04-30T04:27:52.155234Z: E-Field: 51.780 V/m (71.12%), H-Field: 0.223 A/m (186.72%)
2023-04-30 13:57:53,158 INFO: 2023-04-30T04:27:53.156145Z: E-Field: 51.947 V/m (71.58%), H-Field: 0.223 A/m (187.97%)
2023-04-30 13:57:54,158 INFO: 2023-04-30T04:27:54.155295Z: E-Field: 51.824 V/m (71.24%), H-Field: 0.223 A/m (186.60%)
2023-04-30 13:57:55,158 INFO: 2023-04-30T04:27:55.155514Z: E-Field: 51.766 V/m (71.08%), H-Field: 0.222 A/m (186.17%)
```

You can also write the results to a log file by adding the `--log` option.

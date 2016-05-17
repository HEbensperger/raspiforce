# About raspiforce
The Raspberry Pi is a low cost, credit-card sized computer widely used in many educational projects. This project implements a demo kit that uses a Raspberry Pi to implement a temperature sensor and integrate with Salesforce Service Cloud to demonstrate Internet of Things (IoT) capabilities.

The project has hardware and software components involved:
* Raspberry Pi, breadboard and a set of sensors
* Python script salesforce.py for the Raspberry Pi - reads sensor data and connects to Salesforce via Rest API
* Salesforce unmanaged package raspiforce to configure demo details
 
# Hardware
The [Raspberry Pi](https://www.raspberrypi.org/) is available in different edition. This project has used the latest [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
There are many tutorials and projects available. This project is mainly based on the [Adafruit's Raspberry Pi Lesson 11. DS18B20 Temperature Sensing](https://cdn-learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing.pdf) created by Simon Monk. It uses DS18B20 temperature sensor - check out your preferred retailer.

# Python script
The Python script [salesforce.py](https://github.com/tegeling/raspiforce/blob/master/salesforce.py) contains the relevant logic to read temperature data from a sensor and create a Case record in Salesforce when a certain threshold is hit.
The script reads configuration data from a Salesforce org that has the raspiforce package installed. The configuration includes details like connection details to a Salesforce demo org, a temperature threshold, related Account, Contact records and default Asset attributes.
The script reads the configuration data dynamically during startup. This allows remote re-configuration of the device without applying changes directly in the scripts. The intention of this demo kit is to be used easily when demonstrating to different audiences.

## Configuration file
The configuration file [salesforce_login.cfg](https://github.com/tegeling/raspiforce/blob/master/salesforce_login.cfg) contains the username, password and security token of the Salesforce org, where the Raspberry Pi Demo records are stored. This is a one time configuration and statically stored in the configuration file.

## Python package simple-salesforce
Simple Salesforce is a basic Salesforce.com REST API client built for Python. The goal is to provide a very low-level interface to the REST Resource and APEX API, returning a dictionary of the API JSON response. It can be installed using pip from https://pypi.python.org/pypi/simple-salesforce.
See also details at https://github.com/heroku/simple-salesforce

# Salesforce Package raspiforce
The unmanaged package is available at https://login.salesforce.com/packaging/installPackage.apexp?p0=04t58000000Qzg3
It installs a new App Raspberry Pi Demo that contains a new custom object Raspberry Pi Demo. There should be one record maked as Active (boolean field). You can assign asset and case details for the newly created records. This makes it very reusable and easy to adopt.

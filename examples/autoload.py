from dis import COMPILER_FLAG_NAMES
import os
import sys
sys.path.insert(0,"C:\\localDev\\pyhamilton")
import json
from pyhamilton import (HamiltonInterface, LayoutManager, ResourceType, Plate96,
    INITIALIZE, COGNEX_INITIALIZE, COGNEX_AUTOLOAD,
    HamiltonError)

"""
    Helper function to make sure IP address entered in the config file is valid 
"""
def valid_ip(s):
    """
        match IPv4 with 4 decimal parts; split on dot and test that each part is an integer between 0 and 255
    """
    a = s.split(".")
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        if int(x) < 0 or int(x) > 255:
            return False
    return True

# pull the current file directory out of the path; use as reference path to layout and config files --  TODO is this the best way to do this? Should they be hard-coded? Pull from git commit?..... How do we use git in the future for running python files in pyhamilton, config, etc.
current_file_directory = os.path.dirname(os.path.abspath(__file__))

# pull out the layout file and instantiate layout manager
layfile = os.path.abspath(os.path.join( current_file_directory, 'autoload.lay'))
lmgr = LayoutManager(layfile, install=True)

if __name__ == '__main__':

    # read in cognex settings from config file
    cognex_settings_file_path = os.path.abspath(os.path.join( current_file_directory, 'cognexConfig.json'))
    cognex_file = open(cognex_settings_file_path)
    cognex_settings = json.load(cognex_file)
    cognex_file.close()

    # check for valid settings
    try:
        cognex_ip = cognex_settings["CognexIP"]
        cognex_type = cognex_settings["CognexType"]
        cognex_address =  cognex_settings["CognexAddress"]
    except Exception as e:
        print(e)
        exit()
    if not valid_ip(cognex_ip):
        exit()

    # all settings good, launch hamilton interface
    with HamiltonInterface(simulate=True) as hammy:
        print("initializing...")
        print(hammy.wait_on_response(hammy.send_command(INITIALIZE)))

        # initialize cognex
        cmd_dict = {"cognexIP": cognex_ip, "cognexType": cognex_type, "cognexAddress": cognex_address}
        id = hammy.send_command(COGNEX_INITIALIZE, **cmd_dict)
        try:
            step_return_1 = hammy.wait_on_response(id, raise_first_exception=True, return_data=True)
            scanner_id = int(step_return_1)
        except HamiltonError as he:
            print(he)
        print("cognex scanner id: ", scanner_id)

        # call autoload function
        if scanner_id > 0:  # assuming the cognex scanner is loaded successfully, the scannerID will be non-zero
            # autoload input: scannerID, carrierName
            carrier_name = "PlateCarrier_1" # TODO pull this from the layfile??
            carrier_barcode = "********"
            cmd_dict = {"carrierName": carrier_name, "scannerID": str(scanner_id)}
            try:
                id = hammy.send_command(COGNEX_AUTOLOAD, **cmd_dict)
                step_return_1 = hammy.wait_on_response(id, raise_first_exception=False, return_data=False)
            except HamiltonError as he:
                print(he)
                exit()

            scanned_barcodes = step_return_1.split(";")
            for s in scanned_barcodes:
                print(scanned_barcodes)

    print("done")

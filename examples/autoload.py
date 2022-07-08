import os
import json
import sys
sys.path.insert(0,"C:\\localDev\\pyhamilton")
from pyhamilton import (HamiltonInterface, LayoutManager, ResourceType, Plate96,
    INITIALIZE, COGNEX_INITIALIZE, COGNEX_AUTOLOAD,
    HamiltonError)

current_file_directory = os.path.dirname(os.path.abspath(__file__))
layfile = os.path.abspath(os.path.join( current_file_directory, 'autoload.lay'))
lmgr = LayoutManager(layfile, install=True)

if __name__ == '__main__':
    with HamiltonInterface(simulate=True) as hammy:
        print("initializing...")
        print(hammy.wait_on_response(hammy.send_command(INITIALIZE)))

        # default cognex settings
        cognex_ip = ""
        cognex_type = "DM70"  # "Unknown (probably DM260)"  # default
        cognex_address = "COM5"  # default 

        # TODO read cognex settings from config file
        
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
                step_return_1 = hammy.wait_on_response(hammy.send_command(COGNEX_AUTOLOAD, **cmd_dict), raise_first_exception=True, return_data=True)
            except HamiltonError as he:
                print(he)

            scanned_barcodes = step_return_1.split(";")
            for s in scanned_barcodes:
                print(scanned_barcodes)
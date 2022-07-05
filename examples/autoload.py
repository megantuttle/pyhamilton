import os
import sys
sys.path.insert(0,"C:\\localDev\\pyhamilton")
from pyhamilton import (HamiltonInterface, LayoutManager, ResourceType, Plate96,
    INITIALIZE, COGNEX_INITIALIZE,
    HamiltonError)

current_file_directory = os.path.dirname(os.path.abspath(__file__))
layfile = os.path.abspath(os.path.join( current_file_directory, 'autoload.lay'))
lmgr = LayoutManager(layfile)

if __name__ == '__main__':
    with HamiltonInterface(simulate=True) as hammy:
        print('INITIALIZED!!', hammy.wait_on_response(hammy.send_command(INITIALIZE)))

        # default cognex settings
        cognexIP = ""
        cognexType = "Unknown (probably DM260)"  # default
        cognexAddress = "COM5"  # default 

        # TODO read cognex settings from config file
        
        # initialize cognex
        cmd_dict = {"cognexIP": cognexIP, "cognexType": cognexType, "cognexAddress": cognexAddress}
        id = hammy.send_command(COGNEX_INITIALIZE, **cmd_dict)
        try:
            print(hammy.wait_on_response(id, raise_first_exception=True))
        except HamiltonError as he:
            print(he)
        print("cognex initialized!!!!")

        # call autoload function

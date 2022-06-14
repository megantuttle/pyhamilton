import os
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
        cognexType = "" # default: "Unknown (probably DM260)"
        cognexAddress = "" # default should be COM5

        # TODO read cognex settings from config file
        
        # initialize cognex
        cmd_dict = {"cognexIP": cognexIP, "cognexType": cognexType, "cognexAddress": cognexAddress}
        id = hammy.wait_on_response(hammy.send_command(COGNEX_INITIALIZE, **cmd_dict))
        print(hammy.wait_on_response(id, raise_first_exception=True))
        

        # call autoload function

#!python3

import os
from pyhamilton import (HamiltonInterface, LayoutManager, ResourceType, Tip96, Plate96,
    INITIALIZE, PICKUP, EJECT, ASPIRATE, DISPENSE,
    HamiltonError)

current_file_directory = os.path.dirname(os.path.abspath(__file__))
layfile = os.path.abspath(os.path.join(current_file_directory, 'single_ch_aspirate_dispense.lay'))
lmgr = LayoutManager(layfile)

tip_name_from_line = lambda line: LayoutManager.layline_first_field(line)
tip_name_condition = lambda line: LayoutManager.field_starts_with(tip_name_from_line(line), 'HTF_L_')
tips_type = ResourceType(Tip96, tip_name_condition, tip_name_from_line)
tips = lmgr.assign_unused_resource(tips_type)

plate_type = ResourceType(Plate96, 'Cos_96_Rd_0001')
plate = lmgr.assign_unused_resource(plate_type)

if __name__ == '__main__':
    tip_no = 88 # top right corner
    well_no = 7 # bottom left corner
    tip_labware_pos = tips.layout_name() + ', ' + tips.position_id(tip_no) + ';'
    well_labware_pos = plate.layout_name() + ', ' + plate.position_id(well_no) + ';'
    liq_class = 'HighVolumeFilter_Water_DispenseJet_Empty'
    with HamiltonInterface(simulate=True) as hammy:
        hammy.wait_on_response(hammy.send_command(INITIALIZE))
        ids = [hammy.send_command(PICKUP, labwarePositions=tip_labware_pos),
               hammy.send_command(ASPIRATE, labwarePositions=well_labware_pos, volumes=100.0, liquidClass=liq_class),
               hammy.send_command(DISPENSE, labwarePositions=well_labware_pos, volumes=100.0, liquidClass=liq_class),
               hammy.send_command(EJECT, labwarePositions=tip_labware_pos)]
        for id in ids:
            try:
                print(hammy.wait_on_response(id, raise_first_exception=True))
            except HamiltonError as he:
                print(he)

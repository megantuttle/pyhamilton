#!python3

import os
from pyhamilton import (HamiltonInterface, LayoutManager, ResourceType, Tip96, Plate96, INITIALIZE, PICKUP, EJECT, ASPIRATE, DISPENSE, HamiltonError)

# define layout file
layfile = os.path.abspath('C:\localDev\pyhamilton\examples\met82_2ndPcrAmp_simple\MetaMethod-ML_STAR.lay')
lmgr = LayoutManager(layfile)

# define labware
## tips
fifty_ul_tips_type_1 = ResourceType(Tip96, 'TIP_50ulF_L_Adaptive_0001')
fifty_ul_tips_1 = lmgr.assign_unused_resource(fifty_ul_tips_type_1)
fifty_ul_tips_type_2 = ResourceType(Tip96, 'TIP_50ulF_L_Adaptive_0002')
fifty_ul_tips_2 = lmgr.assign_unused_resource(fifty_ul_tips_type_2)
three_hundred_ul_tips_type = ResourceType(Tip96, 'STF_L_Adaptive_0001')
three_hundred_ul_tips = lmgr.assign_unused_resource(three_hundred_ul_tips_type)
## plates
primer_plate_type = ResourceType(Plate96, 'PrimerPlate_1')
primer_plate = lmgr.assign_unused_resource(primer_plate_type)
tailing_plate_type = ResourceType(Plate96, 'TailingPlate_1')
tailing_plate = lmgr.assign_unused_resource(tailing_plate_type) #destination
sample_plate_type = ResourceType(Plate96, 'DilutionPlate_1')
sample_plate = lmgr.assign_unused_resource(sample_plate_type)
## mastermix
mastermix_type = ResourceType(Plate96, 'MasterMix_1')
mastermix = lmgr.assign_unused_resource(mastermix_type)

# define 1-channel MM transfer -- tips
big_tip_no = 0
big_tip_labware_pos = three_hundred_ul_tips.layout_name() + ', ' + three_hundred_ul_tips.position_id(big_tip_no) + ';'

# define 1-channel ASP tranfer from MM -- wells
mm_asp_well_pos = mastermix.layout_name() + ', ' + '1;'

# define 1-channel DISP transfer MM to tailing plate
tailing_well_labware_pos_array_1channel = []
for i in range(0,96):
    tailing_well_labware_pos = tailing_plate.layout_name() + ', ' + tailing_plate.position_id(i) + ';'
    print(tailing_well_labware_pos)
    tailing_well_labware_pos_array_1channel.append(tailing_well_labware_pos)

# define 8-channel PRIMER transfer -- tips
fifty_ul_tip_labware_pos_array_1 = []
for i in range(0,96,8):
    fifty_ul_tip_labware_pos_1 = ';'.join((fifty_ul_tips_1.layout_name() + ', ' + fifty_ul_tips_1.position_id(tip_no) for tip_no in range(i, i+8)))
    print(str(i) + ": "+ fifty_ul_tip_labware_pos_1)
    fifty_ul_tip_labware_pos_array_1.append(fifty_ul_tip_labware_pos_1)

# define 8-channel ASP transfer from PRIMER plate -- wells
primer_well_labware_pos_array = []
for i in range(0,96,8):
    primer_well_labware_pos = ';'.join((primer_plate.layout_name() + ', ' + primer_plate.position_id(well_no) for well_no in range(i, i+8)))
    print(str(i)+": "+primer_well_labware_pos)
    primer_well_labware_pos_array.append(primer_well_labware_pos)

# define 8-channel SAMPLE transfer -- tips
fifty_ul_tip_labware_pos_array_2 = []
for i in range(0,96,8):
    fifty_ul_tip_labware_pos_2 = ';'.join((fifty_ul_tips_2.layout_name() + ', ' + fifty_ul_tips_2.position_id(tip_no) for tip_no in range(i, i+8)))
    print(str(i) + ": "+ fifty_ul_tip_labware_pos_2)
    fifty_ul_tip_labware_pos_array_2.append(fifty_ul_tip_labware_pos_2)

# define 8-channel ASP transfer from SAMPLE plate -- wells
sample_well_labware_pos_array = []
for i in range(0,96,8):
    sample_well_labware_pos = ';'.join((sample_plate.layout_name() + ', ' + sample_plate.position_id(well_no) for well_no in range(i, i+8)))
    print(str(i)+": "+sample_well_labware_pos)
    sample_well_labware_pos_array.append(sample_well_labware_pos)

# define 8-channel DISP transfer to TAILING(dest) plate -- wells
tailing_well_labware_pos_array_8channel = []
for i in range(0,96,8):
    tailing_well_labware_pos = ';'.join((tailing_plate.layout_name() + ', ' + tailing_plate.position_id(well_no) for well_no in range(i, i+8)))
    print(str(i)+": "+tailing_well_labware_pos)
    tailing_well_labware_pos_array_8channel.append(tailing_well_labware_pos)

# define liquid classes
mm_liq_class = '1RXN_pcr2setup_MM_300F_SurfaceEmpty'
primer_liq_class = '1RXN_pcr2setup_Primer_50F_96COREHead_SurfaceEmpty'
sample_liq_class = '1RXN_pcr2setup_Sample_50F_96COREHead_SurfaceEmpty'

# main method
if __name__ == '__main__':
    """
    1. Pickup a 300uL tip on one channel
    2. Pipette 17uL mastermix into each well of the tailing(dest) plate
    3. Dispose of that tip
    4. Pickup 50uL tips on 8 channels
    5. Pipette 4uL primer into 8 wells of the tailing(dest) plate
    6. Dispose of those tips
    7. Repeat 4-6 until all wells of tailing(dest) plate have received primer    
    8. Pickup 50uL tips on 8 channels
    9. Pipette 4uL diluted 1st pcr sample from dilution plate into 8 wells of the tailing(dest) plate
    10. Dispose of those tips
    11. Repeat 8-10 until all wells of tailing(dest) plate have received diluted 1st pcr sample
    
    Done!

    """
    # call up hamilton interface to build+execute commands
    with HamiltonInterface(simulate=True) as hammy:
        # initialize
        hammy.wait_on_response(hammy.send_command(INITIALIZE))

        # build list of commands
        ## step 1
        ids = [hammy.send_command(PICKUP, labwarePositions=big_tip_labware_pos)]
        
        ## step 2 -- MM transfer
        for well_pos in tailing_well_labware_pos_array_1channel:
            ids.append(hammy.send_command(ASPIRATE, labwarePositions=mm_asp_well_pos, volumes=17.0, liquidClass=mm_liq_class))
            ids.append(hammy.send_command(DISPENSE, labwarePositions=well_pos, volumes=17.0, liquidClass=mm_liq_class))
    
        ## step 3
        ids.append(hammy.send_command(EJECT, labwarePositions=big_tip_labware_pos)) ## TODO eject to waste

        ## step 4-6 -- primer transfer
        for n in range(len(tailing_well_labware_pos_array_8channel)):
            ids.append(hammy.send_command(PICKUP, labwarePositions=fifty_ul_tip_labware_pos_array_1[n]))
            ids.append(hammy.send_command(ASPIRATE, labwarePositions=primer_well_labware_pos_array[n], volumes=4.0, liquidClass=primer_liq_class))
            ids.append(hammy.send_command(DISPENSE, labwarePositions=tailing_well_labware_pos_array_8channel[n], volumes=4.0, liquidClass=primer_liq_class))
            ids.append(hammy.send_command(EJECT, labwarePositions=fifty_ul_tip_labware_pos_array_1[n])) ## TODO eject to waste
            
        # step 8-10 -- sample transfer
        for n in range(len(tailing_well_labware_pos_array_8channel)):
            ids.append(hammy.send_command(PICKUP, labwarePositions=fifty_ul_tip_labware_pos_array_2[n]))
            ids.append(hammy.send_command(ASPIRATE, labwarePositions=sample_well_labware_pos_array[n], volumes=4.0, liquidClass=sample_liq_class))
            ids.append(hammy.send_command(DISPENSE, labwarePositions=tailing_well_labware_pos_array_8channel[n], volumes=4.0, liquidClass=sample_liq_class))
            ids.append(hammy.send_command(EJECT, labwarePositions=fifty_ul_tip_labware_pos_array_2[n])) ## TODO eject to waste

        # -- EXECUTE! --
        for id in ids:
            try:
                print(hammy.wait_on_response(id, raise_first_exception=True))
            except HamiltonError as he:
                print(he)


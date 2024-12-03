import cadquery as cq
from cqindustry.dome import Dome, greeble

bp_0 = greeble.CutKeyPentagon()
bp_0.text='0'

bp_1 = greeble.CutKeyHexagon()
bp_1.text='1'
bp_2 = greeble.CutKeyHexagon()
bp_2.text='2'
bp_3 = greeble.CutKeyHexagon()
bp_3.text='3'
bp_4 = greeble.CutKeyHexagon()
bp_4.text='4'
bp_5 = greeble.CutKeyHexagon()
bp_5.text='5'

bp_6 = greeble.CutKeyPentagon()
bp_6.text='6'
bp_7 = greeble.CutKeyHexagon()
bp_7.text='7'
bp_8 = greeble.CutKeyPentagon()
bp_8.text='8'
bp_9 = greeble.CutKeyHexagon()
bp_9.text='9'
bp_10 = greeble.CutKeyPentagon()
bp_10.text='10'
bp_11 = greeble.CutKeyHexagon()
bp_11.text='11'
bp_12 = greeble.CutKeyPentagon()
bp_12.text='12'
bp_13 = greeble.CutKeyHexagon()
bp_13.text='13'
bp_14 = greeble.CutKeyPentagon()
bp_14.text='14'
bp_15 = greeble.CutKeyHexagon()
bp_15.text='15'

#test_bp_2.text_height=10
vent_bp = greeble.VentHexagon()
door_bp = greeble.DoorHexagon()
door_bp.hinge_x_translate = -4.5

bp = Dome()
#bp.render_cut_keys = False
#bp.r1_greeble = []
#bp.r2_greeble_hex = [1,2]

#center
bp.greebles_bp.append(bp_0)

#ring 1
bp.greebles_bp.append(bp_1)
bp.greebles_bp.append(bp_2)
bp.greebles_bp.append(bp_3)
bp.greebles_bp.append(bp_4)
bp.greebles_bp.append(bp_5)

#ring2
bp.greebles_bp.append(bp_6)
bp.greebles_bp.append(bp_7)
bp.greebles_bp.append(bp_8)
bp.greebles_bp.append(bp_9)
bp.greebles_bp.append(bp_10)
bp.greebles_bp.append(bp_11)
bp.greebles_bp.append(bp_12)
bp.greebles_bp.append(bp_13)
bp.greebles_bp.append(bp_14)
bp.greebles_bp.append(bp_15)


bp.make()
#door_bp.parent=None
#door_bp.make()
dome = bp.build()
#show_object(dome)

cq.exporters.export(dome, "./stl/dome_v3_test_numbered.stl")
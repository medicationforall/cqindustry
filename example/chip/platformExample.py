# whatever you do.... DO NOT RENAME this file to platform.py
# There are machinations at play in which man is not entitled to understand.
import cadquery as cq
from cqindustry.chip import Platform

# ---- Platform

bp = Platform()
bp.length = 150
bp.stripe_width = 5
bp.height = 4
bp.render_stripes = True
bp.stripe_padding = .3
bp.make()
platform = bp.build()

#show_object(platform)
cq.exporters.export(platform,'./stl/platform.stl')

# ---- Platform Alt

bp = Platform()
bp.length = 150
bp.stripe_width = 5
bp.corner_chamfer = 30
bp.height = 4
bp.bar_width = 10
bp.render_stripes = True
bp.stripe_padding = .3
bp.make()
platform = bp.build()

cq.exporters.export(platform,'./stl/platform_alt.stl')

# ---- Platform Basic

bp = Platform()
bp.length = 150
bp.width = 75
bp.stripe_width = 5
bp.height = 4
bp.render_stripes = True
bp.stripe_padding = .3
bp.corner_chamfer = 0
bp.render_ladders = False
bp.render_center_cut = False
bp.make()
platform = bp.build()

#show_object(platform)
cq.exporters.export(platform,'./stl/platform_basic.stl')

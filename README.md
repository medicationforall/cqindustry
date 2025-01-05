# cqindustry
Python library for making 3d printable Industrial terrain using cadquery.

---

## Can Tower

[![](./documentation/image/cantower/05.png)](documentation/can.md)<br /><br />

``` python
import cadquery as cq
from cqindustry.can import CanTower

bp_can_tower = CanTower()
bp_can_tower.render_can = False
bp_can_tower.can_height = 122
bp_can_tower.can_diameter = 66
bp_can_tower.cut_padding = .5
bp_can_tower.ring_width = 4.5
bp_can_tower.platform_height = 20
bp_can_tower.platform_ladder_extends = 10
bp_can_tower.make()
can_tower = bp_can_tower.build()

show_object(can_tower.translate((0,0,0)))
```

* [Example](./example/can/can_tower.py)
* [stl](./stl/can_tower.stl)

---

## Chip Tower

[![](./documentation/image/04.png)](documentation/chip.md)<br /><br />

``` python
import cadquery as cq
from cqindustry import ChipTower

bp_tower = ChipTower()
bp_tower.stories = 3
bp_tower.story_height = 75

bp_platform = bp_tower.bp_platform
bp_platform.render_floor = True

bp_tower.make()
tower_ex = bp_tower.build()

show_object(tower_ex)
```

* [Example](./example/chip/chiptower_readme_example.py)
* [stl](./stl/chip_readme_example.stl)

---

## Container

[![](./documentation/image/container/35.png)](documentation/container.md)<br /><br />

``` python
import cadquery as cq
from cqindustry.container import Container

bp_container = Container()
bp_container.bp_hinge.rotate_deg = -90

bp_container.make()

result = bp_container.build()
show_object(result)
```

* [Example](./example/container/container.py)
* [stl](./stl/container.stl)

---

## Dome

[![](./documentation/image/dome/cover.png)](documentation/dome.md)<br /><br />

``` python
import cadquery as cq
from cqindustry.dome import Dome, greeble

#init greebles
vent_bp = greeble.VentHexagon()
door_bp = greeble.DoorHexagon()
door_bp.hinge_x_translate = -4.5

window_pen_bp = greeble.WindowFrame()
window_pen_bp.type="pentagon"
window_pen_bp.margin=.1
window_pen_bp.render_pane = False

window_hex_bp = greeble.WindowFrame()
window_hex_bp.type="hexagon"
window_hex_bp.render_pane = False

# make dome
bp = Dome()

#center
bp.greebles_bp.append(window_pen_bp)

#ring 1
bp.greebles_bp.append(vent_bp)
bp.greebles_bp.append(window_hex_bp)
bp.greebles_bp.append(window_hex_bp)
bp.greebles_bp.append(window_hex_bp)
bp.greebles_bp.append(window_hex_bp)

#ring2
bp.greebles_bp.append(window_pen_bp)
bp.greebles_bp.append(window_hex_bp)
bp.greebles_bp.append(window_pen_bp)
bp.greebles_bp.append(window_hex_bp)
bp.greebles_bp.append(window_pen_bp)
bp.greebles_bp.append(door_bp)
bp.greebles_bp.append(window_pen_bp)
bp.greebles_bp.append(window_hex_bp)
bp.greebles_bp.append(window_pen_bp)
bp.greebles_bp.append(door_bp)

bp.render_greebles = True
bp.make()
dome = bp.build()

show_object(dome)
```

* [Example](./example/dome/dome.py)
* [stl](./stl/dome_complete.stl)

---

## Portal
[![](./documentation/image/portal/cover.png)](documentation/portal.md)<br /><br />

``` python
import cadquery as cq
from cqindustry.portal import Portal

bp_portal = Portal()
bp_portal.bp_frame.length = 150
bp_portal.bp_frame.width = 30
bp_portal.bp_frame.height = 150

bp_portal.render_base = False
bp_portal.render_hinges = True
bp_portal.bp_ramp.width = 10
bp_portal.make()


result_open = bp_portal.build()
show_object(result_open)
```

* [Example](./example/portal/portal.py)
* [stl](stl/portal_open.stl)

---

## Power Station

[![](./documentation/image/power/cover.png)](documentation/power.md)<br /><br />

``` python
import cadquery as cq
from cqspoolterrain import PowerStation, SpoolCladdingGreebled

bp_power = PowerStation()
bp_power.bp_cladding = SpoolCladdingGreebled()
bp_power.bp_cladding.seed="morePower!"
bp_power.make()
power = bp_power.build()
#show_object(power)
cq.exporters.export(power,f"stl/powerStation_seed_{bp_power.bp_cladding.seed}.stl")
```

* [Example](./example/power/powerstationGreebled.py)
* [stl](stl/powerStation_seed_morePower!.stl)

---


## Project Documention
* [Documentation](documentation/documentation.md)
	* [Can](documentation/can.md)
	* [Chip](documentation/chip.md)
    * [Container](documentation/container.md)
	* [Dome](documentation/dome.md)
    * [Portal](documentation/portal.md)
	* [Power](documentation/power.md)


## Changes
* [Changelog](./changes.md)

## Dependencies
* [cqterrain](https://github.com/medicationforall/cqterrain)

---

## 3d Printed Projects
* [Chip Tower](https://miniforall.com/chiptower)
* [Dome Terrain](https://miniforall.com/dometerrain)
* [Portal](https://miniforall.com/portal)
* [Power Station](https://miniforall.com/powerstation)
* [Shipping Container Terrain](https://miniforall.com/shippingcontainer)

---

### Installation
To install cqindustry directly from GitHub, run the following `pip` command:

	pip install git+https://github.com/medicationforall/cqindustry

**OR**

### Local Installation
From the cloned cqindustry directory run.

	pip install ./

---

## Running Example Scripts
[example_runner.py](example_runner.py) runs all examples.

``` bash
C:\Users\<user>\home\3d\cqindustry>python example_runner.py
```

**OR**

### Running individual examples
* From the root of the project run one of the example scripts:
  
``` bash
C:\Users\<user>\home\3d\cqindustry>python ./example/ring.py
```

---



# CQIndustry changelog

## Main wip

## 2.4.0
* Upped cqterrain version to 3.4.1
* Cleaned up instances where I was setting the callback parameter for workplane.eachpoint invocations.
  * https://github.com/CadQuery/cadquery/issues/1395
* Documentatd a bug in chiptower when using the conduit ring type.
  * This is a regression issue from going to the new version of cadquery.
* Changed from using assembly.save (deprecated) to assembly.export
* Fixed dome imports for examples  


## 2.3.0
* Upped cqterrain version to 2.5.0
* Moved cqportal portal code over into cqindustry
* Moved cqportal container code over into cqindustry
* Updated README.md

## 2.2.0
* Upped cqterrain version to 2.1.0
  * This includes spool code
* Moved power station code over into cqindustry

## 2.1.0
* Moved dome code over into cqindustry
* Fix README.md example path

## 2.0.1
* Upped cqterrain version to 2.0.2

## 2.0.0
* Moved code, examples, and documentation around to new packages
  * barrier
  * chip
  * can
  * walkway
* Added annotations to Barrier
* Documented can package
* chip Platform added ladder_width property
* moved Barrier code into cqterrain
* moved walkway code into cqterrain
  
## 1.1.1
* Upped cqterrain version to 1.1.1
* Added intial bridge module

## 1.1.0
* Added soda can tower variant
  * Added CanTower (orchestrator class)
  * Added CanPlatform
  * Added CanRail
  * Added can_tower example
  * Added can_platform example
  * Added can_rail example
  * Added can_tower_set example

## 1.0.3
* Upped cqterrain version to 1.0.3

## 1.0.2
* Upped cqterrain version to 1.0.2

## 1.0.1
* Upped cqterrain version to 1.0.1

## 1.0.0
* Type Annotations
* Upped cqterrain version to 1.0.0
  * Fixed barrier_greebled example
  * Fixed walkway tiled example
* Added example_runner.py
* Added License blocks
* Added GuardRail, with examples
* Added ChipCan
* Added ChipTower and example
* Added RingConduit
* Platform changed how some of the render flags work. 
  * On make the ladder cut and center cut are still made
  * the cut components are just not applied on build if the flags are turned off
* Documentation
* Updated README.md

## 0.1.1
* Upped cqterrain version to 0.3.3

## 0.1.0
* Upped cqterrain version to 0.3.0
* Removed local Base class and instead resolve Base from cadqueryhelper
* Ring build unions the ladders.
* Platform build unions the stripes; also fixed a a syntax bug.
* Walkway build unions
  * rails.
  * irregular grid.
  * tile grid
* Added irregular grid walkway example
* Added tile walkway example

## 0.0.8
* Upped cqterrain version to 0.2.0

## 0.0.7
* Fixed barrier magnet placement bug
* Added z_lift property to barrier cut magnets.

## 0.0.6
* Upped cqterrain version to 0.1.8
* Made platform corner_chamfer optional
* Updated platform example
  * Added new platform stl
* Updated README.md 

## 0.0.5
* Made the platform center cut optional
* Updated README.md

## 0.0.4
* Fix that which lives in the basement, and was causing all of the example files to break.
  * Circular dependency issue from the 5th ring of hell.

## 0.0.3
* Added support to render only the left or right rail on the walkway.
* Updated Dependencies

## 0.0.2
* Upped cadqueryhelper dependency version
* Upped cqterrain dependency version
* Walkway added irregular grid support
* Walkway added grid support
* Added Initial Barrier Design
* Updated the license

## 0.0.1
* Initial release
* chip tube platform code
  * ring code
* walkway code

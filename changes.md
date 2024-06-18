# CQIndustry changelog

## Main wip

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

.. _Coordinate Systems:

Coordinate Systems
==================

`AutoLISP Reference to Coordinate Systems <http://help.autodesk.com/view/OARX/2018/ENU/?guid=GUID-0F0B833D-78ED-4491-9918-9481793ED10B>`_
provided by Autodesk.

To brush up you knowledge about vectors, watch the YouTube tutorials of
`3Blue1Brown`_ about `Linear Algebra`_.

.. _WCS:

WCS
---

World coordinate system - the reference coordinate system. All other coordinate
systems are defined relative to the WCS, which never changes. Values measured
relative to the WCS are stable across changes to other coordinate systems.

.. _UCS:

UCS
---

User coordinate system - the working coordinate system defined by the user to
make drawing tasks easier. All points passed to AutoCAD commands, including those
returned from AutoLISP routines and external functions, are points in the
current UCS. As far as I know, all coordinates stored in DXF files are always
WCS or OCS never UCS.

User defined coordinate systems are not just helpful for interactive CAD,
therefore `ezdxf` provides a converter class :class:`~ezdxf.math.UCS` to translate
coordinates from UCS into WCS and vice versa, but always remember: store only
WCS or OCS coordinates in DXF files, because there is no method to determine
which UCS was active or used to create UCS coordinates.

.. seealso::

    - Table entry :class:`UCS`
    - :class:`ezdxf.math.UCS` - converter between WCS and UCS

.. _OCS:

OCS
---

Object coordinate system  are coordinates relative to the object itself.
The main goal of OCS is to place 2D elements in 3D space and the OCS is defined
by the extrusion vector of the entity.
As long the extrusion vector is (0, 0, 1) (the WCS z-axis) the OCS is coincident
to the WCS, which means the OCS coordinates are equal to the WCS coordinates,
most of the time this is true for 2D entities.

OCS entities: ARC, CIRCLE, TEXT, LWPOLYLINE, HATCH, SOLID, TRACE, INSERT, IMAGE

Because `ezdxf` is just an interface to DXF, it does not automatically convert
OCS into WCS, this is the domain of the user/application. These lines convert
the center of a 3D circle from OCS to WCS::

    ocs = circle.ocs()
    wcs_center = ocs.to_wcs(circle.dxf.center)


.. seealso::

    - :ref:`Object Coordinate System` - deeper insights into OCS
    - :class:`ezdxf.math.OCS` - converter between WCS and OCS

.. _DCS:

DCS
---

Display coordinate system - the coordinate system into which objects are
transformed before they are displayed. The origin of the DCS is the point
stored in the AutoCAD system variable TARGET, and its z-axis is the viewing
direction. In other words, a viewport is always a plan view of its DCS. These
coordinates can be used to determine where something will be displayed to the
AutoCAD user. `Ezdxf` does not use or support DCS in any way.


.. _Linear Algebra: https://www.youtube.com/watch?v=kjBOesZCoqc&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab
.. _3Blue1Brown: https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw

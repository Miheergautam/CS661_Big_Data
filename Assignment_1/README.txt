CS661 Assignment 1 - Isocontour and Volume Visualization
=====================================================

This repository contains implementations for 2D isocontour extraction and 3D volume rendering using VTK.

Prerequisites
------------
- Python 3.x
- VTK library

Installation
------------
Install the required VTK library using pip:
    pip install vtk

Directory Structure
-----------------
.
├── isocontour.py          # 2D isocontour extraction implementation
├── volume_render.py       # 3D volume rendering implementation
├── Data/
│   ├── Isabel_2D.vti     # 2D dataset for isocontour
│   └── Isabel_3D.vti     # 3D dataset for volume rendering
├── contour_output.vtp     # Generated isocontour output
└── README.txt            

Running the Programs
------------------

1. Isocontour Extraction (Question 1)
------------------------------------
Command:
    python isocontour.py

Usage:
- When prompted, enter an isovalue between -1438 and 630
- The program will:
  * Generate the isocontour
  * Display the visualization
  * Save the result as 'contour_output.vtp'
- The visualization window can be interacted with using:
  * Left mouse button: Rotate
  * Mouse wheel: Scroll to control zoom


2. Volume Rendering (Question 2)
-------------------------------
Command:
    python volume_render.py

Usage:
- When prompted, enter:
  * 'y' to enable Phong shading
  * 'n' to disable Phong shading
- The program will:
  * Apply the specified transfer functions
  * Display the volume rendering
- The visualization window can be interacted with using:
  * Left mouse button: Rotate
  * Mouse wheel: Scroll to control zoom

Output Files
-----------
- Isocontour output: 'contour_output.vtp'
  * Can be visualized using ParaView
  * Located in the same directory as the scripts

Troubleshooting
--------------
1. If you encounter "File not found" errors:
   - Ensure the Data directory contains both .vti files
   - Check that you're running the scripts from the correct directory

2. If visualization doesn't appear:
   - Verify VTK installation: python -c "import vtk; print(vtk.vtkVersion().GetVTKVersion())"

3. If performance is slow:
   - For volume rendering, try running without Phong shading

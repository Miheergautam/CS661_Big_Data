Steps to Run Isocontour and Volume Rendering Programs

PREREQUISITES
Ensure you have Python installed with the following libraries:
- vtk

Install VTK using:
pip install vtk

DIRECTORY STRUCTURE
.
├── isocontour.py
├── volume_rendering.py
├── Data
│   └── Isabel_2D.vti (for isocontour)
│   └── Isabel_3D.vti (for volume rendering)
└── contour_output.vtp (generated automatically)

RUNNING THE PROGRAMS

1. Run isocontour.py
This script generates an isocontour from the 2D dataset and saves the result in the output_isocontours directory.

Steps:
python isocontour.py

- Enter the requested iso value when prompted.
- The isocontour will be displayed and saved as a .vtp file in the  same directory.

Output File Location:
contour_output.vtp

2. Run vtk_volume_rendering.py
This script renders the 3D volume from the dataset.

Steps:
python volume_rendering.py

- Enter 'y' or 'n' when prompted to enable or disable Phong shading.
- The volume rendering window will open for visualization.
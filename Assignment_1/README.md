# Steps to Run Isocontour and Volume Rendering Programs

## Prerequisites
Ensure you have Python installed with the following libraries:
- `vtk`

Install VTK using:
```bash
pip install vtk
```

## Directory Structure
```
.
├── isocontour.py
├── volume_rendering.py
├── Data
│   └── Isabel_2D.vti (for isocontour)
│   └── Isabel_3D.vti (for volume rendering)
└── output_isocontours (generated automatically)
```

## Running the Programs

### 1. Run `isocontour.py`
This script generates an isocontour from the 2D dataset and saves the result in the `output_isocontours` directory.

**Steps:**
```bash
python isocontour.py
```

- Enter the requested iso value when prompted.
- The isocontour will be displayed and saved as a `.vtp` file in the `output_isocontours` directory.

**Output File Location:**
```
output_isocontours/isocontour_<iso_value>.vtp
```

### 2. Run `volume_rendering.py`
This script renders the 3D volume from the dataset.

**Steps:**
```bash
python volume_rendering.py
```
- Enter `y` or `n` when prompted to enable or disable Phong shading.
- The volume rendering window will open for visualization.
# CS661 - Assignment 3: Streamline Visualization Using RK4 Integration

## Team Members
- Devashish Nagpal (EXY24018)
- Miheer Gautam (EXY24022)

## How to Run the Code

1. Ensure you have Python installed on your system along with the required VTK library. You can install VTK using the following command:
    ```bash
    pip install vtk
    ```

2. Ensure the `tornado3d_vector.vti` dataset is in the same directory as `solution.py`.

3. Run the script using the command:
    ```bash
    python solution.py
    ```
4. When prompted, enter the 3D seed location (x, y, z) for the streamline generation. This may take a little while on different systems so kindly wait for the prompt.

5. The generated streamline will be saved as `rk4_streamline.vtp` in the same directory.

## Explanation of the Code

The code implements streamline visualization using the Runge-Kutta 4th order (RK4) integration method. Below is a brief explanation of the key components:

1. **Dataset Loading**: The `vtkXMLImageDataReader` is used to load the `tornado3d_vector.vti` dataset, which contains vector field data.

2. **Seed Input**: The user is prompted to input a 3D seed point, which serves as the starting point for the streamline.

3. **Streamline Tracing**: The `trace_streamline` function computes the streamline using RK4 integration. It traces the streamline in both forward and backward directions from the seed point, ensuring it stays within the dataset bounds.

4. **RK4 Integration**: The `rk4_step` function performs a single RK4 step to compute the next position along the streamline based on the vector field.

5. **Streamline Saving**: The computed streamline is saved as a `.vtp` file using VTK's `vtkXMLPolyDataWriter`. This file can be visualized using tools like ParaView.

This implementation provides an interactive way to explore vector fields and visualize streamlines effectively.

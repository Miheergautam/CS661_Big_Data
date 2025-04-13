import vtk
from vtk.util.numpy_support import vtk_to_numpy


def get_vector_at_position(probe_filter, position):
    """Interpolate the vector at the given 3D position using vtkProbeFilter."""
    
    # Create a vtkPoints object to hold the position
    points = vtk.vtkPoints()
    points.InsertNextPoint(position)

    # Create a vtkPolyData object to hold the points
    sample = vtk.vtkPolyData()
    sample.SetPoints(points)

    # Set the input for the probe filter
    probe_filter.SetInputData(sample)
    probe_filter.Update()

    # Get the output of the probe filter
    result = probe_filter.GetOutput()
    vectors = result.GetPointData().GetVectors()

    # Check if the vectors are valid and return the first vector
    return vtk_to_numpy(vectors)[0] if vectors and vectors.GetNumberOfTuples() > 0 else None

def rk4_step(probe_filter, current_pos, step_size):
    """Perform a single Runge-Kutta 4th order integration step."""

    # Get vector at the current position
    v1 = get_vector_at_position(probe_filter, current_pos)
    if v1 is None:
        return None

    # Compute intermediate positions and vectors
    p2 = [p + 0.5 * step_size * v for p, v in zip(current_pos, v1)]
    v2 = get_vector_at_position(probe_filter, p2)
    if v2 is None:
        return None

    p3 = [p + 0.5 * step_size * v for p, v in zip(current_pos, v2)]
    v3 = get_vector_at_position(probe_filter, p3)
    if v3 is None:
        return None

    p4 = [p + step_size * v for p, v in zip(current_pos, v3)]
    v4 = get_vector_at_position(probe_filter, p4)
    if v4 is None:
        return None

    # Compute the next position using RK4 formula
    next_pos = [
        p + (step_size / 6.0) * (v1[i] + 2 * v2[i] + 2 * v3[i] + v4[i])
        for i, p in enumerate(current_pos)
    ]
    return next_pos

def is_inside_bounds(pos, bounds):
    """Check whether a point lies within the dataset bounds."""
    return all(bounds[i] <= pos[i//2] <= bounds[i+1] for i in range(0, 6, 2))

def trace_streamline(seed, probe_filter, bounds, step=0.05, max_steps=1000):
    """Trace streamline using RK4 from a seed point in both directions."""
    streamline = [seed[:]]  # Initialize streamline with the seed point

    # Forward direction tracing
    pos = seed[:]
    for _ in range(max_steps):
        pos = rk4_step(probe_filter, pos, step)
        if pos is None or not is_inside_bounds(pos, bounds): 
            break
        streamline.append(pos)

    # Backward direction tracing
    pos = seed[:]
    backward = []
    for _ in range(max_steps):
        pos = rk4_step(probe_filter, pos, -step)
        if pos is None or not is_inside_bounds(pos, bounds):
            break
        backward.insert(0, pos)

    # Combine forward and backward streamlines
    return backward + streamline  

def request_seed_from_user():
    """Prompt user to input seed coordinates."""
    print("Enter the 3D seed location:\n")
    x = float(input("x: "))
    y = float(input("y: "))
    z = float(input("z: "))
    return [x, y, z]

def save_streamline_to_vtp(streamline_points, filename="streamline_output.vtp"):
    """Save the streamline to a .vtp file."""
    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()

    # Add points and lines to the polydata
    for i, pt in enumerate(streamline_points):
        points.InsertNextPoint(pt)
        if i > 0:
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, i - 1)
            line.GetPointIds().SetId(1, i)
            lines.InsertNextCell(line)

    # Create a vtkPolyData object to hold the points and lines
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)

    # Write the polydata to a .vtp file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(polydata)
    writer.Write()
    print(f"Streamline saved to '{filename}'.")

def main():
    print("Streamline Tracing using RK4\n")
    print("==================================== \n")
    # Load the tornado dataset
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName("tornado3d_vector.vti")
    reader.Update()
    vector_data = reader.GetOutput()

    # Set up the probe filter for vector interpolation
    probe = vtk.vtkProbeFilter()
    probe.SetSourceData(vector_data)

    # Get dataset bounds and seed point from the user
    bounds = vector_data.GetBounds()
    seed_point = request_seed_from_user()

    # Generate the streamline
    streamline = trace_streamline(seed_point, probe, bounds)

    # Save the streamline to a .vtp file
    save_streamline_to_vtp(streamline, "rk4_streamline.vtp")

# Entry point of the script
if __name__ == "__main__":
    main()
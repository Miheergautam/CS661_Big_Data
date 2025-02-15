import os
import vtk

def generate_isocontour(volume_data, iso_value):

    dims = volume_data.GetDimensions()
    width, height = dims[0], dims[1]

    scalar_field = volume_data.GetPointData().GetScalars()

    result_data = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()

    point_cache = {}

    def interpolate_point(x1, y1, v1, x2, y2, v2):
        ratio = (iso_value - v1) / (v2 - v1)
        return x1 + ratio * (x2 - x1), y1 + ratio * (y2 - y1)

    def get_or_create_point(x, y):
        key = (x, y)
        if key not in point_cache:
            point_cache[key] = points.InsertNextPoint(x, y, 0.0)
        return point_cache[key]

    for i in range(width - 1):
        for j in range(height - 1):
            v0 = scalar_field.GetComponent(i + j * width, 0)
            v1 = scalar_field.GetComponent((i+1) + j * width, 0)
            v2 = scalar_field.GetComponent((i+1) + (j+1) * width, 0)
            v3 = scalar_field.GetComponent(i + (j+1) * width, 0)

            corners = [(i, j, v0), (i+1, j, v1), (i+1, j+1, v2), (i, j+1, v3)]
            intersect_points = []

            for idx in range(4):
                x1, y1, val1 = corners[idx]
                x2, y2, val2 = corners[(idx+1) % 4]
                if (val1 < iso_value <= val2) or (val2 < iso_value <= val1):
                    intersect_points.append(interpolate_point(x1, y1, val1, x2, y2, val2))

            if len(intersect_points) == 2:
                p1 = get_or_create_point(*intersect_points[0])
                p2 = get_or_create_point(*intersect_points[1])
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, p1)
                line.GetPointIds().SetId(1, p2)
                lines.InsertNextCell(line)

    result_data.SetPoints(points)
    result_data.SetLines(lines)

    return result_data

# file path
input_file = "Data/Isabel_2D.vti"

# Iso value
try:
    isovalue = float(input("Enter the iso value for pressure: "))
except ValueError:
    print("Invalid input. Please enter a numeric value.")
    exit()

reader = vtk.vtkXMLImageDataReader()
reader.SetFileName(input_file)
reader.Update()

volume = reader.GetOutput()

print(f"Generating isocontour for iso_value: {isovalue}")
isocontour = generate_isocontour(volume, isovalue)


output_dir = "output_isocontours"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, f"isocontour_{isovalue:.2f}.vtp")
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName(output_file)
writer.SetInputData(isocontour)
writer.Write()
print(f"Isocontour saved as '{output_file}'")

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(isocontour)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.2, 0.5, 0.8)
actor.GetProperty().SetLineWidth(3)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.1, 0.1)

window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)
window.SetSize(900, 700)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

window.Render()
print("Displaying isocontour. Close the window to exit.")
interactor.Start()
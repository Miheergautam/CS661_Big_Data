## Import VTK
from vtk import *

# Load dataset
reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()

# Retrieve cell count
total_cells = data.GetNumberOfCells()

# Input isovalue from user
target_iso = float(input("Enter the isovalue for contour generation: "))

# Extract pressure data
pressure_values = data.GetPointData().GetArray('Pressure')

# Initialize VTK objects
line_poly = vtkPolyLine()
vertex_collection = vtkPoints()
segment_cells = vtkCellArray()

# List to track contour points
contour_vertices = []
vertex_index = 0

def compute_iso_vertex(x1, y1, z1, p1, x2, y2, z2, p2, target):
    ratio = (p1 - target) / (p1 - p2)
    x = x1 + ratio * (x2 - x1)
    y = y1 + ratio * (y2 - y1)
    z = z1 + ratio * (z2 - z1)
    return x, y, z

def get_point_coords(point_id):
    return data.GetPoint(point_id)

for cell_id in range(total_cells):
    cell = data.GetCell(cell_id)
    point_ids = [cell.GetPointId(i) for i in range(4)]

    coords = [get_point_coords(pid) for pid in point_ids]
    pressures = [pressure_values.GetValue(pid) for pid in point_ids]

    intersect_vertices = []

    for idx in range(4):
        next_idx = (idx + 1) % 4
        p1, p2 = pressures[idx], pressures[next_idx]
        if (p1 > target_iso and p2 < target_iso) or (p1 < target_iso and p2 > target_iso):
            x1, y1, z1 = coords[idx]
            x2, y2, z2 = coords[next_idx]
            intersect_vertices.append(compute_iso_vertex(x1, y1, z1, p1, x2, y2, z2, p2, target_iso))

    for j in range(0, len(intersect_vertices), 2):
        line_poly.GetPointIds().SetNumberOfIds(2)
        line_poly.GetPointIds().SetId(0, vertex_index)
        line_poly.GetPointIds().SetId(1, vertex_index + 1)
        vertex_index += 2
        segment_cells.InsertNextCell(line_poly)

    contour_vertices.extend(intersect_vertices)

for point in contour_vertices:
    vertex_collection.InsertNextPoint(point)

# Prepare polydata
polydata = vtkPolyData()
polydata.SetPoints(vertex_collection)
polydata.SetLines(segment_cells)

# Write output to file
writer = vtkXMLPolyDataWriter()
writer.SetInputData(polydata)
writer.SetFileName('contour_output.vtp')
writer.Write()

# Visualization
mapper = vtkPolyDataMapper()
mapper.SetInputData(polydata)

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
render_window = vtkRenderWindow()
colors = vtkNamedColors()
renderer.SetBackground(colors.GetColor3d("DarkSlateGray"))
render_window.AddRenderer(renderer)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.AddActor(actor)
render_window.SetFullScreen(True)
render_window.SetWindowName('Isocontour Visualization')
render_window.Render()
interactor.Start()
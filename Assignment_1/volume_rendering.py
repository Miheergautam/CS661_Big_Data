import vtk

def load_volume(file_path):
    # Create a reader to load the VTI file
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(file_path)
    reader.Update()
    return reader

def create_color_transfer_function():
    # Define color mapping based on scalar values
    color_trans_fun = vtk.vtkColorTransferFunction()
    color_points = [
        (-4931.54, 0, 1, 1),
        (-2508.95, 0, 0, 1),
        (-1873.9, 0, 0, 0.5),
        (-1027.16, 1, 0, 0),
        (-298.031, 1, 0.4, 0),
        (2594.97, 1, 1, 0)
    ]
    for val, r, g, b in color_points:
        color_trans_fun.AddRGBPoint(val, r, g, b)
    return color_trans_fun

def create_opacity_transfer_function():
    # Define opacity mapping based on scalar values
    opacity_trans_fun = vtk.vtkPiecewiseFunction()
    opacity_points = [
        (-4931.54, 1.0),
        (101.815, 0.002),
        (2594.97, 0.0)
    ]
    for val, opacity in opacity_points:
        opacity_trans_fun.AddPoint(val, opacity)
    return opacity_trans_fun

def setup_volume_property():
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(create_color_transfer_function())
    volume_property.SetScalarOpacity(create_opacity_transfer_function())
    if input("Enable Phong shading? (y/n): ").strip().lower() == "y":
        volume_property.ShadeOn()
        volume_property.SetAmbient(0.5)
        volume_property.SetDiffuse(0.5)
        volume_property.SetSpecular(0.5)
    else:
        volume_property.ShadeOff()
    return volume_property

def create_volume(reader):
    # volume mapper and volume for rendering
    volume_mapper = vtk.vtkSmartVolumeMapper()
    volume_mapper.SetInputData(reader.GetOutput())
    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(setup_volume_property())
    return volume

def create_outline(reader):
    # Generate an outline around the volume
    outline = vtk.vtkOutlineFilter()
    outline.SetInputData(reader.GetOutput())
    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline.GetOutputPort())
    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)
    outline_actor.GetProperty().SetColor(1, 1, 1)
    return outline_actor

def render_scene(file_path):
    reader = load_volume(file_path)
    volume = create_volume(reader)
    outline_actor = create_outline(reader)

    renderer = vtk.vtkRenderer()
    renderer.AddVolume(volume)
    renderer.AddActor(outline_actor)
    renderer.SetBackground(0.1, 0.1, 0.1)

    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(1000, 1000)
    render_window.AddRenderer(renderer)

    render_interactor = vtk.vtkRenderWindowInteractor()
    render_interactor.SetRenderWindow(render_window)

    renderer.ResetCamera()
    render_window.Render()
    render_interactor.Start()

if __name__ == "__main__":
    # file path for the volume data
    file_path = "Data/Isabel_3D.vti"
    render_scene(file_path)
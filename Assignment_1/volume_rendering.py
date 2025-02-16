import vtk

# Load the 3D dataset
data_reader = vtk.vtkXMLImageDataReader()
data_reader.SetFileName("Data/Isabel_3D.vti")
data_reader.Update()

# Configure color mapping
color_map = vtk.vtkColorTransferFunction()
color_map.AddRGBPoint(-4931.54, 0, 1, 1)
color_map.AddRGBPoint(-2508.95, 0, 0, 1)
color_map.AddRGBPoint(-1873.9, 0, 0, 0.5)
color_map.AddRGBPoint(-1027.16, 1, 0, 0)
color_map.AddRGBPoint(-298.031, 1, 0.4, 0)
color_map.AddRGBPoint(2594.97, 1, 1, 0)

# Configure opacity mapping
opacity_map = vtk.vtkPiecewiseFunction()
opacity_map.AddPoint(-4931.54, 1.0)
opacity_map.AddPoint(101.815, 0.002)
opacity_map.AddPoint(2594.97, 0.0)

# Initialize volume mapper
volume_mapper = vtk.vtkSmartVolumeMapper()
volume_mapper.SetInputData(data_reader.GetOutput())

# Configure volume properties
volume_props = vtk.vtkVolumeProperty()
volume_props.SetColor(color_map)
volume_props.SetScalarOpacity(opacity_map)

# Check shading preference
shading_choice = input("Enable Phong shading? (y/n): ")
if shading_choice.lower() == 'y':
    volume_props.ShadeOn()
    volume_props.SetAmbient(0.5)
    volume_props.SetDiffuse(0.5)
    volume_props.SetSpecular(0.5)
else:
    volume_props.ShadeOff()

# Set up the volume actor
vol_actor = vtk.vtkVolume()
vol_actor.SetMapper(volume_mapper)
vol_actor.SetProperty(volume_props)

# Add an outline for context
outline_filter = vtk.vtkOutlineFilter()
outline_filter.SetInputData(data_reader.GetOutput())
outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())
outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)

# Initialize rendering components
scene_renderer = vtk.vtkRenderer()
scene_renderer.AddVolume(vol_actor)
scene_renderer.AddActor(outline_actor)

window_renderer = vtk.vtkRenderWindow()
window_renderer.SetSize(1000, 1000)
window_renderer.AddRenderer(scene_renderer)

interaction_handler = vtk.vtkRenderWindowInteractor()
interaction_handler.SetRenderWindow(window_renderer)

# Launch visualization
interaction_handler.Initialize()
window_renderer.Render()
interaction_handler.Start()

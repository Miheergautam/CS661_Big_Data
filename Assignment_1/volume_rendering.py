import vtk

class VolumeRenderer:
    """
    A class to perform volume rendering of 3D VTK image data with customizable
    transfer functions and Phong shading capabilities.
    """
    def __init__(self, input_file):
        """
        Initialize the volume renderer with input file and default parameters.
        
        Args:
            input_file (str): Path to the VTK image data file (.vti)
        """
        self.input_file = input_file
        self.dataset = None
        self.volume_mapper = None
        self.volume_property = None
        
        # Color transfer function points
        self.color_points = [
            (-4931.54, (0, 1, 1)),
            (-2508.95, (0, 0, 1)),
            (-1873.9, (0, 0, 0.5)),
            (-1027.16, (1, 0, 0)),
            (-298.031, (1, 0.4, 0)),
            (2594.97, (1, 1, 0))
        ]
        
        # Opacity transfer function points
        self.opacity_points = [
            (-4931.54, 1.0),
            (101.815, 0.002),
            (2594.97, 0.0)
        ]
        
        # Phong shading parameters
        self.shading_params = {
            'ambient': 0.5,
            'diffuse': 0.5,
            'specular': 0.5
        }

    def load_dataset(self):
        """Load and prepare the 3D VTK image data"""
        try:
            reader = vtk.vtkXMLImageDataReader()
            reader.SetFileName(self.input_file)
            reader.Update()
            self.dataset = reader.GetOutput()
            if not self.dataset.GetNumberOfPoints():
                raise RuntimeError("Dataset is empty")
        except Exception as e:
            raise RuntimeError(f"Failed to load dataset: {e}")

    def setup_transfer_functions(self):
        """
        Configure color and opacity transfer functions based on
        predefined control points.
        
        Returns:
            tuple: (vtkColorTransferFunction, vtkPiecewiseFunction)
        """
        # Set up color mapping
        color_tf = vtk.vtkColorTransferFunction()
        for value, (r, g, b) in self.color_points:
            color_tf.AddRGBPoint(value, r, g, b)

        # Set up opacity mapping
        opacity_tf = vtk.vtkPiecewiseFunction()
        for value, opacity in self.opacity_points:
            opacity_tf.AddPoint(value, opacity)

        return color_tf, opacity_tf

    def configure_volume_properties(self, enable_shading=False):
        """
        Configure volume rendering properties including transfer functions
        and optional Phong shading.
        
        Args:
            enable_shading (bool): Whether to enable Phong shading
        """
        self.volume_property = vtk.vtkVolumeProperty()
        
        # Apply transfer functions
        color_tf, opacity_tf = self.setup_transfer_functions()
        self.volume_property.SetColor(color_tf)
        self.volume_property.SetScalarOpacity(opacity_tf)
        
        # Configure shading if enabled
        if enable_shading:
            self.volume_property.ShadeOn()
            self.volume_property.SetAmbient(self.shading_params['ambient'])
            self.volume_property.SetDiffuse(self.shading_params['diffuse'])
            self.volume_property.SetSpecular(self.shading_params['specular'])
        else:
            self.volume_property.ShadeOff()

    def setup_volume_mapper(self):
        """Configure the volume mapper with the loaded dataset"""
        self.volume_mapper = vtk.vtkSmartVolumeMapper()
        self.volume_mapper.SetInputData(self.dataset)

    def create_volume_actor(self):
        """
        Create and configure the volume actor.
        
        Returns:
            vtkVolume: Configured volume actor
        """
        volume = vtk.vtkVolume()
        volume.SetMapper(self.volume_mapper)
        volume.SetProperty(self.volume_property)
        return volume

    def create_outline_actor(self):
        """
        Create an outline actor for the volume boundary.
        
        Returns:
            vtkActor: Configured outline actor
        """
        outline = vtk.vtkOutlineFilter()
        outline.SetInputData(self.dataset)
        
        outline_mapper = vtk.vtkPolyDataMapper()
        outline_mapper.SetInputConnection(outline.GetOutputPort())
        
        outline_actor = vtk.vtkActor()
        outline_actor.SetMapper(outline_mapper)
        return outline_actor

    def setup_visualization(self):
        """
        Set up the visualization pipeline with renderer and interaction handlers.
        
        Returns:
            tuple: (vtkRenderWindow, vtkRenderWindowInteractor)
        """
        # Create and configure renderer
        renderer = vtk.vtkRenderer()
        
        # Add volume and outline
        volume_actor = self.create_volume_actor()
        outline_actor = self.create_outline_actor()
        renderer.AddVolume(volume_actor)
        renderer.AddActor(outline_actor)
        
        # Configure render window
        render_window = vtk.vtkRenderWindow()
        render_window.SetSize(1000, 1000)
        render_window.AddRenderer(renderer)
        
        # Set up interaction
        interactor = vtk.vtkRenderWindowInteractor()
        interactor.SetRenderWindow(render_window)
        
        return render_window, interactor

def main():
    """Main function to run the volume rendering visualization"""
    # Initialize renderer
    renderer = VolumeRenderer('Data/Isabel_3D.vti')
    
    try:
        # Load and prepare data
        renderer.load_dataset()
        renderer.setup_volume_mapper()
        
        # Get user preference for shading
        shading_choice = input("Enable Phong shading? (y/n): ").lower()
        enable_shading = shading_choice == 'y'
        
        # Configure volume properties
        renderer.configure_volume_properties(enable_shading)
        
        # Setup and start visualization
        render_window, interactor = renderer.setup_visualization()
        interactor.Initialize()
        render_window.Render()
        interactor.Start()
        
    except Exception as e:
        print(f"Error during visualization: {e}")

if __name__ == "__main__":
    main()
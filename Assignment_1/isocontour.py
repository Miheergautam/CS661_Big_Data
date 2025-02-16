from vtk import *

class IsocontourExtractor:
    """
    Extract isocontours from 2D VTK image data.
    Implements a simplified version of the marching squares algorithm.
    """
    def __init__(self, input_file):
        """
        Initialize the extractor with input file path and setup VTK objects.
        
        Arguments:
            input_file (str): Path to the VTK image data file (.vti)
        """
        self.input_file = input_file
        self.dataset = None
        self.pressure_data = None
        self.isovalue = None
        self.initialize_vtk_objects()

    def initialize_vtk_objects(self):
        """Initialize necessary VTK objects for contour extraction"""
        # Points to store contour vertices
        self.points = vtkPoints()
        # Cells to store contour line segments
        self.cells = vtkCellArray()
        # Polyline object for creating line segments
        self.polyline = vtkPolyLine()
        # Counter for vertex indexing
        self.vertex_count = 0
        # List to store contour intersection points
        self.contour_points = []

    def load_dataset(self):
        """
        Load and prepare the VTK image data.
        
        Returns:
            int: Total number of cells in the dataset
        """
        data_reader = vtkXMLImageDataReader()
        data_reader.SetFileName(self.input_file)
        data_reader.Update()
        self.dataset = data_reader.GetOutput()
        # Get the pressure scalar array
        self.pressure_data = self.dataset.GetPointData().GetArray('Pressure')
        return self.dataset.GetNumberOfCells()

    def set_isovalue(self, value):
        """
        Set and validate the isovalue for contour generation.
        
        Arguments:
            value: The isovalue to extract contours at
            
        Raises:
            ValueError: If the isovalue is invalid or out of range
        """
        try:
            self.isovalue = float(value)
            # Check if isovalue is within the valid range
            if not (-1438 <= self.isovalue <= 630):
                raise ValueError("Isovalue must be between -1438 and 630")
        except ValueError as e:
            raise ValueError(f"Invalid isovalue: {e}")

    def interpolate_point(self, p1_data, p2_data):
        """
        Interpolate the position where the isocontour intersects an edge.
        
        Arguments:
            p1_data (dict): First point data with coordinates and pressure
            p2_data (dict): Second point data with coordinates and pressure
            
        Returns:
            tuple: Interpolated (x, y, z) coordinates
        """
        x1, y1, z1 = p1_data['coords']
        x2, y2, z2 = p2_data['coords']
        pressure1 = p1_data['pressure']
        pressure2 = p2_data['pressure']
        
        # Linear interpolation factor
        t = (pressure1 - self.isovalue) / (pressure1 - pressure2)
        
        # Interpolate each coordinate component
        return (
            x1 + t * (x2 - x1),
            y1 + t * (y2 - y1),
            z1 + t * (z2 - z1)
        )

    def process_cell(self, cell_idx):
        """
        Process a single cell to find contour intersections.
        Traverses cell vertices in counterclockwise order.
        
        Arguments:
            cell_idx (int): Index of the cell to process
        """
        cell = self.dataset.GetCell(cell_idx)
        cell_data = []
        
        # Gather data for all vertices of the cell
        for i in range(4):
            point_id = cell.GetPointId(i)
            cell_data.append({
                'coords': self.dataset.GetPoint(point_id),
                'pressure': self.pressure_data.GetValue(point_id)
            })

        intersection_points = []
        
        # Check each edge for intersections with the isovalue
        for i in range(4):
            next_i = (i + 1) % 4  # Next vertex (wraps around to 0)
            p1, p2 = cell_data[i], cell_data[next_i]
            
            # If edge crosses the isovalue, calculate intersection point
            if self.crosses_isovalue(p1['pressure'], p2['pressure']):
                intersection_points.append(
                    self.interpolate_point(p1, p2)
                )

        # Add found intersection points to contour
        self.add_contour_segments(intersection_points)

    def crosses_isovalue(self, p1, p2):
        """
        Check if an edge crosses the isovalue.
        
        Arguments:
            p1 (float): Pressure value at first point
            p2 (float): Pressure value at second point
            
        Returns:
            bool: True if edge crosses isovalue, False otherwise
        """
        return (p1 > self.isovalue and p2 < self.isovalue) or \
               (p1 < self.isovalue and p2 > self.isovalue)

    def add_contour_segments(self, points):
        """
        Add line segments to the contour for pairs of intersection points.
        
        Arguments:
            points (list): List of intersection points to connect
        """
        # Process points in pairs to create line segments
        for i in range(0, len(points), 2):
            if i + 1 < len(points):
                # Create a line segment between each pair of points
                self.polyline.GetPointIds().SetNumberOfIds(2)
                self.polyline.GetPointIds().SetId(0, self.vertex_count)
                self.polyline.GetPointIds().SetId(1, self.vertex_count + 1)
                self.vertex_count += 2
                self.cells.InsertNextCell(self.polyline)
                self.contour_points.extend([points[i], points[i + 1]])

    def create_visualization(self):
        """
        Create the VTK polydata object for visualization.
        
        Returns:
            vtkPolyData: The complete contour geometry
        """
        # Add all collected points to the vtkPoints object
        for point in self.contour_points:
            self.points.InsertNextPoint(point)

        # Create and setup the polydata object
        polydata = vtkPolyData()
        polydata.SetPoints(self.points)
        polydata.SetLines(self.cells)
        return polydata

    def save_output(self, polydata, output_file):
        """
        Save the contour as a VTP file.
        
        Arguments:
            polydata (vtkPolyData): The contour geometry to save
            output_file (str): Output file path
        """
        writer = vtkXMLPolyDataWriter()
        writer.SetInputData(polydata)
        writer.SetFileName(output_file)
        writer.Write()

    def setup_visualization(self, polydata):
        """
        Setup the visualization pipeline for displaying the contour.
        
        Arguments:
            polydata (vtkPolyData): The contour geometry to visualize
            
        Returns:
            tuple: (vtkRenderWindow, vtkRenderWindowInteractor) for visualization
        """
        # Create visualization pipeline
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
        
        return render_window, interactor

def main():
    """Main function to run the isocontour extraction"""
    # Initialize the extractor
    extractor = IsocontourExtractor('Data/Isabel_2D.vti')
    
    # Get and validate user input
    isovalue = input("Enter the isovalue for contour generation: ")
    extractor.set_isovalue(isovalue)
    
    # Load the dataset and get cell count
    total_cells = extractor.load_dataset()
    
    # Process each cell to generate contours
    for cell_idx in range(total_cells):
        extractor.process_cell(cell_idx)
    
    # Create visualization and save output
    polydata = extractor.create_visualization()
    extractor.save_output(polydata, 'contour_output.vtp')
    
    # Setup and start interactive visualization
    render_window, interactor = extractor.setup_visualization(polydata)
    render_window.Render()
    interactor.Start()

if __name__ == "__main__":
    main()
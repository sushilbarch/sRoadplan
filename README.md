# sRoadplan
View road plan from excel to drawing.
The provided Python script is a tool for generating a road plan layout from data in an Excel file, including plotting road edges, drains, and retaining walls, and outputting the layout to both a visual representation using Matplotlib and a CAD drawing using EzDXF. Here's a detailed breakdown of the components and the workflow of the script:

1. Overview
The script:
Loads data from an Excel file using a file dialog.
Processes the road geometry, including road edges, drain positions, and retaining wall positions.
Calculates the road plan layout and plots it using Matplotlib.
Generates a CAD drawing of the layout using EzDXF.
The road layout includes the left and right edges, left-hand side (LHS) and right-hand side (RHS) drains, and retaining walls.
2. Components of the Script
2.1 Import Statements
Pandas: For reading data from an Excel file.
Matplotlib: For plotting the road layout.
Numpy: To manipulate arrays, simplifying operations.
Tkinter (filedialog): For selecting the Excel file.
EzDXF: To generate a CAD file for the road layout.
2.2 File Dialog to Select Excel File
Tkinter is used to create a dialog for selecting the input Excel file.
The file path is verified for existence using os.path.exists().
pd.read_excel(file_path) is used to load the data into a DataFrame.
2.3 Extracting Data from Excel File
The required columns are:
Road Length, Road Width, LHS Drain Width, RHS Drain Width, LHS Wall Length, and RHS Wall Length.
The data is extracted from the DataFrame and converted to NumPy arrays for easy manipulation.
2.4 Defining Road Elements
Lists are initialized to store the coordinates of:
Left and Right Road Edges.
LHS and RHS Drains.
LHS and RHS Retaining Walls.
2.5 Generating Road Layout and Edges
Loop Through Chanage Data:
For each segment of the road:
Calculate the positions of the road edges, drains, and retaining walls based on the provided lengths and widths.
Append the coordinates for each element (edges, drains, walls) to the corresponding list.
Current Position is incremented by road length at each iteration.
A fixed increment of 10 meters is used within each segment for detailed plotting.
2.6 Plotting the Road Plan Using Matplotlib
The road layout is visualized using Matplotlib:
Road Edges are plotted as dashed black lines.
Drains (if present) are plotted as blue lines.
Retaining Walls (if present) are plotted as red dashed lines.
Additional details such as title, labels, legend, and grid are added for clarity.
Annotations:
The script adds text annotations to indicate the widths at each channage point, showing the road width, drain width, and retaining wall width where applicable.
2.7 Calculating Summary Values
Total lengths for various components are calculated:
Total Road Length: Sum of all road segments.
Total Drain and Wall Lengths: Only segments with non-zero values are considered.
A summary is printed with the following information:
Total Road Length.
Total Lengths of LHS and RHS Drains.
Total Lengths of LHS and RHS Retaining Walls.
3. CAD Drawing with EzDXF
A CAD drawing is generated using EzDXF:
Modelspace is used to add lines representing the road layout.
The script draws lines for:
Left and Right Road Edges (color set to black).
LHS and RHS Drains (color set to blue).
LHS and RHS Retaining Walls (color set to red).
The CAD drawing is saved as 'road_plan.dxf'.
4. Workflow of the Script
Load Data:
The user selects an Excel file using the file dialog.
The script verifies that the file exists and loads the data into a DataFrame.
Extract Road Data:
Extracts relevant data such as road length, road width, drain widths, and retaining wall lengths.
Generate Road Layout:
Initializes arrays for different road elements.
Iteratively calculates positions for road edges, drains, and retaining walls.
Plotting:
Plots the road plan layout using Matplotlib.
Annotations are added to indicate the widths of road elements.
Generate CAD Drawing:
Uses EzDXF to draw the road plan as a CAD drawing.
Summary:
Prints a summary of the total lengths of road elements.
5. Key Points
Road Layout Elements:
Left and Right Road Edges: Represent the boundaries of the road.
Drains: Positioned on either side of the road, based on input data.
Retaining Walls: Positioned beyond the drains, with an offset of 0.5m if drains are present.
Incremental Plotting:
To create a detailed plot of the road layout, increments of 10 meters are used for detailed plotting of the road geometry.
Summary Calculation:
Calculates total lengths for each element (road edges, drains, retaining walls) and prints a summary.
Plot and CAD Generation:
The road plan is visualized using Matplotlib and saved as a PNG.
The road plan is also generated in a CAD format (DXF) using EzDXF for further engineering use.
6. Improvements and Enhancements
User Input:
The script could be enhanced with a user-friendly GUI for entering parameters instead of using only Excel.
Error Handling:
Add more comprehensive error handling for missing columns and invalid data types in the Excel file.
Detailed CAD Drawing:
Add more details to the CAD drawing, such as labels, dimensions, and annotations for the retaining walls and drains.
Dynamic Interval for Plotting:
The increment for plotting (10 meters) could be made dynamic, allowing for different levels of detail based on user preference.
7. Usage Scenario
Civil Engineering Projects:
This script is useful for planning road layouts where data is provided in Excel format.
Engineers can visualize the layout, including road edges, drains, and retaining structures.
The CAD output provides a ready-to-use representation for further design and engineering adjustments.
The script provides a complete workflow for managing road design data, from data extraction and calculation to visualization and CAD generation. It is well-suited for applications in road design and infrastructure planning, where detailed layout visualization and documentation are crucial.

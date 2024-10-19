import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog
import ezdxf

# Load Data from Excel File Using File Dialog
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", "*.xls *.xlsx")])

# Check if the file exists
if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    exit()
else:
    print(f"File found: {file_path}")

try:
    data = pd.read_excel(file_path)
    print(f"Successfully loaded data from {file_path}")
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit()
except Exception as e:
    print(f"Error while reading the Excel file: {e}")
    exit()

# Extract Data from Excel Sheet
try:
    road_length = data['Road Length'][1:].astype(float).values
    road_width = data['Road Width'][1:].astype(float).values
    lhs_drain_width = data['LHS Drain Width'][1:].astype(float).values
    rhs_drain_width = data['RHS Drain Width'][1:].astype(float).values
    lhs_retain_length = data['LHS Wall Length'][1:].astype(float).values
    rhs_retain_length = data['RHS Wall Length'][1:].astype(float).values
    chanage_data = list(zip(road_length, road_width, lhs_drain_width, rhs_drain_width, lhs_retain_length, rhs_retain_length))
except KeyError as e:
    print(f"Error: Missing column in data - {e}")
    exit()
except Exception as e:
    print(f"Error: {e}")
    exit()

# Initialize Road Elements
left_edge = []
right_edge = []
lhs_drain = []
rhs_drain = []
lhs_retaining_wall = []
rhs_retaining_wall = []

# Generate Road Layouts and Edges
current_position = 0
for i, (road_length, road_width, lhs_drain_width, rhs_drain_width, lhs_retain_length, rhs_retain_length) in enumerate(chanage_data):
    end = current_position + road_length
    # Update current position with road length increment
    current_position += road_length
    while current_position <= end:
        # Calculate Half Width for Each Side of Road
        half_width = road_width / 2

        # Define Road Edges
        left_edge.append((current_position, -half_width))
        right_edge.append((current_position, half_width))

        # Define Drain Positions (at the edge of the half-width)
        if lhs_drain_width > 0:
            lhs_drain.append((current_position, -half_width - lhs_drain_width))
        if rhs_drain_width > 0:
            rhs_drain.append((current_position, half_width + rhs_drain_width))

        # Define Retaining Wall Positions (offset from the drain by 0.5m if drain exists)
        if lhs_retain_length > 0 and lhs_drain_width > 0:
            lhs_retaining_wall.append((current_position, -half_width - lhs_drain_width - 0.5))
        elif lhs_retain_length > 0 and lhs_drain_width == 0:
            lhs_retaining_wall.append((current_position, -half_width - 0.5))
        if rhs_retain_length > 0 and rhs_drain_width > 0:
            rhs_retaining_wall.append((current_position, half_width + rhs_drain_width + 0.5))
        elif rhs_retain_length > 0 and rhs_drain_width == 0:
            rhs_retaining_wall.append((current_position, half_width + 0.5))

        # Increment Current Position
        current_position += 10  # interval in meters for plotting

# Convert to Numpy Arrays for Easy Plotting
left_edge = np.array(left_edge)
right_edge = np.array(right_edge)
lhs_drain = np.array(lhs_drain) if len(lhs_drain) > 0 else np.empty((0, 2))
rhs_drain = np.array(rhs_drain) if len(rhs_drain) > 0 else np.empty((0, 2))
lhs_retaining_wall = np.array(lhs_retaining_wall) if len(lhs_retaining_wall) > 0 else np.empty((0, 2))
rhs_retaining_wall = np.array(rhs_retaining_wall) if len(rhs_retaining_wall) > 0 else np.empty((0, 2))

# Calculate Total Road Length
total_road_length = np.sum(road_length)

# Calculate Total Values for Drains and Retaining Walls
total_lhs_drain_length = np.sum([length for length, width, lhs_drain, rhs_drain, lhs_wall, rhs_wall in chanage_data if lhs_drain > 0])
total_rhs_drain_length = np.sum([length for length, width, lhs_drain, rhs_drain, lhs_wall, rhs_wall in chanage_data if rhs_drain > 0])
total_lhs_wall_length = np.sum([length for length, width, lhs_drain, rhs_drain, lhs_wall, rhs_wall in chanage_data if lhs_wall > 0])
total_rhs_wall_length = np.sum([length for length, width, lhs_drain, rhs_drain, lhs_wall, rhs_wall in chanage_data if rhs_wall > 0])

# Summary of Final Road Layout Calculations
summary = f"""
Summary of Final Road Layout Calculations:
- Total Road Length: {total_road_length} meters
- Total LHS Drain Length: {total_lhs_drain_length} meters
- Total RHS Drain Length: {total_rhs_drain_length} meters
- Total LHS Wall Length: {total_lhs_wall_length} meters
- Total RHS Wall Length: {total_rhs_wall_length} meters
"""
print(summary)

# Plotting the Road Plan
plt.figure(figsize=(14, 10))

# Plot Road Edges
plt.plot(left_edge[:, 0], left_edge[:, 2], label="Left Edge of Road", color="black", linestyle="--")
plt.plot(right_edge[:, 0], right_edge[:, 2], label="Right Edge of Road", color="black", linestyle="--")

# Plot Drains
if len(lhs_drain) > 0:
    plt.plot(lhs_drain[:, 0], lhs_drain[:, 2], label="LHS Drain", color="blue", linestyle="-")
if len(rhs_drain) > 0:
    plt.plot(rhs_drain[:, 0], rhs_drain[:, 2], label="RHS Drain", color="blue", linestyle="-")

# Plot Retaining Walls
if len(lhs_retaining_wall) > 0:
    plt.plot(lhs_retaining_wall[:, 0], lhs_retaining_wall[:, 2], label="LHS Retaining Wall", color="red", linestyle="-.")
if len(rhs_retaining_wall) > 0:
    plt.plot(rhs_retaining_wall[:, 0], rhs_retaining_wall[:, 2], label="RHS Retaining Wall", color="red", linestyle="-.")

# Add Plot Details
plt.xlabel('Distance along Road (m)', fontsize=12)
plt.ylabel('Width of Elements (m)', fontsize=12)
plt.title('Road Plan with Drains and Retaining Walls', fontsize=16)
plt.axhline(0, color='gray', linestyle='-', linewidth=0.8)  # Centerline
plt.legend()
plt.grid(True)

# Show Widths at Each Channage
for i, (length, width, lhs_drain, rhs_drain, lhs_wall, rhs_wall) in enumerate(chanage_data):
    position = sum(data['Road Length'][:i].astype(float).values)
    plt.text(position + length / 2, max(right_edge[:, 1]) + 5, f"Road Width: {width}m", fontsize=10, ha='center', color='green')
    if lhs_drain > 0:
        plt.text(position + length / 2, -half_width - lhs_drain - 1, f"LHS Drain Width: {lhs_drain}m", fontsize=10, ha='center', color='blue')
    if rhs_drain > 0:
        plt.text(position + length / 2, half_width + rhs_drain + 1, f"RHS Drain Width: {rhs_drain}m", fontsize=10, ha='center', color='blue')
    if lhs_wall > 0:
        plt.text(position + length / 2, -half_width - lhs_drain - lhs_wall - 1, f"LHS Wall Width: {lhs_wall}m", fontsize=10, ha='center', color='red')
    if rhs_wall > 0:
        plt.text(position + length / 2, half_width + rhs_drain + rhs_wall + 1, f"RHS Wall Width: {rhs_wall}m", fontsize=10, ha='center', color='red')

# Display the Plot
plt.tight_layout()
plt.savefig('road_plan.png')
plt.show()

# Generate CAD File
dwg = ezdxf.new()
modelspace = dwg.modelspace()

# Draw Road Edges in CAD
for i in range(len(left_edge) - 1):
    modelspace.add_line(start=left_edge[i], end=left_edge[i + 1], dxfattribs={'color': 1})
    modelspace.add_line(start=right_edge[i], end=right_edge[i + 1], dxfattribs={'color': 1})

# Draw Drains in CAD
if len(lhs_drain) > 0:
    for i in range(len(lhs_drain) - 1):
        modelspace.add_line(start=lhs_drain[i], end=lhs_drain[i + 1], dxfattribs={'color': 3})
if len(rhs_drain) > 0:
    for i in range(len(rhs_drain) - 1):
        modelspace.add_line(start=rhs_drain[i], end=rhs_drain[i + 1], dxfattribs={'color': 3})

# Draw Retaining Walls in CAD
if len(lhs_retaining_wall) > 0:
    for i in range(len(lhs_retaining_wall) - 1):
        modelspace.add_line(start=lhs_retaining_wall[i], end=lhs_retaining_wall[i + 1], dxfattribs={'color': 5})
if len(rhs_retaining_wall) > 0:
    for i in range(len(rhs_retaining_wall) - 1):
        modelspace.add_line(start=rhs_retaining_wall[i], end=rhs_retaining_wall[i + 1], dxfattribs={'color': 5})

# Save CAD File
dwg.saveas('road_plan.dxf')

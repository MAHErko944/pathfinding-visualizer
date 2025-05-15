# Path Finder with Algorithms

A Python-based visual pathfinding application built with Pygame, showcasing various search algorithms like BFS, DFS, Dijkstra, and A*. This project allows users to interactively set start/end points, add obstacles, assign weights, and visualize how each algorithm finds the shortest path in a grid-based environment.

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Algorithms](#algorithms)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features
- Interactive grid interface to set start/end points, obstacles, and weights.
- Visualizes the pathfinding process for BFS, DFS, Dijkstra, and A* algorithms.
- Supports weighted cells to simulate real-world pathfinding scenarios.
- Measures and displays the execution time for each algorithm.
- Clear and reset functionality to experiment with different setups.
- User-friendly controls with click-and-drag support for placing obstacles.

## Demo
Below is a quick demo of the application in action:


1. Set a start point (green) and end point (blue).
2. Add obstacles (red) and weights (orange) as needed.
3. Choose an algorithm (BFS, DFS, Dijkstra, or A*) to visualize the path (yellow).

## Prerequisites
To run this project, ensure you have the following installed:
- Python 3.8 or higher
- Pygame (`pygame>=2.0.0`)
- A compatible operating system (Windows, macOS, or Linux)

## Installation
Follow these steps to set up the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MAHErko944/pathfinding-visualizer
   cd pathfinding-visualizer
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install pygame
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

## Usage
1. Launch the application by running `main.py`.
2. Use the buttons on the right to select an action:
   - **Set Start/End**: Click on the grid to place the start (green) and end (blue) points.
   - **Add Obstacles**: Click and drag on the grid to place obstacles (red).
   - **Add Weight**: Click on a cell to increase its weight (orange, up to 9).
   - **Reset**: Clear the grid and start over.
   - **Clear Path**: Remove the path and searched cells, keeping start/end points and obstacles.
   - **Algorithms (BFS, DFS, Dijkstra, A*)**: Run the selected algorithm to visualize the pathfinding process.
3. Right-click on a cell to remove an obstacle or reset its weight.
4. Observe the execution time displayed at the bottom-right after running an algorithm.

## Algorithms
The project implements the following pathfinding algorithms:
- **Breadth-First Search (BFS)**: Guarantees the shortest path in an unweighted grid.
- **Depth-First Search (DFS)**: Explores as far as possible along each branch before backtracking.
- **Dijkstra's Algorithm**: Finds the shortest path in a weighted grid.
- **A* (A-Star)**: Uses heuristics (Manhattan distance) to efficiently find the shortest path in a weighted grid.

Each algorithm visualizes the search process by coloring explored cells gray and the final path yellow.

## Project Structure
```
path-finder-algorithms/
├── main.py               # Main script containing the application logic
├── README.md             # Project documentation (this file)
└── .gitignore            # Git ignore file for excluding unnecessary files
```




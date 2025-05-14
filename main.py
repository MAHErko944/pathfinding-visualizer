import pygame
import sys
import time
from collections import deque
import heapq
import math
import asyncio

# Constants for screen dimensions
WIDTH, HEIGHT = 1010, 700
GRID_WIDTH = 750
CELL_SIZE = 25
GRID_COLS = GRID_WIDTH // CELL_SIZE
GRID_ROWS = HEIGHT // CELL_SIZE
GRID_COLOR = (50, 50, 50)

# Colors
START_COLOR = (0, 255, 0)
FINISH_COLOR = (0, 100, 255)
OBSTACLE_COLOR = (255, 0, 0)
SEARCHED_COLOR = (150, 150, 150)
PATH_COLOR = (255, 255, 0)
BUTTON_COLOR = (180, 180, 180)
SELECTED_BUTTON_COLOR = (100, 100, 150)
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (30, 30, 30)
WEIGHT_COLOR = (255, 165, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" Path Finder with Algorithms ")
font = pygame.font.SysFont(None, 26)
weight_font = pygame.font.SysFont(None, 24)


def draw_grid():
    """Draw grid lines in the grid area"""
    for x in range(0, GRID_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (GRID_WIDTH, y))


def draw_buttons(buttons, selected_button):
    """Draw control buttons"""
    button_names = ['Set Start', 'Set End', 'Add Obstacles', 'Add Weight', 'Reset',
                    'BFS', 'DFS', 'Dijkstra', 'A*', 'Clear Path']

    for index, button in enumerate(buttons):
        color = SELECTED_BUTTON_COLOR if index == selected_button else BUTTON_COLOR
        pygame.draw.rect(screen, color, button)
        pygame.draw.rect(screen, GRID_COLOR, button, 2)
        text = font.render(button_names[index], True, TEXT_COLOR)
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)


def handle_button_click(buttons, mouse_pos):
    """Check if a button was clicked"""
    for index, button in enumerate(buttons):
        if button.collidepoint(mouse_pos):
            return index
    return None


def draw_cell(cell, color):
    """Draw a single cell with specified color"""
    x, y = cell
    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_weights(weights):
    """Draw weight values on cells"""
    for cell, weight in weights.items():
        if weight > 1:
            x, y = cell
            text = weight_font.render(str(weight), True, TEXT_COLOR)
            text_rect = text.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
            screen.blit(text, text_rect)


def display_algorithm_time(time_taken, algorithm_name):
    """Display the execution time for the algorithm"""
    info_text = f"{algorithm_name} Time: {time_taken:.4f} seconds"
    text_surface = font.render(info_text, True, TEXT_COLOR)
    screen.blit(text_surface, (GRID_WIDTH + 20, HEIGHT - 30))
    pygame.display.update()


def clear_path(start, end, obstacles, weights):
    """Clear the path and searched cells, preserving start, end, obstacles, and weights"""
    screen.fill(BACKGROUND_COLOR, (0, 0, GRID_WIDTH, HEIGHT))
    draw_grid()

    for cell, weight in weights.items():
        if weight > 1 and cell not in obstacles and cell != start and cell != end:
            draw_cell(cell, WEIGHT_COLOR)

    for obstacle in obstacles:
        draw_cell(obstacle, OBSTACLE_COLOR)

    if start:
        draw_cell(start, START_COLOR)
    if end:
        draw_cell(end, FINISH_COLOR)

    draw_weights(weights)
    pygame.display.update()


def draw_path(came_from, start, end, weights):
    """Draw the path while preserving start and end colors"""
    path_cells = []
    current = end
    while current is not None:
        if current != start and current != end:
            path_cells.append(current)
        current = came_from.get(current)

    for cell in path_cells:
        draw_cell(cell, PATH_COLOR)

    if start:
        draw_cell(start, START_COLOR)
    if end:
        draw_cell(end, FINISH_COLOR)

    draw_weights(weights)
    pygame.display.update()


def is_valid_cell(cell):
    """Check if cell is within grid bounds"""
    x, y = cell
    return 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS


def get_neighbors(current):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []
    for dx, dy in directions:
        neighbor = (current[0] + dx, current[1] + dy)
        if is_valid_cell(neighbor):
            neighbors.append(neighbor)
    return neighbors


def bfs(start, end, obstacles, weights):
    """Breadth-First Search implementation with time measurement"""
    start_time = time.time()

    queue = deque([start])
    came_from = {start: None}
    searched_cells = set()

    while queue:
        current = queue.popleft()
        if current == end:
            break

        for neighbor in get_neighbors(current):
            if neighbor not in obstacles and neighbor not in came_from:
                queue.append(neighbor)
                came_from[neighbor] = current
                if neighbor != end:
                    draw_cell(neighbor, SEARCHED_COLOR)
                searched_cells.add(neighbor)
        pygame.display.update()
        pygame.time.delay(5)

    for cell in searched_cells:
        if cell != start and cell != end:
            if weights.get(cell, 1) > 1:
                draw_cell(cell, WEIGHT_COLOR)
            else:
                draw_cell(cell, BACKGROUND_COLOR)

    draw_path(came_from, start, end, weights)
    end_time = time.time()
    execution_time = end_time - start_time
    display_algorithm_time(execution_time, "BFS")

    return came_from


def dfs(start, end, obstacles, weights):
    """Depth-First Search implementation with time measurement"""
    start_time = time.time()

    stack = [start]
    came_from = {start: None}
    searched_cells = set()

    while stack:
        current = stack.pop()
        if current == end:
            break

        for neighbor in get_neighbors(current):
            if neighbor not in obstacles and neighbor not in came_from:
                stack.append(neighbor)
                came_from[neighbor] = current
                if neighbor != end:
                    draw_cell(neighbor, SEARCHED_COLOR)
                searched_cells.add(neighbor)
        pygame.display.update()
        pygame.time.delay(5)

    for cell in searched_cells:
        if cell != start and cell != end:
            if weights.get(cell, 1) > 1:
                draw_cell(cell, WEIGHT_COLOR)
            else:
                draw_cell(cell, BACKGROUND_COLOR)

    draw_path(came_from, start, end, weights)

    end_time = time.time()
    execution_time = end_time - start_time
    display_algorithm_time(execution_time, "DFS")

    return came_from


def dijkstra(start, end, obstacles, weights):
    """Dijkstra's algorithm implementation with weights and time measurement"""
    start_time = time.time()

    pq = [(0, start)]
    came_from = {start: None}
    cost_to_come = {start: 0}
    searched_cells = set()

    while pq: 
        cost, current = heapq.heappop(pq)
        if current == end:
            break

        if cost > cost_to_come.get(current, float('inf')):
            continue

        for neighbor in get_neighbors(current):
            if neighbor not in obstacles:

                cell_weight = weights.get(neighbor, 1)
                new_cost = cost_to_come[current] + cell_weight

                if neighbor not in cost_to_come or new_cost < cost_to_come[neighbor]:
                    cost_to_come[neighbor] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor))
                    came_from[neighbor] = current
                    if neighbor != end:
                        draw_cell(neighbor, SEARCHED_COLOR)
                    searched_cells.add(neighbor)
        pygame.display.update()
        pygame.time.delay(5)

    for cell in searched_cells:
        if cell != start and cell != end:
            if weights.get(cell, 1) > 1:
                draw_cell(cell, WEIGHT_COLOR)
            else:
                draw_cell(cell, BACKGROUND_COLOR)

    draw_path(came_from, start, end, weights)

    end_time = time.time()
    execution_time = end_time - start_time
    display_algorithm_time(execution_time, "Dijkstra")

    return came_from


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(start, end, obstacles, weights):
    """A* algorithm implementation with weights and time measurement"""
    start_time = time.time()

    pq = [(0, 0, start)]
    came_from = {start: None}
    g_score = {start: 0}
    searched_cells = set()

    while pq and pq[0][2] != end:
        _, current_g, current = heapq.heappop(pq)

        if current == end:
            break

        if current in g_score and current_g > g_score[current]:
            continue

        for neighbor in get_neighbors(current):
            if neighbor not in obstacles:
                # Use weight for the cell
                cell_weight = weights.get(neighbor, 1)
                tentative_g_score = g_score[current] + cell_weight

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + manhattan_distance(neighbor, end)
                    heapq.heappush(pq, (f_score, tentative_g_score, neighbor))
                    if neighbor != end:
                        draw_cell(neighbor, SEARCHED_COLOR)
                    searched_cells.add(neighbor)
        pygame.display.update()
        # Short delay to see the algorithm work
        pygame.time.delay(5)

    # Clear searched cells
    for cell in searched_cells:
        if cell != start and cell != end:
            if weights.get(cell, 1) > 1:
                draw_cell(cell, WEIGHT_COLOR)
            else:
                draw_cell(cell, BACKGROUND_COLOR)

    draw_path(came_from, start, end, weights)

    end_time = time.time()
    execution_time = end_time - start_time
    display_algorithm_time(execution_time, "A*")

    return came_from


async def main():
    clock = pygame.time.Clock()
    start_point = None
    finish_point = None
    obstacles = set()
    cell_weights = {}
    last_execution_time = 0
    last_algorithm = None

    button_width, button_height = 150, 35
    button_x = GRID_WIDTH + 20
    button_y = 20
    button_gap = 45
    buttons = [
        pygame.Rect(button_x, button_y + i * button_gap, button_width, button_height)
        for i in range(10)
    ]
    selected_button = None
    mouse_held_down = False
    search_initiated = False
    instructions = [
        "Left click: Add/Select",
        "Right click: Remove weight",
        "Click and drag: Add multiple obstacles",
        "Select button then click grid"
    ]

    def update_loop():
        nonlocal start_point, finish_point, obstacles, selected_button, mouse_held_down, search_initiated, cell_weights
        nonlocal last_execution_time, last_algorithm

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
                cell = (grid_x, grid_y)

                button_index = handle_button_click(buttons, (mouse_x, mouse_y))
                if button_index is not None:
                    selected_button = button_index
                    mouse_held_down = False

                    if button_index == 4:
                        start_point = None
                        finish_point = None
                        obstacles.clear()
                        cell_weights.clear()
                        search_initiated = False
                        last_execution_time = 0
                        last_algorithm = None
                        clear_path(start_point, finish_point, obstacles, cell_weights)
                    elif button_index == 5 and start_point and finish_point:  # BFS
                        search_initiated = True
                        clear_path(start_point, finish_point, obstacles, cell_weights)
                        last_algorithm = "BFS"
                        bfs(start_point, finish_point, obstacles, cell_weights)
                    elif button_index == 6 and start_point and finish_point:  # DFS
                        search_initiated = True
                        clear_path(start_point, finish_point, obstacles, cell_weights)
                        last_algorithm = "DFS"
                        dfs(start_point, finish_point, obstacles, cell_weights)
                    elif button_index == 7 and start_point and finish_point:  # Dijkstra
                        search_initiated = True
                        clear_path(start_point, finish_point, obstacles, cell_weights)
                        last_algorithm = "Dijkstra"
                        dijkstra(start_point, finish_point, obstacles, cell_weights)
                    elif button_index == 8 and start_point and finish_point:  # A*
                        search_initiated = True
                        clear_path(start_point, finish_point, obstacles, cell_weights)
                        last_algorithm = "A*"
                        a_star(start_point, finish_point, obstacles, cell_weights)
                    elif button_index == 9:
                        search_initiated = False
                        last_execution_time = 0
                        last_algorithm = None
                        clear_path(start_point, finish_point, obstacles, cell_weights)
                elif event.button == 1 and mouse_x < GRID_WIDTH:
                    if selected_button == 0:
                        if start_point:
                            obstacles.discard(start_point)
                        start_point = cell
                        obstacles.discard(cell)
                        search_initiated = False
                    elif selected_button == 1:
                        if finish_point:
                            obstacles.discard(finish_point)
                        finish_point = cell
                        obstacles.discard(cell)
                        search_initiated = False
                    elif selected_button == 2:
                        if cell != start_point and cell != finish_point:
                            obstacles.add(cell)
                            cell_weights.pop(cell, None)
                            mouse_held_down = True
                            search_initiated = False
                    elif selected_button == 3:
                        if cell != start_point and cell != finish_point and cell not in obstacles:
                            current_weight = cell_weights.get(cell, 1)
                            if current_weight < 9:
                                cell_weights[cell] = current_weight + 1
                            else:
                                cell_weights[cell] = 1
                            search_initiated = False

                elif event.button == 3 and mouse_x < GRID_WIDTH:  # Right click in grid
                    if cell in obstacles:
                        obstacles.remove(cell)
                    elif cell_weights.get(cell, 1) > 1:
                        del cell_weights[cell]

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_held_down = False
            elif event.type == pygame.MOUSEMOTION and mouse_held_down and selected_button == 2:
                mouse_x, mouse_y = event.pos
                if mouse_x < GRID_WIDTH:
                    grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
                    cell = (grid_x, grid_y)
                    if cell != start_point and cell != finish_point:
                        obstacles.add(cell)
                        cell_weights.pop(cell, None)

        if not search_initiated:
            screen.fill(BACKGROUND_COLOR)
            draw_grid()
            draw_buttons(buttons, selected_button)
            for cell, weight in cell_weights.items():
                if weight > 1 and cell not in obstacles and cell != start_point and cell != finish_point:
                    draw_cell(cell, WEIGHT_COLOR)

            # Draw obstacles on top of weighted cells
            for obstacle in obstacles:
                draw_cell(obstacle, OBSTACLE_COLOR)

            # Draw start and finish points on top of everything
            if start_point:
                draw_cell(start_point, START_COLOR)
            if finish_point:
                draw_cell(finish_point, FINISH_COLOR)

            # Draw weight values
            draw_weights(cell_weights)

            # Draw instructions
            for i, instruction in enumerate(instructions):
                text = font.render(instruction, True, TEXT_COLOR)
                screen.blit(text, (GRID_WIDTH + 20, HEIGHT - 150 + i * 25))

            # Display algorithm info if available
            if last_algorithm:
                display_algorithm_time(last_execution_time, last_algorithm)

        pygame.display.flip()

    FPS = 60
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)


if __name__ == "__main__":
    asyncio.run(main())
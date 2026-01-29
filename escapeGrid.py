import pygame
import time
import sys
from utils import Problem
from uninformedSearch import *
from informedSearch import *

class EscapeGrid(Problem):
    def __init__(self, initial, goal, grid):
        super().__init__(initial, goal)
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def actions(self, state):
        x, y = state
        moves = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                if self.grid[nx][ny] == 0 or (nx, ny) == self.goal:
                    moves.append((nx, ny))
        return moves

    def result(self, state, action):
        return action

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):
        x1, y1 = node.state
        x2, y2 = self.goal
        return abs(x1-x2) + abs(y1-y2)

ROWS, COLS = 10, 10
cell = 50
header = 60
width = COLS * cell
height = ROWS * cell + header

grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
START = (0,0)
GOAL = (9,9)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Escape Room AI Search - Smooth")

white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
green = (0,200,0)
yellow = (255,200,0)
gray = (180,180,180)
blue = (0,0,200)

font = pygame.font.SysFont(None, 36)
small = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

def draw_grid(current=None, path=[], algo_name="EDIT MODE", agent_pos=None):
    screen.fill(white)
    pygame.draw.rect(screen, (220,220,220), (0,0,width,header))

    title = font.render(f"Algorithm: {algo_name}", True, black)
    help_text = small.render(
        "Left click: wall | S: start | G: goal | SPACE: run", True, black
    )
    screen.blit(title, (10,10))
    screen.blit(help_text, (10,35))

    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(j*cell, i*cell+header, cell, cell)
            if grid[i][j] == 1:
                pygame.draw.rect(screen, black, rect)
            else:
                pygame.draw.rect(screen, gray, rect, 1)

            if (i,j) in path:
                pygame.draw.rect(screen, yellow, rect)

            if (i,j) == current:
                pygame.draw.rect(screen, red, rect)

            if (i,j) == START:
                pygame.draw.rect(screen, blue, rect)

            if (i,j) == GOAL:
                pygame.draw.rect(screen, green, rect)

    if agent_pos is not None:
        pygame.draw.rect(screen, red, (*agent_pos, cell, cell))

    pygame.display.flip()

def animate_smooth(path, name):
    if not path:
        return
    agent_pos = [START[1]*cell, START[0]*cell + header]  # x, y

    draw_grid(path=path, algo_name=name, agent_pos=agent_pos)
    pygame.time.delay(200)

    for step in path:
        target_pos = [step[1]*cell, step[0]*cell + header]
        frames = 10
        dx = (target_pos[0] - agent_pos[0]) / frames
        dy = (target_pos[1] - agent_pos[1]) / frames

        for _ in range(frames):
            agent_pos[0] += dx
            agent_pos[1] += dy
            draw_grid(path=path, algo_name=name, agent_pos=agent_pos)
            pygame.time.delay(30)  # delay per frame

    draw_grid(path=path, algo_name=name, agent_pos=target_pos)
    pygame.time.delay(200)

def run_algorithms():
    problem = EscapeGrid(START, GOAL, grid)
    algorithms = [
        ("BFS", breadth_first_graph_search(problem)),
        ("DFS", depth_first_graph_search(problem)),
        ("UCS", uniform_cost_search(problem)),
        ("Greedy", greedy_best_first_graph_search(problem)),
        ("A*", astar_search(problem)),
    ]

    for name, result in algorithms:
        if result is None:
            print(f"{name}: No solution found!")
            draw_grid(algo_name=f"{name} - NO SOLUTION")
            pygame.time.delay(1000)
        else:
            animate_smooth(result.solution(), name)

def main():
    global START, GOAL
    running = True
    draw_grid()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            x, y = pygame.mouse.get_pos()
            if y > header:
                row = (y-header)//cell
                col = x//cell
                state = (row, col)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and state != START and state != GOAL:
                    grid[row][col] = 1 - grid[row][col]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    START = state
                if event.key == pygame.K_g:
                    GOAL = state
                if event.key == pygame.K_SPACE:
                    run_algorithms()

        draw_grid()

if __name__ == "__main__":
    main()

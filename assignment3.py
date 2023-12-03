from sys import argv

def main():
    if len(argv) != 2:
        print("Invalid Input")
        return 1

    # load file into a list
    with open(argv[1], "r") as finput:
        lines = finput.readlines()
        grid = make_list(lines)

    # start game into a loop, stop when game over
    game_over = False
    score = 0
    while game_over == False:
        print_grid(grid, score)
        pos_x, pos_y = get_input_pos(grid)
        del_pos = check_neighbors(grid, pos_x, pos_y)

        if len(del_pos) < 2:
            print("No movement happened try again\n")
            continue

        score = score_count(grid, del_pos, score)
        grid = del_cells(grid, del_pos)
        game_over = check_game_over(grid)
    
    print_grid(grid, score)
    print("\nGame Over")

        
def make_list(lines):
    grid = []

    for line in lines:
        values = line.strip().split()
        values = [int(val) for val in values]
        grid.append(values)
    
    return grid

def print_grid(grid, score):
    for line in grid:
        for num in line:
            print(num, end=" ")
        print()
    print(f"\nYour score is: {score}")


def get_input_pos(grid):
    while True:
        pos_input = input(str("\nPlease enter a row and a column number: "))
        print()

        try:
            pos_x_str, pos_y_str = pos_input.split()
            pos_x = int(pos_x_str) - 1
            pos_y = int(pos_y_str) - 1
        except ValueError:
            print("Please enter a correct position!")
            continue
        if pos_x > len(grid) or pos_y > len(grid[0]):
            print("Please enter a correct size!")
            continue
        if grid[pos_x][pos_y] == " ":
            print("please Enter a correct position!")
            continue

        break
    
    return pos_x, pos_y

def check_neighbors(grid, pos_x, pos_y, del_pos=None):
    if del_pos is None:
        del_pos = set()

    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    
    for dir_x, dir_y in directions:
        new_x, new_y = pos_x + dir_x, pos_y + dir_y
        if (0 <= new_x < len(grid) and
            0 <= new_y < len(grid[0]) and
            grid[new_x][new_y] == grid[pos_x][pos_y] and
            (new_x, new_y) not in del_pos):
            del_pos.add((new_x, new_y))
            check_neighbors(grid, new_x, new_y, del_pos)

    return sorted(del_pos)

def del_cells(grid, del_pos):
    if del_pos == None:
        print("Please enter a correct position!")
        return grid
    
    if len(del_pos) < 2:
        print("No movement happened try again")
        return grid

    for row, col in del_pos:
        grid[row][col] = " "
        for i in range(row, 0, -1):
            grid[i][col] = grid[i-1][col]
        grid[0][col] = " "

    return grid

def score_count(grid, del_pos, score):
    if not del_pos:
        return score
    
    for row, col in del_pos:
        score += grid[row][col]
    return score

def check_game_over(grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == " ":
                continue
            if check_neighbors(grid, row, col):
                return False
    return True

main()
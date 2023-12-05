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
        del_pos = check_neighbors(grid, pos_x, pos_y) # get positions of cells that will be deleted

        # if there is only 1 cell to delete, then delete nothing
        if len(del_pos) < 2:
            print("No movement happened try again\n")
            continue

        score = score_count(grid, del_pos, score)
        grid = del_cells(grid, del_pos) # delete cells according to the positions previously aquired
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
    # get input through a loop until a correct input is given
    while True:
        pos_input = input(str("\nPlease enter a row and a column number: "))
        print()

        # check if input is integer
        try:
            pos_x_str, pos_y_str = pos_input.split()
            pos_x = int(pos_x_str) - 1
            pos_y = int(pos_y_str) - 1
        except ValueError:
            print("Please enter a correct position!")
            continue
        
        # check if input is correct size
        if pos_x > len(grid) or pos_y > len(grid[0]):
            print("Please enter a correct size!")
            continue

        # check if input is not a blank cell
        if grid[pos_x][pos_y] == " ":
            print("please Enter a correct position!")
            continue

        break
    
    return pos_x, pos_y

def check_neighbors(grid, pos_x, pos_y, del_pos=None):
    if del_pos is None:
        del_pos = set()

    # directions for left, right, top, bottom of cell
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    
    for dir_x, dir_y in directions:
        new_x, new_y = pos_x + dir_x, pos_y + dir_y
        if (0 <= new_x < len(grid) and
            0 <= new_y < len(grid[0]) and
            grid[new_x][new_y] == grid[pos_x][pos_y] and
            (new_x, new_y) not in del_pos):
            del_pos.add((new_x, new_y))
            check_neighbors(grid, new_x, new_y, del_pos) # recurse for all possible neighbors

    return sorted(del_pos)

def del_cells(grid, del_pos):
    # loop through all del_pos and delete their values
    for row, col in del_pos:
        grid[row][col] = " "
        for i in range(row, 0, -1):
            grid[i][col] = grid[i-1][col]
        grid[0][col] = " "

    # move columns to the left if there is an empty columns
    for col in range(len(grid[0])):
        del_col = True
        for row in range(len(grid)):
            if grid[row][col] != " ":
                del_col = False
        if del_col == True:
            for i in range(col, len(grid[0])):
                for row in range(len(grid)):
                    if i != len(grid[0]) - 1:
                        grid[row][i] = grid[row][i+1]
                    else:
                        grid[row][i] = " "

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
            if check_neighbors(grid, row, col): # check if there is any possible solvable cells left
                return False
    return True

main()
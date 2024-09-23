import time
import random

# def initialize_board():
#     board = [[" " for _ in range(7)] for _ in range(6)]

#     # Add a 2-by-3 block of obstructed cells at the bottom
#     obstructed_row = 4  # Place it at the bottom
#     obstructed_col = random.randint(0, 4)                                                                     #This was the code for the task to get it to randomly generate a 2 by 3 block of obstructed cells 
#     for i in range(2):
#         for j in range(3):
#             board[obstructed_row + i][obstructed_col + j] = "B"  # "B" represents an obstructed cell

#     return board





def initialize_board(obstructed_rows, obstructed_cols):
    board = [[" " for _ in range(7)] for _ in range(6)]         # This will create the 2D board using the parameters inputted (7 and 6)

    # Add an obstructed block at the bottom
    obstructed_row = 6 - obstructed_rows  # Place it at the bottom
    obstructed_col = random.randint(0, 7 - obstructed_cols)                                                     #This is the user defined obstructed block of cells (Advanced Functionality)
    
    for i in range(obstructed_rows):
        for j in range(obstructed_cols):
            board[obstructed_row + i][obstructed_col + j] = "B"  # "B" represents an obstructed cell

    return board


def print_board(board):
    for row in board:
        print("|", end="")          # This is using the outer loop to create the rows 
        for cell in row:
            print(f" {cell} |", end="")         # This is using the inner loop to seperate the cells 
        print("\n" + "-" * 29)


def make_move(board, column, player, special_disc):
    for row in range(5, -1, -1):                            # This checks the rows in reverse order (from 5 to 0) as it need to check the bottom row first before moving upwards
        if board[row][column] == " ":                   # Checks to see if the row and colummn is empty
            board[row][column] = player
            if special_disc:
                remove_adjacent_discs(board, row, column)       # If the special disc is turned true it will run this (reMoving adjacent discs)
            break


def remove_adjacent_discs(board, row, col):
    for i in range(-1, 2):                      # This iterates over the rows of a 3x3 grid created
        for j in range(-1, 2):                  # This iterates over the columns of the 3x3 grid created
            new_row, new_col = row + i, col + j
            if 0 <= new_row < 6 and 0 <= new_col < 7 and board[new_row][new_col] != "B":            # It makes sure its not going to remove a cell that contains B because thats an obstructed cell
                board[new_row][new_col] = " "


def count_four_in_a_row(board, player):
    count = 0

    # Check horizontal
    for row in board:
        for col in range(4):
            if all(row[col + i] == player for i in range(4)):
                count += 1

    # Check vertical
    for col in range(7):
        for row in range(3):
            if all(board[row + i][col] == player for i in range(4)):
                count += 1

    # Check diagonal (bottom-left to top-right)
    for row in range(3, 6):
        for col in range(4):
            if all(board[row - i][col + i] == player for i in range(4)):
                count += 1

    # Check diagonal (top-left to bottom-right)
    for row in range(3):
        for col in range(4):
            if all(board[row + i][col + i] == player for i in range(4)):
                count += 1

    return count


# This checks whether or not the board is full
def is_board_full(board):
    return all(cell != " " for row in board for cell in row)


# This swutches the players go one after each other
def switch_player(current_player):
    return "O" if current_player == "X" else "X"


def play_connect4():
    global current_player
    global obstruction_size  # Declaring obstruction_size as a global variable

    # Allow the user to enter the size of the obstruction block
    while True:
        try:
            print ("Welcome to Daniel's connect four, please enjoy and let the best player win! \n")            # A welcoming input so the users know they have entered the game and what it is
            obstruction_rows = int(input("Enter the number of rows for the obstruction block (1-6): "))
            obstruction_cols = int(input("Enter the number of columns for the obstruction block (1-7): "))      # The advanced functionality input
            
            if 1 <= obstruction_rows <= 6 and 1 <= obstruction_cols <= 7:
                break
            else:
                print("Invalid size. Please enter valid numbers.")              # Validation to ensure the users dont enter a value bigger than the grid itself
        except ValueError:
            print("Invalid input. Please enter numbers.")

    obstruction_size = (obstruction_rows, obstruction_cols)
    board = initialize_board(*obstruction_size)
    scores = {"X": 0, "O": 0}                                   # The starting scores for each player
    current_player = "X"                                        # The player which will start the game
    special_disc_used = {"X": False, "O": False}                # Checking whether the special disc has been used yet or not


    # The user getting the choice of wanting to play the special disc or not
    def get_special_disc_input(player):
        if not special_disc_used[player]:
            while True:
                try:
                    choice = input(f"Player {player}, do you want to place a special disc? (yes/no): ").lower()         # asking the user if they want to play their disc, using lower to avoid an error if they use capital letters o spell yes or no
                    print()
                    if choice == "yes":
                        special_disc_used[player] = True        # Makes the speical disc active by turning it to true
                        return True
                    elif choice == "no":
                        return False                            # Keeps the special disc status at false
                    else:
                        print("Invalid choice. Please enter 'yes' or 'no'.")            # validation checking
                except ValueError:
                    print("Invalid input. Please enter 'yes' or 'no'.")
        else:
            print(f"Player {player}, you have already used your special disc.")         # This appears once the user has already played their special disc so they know they have used it
            print()
            return False


    def get_column_input(player):
        start_time = time.time()        # creates the timer to start 
        column_input = None

        while column_input is None:
            try:
                column = int(input(f"Player {player}, choose a column (1-7): ")) - 1        # This input comes to the user at the start of their go

                # Check if the chosen column is valid
                if 0 <= column < 7 and board[0][column] == " ":             # Makes sure it is between the columns and rows and is empty 
                    column_input = column
                else:
                    print("\nInvalid move. Try again.")                     # Validation checking
            except ValueError:
                print("\nInvalid input. Please enter a number.")

            # Check if 5 seconds have elapsed
            if time.time() - start_time >= 5:           # Checks to see if time has gone over the 5 second period
                print(f"\nPlayer {player} took too long to make a move. Switching to Player {'O' if player == 'X' else 'X'}.\n")            # Tells the user they have took too long and will now switch to the next player
                return None

        return column_input


    def player_turn():
        global current_player

        print_board(board)
        print(f"Current Points Tally - Player X: {scores['X']} | Player O: {scores['O']} \n")           # This shows the current score for each player

        made_move = False           # Keeps track of whether a move has been made, currently set to false
        special_disc = get_special_disc_input(current_player)
        column = get_column_input(current_player)

        if column is not None:
            make_move(board, column, current_player, special_disc)

            # Check for a new instance of the winner
            if count_four_in_a_row(board, current_player) > scores[current_player]:
                print_board(board)
                print(f"Player {current_player} wins this round!")      
                scores[current_player] += 1

            # Switch players
            current_player = switch_player(current_player)
            made_move = True                                # Uses the made_move in order to switch the player

        return made_move

    while not is_board_full(board):
        move_made = player_turn()               # Will get the players turn and check if a move is made as long as the board isnt full

        # Check if a move was made within the time limit, otherwise switch players
        if not move_made:
            current_player = switch_player(current_player)

    print_board(board)
    print("The game is over!")
    print()

    # Display the final points tally
    print(f"Final Points Tally - Player X: {scores['X']} | Player O: {scores['O']}")
    print()

    # Determine the winner based on points
    if scores["X"] > scores["O"]:
        print(f"Player X wins with {scores['X']} points!")
    elif scores["O"] > scores["X"]:
        print(f"Player O wins with {scores['O']} points!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_connect4()
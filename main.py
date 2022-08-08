import random


def get_state(n: int) -> list:
    i: int = 0
    remainders: list[int] = [0 for i in range(9)]
    while n!= 0:
        r = int(n % 3)
        remainders[i] = r
        n = (n-r) / 3
        i += 1
    return remainders

def get_index(state: list) -> int:
    index: int = 0
    state_len: int = len(state)
    for i in range(state_len):
        index += state[i]*3**i
    return index

def get_possible_states(state: list, player: int) -> list:
    possible_states: list = []
    state_len: int = len(state)
    for i in range(state_len):
        temp: list[int] = state.copy()
        if state[i] == 0:
            temp[i] = player+1
            possible_states.append(temp)
    return possible_states

def train_choice(state: list, state_values: list, player: int, game_num: int) -> list:
    exploit: float
    if player == 0:
        exploit = 1-1/game_num
    else:
        exploit = 1-1/game_num
        
    value: float = random.uniform(0, 1)
    possible_states: list = get_possible_states(state, player)
    ps_len: int = len(possible_states)
    
    if value < exploit:
        indices: list = [get_index(state) for state in possible_states]
        possible_values: list = [state_values[index] for index in indices]
        best_index: int = possible_values.index(max(possible_values))
        return possible_states[best_index]
    else:
        index: int = random.randint(0, ps_len-1)
        return possible_states[index]

def choice(state: list, state_values: list, player: int) -> list:
    exploit: float = 0.92
    value: float = random.uniform(0, 1)
    possible_states: list = get_possible_states(state, player)
    ps_len: int = len(possible_states)
    
    if value < exploit:
        indices: list = [get_index(state) for state in possible_states]
        possible_values: list = [state_values[index] for index in indices]
        best_index: int = possible_values.index(max(possible_values))
        return possible_states[best_index]
    else:
        index: int = random.randint(0, ps_len-1)
        return possible_states[index]

def is_endgame(state: list) -> int:
    diag1: list = [[state[4*i] for i in range(3)]]
    diag2: list = [[state[2*i] for i in range(1, 4)]]
    cols: list = [[state[i+3*j] for j in range(3)] for i in range(3)]
    rows: list = [[state[3*i+j] for j in range(3)] for i in range(3)]
    winning_lines = cols+rows+diag1+diag2
    
    for line in winning_lines:
        if line[0] != 0:
            ref = [line[0] for i in range(3)]
            if ref == line:
                return line[0]-1
                
    if 0 not in state:
        return 2

    return 3

def update(game, state_values, reward):
    for state in game:
        state_values[get_index(state)] += reward
    return state_values

def display_game(game: list) -> None:
    print('', flush=True, end='\r')
    print('*'*11, '\n')
    for state in game:
        rows: list = [[state[3*i+j] for j in range(3)] for i in range(3)]

        for row in rows:
            for e in row:
                if e == 0:
                    print(" -", end='  ')
                elif e == 1:
                    print(" O", end='  ')
                else:
                    print(" X", end='  ')
            print('\n')
        print('')
        print('*'*11)
    

def train_play(board_states: list, state_values: list, num_of_games: int) -> None:
    game: list = []
    player0_moves: list = []
    player1_moves: list = []
    game_num: int = 1
    player0_wins: int = 0
    player1_wins: int = 0

    while game_num < num_of_games:
        game = []
        player0_moves = []
        player1_moves = []
        player: int = random.randint(0, 1)
        blank_state: list = [0 for i in range(9)]
        current_state: list = train_choice(blank_state, state_values, player, game_num)
        outcome: int = is_endgame(current_state)
        game.append(current_state)
        if player == 0:
            player0_moves.append(current_state)
        else:
            player1_moves.append(current_state)
    
        while outcome == 3:
            player = (player+1) % 2
            current_state = train_choice(current_state, state_values, player, game_num)
            outcome = is_endgame(current_state)
            game.append(current_state)
            if player == 0:
                player0_moves.append(current_state)
            else:
                player1_moves.append(current_state)
    
        if outcome == 0:
            player0_wins += 1
            state_values = update(player0_moves, state_values, 0.15)
            state_values = update(player1_moves, state_values, -0.2)
        else:
            if outcome == 1:
                player1_wins += 1  
                state_values = update(player0_moves, state_values, -0.2)
                state_values = update(player1_moves, state_values, 0.15)
            else:
                state_values = update(player0_moves, state_values, -0.015)
                state_values = update(player1_moves, state_values, -0.015)
            
        #if game_num+5 > num_of_games:
        #    print('+'*10)
        #    display_game(game)
        print("PLAYER 0: {:.2f} | PLAYER 1: {:.2f}".format(player0_wins/game_num, player1_wins/game_num), flush=True, end='\r')
        game_num += 1
    print('')
    return state_values

def play(board_states, state_values):
    play_again = 'y'
    while play_again == 'y':
        player0_moves: list = []
        player: int = random.randint(0, 1)
        blank_state: list = [0 for i in range(9)]
    
        if player == 1:
            display_game([blank_state])
            move = input("Enter your move: ")
            move = [int(m) for m in move.split(" ")]
            current_state = blank_state.copy()
            index = [move[i]*3**i for i in range(len(move))]
            current_state[sum(index)] = 2
        else:
            current_state: list = choice(blank_state, state_values, player)
            player0_moves.append(current_state)
            display_game([current_state])
    
        outcome: int = is_endgame(current_state)
    
        while outcome == 3:
            player = (player+1) % 2
            if player == 1:
                #invalid_move = False
                #while not invalid_move:
                move = input("Enter your move: ")
                move = [int(m) for m in move.split(" ")]
                index = [move[i]*3**i for i in range(len(move))]        
                current_state[sum(index)] = 2
                outcome = is_endgame(current_state)
                
                
            else:
                current_state = choice(current_state, state_values, player)
                outcome = is_endgame(current_state)
                player0_moves.append(current_state)
            
            display_game([current_state])
    
        if outcome == 0:
            state_values = update(player0_moves, state_values, 10)
        else:
            if outcome == 1:
                state_values = update(player0_moves, state_values, -12)
            else:
                state_values = update(player0_moves, state_values, -5)
    
        play_again = input("PLAY AGAIN: ")

    
    
def main() -> None:
    total_states: int = sum([2*3**i for i in range(9)])+1
    state_values: list[int] = [0 for i in range(total_states)]
    board_states: list = [get_state(i) for i in range(total_states)]

    print("TRAINING ...\n")
    state_values = train_play(board_states, state_values, 200)
    print("STARTING GAME\n", '+'*11)
    play(board_states, state_values)
    

if __name__ == "__main__":
    main()
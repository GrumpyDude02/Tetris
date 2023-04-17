import enum

class GameStates(enum.Enum):
    initilized="initilized"
    main_menu="main_menu"
    in_game="in_game"
    paused="paused"
    game_over="game_over"
    quitting="quitting"
    resetting="resetting"
    changing_res="changing_res"
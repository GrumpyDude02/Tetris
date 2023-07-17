import enum


class GameStates(enum.Enum):
    initilized = "initilized"
    main_menu = "main_menu"
    selection_menu = "selection_menu"
    practice = "practice"
    custom = "custom"
    Tetris = "Tetris"
    paused = "paused"
    game_over = "game_over"
    in_settings = "in_settings"
    quitting = "quitting"
    resetting = "resetting"
    changing_res = "changing_res"

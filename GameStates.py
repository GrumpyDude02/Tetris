import enum


class GameStates(enum.Enum):
    initilized = "initilized"
    main_menu = "main_menu"
    selection_menu = "selection_menu"
    practice_settings = "practice_settings"
    practice_game = "practice_game"
    custom_settings = "custom_settings"
    custom_game = "custom_game"
    classic_settings = "classic_settings"
    Tetris = "Tetris"
    paused = "paused"
    game_over = "game_over"
    in_settings = "in_settings"
    quitting = "quitting"
    resetting = "resetting"
    changing_res = "changing_res"

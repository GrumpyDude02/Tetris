import enum


class GameStates(enum.Enum):
    initilized = "initilized"
    main_menu = "main_menu"
    selection_menu = "selection_menu"
    in_settings = "in_settings"

    practice_settings = "practice_settings"
    practice_game = "practice_game"

    custom_settings = "custom_settings"
    custom_game = "custom_game"

    classic_settings = "classic_settings"
    Tetris = "Tetris"

    dig_settings = "dig_settings"
    dig_mode = "dig_mode"

    paused = "paused"
    game_over = "game_over"

    quitting = "quitting"
    resetting = "resetting"
    changing_res = "changing_res"

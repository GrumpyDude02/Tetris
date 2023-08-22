import enum


class GameStates(enum.Enum):
    initilized = "initilized"
    main_menu = "main_menu"
    selection_menu = "selection_menu"
    in_settings = "in_settings"

    video_settings = "video_settings"
    sound_settings = "sound_settings"
    controls_settings = "controls_settings"

    practice_settings = "practice_settings"

    custom_settings = "custom_settings"

    classic_settings = "classic_settings"

    dig_settings = "dig_settings"

    game = "game"

    paused = "paused"
    game_over = "game_over"

    quitting = "quitting"
    resetting = "resetting"
    changing_res = "changing_res"

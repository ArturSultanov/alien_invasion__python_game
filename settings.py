class Settings():
    """Class for saving settings of the game."""

    def __init__(self):
        """Initializes game settings. """
        # Screen parameters
        self.screen_width = 1024
        self.screen_height = 640
        self.bg_color = (40, 10, 50)

        # Ship speed
        self.ship_speed_factor = 10


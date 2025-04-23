import pyautogui

class GuiSettings:
    """ A central location to store settings needed throughout this program."""
    def __init__(self, pct:float =0.75):
        # calculate game size as a percentage of device screen size
        self.__device_width, self.__device_height = pyautogui.size()
        self.screenPct: float = pct

        # calculate scaled screen width & height rounded to a  multiple of 10
        self.__scaled_width: int = int((self.__device_width * self.screenPct // 10) * 10)
        self.__scaled_height: int = int((self.__device_height * self.screenPct // 10) * 10)

    @property
    def device_width(self) -> int:
        """Device width in pixels."""
        return self.__device_width

    @property
    def device_height(self) -> int:
        """Device height in pixels."""
        return self.__device_height

    @property
    def scaled_height(self) -> int:
        """Scaled height in pixels."""
        return self.__scaled_height

    @property
    def scaled_width(self) -> int:
        """Scaled width in pixels."""
        return self.__scaled_width

    @property
    def center_of_device(self) -> tuple:
        """Center of device as an (x, y) tuple"""
        return (self.device_width // 2, self.device_height // 2)

    def __str__(self) -> str:
        return (f'device width: {self.__device_width}, device height: {self.__device_height}'
                f'\n\tscaled width: {self.__scaled_width}, '
                f'scaled height: {self.__scaled_height}, '
                f'Center of device: {self.center_of_device}')

    def __repr__(self) -> str:
        return (f'device width: {self.__device_width}, device height: {self.__device_height}'
                f'\n\tscaled width: {self.__scaled_width}, '
                f'scaled height: {self.__scaled_height}, '
                f'center of device: {self.center_of_device}')
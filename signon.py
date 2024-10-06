import random
import platform
import ctypes
from ctypes import wintypes
from dataclasses import dataclass

@dataclass(frozen=True)
class AnsiConstants:
    pass

@dataclass(frozen=True)
class Colors(AnsiConstants):
    """ANSI colors Constants"""
    RED: str = "\033[31m"
    GREEN: str = "\033[32m"
    YELLOW: str = "\033[33m"
    BLUE: str = "\033[34m"
    MAGENTA: str = "\033[35m"
    CYAN: str = "\033[36m"
    WHITE: str = "\033[37m"

@dataclass(frozen=True)
class AnsiMethods(AnsiConstants):
    """Additional ANSI escapes constants"""
    BOLD: str = "\033[1m"
    UNDERLINE: str = "\033[4m"
    ITALIC: str = "\033[3m"
    RESET: str = "\033[0m"

class ColorMap:
    """Color arg map"""
    color_map = {
        'r': Colors.RED,
        'g': Colors.GREEN,
        'y': Colors.YELLOW,
        'b': Colors.BLUE,
        'm': Colors.MAGENTA,
        'c': Colors.CYAN,
        'w': Colors.WHITE
    }

class SignonTypeDescriptor:
    """Validating and assigning provided color and str object"""
    __slots__ = ["color_map"]

    def __init__(self):
        self.color_map = ColorMap.color_map

    def __get__(self, instance, owner):
        return instance._color, instance._text

    def __set__(self, instance, values):
        if not isinstance(values, tuple):
            raise ValueError("Expected a tuple type")

        if len(values) == 1:
            _text, _color = values[0], None
        elif len(values) == 2:
            _text, _color = values
        else:
            raise ValueError("Expected a tuple with 1 or 2 elements: (string,) or (string, color)")

        if not isinstance(_text, str):
            raise ValueError(f"Must be a string. Got {type(_text).__name__}")

        if _color is not None and _color.lower() not in self.color_map:
            raise ValueError(f"Invalid color type: {_color}")

        instance._text = _text # assigning str object
        instance._color = self.color_map.get(_color.lower()) if _color else None # assigning color if any provided

class Signon:
    """
    Signon mean style on hebrew :-)

    A class to apply ANSI color codes and text styles to a given string for terminal output.

    This class supports applying multiple text styles such as bold, underline, and italic,
    as well as coloring the text with ANSI color codes. It allows for both whole-text coloring 
    and character-by-character random coloring when no specific color is provided.

    Avaible colors: r = red, g = green, y = yellow, c = cyan, b = blue, m = magneta, w = white
    Avaible styles: bold, underline, italic

    Example usage:
        msg = "Hello Rabbit"
        Signon(msg) # Each character of the string colored by random color, no styles
        Signon(msg, 'r') # One colored string (example output: red string)
        Signon(msg, 'c', bold=True) # One colored string with bold style enabled (example output: cyan colored string with bold style enabled)
        Signon(msg, 'g', underline=True) # One colored string with underline style enabled (example output: cyan colored string with underline style enabled)    
        Signon(msg, 'm', italic=True) # One colored string with italic style enabled (example output: magneta colored string with italic style enabled)
        Signon(msg, bold=True, underline=True, italic=True) # Each character colored by random color with all avaible styles enabled (example output: colorful string with bold, underline, and italic  styles enabled)


    Attributes:
        colors (Colors): 
        - An instance of the Colors class containing ANSI color codes.

        methods (AnsiMethods): 
        - An instance of the AnsiMethods class containing ANSI string style codes.

        text (ArgTypeDescriptor): 
        - A descriptor for handling the string and color arguments.

        bold (bool): 
        - A flag to apply bold styling to the string.

        underline (bool): 
        - A flag to apply underline styling to the string.

        italic (bool): 
        - A flag to apply italic styling to the string.

        string (str): 
        - The final styled and colored string ready for output.

        style_prefix (str): 
        - The combined ANSI codes for the specified string styles.

    Methods:
        apply_style_prefix():
        - Constructs the style prefix based on the provided flags.

        apply_color(color, string): 
        - Applies the specified color to the string and resets the style.

        apply_style_and_color(color, string): 
        - Applies both the styles and the color to the string.

        apply_color_and_style_per_char(): 
        - Applies random colors to each character in the string if no specific color is provided.

        colorize(): 
        - The main method that applies the specified styles and colors to the string.

        win_console_method(): 
        - Configures the Windows terminal to support ANSI escape codes.

        __str__(): Returns the final styled and colored string.
    """
    colors = Colors()
    methods = AnsiMethods()
    args = SignonTypeDescriptor()

    def __init__(self, *args, bold: bool = False, underline: bool = False, italic: bool = False):
        self.bold = bold # Bold flag
        self.underline = underline # Underline flag
        self.italic = italic # Italic flag
        self.args = args  # ArgTypeDescriptor handling validation and assignment
        self.string = '' # Final string
        self.style_prefix = '' # Styles prefix holder
        self.apply_style_prefix() # Constructs style prefixes if any
        if platform.system() == "Windows":  # Check if OS is Windows and if yes, use win_console_method
            self.win_console_method()
        
        print(self.__str__())  # prints the msg without additional calls for demo purposes, comment out if need the str

    def apply_style_prefix(self) -> None:
        """Applying provided styles on str object"""        
        if self.bold:
            self.style_prefix += self.methods.BOLD
        if self.underline:
            self.style_prefix += self.methods.UNDERLINE
        if self.italic:
            self.style_prefix += self.methods.ITALIC

    def apply_color(self, color: str, string: str) -> str:
        """Applying color on str object and reset"""
        return color + string + self.methods.RESET

    def apply_style_and_color(self, color: str, string: str) -> None:
        """Applying style and color on str object and reset"""
        self.string += self.style_prefix + self.apply_color(color, string)

    def apply_color_and_style_per_char(self) -> None:
        """Applying style and color on each character of provided str object"""
        _color_values = [value for key, value in self.colors.__dict__.items()]
        for char in self._text:
            if char.isprintable() and not char.isspace():
                _color = random.choice(_color_values)
                self.apply_style_and_color(_color, char)
            else:
                self.string += char

    def colorize(self) -> None:
        """Main method to colorize text and reset"""
        if self._color:
            self.apply_style_and_color(self._color, self._text)
        else:
            self.apply_color_and_style_per_char()


    def win_console_method(self) -> None:
        """Windows API method, loading kernel with ctypes and setting up the console"""
        kl32 = ctypes.windll.kernel32  # Getting the kernel with ctypes
        handle = kl32.GetStdHandle(-11)  # (STD_OUTPUT_HANDLE) -11 standard Windows standard output
        mode = wintypes.DWORD()  # Create an instance of 32-bit unsigned integer datatype
        kl32.GetConsoleMode(handle, ctypes.byref(mode))  # Getting current input mode of a console input buffer from the kernel32.dll
        mode.value |= 0x0004  # Enable virtual terminal processing
        kl32.SetConsoleMode(handle, mode)  # Setting new mode for console with virtual terminal flag enabled

    def __str__(self) -> str:
        self.colorize()
        return self.string.strip()

# How to use
if __name__ == "__main__":
    msg = "Hello world!!!!"
    Signon(msg, 'r', italic=True, underline=True)
    Signon(msg, 'm', italic=True, underline=True)
    Signon(msg, 'c', bold=True, underline=True)
    Signon(msg, 'b', bold=True, underline=True)
    Signon(msg, 'g', bold=True, underline=True)
    Signon(msg, 'y', bold=True, underline=True)
    Signon(msg, 'w', bold=True, underline=True)
    Signon(msg, bold=True, underline=True, italic=True)




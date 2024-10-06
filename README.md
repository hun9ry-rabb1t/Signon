# Signon: Text Styling and Colorizing Tool 🎨

**Signon** is a terminal-based text styling and coloring tool. It allows you to easily apply ANSI color codes and text styles (bold, underline, italic) to strings for visually appealing output. With support for individual characters or whole-text styling, Signon makes it easy to enhance your console output.

## Features ✨

- **Text Colors:** Supports ANSI colors like red, green, blue, yellow, cyan, magenta, white.
- **Text Styles:** Apply bold, italic, or underline to your text.
- **Character-by-Character Coloring:** When no color is provided, each character can be colored randomly.
- **Platform Support:** Works on both Windows and Unix-based systems (enables ANSI codes for Windows).

## Usage 💻

To colorize text, you can use Signon by passing your string along with an optional color and style parameters.

### Example Usage

```python
msg = "Hello, world!"

# Colorize whole text with red
Signon(msg, 'r')

# Apply cyan color with bold styling
Signon(msg, 'c', bold=True)

# Apply yellow color with italic and underline
Signon(msg, 'y', italic=True, underline=True)

# Random colors for each character with all styles (bold, underline, italic)
Signon(msg, bold=True, underline=True, italic=True)
```

### Available Colors
- **r**: Red
- **g**: Green
- **y**: Yellow
- **b**: Blue
- **m**: Magenta
- **c**: Cyan
- **w**: White

### Available Styles
- **bold**: Bold text
- **italic**: Italic text
- **underline**: Underlined text

## Installation 🚀

No additional installation required. Just copy the code to your project and run it in your terminal.

## How it Works

Signon takes a string and applies styling and coloring by combining ANSI codes. It supports both colorizing the whole string or applying random colors per character. On Windows, it automatically configures the console to support ANSI codes.

---

Enjoy styling your terminal output with **Signon**! 🎉
# Matrix Rain 🟩

A colorful "Matrix digital rain" animation for your terminal, built with [Rich](https://github.com/Textualize/rich). Classic green by default, with support for single colors, random multi-color palettes, and multiple glyph sets (katakana, ASCII, binary, symbols).

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Preview

```
セ ナ ナメ      オ  イ ン    ヤ サ マタ セ      チ モ  ヨ ヤ   ロア ラ  ネ
リ          シツ モ
    サ コシ      モ  ア シ    ハ マワムメ ヌ      ホ イ  フ ン   ヨ  ト
カ          マヒ ル
```

## Features

- 🟢 Classic green Matrix-style rain, or any single color you choose
- 🌈 `--multi` mode with a randomized color palette per column
- 🔤 Multiple character sets: katakana (default), ASCII, binary, symbols
- ⚡ Adjustable animation speed
- ⏱️ Optional auto-stop duration
- 🖥️ Automatically sizes to your terminal window

## Installation

```bash
git clone https://github.com/yourusername/matrix-rain.git
cd matrix-rain
pip install -r requirements.txt
```

Or just install the single dependency directly:

```bash
pip install rich
```

## Usage

```bash
python3 matrix_rain.py
```

Press `Ctrl+C` to stop at any time.

### Options

| Flag         | Description                                              | Default    |
|--------------|-----------------------------------------------------------|------------|
| `--color`    | Single color to use (rich color name, e.g. `cyan`)        | `green`    |
| `--multi`    | Use a randomized color palette across columns             | off        |
| `--colors`   | Comma-separated palette used with `--multi`                | see below  |
| `--charset`  | Glyph set: `katakana`, `ascii`, `binary`, `symbols`         | `katakana` |
| `--speed`    | Seconds between frames (lower = faster)                   | `0.05`     |
| `--duration` | Auto-stop after N seconds (omit to run until Ctrl+C)       | none       |

### Examples

```bash
# Classic green rain
python3 matrix_rain.py

# Single custom color
python3 matrix_rain.py --color cyan

# Random colors per column
python3 matrix_rain.py --multi

# Custom color palette
python3 matrix_rain.py --multi --colors green,cyan,magenta,yellow

# ASCII characters instead of katakana
python3 matrix_rain.py --charset ascii

# Faster animation, runs for 10 seconds then stops
python3 matrix_rain.py --speed 0.02 --duration 10
```

## Requirements

- Python 3.8+
- [rich](https://pypi.org/project/rich/)

## License

MIT

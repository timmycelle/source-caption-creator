# source-caption-creator
is a tool for creating, managing and compiling captions/subtitles for the Source Engine.

It takes JSON data as input and outputs .txt, .dat or .kv3 resource files.

> [!NOTE]
> For more information on Closed Captions in the Source Engine, visit the [Valve Developer Community](https://developer.valvesoftware.com/wiki/Closed_Captions).

> [!IMPORTANT]
> The tool is currently only available as cli (converting/compiling only), the GUI version is work-in-progress!

### Conversion procedure
The tool uses an inheritance-based system to build captions. This allows you to define global styles and override them for specific lines.

The system goes as follows:

**1. Data merging**

The program processes each language (e.g. `english`, `german`, etc.) by merging its specific data with the data of the `shared` block.
`shared` is mainly used for colors, general formatting and miscellaneous data that should be *shared* across every language.

Order: shared ➔ language (Language overrides Shared).

**2. Category & Line overrides**

Within a language, lines inherit properties (like color (`clr`) or display names (`dn`)) from their parent category and apply their own on top.

Order: category ➔ line (Line overrides Category).

**3. Line processing**

Once the current line has finished properties, the program takes them and formats them into a caption token that the user can then use.

**Example:**

Input (`*.json`)
```json
{
    "info": "My Epic Portal 2 Mod | 2026 timmycelle",
    "data": {
        "variables": {
            "color1": "#ff00ff",
            "color2": "#ffff00",
            "color3": "#ff0000"
        },
        "subtitles": {
            "shared": {
                "glados": {
                    "clr": "$color1",
                    "lines": {
                        "mod-2-yellow": {
                            "clr": "$color2",
                            "ndn": true
                        },
                        "mod-3-red": {
                            "clr": "$color3",
                            "bold": true
                        }
                    }
                }
            },
            "english": {
                "glados": {
                    "dn": "GLaDOS",
                    "lines": {
                        "mod-1-magenta": { "txt": "I'm magenta." },
                        "mod-2-yellow": { "txt": "I'm yellow and I won't show you my name!" },
                        "mod-3-red": { "txt": "I'm red and I'm...bold?" }
                    }
                }
            }
        }
    }
}
```
Output (`subtitles_english.txt`)
```
"lang"
{
	"Language" "english"
	"Tokens"
	{
		"glados.mod-2-yellow" "<clr:255,255,0>I'm yellow and I won't show you my name!"
		"glados.mod-3-red" "<clr:255,0,0><B>GLaDOS:<B> <B>I'm red and I'm...bold?"
		"glados.mod-1-magenta" "<clr:255,0,255><B>GLaDOS:<B> I'm magenta."
	}
}

// My Epic Portal 2 Mod | 2026 timmycelle

// Generated with source-caption-creator INDEV by timmycelle
// See https://www.github.com/timmycelle/source-caption-creator for more info

```

### Supported keys
|Key|Type|Description|
|-|-|-|
|`txt`|String|The actual caption message.|
|`dn` |String|Display name (Speaker).|
|`ndn`|Bool|If `true`, hides the display name.|
|`clr`|String| Color in `"R,G,B"` or `"#HEX"`.|
|`playerclr`|List|`["client_color", "other_color"]` for specific targeting.|
|`sfx`|Bool|Marks the line as a sound effect.|
|`bold`/`italic`|Bool| Toggles text styling.|
|`len`|Int| Overrides display duration (seconds).|
|`norepeat`|Int|Sets how often a line can repeat.|
|`nocatinkey`|Bool|Removes the `category.` prefix from the output key.|

### Arguments (cli)
|Option(s)|Type|Description|
|-|-|-|
|`-game`|String|Full path to Source Engine game directory | e.g.: `...\Portal 2\portal2_dlc3`|
|`-json`|String|Full path to JSON Caption File|
|`--subtitles-to-kv3`|Flag|(Strata Source) Convert subtitles from JSON to `subtitles_<lang>.kv3`|
|`--closecaptions-to-kv3`|Flag|(Strata Source) Convert closed captions from JSON to `closecaption_<lang>.kv3`|
|`--subtitles-to-txt`|Flag|Convert subtitles from JSON to `subtitles_<lang>.txt`|
|`--closecaptions-to-txt`|Flag|(Strata Source) Convert closed captions from JSON to `closecaption_<lang>.txt`|
|`--subtitles-to-dat`|Flag|Compile converted subtitles (`subtitles_<lang>.txt`) to `subtitles_<lang>.dat`|
|`--closecaptions-to-dat`|Flag|Compile converted closed captions (`closecaption_<lang>.txt`) to `closecaption_<lang>.dat`|

### Building
1. Clone the repository:
`git clone https://github.com/timmycelle/source-caption-creator.git/`
2. Create virtual environment:
`python -m venv venv`
3. Activate virtual environment:
Linux: `source venv/bin/activate` | Windows: `.\venv\Scripts\activate.ps1`
4. Install required modules:
`pip install -r requirements.txt`
5. Install PyInstaller:
`pip install pyinstaller`
6. Create executable(s):
`pyinstaller scc.spec` or `pyinstaller cli.spec`
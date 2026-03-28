# source-caption-creator
is a tool for creating, managing and compiling captions/subtitles for the Source Engine.

It takes JSON data as input and outputs .txt resource files. Optionally, you can then compile the .txt files to .dat that the engine can then use as actual captions in-game.
It also supports Strata Source (.kv3).

> [!NOTE]
> For more information on Closed Captions in the Source Engine, visit the [Valve Developer Community](https://developer.valvesoftware.com/wiki/Closed_Captions).

The tool has two versions:
### Main version (WIP, not usable)
The main version has a GUI for editing, creating and compiling captions.
### CLI version
The CLI version is the console version and only supports converting/compiling. Requires arguments.

## JSON
### Example
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
                        "mod-1-magenta": {
                            "txt": "I'm magenta."
                        },
                        "mod-2-yellow": {
                            "txt": "I'm yellow and I won't show you my name!"
                        },
                        "mod-3-red": {
                            "txt": "I'm red and I'm...bold?"
                        }
                    }
                }
            }
        }
    }
}
```
### Supported keys
|Key|Meaning|Type|Example|Additional Notes|
|-|-|-|-|-|
|`txt`|Caption message|String|`"What's up?"`|-|
|`dn`|Display name|String|`"Wheatley"`|-|
|`ndn`|Don't show display name|Bool|`true`|-|
|`sfx`|Marks line as sound effect|Bool|`true`|-|
|`clr`|Color of the caption|String|`"#ff00ff"` or `"255,0,255"`|RGB and HEX codes are both supported.|
|`playerclr`|Color of the caption depending on whether it is coming from the player or from something else|List|`["255,255,0", "#00ffff"]`|First color is for the client, second color is for anything else. RGB and HEX codes are both supported.|
|`bold`|Turns the caption message bold|Bool|`true`|-|
|`italic`|Turns the caption message italic|Bool|`true`|-|
|`norepeat`|Controls how often a line can be repeated.|Integer|`10`|-|
|`len`|Overrides how long the line will display.|Integer|`5`|-|
|`nocatinkey`|Removes `"<category>."` prefix of line name|Bool|Turns `"glados.mod-1-magenta"` to just `"mod-1-magenta"`|-|
## Arguments (cli)
|Option(s)|Type|Meaning|
|-|-|-|
|`-game`|String|Full path to Source Engine game directory | e.g.: `...\Portal 2\portal2_dlc3`|
|`-json`|String|Full path to JSON Caption File|
|`--subtitles-to-kv3`|Flag|(Strata Source) Convert subtitles from JSON to `subtitles_<lang>.kv3`|
|`--closecaptions-to-kv3`|Flag|(Strata Source) Convert closed captions from JSON to `closecaption_<lang>.kv3`|
|`--subtitles-to-txt`|Flag|Convert subtitles from JSON to `subtitles_<lang>.txt`|
|`--closecaptions-to-txt`|Flag|(Strata Source) Convert closed captions from JSON to `closecaption_<lang>.txt`|
|`--subtitles-to-dat`|Flag|Compile converted subtitles (`subtitles_<lang>.txt`) to `subtitles_<lang>.dat`|
|`--closecaptions-to-dat`|Flag|Compile converted closed captions (`closecaption_<lang>.txt`) to `closecaption_<lang>.dat`|
## Building
1. `git clone https://github.com/timmycelle/source-caption-creator.git/`
2. `python -m venv venv`
3. Linux: `source venv/bin/activate` | Windows: `.\venv\Scripts\activate.ps1`
4. `pip install -r requirements.txt`
5. `pip install pyinstaller`
6. `pyinstaller SCCcli.spec` or `pyinstaller SCC.spec`
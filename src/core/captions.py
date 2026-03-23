from pycaptioncompiler import Subtitles as pycc
from srctools import Keyvalues
import colour

import os
import json as jsonlib

def convert(game: str, json: dict, subtitles: bool = False, captions: bool = False):
    if not "data" in json: return

    def process(type: str):
        if not type in json["data"]: return
        print(f"converting {type}")
        for lang in list(json["data"][type].keys()):
            if not lang == "shared":
                p_txt = os.path.join(game, "resource", f"{type}_{lang}.txt")
                print(lang)
                tokens = Keyvalues("Tokens", [])

                def merge(dict1, dict2):
                    for key, value in dict2.items():
                        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                            merge(dict1[key], value)
                        else:
                            dict1[key] = value
                    return dict1

                data = merge(json["data"][type]["shared"], json["data"][type][lang])

                print(jsonlib.dumps(data, indent=4).encode().decode("unicode-escape"))

                # line conversion
                for char in data:
                    for line in data[char]["lines"]:
                        key = f"{char}.{line}"

                        if "clr" in line_data:
                            clr = line_data["clr"]
                            if "#" in clr: clr = colour.hex2rgb(clr)

                        value = f""

                        print(line)
                        line_data = data[char]["lines"][line]
                        print(line_data)
                        print(f"\"{key}\" \"\"")


                txt = Keyvalues("lang", [Keyvalues("Language", lang), tokens])
                #print(txt)
                #open(p_txt, "w", encoding="utf-16").write(str(txt))

    if subtitles: process("subtitles")
    if captions: process("captions")

def compile(game: str, json: dict, subtitles: bool = False, captions: bool = False):
    if not "data" in json: return

    def process(type: str):
        if not type in json["data"]: return
        print(f"converting {type}")
        for lang in list(json["data"][type].keys()):
            if not lang == "shared":
                p_txt = os.path.join(game, "resource", f"{type}_{lang}.txt")
                p_dat = os.path.join(game, "resource", f"{type}_{lang}.dat")
                dat = pycc.from_path(p_txt)
                open(p_dat, "wb").write(dat.serialize())

    if subtitles: process("subtitles")
    if captions: process("captions")
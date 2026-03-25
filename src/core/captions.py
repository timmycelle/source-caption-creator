from shared import *

from pycaptioncompiler import Subtitles as pycc
from srctools import Keyvalues
import colour

import os
import json as jsonlib

def convert(game: str, json: dict, subtitles: bool = False, captions: bool = False):
    if not "data" in json: return

    def process(type: str):
        if not type in json["data"]: return
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

                #if args.dev: print(jsonlib.dumps(data, indent=4).encode().decode("unicode-escape"))

                # line conversion
                for char in data:
                    char_data = data["char"].pop("lines")
                    for line in data[char]["lines"]:
                        line_data = merge(char_data, data[char]["lines"][line])

                        key = f"{char}.{line}"
                        if "usecharinkey" in line_data:
                            if line_data["usecharinkey"] == False: key = line

                        txt = ""
                        if "txt" in line_data:
                            txt = line_data["txt"]
                        
                        dnbold = True
                        if "dnbold" in line_data:
                            dnbold = line_data["dnbold"]
                        if dnbold: dnbold = "<B>"
                        else: dnbold = ""

                        dn = ""
                        if "dn" in line_data:
                            if "ndn" in line_data and "ndn":
                                dn = f"{dnbold}[{line_data["dn"]}]{dnbold}"
                            else:
                                dn = ""
                        
                        codes = ""
                        if "clr" in line_data:
                            clr = line_data["clr"]
                            if "#" in clr: clr = ",".join(str(int(x * 255)) for x in colour.hex2rgb(clr))
                            codes.__add__(f"<clr:{clr}>")
                        if "bold" in line_data:
                            if line_data["bold"]: codes.__add__("<B>")
                        if "italic" in line_data:
                            if line_data["italic"]: codes.__add__("<I>")

                        value = f"{dn} {codes}{txt}"

                        print(f"finished line \"{key}\"!")
                        #if args.dev: print(f"\"{key}\" \"{value}\"")
                        tokens.append(Keyvalues(key, value))

                txt = Keyvalues("lang", [Keyvalues("Language", lang), tokens])
                #if args.dev: open(p_txt, "w", encoding="utf-16").write(str(txt))
                print(f"finished converting data to '{p_txt}'!")

    if subtitles: process("subtitles")
    if captions: process("captions")

def compile(game: str, json: dict, subtitles: bool = False, captions: bool = False):
    if not "data" in json: return

    def process(type: str):
        if not type in json["data"]: return
        for lang in list(json["data"][type].keys()):
            if not lang == "shared":
                p_txt = os.path.join(game, "resource", f"{type}_{lang}.txt")
                p_dat = os.path.join(game, "resource", f"{type}_{lang}.dat")
                dat = pycc.from_path(p_txt)
                open(p_dat, "wb").write(dat.serialize())
                print(f"finished compiling '{p_txt}' to '{p_dat}'!")

    if subtitles: process("subtitles")
    if captions: process("captions")
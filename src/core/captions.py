from shared import *

from pcslogger import Logger
from pycaptioncompiler import Subtitles as pycc
from srctools import Keyvalues
import colour

import os
import copy
import logging

Logger.RegisterMainApplication(name)

def convert(game: str, json: dict, subtitles: bool = False, closecaption: bool = False):
    if not "data" in json: return

    def process(type: str):
        if not type in json["data"]: return

        def merge(dict1: dict, dict2: dict):
            for key, value in dict2.items():
                if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                    merge(dict1[key], value)
                else:
                    dict1[key] = value
        def insertvariables(value: str):
            if not "variables" in json["data"]: return value
            for variable in json["data"]["variables"]:
                value = value.replace(f"${variable}", json["data"]["variables"][variable])
            return value

        for lang in json["data"][type]:
            if lang == "shared": continue # ignore "shared" dict

            p_txt = os.path.join(game, "resource", f"{type}_{lang}.txt")

            tokens = Keyvalues("Tokens", []) # place for the fisished lines

            data = copy.deepcopy(json["data"][type]["shared"])
            merge(data, json["data"][type][lang])

            # line conversion
            for cat in data:
                cat_data = data[cat] # get data of desired category
                for line in cat_data["lines"]:
                    # copy category data and merge it with data of current line 
                    line_data: dict = copy.deepcopy(cat_data)
                    merge(line_data, cat_data["lines"][line])
                    line_data.pop("lines", None)

                    key = f"{cat}.{line}"

                    if "nocatinkey" in line_data: # removes "<category>." prefix
                        if bool(line_data["nocatinkey"]): key = line
                    txt = "" # actual message of the caption
                    if "txt" in line_data:
                        txt = str(line_data["txt"]).replace("\n", "<br>")
                    dnbold = True
                    if "dnbold" in line_data:
                        dnbold = bool(line_data["dnbold"])
                    if dnbold: dnbold = "<B>"
                    else: dnbold = ""
                    dnitalic = False
                    if "dnitalic" in line_data:
                        dnitalic = bool(line_data["dnitalic"])
                    if dnitalic: dnitalic = "<I>"
                    else: dnitalic = ""
                    dn = ""
                    if "dn" in line_data:
                        dn = f"{dnitalic}{dnbold}{line_data["dn"]}:{dnbold}{dnitalic} "
                        if "ndn" in line_data:
                            if bool(line_data["ndn"]):
                                dn = ""      
                    
                    codes_predn = ""
                    codes_sufdn = ""

                    if "sfx" in line_data:
                        if bool(line_data["sfx"]): codes_predn = f"{codes_predn}<sfx>"
                    if "clr" in line_data:
                        clr = str(line_data["clr"])
                        clr = insertvariables(clr)
                        if "#" in clr: clr = ",".join(str(int(x * 255)) for x in colour.hex2rgb(clr))
                        codes_predn = f"{codes_predn}<clr:{clr}>"
                    if "playerclr" in line_data:
                        playerclr = list(line_data["playerclr"]) # for example: ["#ffff55", "255,0,200"]
                        for color in range(2):
                            color-=1
                            playerclr[color] = insertvariables(playerclr[color])
                            if "#" in playerclr[color]:
                                playerclr[color] = ",".join(str(int(x * 255)) for x in colour.hex2rgb(playerclr[color]))
                        codes_predn = f"{codes_predn}<playerclr:{playerclr[0]}:{playerclr[1]}>"
                    if "bold" in line_data:
                        if bool(line_data["bold"]): codes_sufdn = f"{codes_sufdn}<B>"
                    if "italic" in line_data:
                        if bool(line_data["italic"]): codes_sufdn = f"{codes_sufdn}<I>"
                    if "norepeat" in line_data:
                        codes_predn = f"{codes_predn}<norepeat:{int(line_data["norepeat"])}>"
                    if "len" in line_data:
                        codes_predn = f"{codes_predn}<len:{int(line_data["len"])}>"

                    value = f"{codes_predn}{dn}{codes_sufdn}{txt}"

                    logging.info(f"Finished line '{key}':\n\"{key}\" \"{value}\"\n")
                    tokens.append(Keyvalues(key, value))

            txt = Keyvalues("lang", [Keyvalues("Language", lang), tokens])
            txt = txt.serialise(indent_braces=False)
            for comment in json["info"].split("\n"):
                txt = f"{txt}\n// {comment}"
            txt = f"{txt}\n\n// Generated with {name} by timmycelle\n// See {url} for more info\n"
            open(p_txt, "w", encoding="utf-16").write(txt)
            logging.info(f"Finished converting data to '{p_txt}'!")

    if subtitles: process("subtitles")
    if closecaption: process("closecaption")

def compile(game: str, json: dict, subtitles: bool = False, closecaption: bool = False):
    if not "data" in json: return

    def process(type: str):
        if not type in json["data"]: return
        for lang in list(json["data"][type].keys()):
            if not lang == "shared":
                p_txt = os.path.join(game, "resource", f"{type}_{lang}.txt")
                p_dat = os.path.join(game, "resource", f"{type}_{lang}.dat")
                dat = pycc.from_path(p_txt)
                open(p_dat, "wb").write(dat.serialize())
                logging.info(f"Finished compiling '{p_txt}' to '{p_dat}'!")

    if subtitles: process("subtitles")
    if closecaption: process("closecaption")
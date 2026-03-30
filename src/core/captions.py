from shared import *

from pcslogger import Logger
from pycaptioncompiler import Subtitles as pycc
from srctools import Keyvalues
import colour
import keyvalues3

import os
import copy
import logging
import io

Logger.RegisterMainApplication(name)

def convert(game: str, json: dict, strata: bool = False, subtitles: bool = False, closecaption: bool = False):
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
            p_kv3 = os.path.join(game, "resource", f"{type}_{lang}.kv3")

            # place for the fisished lines
            txt_tokens = Keyvalues("Tokens", [])
            kv3_tokens = {}

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
                    dn = ""
                    if "dn" in line_data:
                        dn = f"{"<b>" if strata else "<B>"}{line_data["dn"]}:{"</b>" if strata else "<B>"} "
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
                        if strata:
                            codes_predn = f"{codes_predn}<font color=\\\"rgb({clr})\\\">"
                        else:
                            codes_predn = f"{codes_predn}<clr:{clr}>"
                    if "playerclr" in line_data:
                        playerclr = list(line_data["playerclr"]) # for example: ["#ffff55", "255,0,200"]
                        for color in range(2):
                            color-=1
                            playerclr[color] = insertvariables(playerclr[color])
                            if "#" in playerclr[color]:
                                playerclr[color] = ",".join(str(int(x * 255)) for x in colour.hex2rgb(playerclr[color]))
                        codes_predn = f"{codes_predn}<playerclr{"=" if strata else ":"}{playerclr[0]}:{playerclr[1]}>"
                    if "bold" in line_data:
                        if bool(line_data["bold"]): codes_sufdn = f"{codes_sufdn}<b>" if strata else f"{codes_sufdn}<B>"
                    if "italic" in line_data:
                        if bool(line_data["italic"]): codes_sufdn = f"{codes_sufdn}<i>" if strata else f"{codes_sufdn}<I>"
                    if "norepeat" in line_data:
                        codes_predn = f"{codes_predn}<norepeat{"=" if strata else ":"}{int(line_data["norepeat"])}>"
                    if "len" in line_data:
                        codes_predn = f"{codes_predn}<len{"=" if strata else ":"}{int(line_data["len"])}>"

                    value = f"{codes_predn}{dn}{codes_sufdn}{txt}"

                    logging.info(f"Finished line '{key}':\n\"{key}\" \"{value}\"\n")
                    if strata:
                        kv3_tokens[key] = value
                    else:
                        txt_tokens.append(Keyvalues(key, value))
            credits = f"// Generated with {name} {ver} by timmycelle\n// See {url} for more info\n"
            if strata:
                kv3 = {
                    "format_version": 0,
                    "language": lang,
                    "tokens": kv3_tokens
                }
                kv3 = keyvalues3.from_value(kv3)
                kv3_output = io.StringIO()
                keyvalues3.write(kv3, kv3_output)
                kv3_output = kv3_output.getvalue()
                kv3 = kv3_output
                if "info" in json:
                    for comment in json["info"].split("\n"):
                        kv3 = f"{kv3}\n// {comment}"
                kv3 = f"{kv3}\n\n{credits}"
                if not os.path.exists(p_kv3): os.makedirs(os.path.dirname(p_kv3), exist_ok=True)
                open(p_kv3, "w", encoding="utf-8").write(kv3)
                logging.info(f"Finished converting {type} to '{p_kv3}'!")
            else:
                txt = Keyvalues("lang", [Keyvalues("Language", lang), txt_tokens])
                txt = txt.serialise(indent_braces=False)
                if "info" in json:
                    for comment in json["info"].split("\n"):
                        txt = f"{txt}\n// {comment}"
                txt = f"{txt}\n\n{credits}"
                if not os.path.exists(p_txt): os.makedirs(os.path.dirname(p_txt), exist_ok=True)
                open(p_txt, "w", encoding="utf-16").write(txt)
                logging.info(f"Finished converting {type} to '{p_txt}'!")

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
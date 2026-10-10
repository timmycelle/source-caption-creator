from shared import *

from pcslogger import Logger
from pycaptioncompiler import Subtitles as pycc
from srctools import Keyvalues
import colour
import keyvalues3

import os
import copy
import io

Logger.RegisterMainApplication(project_name)

def convert(game: str, json: dict, filetype: str, captiontype: str):
    if not "data" in json: return

    if not captiontype in json["data"]: return

    def merge(dict1: dict, dict2: dict):
        for key, value in dict2.items():
            if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                merge(dict1[key], value)
            else:
                dict1[key] = value
    def variable(value: str):
        if not "variables" in json: return value
        for variable in json["variables"]:
            value = value.replace(f"${r"{"}{variable}{r"}"}", json["variables"][variable])
        return value

    for lang in json["data"][captiontype]:
        if lang == "shared": continue # ignore "shared" dict

        p_txt = os.path.join(game, "resource", f"{captiontype}_{lang}.txt")
        p_kv3 = os.path.join(game, "resource", f"{captiontype}_{lang}.kv3")

        # place for the fisished lines
        txt_tokens = Keyvalues("Tokens", [])
        kv3_tokens = {}

        data = {}
        if json["data"][captiontype].get("shared"): data = copy.deepcopy(json["data"][captiontype]["shared"])
        merge(data, json["data"][captiontype][lang])

        # line conversion
        for cat in data:
            cat_data = data[cat] # get data of desired category
            for line in cat_data.get("lines", {}):
                # copy category data and merge it with data of current line 
                line_data: dict = copy.deepcopy(cat_data)
                merge(line_data, cat_data["lines"][line])
                line_data.pop("lines", None)

                key = f"{cat}.{line}"

                if "nocatinkey" in line_data: # removes "<category>." prefix
                    if bool(line_data["nocatinkey"]): key = line
                txt = "" # actual message of the caption
                if "txt" in line_data:
                    txt = variable(str(line_data["txt"]))
                    txt = txt.replace("[b]", "<b>" if filetype == "kv3" else "<B>")
                    txt = txt.replace("[/b]", "</b>" if filetype == "kv3" else "<B>")
                    txt = txt.replace("[i]", "<i>" if filetype == "kv3" else "<I>")
                    txt = txt.replace("[/i]", "</i>" if filetype == "kv3" else "<I>")
                    txt = txt.replace("\n", "<br>" if filetype == "kv3" else "<cr>")
                dn = ""
                if "dn" in line_data:
                    dn = f"{"<b>" if filetype == "kv3" else "<B>"}{variable(line_data["dn"])}:{"</b>" if filetype == "kv3" else "<B>"} "
                    if "ndn" in line_data:
                        if bool(line_data["ndn"]):
                            dn = ""      
                
                codes_predn = ""
                codes_sufdn = ""

                if "sfx" in line_data:
                    sfx = str(line_data["sfx"])
                    if sfx: codes_predn = f"{codes_predn}<sfx>[{sfx}]"
                if "clr" in line_data:
                    clr = variable(str(line_data["clr"]))
                    if "#" in clr: clr = ",".join(str(int(x * 255)) for x in colour.hex2rgb(clr))
                    if filetype == "kv3":
                        codes_predn = f"{codes_predn}<font color=\\\"rgb({clr})\\\">"
                    else:
                        codes_predn = f"{codes_predn}<clr:{clr}>"
                # playerclr wont be supported for kv3 for now
                # due to the current lack of documentation
                # on the format
                if filetype != "kv3":
                    if "playerclr" in line_data:
                        playerclr = list(line_data["playerclr"]) # for example: ["#ffff55", "255,0,200"]
                        for color in range(2):
                            color-=1
                            playerclr[color] = variable(playerclr[color])
                            if "#" in playerclr[color]:
                                playerclr[color] = ",".join(str(int(x * 255)) for x in colour.hex2rgb(playerclr[color]))
                        codes_predn = f"{codes_predn}<playerclr:{playerclr[0]}:{playerclr[1]}>"
                if "bold" in line_data:
                    if bool(line_data["bold"]): codes_sufdn = f"{codes_sufdn}<b>" if filetype == "kv3" else f"{codes_sufdn}<B>"
                if "italic" in line_data:
                    if bool(line_data["italic"]): codes_sufdn = f"{codes_sufdn}<i>" if filetype == "kv3" else f"{codes_sufdn}<I>"
                if "norepeat" in line_data:
                    codes_predn = f"{codes_predn}<norepeat{"=" if filetype == "kv3" else ":"}{int(variable(str(line_data["norepeat"])))}>"
                if "len" in line_data:
                    codes_predn = f"{codes_predn}<len{"=" if filetype == "kv3" else ":"}{int(variable(str(line_data["len"])))}>"

                value = f"{codes_predn}{dn}{codes_sufdn}{txt}"

                print(f"\"{key}\" \"{value}\"")
                if filetype == "kv3":
                    kv3_tokens[key] = value
                else:
                    txt_tokens.append(Keyvalues(key, value))
        credits = f"// Generated with {project_name} {project_ver} by {author_name}\n// See {project_url} for more info\n"
        if filetype == "kv3":
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
            print(f"Finished converting {captiontype} to '{p_kv3}'!")
        else:
            txt = Keyvalues("lang", [Keyvalues("Language", lang), txt_tokens])
            txt = txt.serialise(indent_braces=False)
            if "info" in json:
                for comment in json["info"].split("\n"):
                    txt = f"{txt}\n// {comment}"
            txt = f"{txt}\n\n{credits}"
            if not os.path.exists(p_txt): os.makedirs(os.path.dirname(p_txt), exist_ok=True)
            open(p_txt, "w", encoding="utf-16").write(txt)
            print(f"Finished converting {captiontype} to '{p_txt}'!")

def compile(game: str, json: dict, captiontype: str):
    if not "data" in json: return

    if not captiontype in json["data"]: return
    for lang in list(json["data"][captiontype].keys()):
        if not lang == "shared":
            p_txt = os.path.join(game, "resource", f"{captiontype}_{lang}.txt")
            p_dat = os.path.join(game, "resource", f"{captiontype}_{lang}.dat")
            dat = pycc.from_path(p_txt)
            open(p_dat, "wb").write(dat.serialize())
            print(f"Finished compiling '{p_txt}' to '{p_dat}'!")
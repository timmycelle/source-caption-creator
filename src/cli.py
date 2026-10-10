from shared import *
from core import (
    captions
)

import json

args_group1 = parser.add_argument_group("paths")
args_group1.add_argument("-game", type=str, required=True, help="Full path to Source Engine game directory | e.g.: \"...\\Portal 2\\portal2_dlc3\"")
args_group1.add_argument("-json", "-i", "-input", type=str, required=True, help="Full path to JSON Caption File")
args_group2 = parser.add_argument_group("convert/compile options")
args_group2.add_argument("--to-kv3", "-kv3", action="append", help="(Strata Source) Convert subtitles from JSON to \"subtitles_<lang>.kv3\"")
args_group2.add_argument("--to-txt", "-txt", action="append", help="Convert subtitles from JSON to \"subtitles_<lang>.txt\"")
args_group2.add_argument("--to-dat", "-dat", action="append", help="Compile converted subtitles (\"subtitles_<lang>.txt\") to \"subtitles_<lang>.dat\"")
args = parser.parse_args()

SCC.p_game = args.game
print(f"Game directory: '{SCC.p_game}'")

SCC.p_json = args.json
SCC.json = json.load(open(SCC.p_json, "r", encoding="utf-8"))
print(f"JSON File: '{SCC.p_json}'")

if args.to_kv3:
    for type in args.to_kv3:
        captions.convert(game=SCC.p_game, json=SCC.json, filetype="kv3", captiontype=type)
if args.to_txt:
    for type in args.to_txt:
        captions.convert(game=SCC.p_game, json=SCC.json, filetype="txt", captiontype=args.to_txt)
if args.to_dat:
    for type in args.to_dat:
        captions.compile(game=SCC.p_game, json=SCC.json, captiontype=args.to_dat)
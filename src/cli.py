from shared import *
from core import (
    captions
)

import json
import logging

args_group1 = parser.add_argument_group("paths")
args_group1.add_argument("-game", type=str, required=True, help="Full path to Source Engine game directory | e.g.: \"...\\Portal 2\\portal2_dlc3\"")
args_group1.add_argument("-json", "-i", "-input", type=str, required=True, help="Full path to JSON Caption File")
args_group2 = parser.add_argument_group("convert/compile options")
args_group2.add_argument("--subtitles-to-kv3", "--subs-kv3", action="store_true", help="(Strata Source) Convert subtitles from JSON to \"subtitles_<lang>.kv3\"")
args_group2.add_argument("--closecaptions-to-kv3", "--cc-kv3", action="store_true", help="(Strata Source) Convert closed captions from JSON to \"closecaption_<lang>.kv3\"")
args_group2.add_argument("--subtitles-to-txt", "--subs-txt", action="store_true", help="Convert subtitles from JSON to \"subtitles_<lang>.txt\"")
args_group2.add_argument("--closecaptions-to-txt", "--cc-txt", action="store_true", help="Convert closed captions from JSON to \"closecaption_<lang>.txt\"")
args_group2.add_argument("--subtitles-to-dat", "--subs-dat", action="store_true", help="Compile converted subtitles (\"subtitles_<lang>.txt\") to \"subtitles_<lang>.dat\"")
args_group2.add_argument("--closecaptions-to-dat", "--cc-dat", action="store_true", help="Compile converted closed captions (\"closecaption_<lang>.txt\") to \"closecaption_<lang>.dat\"")
args = parser.parse_args()

if args.game:
    SCC.p_game = args.game
    logging.info(f"Game directory: '{SCC.p_game}'")
if args.json:
    SCC.p_json = args.json
    SCC.json = json.load(open(SCC.p_json, "r", encoding="utf-8"))
    logging.info(f"JSON File: '{SCC.p_json}'")

if args.subtitles_to_kv3: captions.convert(game=SCC.p_game, json=SCC.json, strata=True, subtitles=True)
if args.closecaptions_to_kv3: captions.convert(game=SCC.p_game, json=SCC.json, strata=True, closecaption=True)
if args.subtitles_to_txt: captions.convert(game=SCC.p_game, json=SCC.json, subtitles=True)
if args.closecaptions_to_txt: captions.convert(game=SCC.p_game, json=SCC.json, closecaption=True)
if args.subtitles_to_dat: captions.compile(game=SCC.p_game, json=SCC.json, subtitles=True)
if args.closecaptions_to_dat: captions.compile(game=SCC.p_game, json=SCC.json, closecaption=True)
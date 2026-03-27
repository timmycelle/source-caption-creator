from shared import *
from core import (
    captions
)

import json
import logging

parser.add_argument_group("paths")
parser.add_argument("-game", type=str, required=True, help="Source Engine game directory | e.g. \"Portal 2\\portal2_dlc3\"")
parser.add_argument("-json", "-i", "-input", type=str, required=True, help="Path to JSON Caption File")
parser.add_argument_group("convert/compile options")
parser.add_argument("--convert-subtitles", "--conv-s", action="store_true", help="Convert subtitles from JSON to subtitles_<lang>.txt")
parser.add_argument("--convert-closecaptions", "--conv-c", action="store_true", help="Convert closed captions from JSON to closecaption_<lang>.txt")
parser.add_argument("--compile-subtitles", "--comp-s", action="store_true", help="Compile converted subtitles to subtitles_<lang>.dat")
parser.add_argument("--compile-closecaptions", "--comp-c", action="store_true", help="Compile converted closed captions to closecaption_<lang>.dat")
args = parser.parse_args()

if args.game:
    SCC.p_game = args.game
    logging.info(f"Game directory: '{SCC.p_game}'")
if args.json:
    SCC.p_json = args.json
    SCC.json = json.load(open(SCC.p_json, "r", encoding="utf-8"))
    logging.info(f"JSON File: '{SCC.p_json}'")

if args.convert_subtitles: captions.convert(game=SCC.p_game, json=SCC.json, subtitles=True)
if args.convert_closecaptions: captions.convert(game=SCC.p_game, json=SCC.json, closecaption=True)
if args.compile_subtitles: captions.compile(game=SCC.p_game, json=SCC.json, subtitles=True)
if args.compile_closecaptions: captions.compile(game=SCC.p_game, json=SCC.json, closecaption=True)
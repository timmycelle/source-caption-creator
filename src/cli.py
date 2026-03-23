from shared import *
from core import (
    captions
)

import json

parser.add_argument_group("paths")
parser.add_argument("-game", type=str, help="Source Engine game directory | e.g. \"Portal 2\\portal2\"")
parser.add_argument("-json", "-i", "-input", type=str, help="Path to JSON Caption File")
parser.add_argument_group("convert/compile options")
parser.add_argument("--convert-subtitles", "--conv-s", action="store_true", help="Convert captions from JSON to subtitles_<lang>.txt")
parser.add_argument("--convert-captions", "--conv-c", action="store_true", help="Convert captions from JSON to closecaption_<lang>.txt")
parser.add_argument("--compile-subtitles", "--comp-s", action="store_true", help="Compiles converted subtitles into subtitles_<lang>.dat")
parser.add_argument("--compile-captions", "--comp-c", action="store_true", help="Compiles converted captions into closecaption_<lang>.dat")
args = parser.parse_args()

#if args.compile_captions: args.convert_captions = True
#if args.compile_subtitles: args.convert_subtitles = True

if args.game:
    SCC.p_game = args.game
    print(SCC.p_game)
if args.json:
    SCC.p_json = args.json
    SCC.json = json.load(open(SCC.p_json, "r", encoding="utf-8"))
    print(SCC.p_json)
    #print(SCC.json)

if args.convert_subtitles: captions.convert(game=SCC.p_game, json=SCC.json, subtitles=True)
if args.convert_captions: captions.convert(game=SCC.p_game, json=SCC.json, captions=True)
if args.compile_subtitles: captions.compile(game=SCC.p_game, json=SCC.json, subtitles=True)
if args.compile_captions: captions.compile(game=SCC.p_game, json=SCC.json, captions=True)
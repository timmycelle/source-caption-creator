name = "source-caption-creator"
desc = "Tool for creating, managing and compiling captions/subtitles for Source Engine games."
ver = "INDEV"
url = "https://www.github.com/timmycelle/source-caption-creator"

class SCC:
    json: dict = {}
    p_game: str = ""
    p_json: str

frm = {
    "DEV": "\033[96m",
    "VERBOSE": "\033[90m",
    "INFO": "\033[94m",
    "SUCCESS": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ITALIC": "\033[3m",
    "BOLD": "\033[1m",
    "END": "\033[0m"
}

import argparse

parser = argparse.ArgumentParser(description=f"{frm["BOLD"]}{name}{frm["END"]}\n\n{desc}\nCreated by timmycelle.\nProtected under the MIT License.\n\nSee more at {url}", formatter_class=argparse.RawDescriptionHelpFormatter)

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s :: [%(levelname)s] :: %(message)s")
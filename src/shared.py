from info import *

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

parser = argparse.ArgumentParser(description=f"{frm["BOLD"]}{project_name}{frm["END"]}\n\n{project_desc}\nCreated by {author_name}.\nProtected under the MIT License.\n\nSee more at {project_url}", formatter_class=argparse.RawDescriptionHelpFormatter)
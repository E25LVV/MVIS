#!/usr/bin/env python3
#
# ==========================================================
# McQueen Voice ID Scheduler (MVIS)
# Version 1.0.0
#
# Node : AllStarLink Node 64679
# Author : E25MQ
# ==========================================================

import configparser
import os
import subprocess
import sys
import time
from datetime import datetime


VERSION = "1.0.0"


CONFIG_FILE = "config.ini"


# ----------------------------------------------------------
# Load configuration
# ----------------------------------------------------------

def load_config():

    if not os.path.exists(CONFIG_FILE):
        print(f"Config not found : {CONFIG_FILE}")
        sys.exit(1)

    parser = configparser.ConfigParser()
    parser.read(CONFIG_FILE)

    if "MVIS" not in parser:
        print("Missing [MVIS] section")
        sys.exit(1)

    cfg = {
    "node": parser["MVIS"]["node"],
    "call": parser["MVIS"]["call"],
    "voice_file": parser["MVIS"]["voice_file"],
    "interval": int(parser["MVIS"]["interval"]),
    "asterisk": parser["MVIS"]["asterisk_cmd"],
}

    return cfg


# ----------------------------------------------------------
# Logger
# ----------------------------------------------------------



# ----------------------------------------------------------
# Version
# ----------------------------------------------------------

def show_version():

    print("McQueen Voice ID Scheduler")
    print(f"Version {VERSION}")


# ----------------------------------------------------------
# Status
# ----------------------------------------------------------

def show_status():

    cfg = load_config()

    print("MVIS Status")
    print()

    print(f"Node      : {cfg['node']}")
    print(f"Call      : {cfg['call']}")
    print(f"Interval  : {cfg['interval']} min")
    print(f"Voice     : {cfg['voice_file']}")
    print(f"Asterisk  : {cfg['asterisk']}")
    
    # ----------------------------------------------------------
# Play Voice
# ----------------------------------------------------------

def play_voice():

    cfg = load_config()

    cmd = [
        "sudo",
        cfg["asterisk"],
        "-rx",
        f"rpt localplay {cfg['node']} {cfg['voice_file']}"
    ]

    result = subprocess.run(cmd)

    
        

    if result.returncode == 0:
        return True

    return False


# ----------------------------------------------------------
# Test
# ----------------------------------------------------------

def test():

    print("Testing Voice Playback...")
    print()

    if play_voice():
        print("SUCCESS")
    else:
        print("FAILED")
  # ----------------------------------------------------------
# Run Scheduler
# ----------------------------------------------------------

def run():

    cfg = load_config()

    interval = cfg["interval"] * 60

    print("========================================")
    print(" McQueen Voice ID Scheduler")
    print(f" Version {VERSION}")
    print("========================================")
    print(f"Node      : {cfg['node']}")
    print(f"Call      : {cfg['call']}")
    print(f"Interval  : {cfg['interval']} minute(s)")
    print()

    

    while True:

        play_voice()

        print(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "- waiting",
            cfg["interval"],
            "minute(s)"
        )

        time.sleep(interval)


# ----------------------------------------------------------
# Usage
# ----------------------------------------------------------

def usage():

    print("Usage:")
    print("  mvis version")
    print("  mvis status")
    print("  mvis test")
    print("  mvis run")


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "version":
        show_version()

    elif cmd == "status":
        show_status()

    elif cmd == "test":
        test()

    elif cmd == "run":
        run()

    else:
        usage()
        sys.exit(1)      
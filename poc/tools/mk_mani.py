# mk_mani.py
# Make a manifest out of stuff

import argparse
import json
import os

from copy import copy
from pprint import pprint


def doit(args):

    kicad_full = os.path.join( args.board_dir, args.model, args.kicad_file)
    kicad = json.load(open(kicad_full))

    kicad2 = {
        'buttons': list(zip( kicad['button_labels'], kicad['button_pins'])),
        'leds': list(zip( kicad['led_labels'], kicad['led_pins'] )),
        'adcs': list(zip( kicad['adc_labels'], kicad['adc_pins'] )),
        'pwms': list(zip( kicad['pwm_labels'], kicad['pwm_pins'] )),
        'neos': list(zip( kicad['neo_labels'], kicad['neo_pins'] )),
    }

    kicad_full = os.path.join( args.board_dir, args.model, "kicad2.json" )
    json.dump(kicad2, open(kicad_full, 'w'), indent=2)
    kicad = json.load(open(kicad_full))


    pprint(kicad)

    driver = args.model.title()

    manifest = {
            'model': args.model,
            "main": "edge",
            "driver": driver,
            "init": "init",
            }

    f = open( "{}.py".format(args.model), "w" )
    f.write("from driver import Driver\n\n")
    f.write("class {}(driver):\n\n".format(driver))

    parameters = []
    for label,pin in kicad['buttons']:
        parameters.append(
                { "name": label,
                    "type": "button",
                    "pin": pin,
                    "old_value": None,
                    } )

    inputs = []

    for label in kicad['buttons']:

        name = f"{label}_on"
        inputs.append( { "name": name } )
        f.write(f"    def {name}(self):\n")
        f.write(f"        return self.button_ck( '{label}', 0 )\n\n")

        name = f"{label}_off"
        inputs.append( { "name": name } )
        f.write(f"    def {name}(self):\n")
        f.write(f"        return self.button_ck( '{label}', 1 )\n\n")


    for label in kicad['adcs']:
        name = f"{label}"
        inputs.append( { "name": name,
            "range": {"low":0, "high": 4096}} )
        f.write(f"    def {name}(self):\n")
        f.write(f"        return self.button_ck( '{label}', 1 )\n\n")

    outputs = []

    for label in kicad['leds']:

        name = f"{label}_on"
        outputs.append( { "name": name } )
        f.write(f"    def {name}(self):\n")
        f.write(f"        return self.button_set( '{label}', 0 )\n\n")

        name = f"{label}_off"
        outputs.append( { "name": name } )
        f.write(f"    def {name}(self):\n")
        f.write(f"        return self.button_set( '{label}', 1 )\n\n")

        name = f"{label}_toggle"
        outputs.append( { "name": name } )
        f.write(f"    def {name}(self):\n")
        f.write(f"        return self.button_toggle( '{label}'1 )\n\n")

    manifest['parameters'] = parameters
    manifest['inputs'] = inputs
    manifest['outputs'] = outputs

    pprint(manifest, sort_dicts=False)

    manifest_full = os.path.join(
            args.board_dir, args.model, "manifest.json")
    json.dump(manifest, open(manifest_full, 'w'), indent=2)

    f.close()

    """

led_pins': ['E9', 'E10', 'E12', 'E14', 'D13'],
 'neo_labels': ['NEO_STATUS', 'NEO_STRIP'],
 'neo_num_pixels': [1, 5],
 'neo_pins': ['D8', 'E4'],
 'pwm_labels': ['BUZZER'],
 'pwm_pins': ['A2']}

"""


def get_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("--board_dir", default="boards",
            help="dir of boards")
    parser.add_argument("--model", default="joypad",
            help="board model, dir in boards to find kicad file")
    parser.add_argument("--kicad_file", default="kicad.json",
            help="name of kicad file")

    parser.add_argument("--output", default="manifest.json",
            help="output filename")

    args = parser.parse_args()

    return args

def main():
    args = get_args()
    doit(args)


if __name__ == "__main__":
    main()




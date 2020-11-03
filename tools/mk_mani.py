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

    if "button_labels" in kicad:

        kicad2 = {
            'buttons': list(zip( kicad['button_labels'], kicad['button_pins'])),
            'adcs': list(zip( kicad['adc_labels'], kicad['adc_pins'] )),
            'leds': list(zip( kicad['led_labels'], kicad['led_pins'] )),
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

    py_full = os.path.join(
            args.board_dir, args.model, "{}.py".format(args.model))
    f = open( py_full, "w" )
    f.write("from driver import Driver\n\n")
    f.write("class {}(Driver):\n\n".format(driver))

    # f.write(f"    # parameters \n\n")
    parameters = []
    inputs = []
    outputs = []

    f.write(f"    # buttons:\n\n")

    for label,pin in kicad['buttons']:

        label = label.lower()
        pin = pin.lower()

        parameters.append(
                { "name": label,
                    "type": "button",
                    "pin": pin,
                    "old": None,
                    } )

        name = f"{label}"
        inputs.append( { "name": name } )
        f.write(f"    def {name}(self):\n")
        f.write(f"        return self.button_ck( '{label}' )\n\n")


    f.write(f"    # adcs:\n\n")

    for label,pin in kicad['adcs']:

        label = label.lower()
        pin = pin.lower()

        parameters.append(
                { "name": label,
                    "type": "adc",
                    "pin": pin,
                    "old": None,
                    "noise": 20,
                    } )

        name = f"{label}"
        inputs.append( { "name": name,
            "range": {"low":0, "high": 4096}} )

        f.write(f"    def {name}(self):\n")
        f.write(f"        return self.adc( '{label}' )\n\n")

    f.write(f"    # leds:\n\n")

    for label,pin in kicad['leds']:

        label = label.lower()
        pin = pin.lower()

        parameters.append(
                { "name": label,
                    "type": "led",
                    "pin": pin,
                    "value": 0,
                    "dirty": True,
                    } )

        name = f"{label}"
        outputs.append( { "name": name } )
        f.write(f"    def {name}(self,value):\n")
        f.write(f"        return self.led_set( '{label}', value )\n\n")

    f.write(f"    # pwms:\n\n")

    for label,pin in kicad['pwms']:

        parameters.append(
                { "name": label,
                    "type": "pwm",
                    "pin": pin,
                    "value": 0,
                    "dirty": True,
                    } )

        name = f"{label}"
        outputs.append( { "name": name,
            "range": {"low":0, "high": 4096}} )

        f.write(f"    def {name}(self, value):\n")
        f.write(f"        return self.led_dim( '{label}', value )\n\n")

    f.write(f"    # neos:\n\n")

    for label,pin in kicad['neos']:

        parameters.append(
                { "name": label,
                    "type": "neo",
                    "pin": pin,
                    "value": 0,
                    "dirty": False,
                    } )

        name = f"{label}"
        outputs.append( { "name": name } )
        f.write(f"    def {name}(self, value):\n")
        f.write(f"        return self.neo_play( '{label}', value )\n\n")


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

    parser.add_argument("--board_dir", default="boards/edges",
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




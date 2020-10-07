# mix.py
# mix the map and manifests to make mapo to feed zorg

import argparse
import json
import os

from copy import copy
from pprint import pprint

function_priorities = {
        "high": "FH",
        "medium": "FM",
        "low":"FL",
        }


def doit(args):

    # where the results go:
    mapo = {}

    map_name = os.path.join( args.system_dir, args.name, "map.json")
    map_max = json.load(open(map_name))

    mapo['version'] = map_max['version']

    mapo['boards'] = {}
    boards = map_max['boards']

    # pull in the maifests:
    # make mapo slots
    for key in boards:

        model = boards[key]['model']
        manifest_name = os.path.join( args.board_dir, model, "manifest.json")
        manifest = json.load(open(manifest_name))
        boards[key]['manifest'] = manifest

        mapo['boards'][key] = {
                'inputs': [],
                'outputs': [],
                'parameters': []
                }

        # messy?
        if "heart" in boards[key]:
            mapo[key]["heart"] = boards[key]["heart"]

    # for each map, create a tokenized map half,
    # save each half in its board
    for map_ in map_max['maps']:
        input_ = map_['input']

        board_name = input_['board']
        board = boards[board_name]

        function_name = input_['function']
        function_no = [ d['name'] for d in board['manifest']['inputs'] ].index(function_name)

        # default priority: medium
        channel = function_priorities[ input_.get( 'priority', "medium") ]

        source = {
                "channel": channel,
                "function_no": function_no,
                }

        # messy?
        if "range" in input_:
            source['range'] = input_['range']
        elif "range" in  board['manifest']['inputs'][function_no]:
            source['range'] = board['manifest']['inputs'][function_no]['range']

        mapo['boards'][board_name]['inputs'].append(copy(source))

        source['board_name']=board_name

        print("outputs:")
        for output in map_['outputs']:
            print(output)

            board_name = output['board']
            board = boards[board_name]

            function_name = output['function']
            function_no = [
                    d['name'] for d in board['manifest']['outputs'] ].index(
                            function_name)
            o = {
                'source': source,
                "function_no": function_no,
                }
            # messy?
            if "range" in output:
                o['range'] = output['range']
            elif "range" in  board['manifest']['outputs'][function_no]:
                o['range'] = board['manifest']['outputs'][function_no]['range']

            mapo['boards'][board_name]['outputs'].append(o)

    pprint(map_max)
    print()
    pprint(mapo)

    mapo_name = os.path.join( args.output_dir, "mapo.json")
    json.dump(mapo, open(mapo_name, 'w'), indent=2)


def get_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("--name", default="ls2oh",
            help="dir in systems")

    parser.add_argument("--system_dir", default="systems",
            help="dir of systems")
    parser.add_argument("--board_dir", default="boards",
            help="dir of boards (manifests)")
    parser.add_argument("--output_dir", default="systems",
            help="dir for mapo.json")

    args = parser.parse_args()

    return args

def main():
    args = get_args()
    doit(args)


if __name__ == "__main__":
    main()




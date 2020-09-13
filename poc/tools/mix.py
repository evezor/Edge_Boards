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
    boards = map_max['boards']

    # pull in the maifests:
    # make mapo slots
    for key in boards:
        model = boards[key]['model']
        manifest_name = os.path.join( args.board_dir, model, "manifest.json")
        manifest = json.load(open(manifest_name))
        boards[key]['manifest'] = manifest
        mapo[key] = {
                'inputs': [],
                'outputs': [],
                'parameters': []
                }

    # for each map, create a tokenized map half,
    # save each half in its board
    for m in map_max['maps']:

        board_name = m['input']['board']

        function_name = m['input']['function']
        function_no = boards[board_name]['manifest']['inputs'].index(
                function_name)

        channel = function_priorities[ m['priority'] ]

        source = {
                "channel": channel,
                "function_no": function_no,
                }

        mapo[board_name]['inputs'].append(copy(source))

        source['board_name']=board_name

        for output in m['outputs']:
            output_board_name = output['board']
            function_name = output['function']
            function_no = \
                    boards[output_board_name]['manifest']['outputs'].index(
                    function_name)

            mapo[output_board_name]['outputs'].append( {
                    'source': source,
                    "function_no": function_no,
                    })

    pprint(map_max)
    print()
    pprint(mapo)

    mapo_name = os.path.join( args.output_dir, args.name, "mapo.json")
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



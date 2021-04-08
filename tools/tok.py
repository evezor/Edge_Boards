# tok.py
# tokenize the map and manifests to make mapo to feed zorg

import argparse
import json
import os

from copy import copy
from pprint import pprint

def mk_source(input_, board):

    pprint(board)
    channel = "{type}{priority}".format(**input_)
    function_no = [ d['name'] for d in board['manifest']['inputs'] ].index(input_["input_function_name"])

    source = {
            "channel": channel,
            "function_no": function_no,
            }

    return source


def doit(args):

    # where the results go:
    mapo = {}

    map_name = os.path.join( args.system_dir, args.name, "map.json")
    map_max = json.load(open(map_name))

    mapo['version'] = map_max['version']

    mapo['boards'] = {}
    boards = map_max['boards']

    # pull in the maifests:
    # and make mapo slots
    for board_name in boards:

        model = boards[board_name]['model']
        manifest_name = os.path.join( args.board_dir, model, "manifest.json")
        print(manifest_name)
        manifest = json.load(open(manifest_name))
        pprint(manifest)
        boards[board_name]['manifest'] = manifest

        mapo['boards'][board_name] = {
                'inputs': [],
                'outputs': [],
                'parameters': []
                }

        # messy?
        if "heart" in boards[board_name]:
            mapo[board_name]["heart"] = boards[board_name]["heart"]

    # for each board, tokenize and put in mapo
    for board in boards.values():

        print("inputs:")
        for input_ in board['inputs']:
            print(input_)

            source = mk_source(input_, board)
            """
            channel = "{type}{priority}".format(**input_)
            function_no = [ d['name'] for d in board['manifest']['inputs'] ].index(inputs_["input_function_name"])

            source = {
                    "channel": channel,
                    "function_no": function_no,
                    }
            """

            # messy?
            # not tested either
            function_no = source['function_no']
            if "range" in input_:
                source['range'] = input_['range']
            elif "range" in  board['manifest']['inputs'][function_no]:
                source['range'] = board['manifest']['inputs'][function_no]['range']

            # add to mapo
            mapo['boards'][board_name]['inputs'].append(copy(source))

        # ??? source['board_name']=board_name

        print("outputs:")
        for output in board['outputs']:
            print(output)

            pprint(boards)
            inboard = boards[output['source']['board']]
            # inboard = [b for b in boards if b['manifest']['info']['model'] ==output['source']['board']][0]

            source = mk_source(output['source'], inboard)
            source['board'] = output['source']['board']

            function_no = [
                    d['name'] for d in board['manifest']['outputs'] ].index(
                            output['output_function_name'])
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
    parser.add_argument("--board_dir", default="boards/edges",
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




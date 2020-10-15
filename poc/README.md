board,py: Generic CAN bus abstract class. 2 Children, Zorg and Edge
bundle.py: Bundles bits together into an arbitration ID
deploy.sh: Copies a bunch of files onto carls cardboard box boards (not useful to others)
edge.py: Hosts IRIS. All about translation of messages to talk to the driver. Eg map numbers to function name
main.py: "A very lightweight thing" all it does is look at manifest to figure out if the board in question is a zorg or an edges
ocan.py: OSHBus library. Takes bits and turns them into the appropriate arbitration ID's based on function

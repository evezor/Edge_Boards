# bits.py
# pack values into a bundle of bits

from collections import OrderedDict

bundle = OrderedDict()
bundle["channel"] = 4
bundle["cid"] = 7
bundle["bonus"] = 18

bundle_size = sum(bundle.values())
assert bundle_size == 29


def pack(**kwargs):

    b = 0

    for k in bundle:

        assert 0 <= kwargs[k] < 2 ** bundle[k]

        # move the previous bits out of the way:
        b = b << bundle[k]
        # drop in the new bits:
        b += kwargs[k]

    return b


def show(b):

    bits = "{x:0{width}b}".format(x=b, width=bundle_size)
    # uPython doesn't support this yet:
    # bits = f"{b:0{bundle_size}b}"
    print("bundle:", bits)
    s = 0
    for k in bundle:
        size = bundle[k]
        e = s + size
        print("{}: {}".format(k, bits[s:e]))
        s += size


def unpack(b):

    r = {}
    keys = list(bundle.keys())
    keys.reverse()
    for k in keys:

        r[k] = b & (2 ** bundle[k] - 1)
        b = b >> bundle[k]

    return r


def show_it():

    def check(channel, cid, bonus):
        b = pack(channel=channel, cid=cid, bonus=bonus)
        show(b)
        print(unpack(b))

    # little numbers:
    check(1, 2, 3)

    # all the bits:
    check(channel=2 ** bundle["channel"] - 1,
            cid=2 ** bundle["cid"] - 1,
            bonus=2 ** bundle["bonus"] - 1)

    # one too many bits:
    check(2 ** bundle["channel"], 0,0)

if __name__=='__main__':
    show_it()

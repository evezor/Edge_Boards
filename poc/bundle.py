# bundle.py
# pack values into a bundle of bits

from collections import OrderedDict
from collections import namedtuple


class Bundle():

    bundle_size = None

    def __init__(self):
        assert  sum(self.bundle.values()) == self.bundle_size, "item sizes don't add up to bundle_size"

    def pack(self, **kwargs):

        b = 0
        for key in self.bundle:

            assert 0 <= kwargs[key] < 2 ** self.bundle[key], "{} overfow {} bits: {}".format(key, self.bundle[key], kwargs)

            # move the previous bits out of the way:
            b = b << self.bundle[key]
            # drop in the new bits:
            b += kwargs[key]

        return b


    def unpack(self, b):

        ret = {}
        keys = list(self.bundle.keys())
        keys.reverse()
        for k in keys:

            ret[k] = b & (2 ** self.bundle[k] - 1)
            b = b >> self.bundle[k]

        # convert the dict to a namedtuple
        classname= type(self).__name__
        nt = namedtuple(classname, list(ret.keys()))
        ret = nt(**ret)

        return ret

    def as_bits(self, v):

        bits = "{x:0{width}b}".format(x=v, width=self.bundle_size)
        # uPython doesn't support this yet:
        # bits = f"{b:0{bundle_size}b}"
        print("bundle:", bits)
        s = 0
        for k in self.bundle:
            size = self.bundle[k]
            e = s + size
            print("{}: {}".format(k, bits[s:e]))
            s += size


class CanMessageId(Bundle):

    def __init__(self):
        self.bundle = OrderedDict()
        self.bundle["channel"] = 4
        self.bundle["can_id"] = 7
        self.bundle["header"] = 18
        self.bundle_size = 29


class Header(Bundle):

    def __init__(self):
        self.bundle = OrderedDict()
        self.bundle["rfe"] = 4
        self.bundle["random"] = 14
        self.bundle_size = 18


def demo():

    def check(channel, can_id, header):
        can = CanMessageId()
        mid = can.pack(channel=channel, can_id=can_id, header=header)
        can.as_bits(mid)
        print(can.unpack(mid))

    # little numbers:
    check(1, 2, 3)

    # all the bits:
    can = CanMessageId()
    check(channel=2 ** can.bundle["channel"] - 1,
            can_id=2 ** can.bundle["can_id"] - 1,
            header=2 ** can.bundle["header"] - 1)

    oHead = Header()
    head = oHead.pack(rfe=2,random=4567)
    oHead.as_bits(head)
    print(oHead.unpack(head))

    # one too many bits:
    can = CanMessageId()
    check(2 ** can.bundle["channel"], 0,0)

if __name__=='__main__':
    demo()

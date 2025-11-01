""" Test miner values. """

import miner
import material

def test_mk2():
    """ Test mk2. """

    mk2 = miner.MK2(material.IRON_ORE, miner.IMPURE)
    assert mk2.per_min == 60

    mk2 = miner.MK2(material.IRON_ORE, miner.NORMAL)
    assert mk2.per_min == 120

    mk2 = miner.MK2(material.IRON_ORE, miner.PURE)
    assert mk2.per_min == 240

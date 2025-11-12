""" Test satisfactory. """

# pylint: disable=consider-using-f-string

import satisfactory
import miner
import recipe
import material


def test_iron_ore_satisfactory():
    """ Test iron ore decisions from a cookbook. """

    miners = [miner.MK2(material.IRON_ORE, miner.NORMAL)]
    ans = satisfactory.maximize(miners, recipe.CookBook([recipe.IronIngot()]),
                                material.IRON_INGOT)
    assert ans
    for (item, amount) in ans.items():
        print("%-20s %9.2f" % (item, amount))


def test_iron_rod_satisfactory():
    """ Test iron ore decisions from a cookbook. """

    miners = [miner.MK2(material.IRON_ORE, miner.NORMAL)]
    ans = satisfactory.maximize(miners, recipe.STANDARD, material.IRON_ROD)

    assert ans
    for (item, amount) in ans.items():
        print("%-20s %9.2f" % (item, amount))


def test_iron_plate_satisfactory():
    """ Test iron ore decisions from a cookbook. """

    miners = [miner.MK2(material.IRON_ORE, miner.NORMAL)]
    ans = satisfactory.maximize(miners, recipe.STANDARD, material.IRON_PLATE)

    assert ans
    for (item, amount) in ans.items():
        print("%-20s %9.2f" % (item, amount))


def test_reinforced_reinforced_plate():
    """ Test iron ore decisions from a cookbook. """

    miners = [miner.MK2(material.IRON_ORE, miner.NORMAL)]
    ans = satisfactory.maximize(miners, recipe.STANDARD,
                                material.REINFORCED_IRON_PLATE)
    assert ans
    for (item, amount) in ans.items():
        print("%-20s %s" % (item, amount))
        #print("%-20s %9.2f" % (item, amount))

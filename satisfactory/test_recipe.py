""" Test recipe. """
import recipe
import miner
import material


def test_materials():
    """ Test materials. """

    assert recipe.IronIngot()
    assert recipe.IronPlate()
    assert recipe.IronRod()
    assert recipe.Screws()
    assert recipe.ReinforcedIronPlate()


def test_iron_ore():
    """ test iron ingot. """

    iron_ore = miner.MK2(material.IRON_ORE, miner.IMPURE)
    assert iron_ore.per_min == 60.0

    iron_ore = miner.MK2(material.IRON_ORE, miner.NORMAL)
    assert iron_ore.per_min == 120.0

    iron_ore = miner.MK2(material.IRON_ORE, miner.PURE)
    assert iron_ore.per_min == 240.0


def test_iron_ingot():
    """ Assert producer. """

    item = recipe.IronIngot()
    assert item.is_producer(material.IRON_INGOT)

    cookbook = recipe.CookBook([recipe.IronIngot()])
    item = cookbook.find(material.IRON_INGOT)
    assert item

""" Test satisfactory. """
import satisfactory
import miner
import recipe
import material


def test_iron_ore_satisfactory():
    """ Test iron ore decisions from a cookbook. """

    miners = [miner.MK2(material.IRON_ORE, miner.NORMAL)]
    plan = satisfactory.maximize(miners, recipe.CookBook([recipe.IronIngot()]),
                                 material.IRON_INGOT)
    plan.show()
    assert plan

""" Test equation functionality. """
import equations
import material

def test_output_name():
    """ Test output singleton. """

    assert equations.VAR_OUT_GEN

    value = equations.VAR_OUT_GEN.get(material.IRON_ORE)
    assert value == f"{material.IRON_ORE} output 0"

    value = equations.VAR_OUT_GEN.get(material.IRON_ORE)
    assert value == f"{material.IRON_ORE} output 1"

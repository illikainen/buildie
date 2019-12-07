# pylint: disable=protected-access
def test_cleanup(recipe):
    assert recipe._workdir.exists()
    recipe.cleanup()
    assert not recipe._workdir.exists()

    recipe.cleanup()
    assert not recipe._workdir.exists()

from unittest.mock import patch


def test_steps(recipe):
    with patch.object(recipe, "verify") as mock:
        recipe.run()
        assert mock.call_count == 1

    with patch.object(recipe, "extract") as mock:
        recipe.run()
        assert mock.call_count == 1

    with patch.object(recipe, "build") as mock:
        recipe.run()
        assert mock.call_count == 1

    with patch.object(recipe, "test") as mock:
        recipe.run()
        assert mock.call_count == 1

    with patch.object(recipe, "install") as mock:
        recipe.run()
        assert mock.call_count == 1

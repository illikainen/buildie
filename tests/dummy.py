from src.recipe import Recipe


class DummyDefaultRecipe(Recipe):
    name = "dummy"
    variant = "default"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prepare()

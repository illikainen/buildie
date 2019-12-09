from src.recipe import Recipe


class DefaultRecipe(Recipe):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prepare()

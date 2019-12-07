class BuildieError(Exception):
    pass


class BuildieRecipeError(BuildieError):
    pass


class BuildieExistError(BuildieError):
    pass


class BuildieDependencyError(BuildieError):
    pass


class BuildieDownloadError(BuildieError):
    pass


class BuildieVerifyError(BuildieError):
    pass


class BuildieCommandError(BuildieError):
    pass

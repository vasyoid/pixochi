class PixochiNotFoundError(Exception):
    message = "This name is occupied"


class NameOccupiedError(Exception):
    message = "No Pixochi with this name"


class PixochiDeadError(Exception):
    message = "Pixochi is already dead"

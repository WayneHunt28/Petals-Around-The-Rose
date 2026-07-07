def calculate_petals(dice):
    """
    dice: list of 5 integers (1-6)
    returns: number of petals around the rose
    """

    petals = 0

    for die in dice:
        if die == 3:
            petals += 2
        elif die == 5:
            petals += 4

    return petals

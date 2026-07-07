import random

def roll_dice(n=5):
    """Roll n six-sided dice and return a list of integers"""
    return [random.randint(1, 6) for _ in range(n)]

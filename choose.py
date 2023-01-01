import random


# Selects and executes an action (function) in the provided list according to the provided weights.
# Each weight should correspond to a function in the actions list at the same index. The probability that
# an item is selected is its weight divided by the sum of all the weights.
# Returns whatever the chosen function returns.
def choose_action(weights, actions):
    assert len(weights) > 0
    assert len(weights) == len(actions)

    return random.choices(actions, weights=weights, k=1)[0]()

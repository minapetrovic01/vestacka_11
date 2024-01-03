class Player:
    def __init__(self, is_x, is_human):
        self.is_x = is_x # X je crni igrac i igra prvi
        self.is_human = is_human
        self.stack_score = 0
    def increase_stack_score(self):
        self.stack_score += 1

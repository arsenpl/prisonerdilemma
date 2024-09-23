import random
import csv

cooperate_cooperate=3
cooperate_betray=0
betray_cooperate=5
betray_betray=1

#Strategy with cooperation every time also known as nybegger strategy
class Nybegger:
    def decide(self, opp_prev_move=None):
        return 'cooperate'

#Strategy with betrayal every time
class Badguy:
    def decide(selfself, opp_prev_move):
        return 'betray'

#Strategy tit-for-tat
class TitforTat:
    def decide(self, opp_prev_move):
        if opp_prev_move == 'betray':
            return 'betray'
        else:
            return 'cooperate'

#Strategy tit-for-tat with forgiveness in 10% cases
class TitForTatWithForgiveness:
    def __init__(self, forgiveness_rate=0.1):
        self.forgiveness_rate=forgiveness_rate

    def decide(self, opp_prev_move):
        if opp_prev_move == 'betray':
            if random.random() <= self.forgiveness_rate:
                return 'cooperate'
            else:
                return 'betray'
        else:
            return 'cooperate'

#Random strategy
class RandomStrategy:
    def decide(self, opp_prev_move):
        if random.random() <= 0.5:
            return 'cooperate'
        else:
            return 'betray'

#Joss strategy act like Tit-for-tat in 90% cases and randomly betraay or cooperate in 10% cases
class Joss:

    def decide(self, opponent_previous_move=None):
        # Follow Tit-for-Tat with a 90% chance
        if random.random() <= 0.9:
            if opponent_previous_move == 'betray':
                self.cooperated_last_round = False
                return 'betray'
            else:
                return 'cooperate'
        else:
            # Randomly choose to cooperate or betray with a 10% chance
            return random.choice(['cooperate', 'betray'])

#Friedman strategy cooperate till opponent betrayl, after only betray
class Friedman:
    def __init__(self):
        self.cooperated_last_round = True  # Start by cooperating

    def decide(self, opponent_previous_move=None):
        if self.cooperated_last_round:
            if opponent_previous_move == 'betray':
                self.cooperated_last_round = False
                return 'betray'
            else:
                return 'cooperate'
        else:
            return 'betray'

#Tideman Chieruzzi strategy that change cooperation probability
class TidemanChieruzzi:
    def __init__(self):
        self.cooperate_prob = 0.5

    def decide(self, opponent_previous_move=None):
        if opponent_previous_move == 'betray':
            my_move = 'betray'
            self.cooperate_prob *= 0.9
        else:
            my_move = 'cooperate' if random.random() < self.cooperate_prob else 'betray'
            if my_move == 'cooperate':  # If we cooperated
                self.cooperate_prob = min(0.9, self.cooperate_prob * 1.1)
        self.cooperate_prob = max(0.1, self.cooperate_prob)
        return my_move

def play(player1_stg, player2_stg, num_of_rounds):
    player1_score=0
    player2_score=0
    player1_prev_move=None
    player2_prev_move=None

    for _ in range(num_of_rounds):
        move1=player1_stg.decide(player2_prev_move)
        move2=player2_stg.decide(player1_prev_move)

        if move1=='cooperate' and move2=='cooperate':
            player1_score+=cooperate_cooperate
            player2_score+=cooperate_cooperate
        elif move1=='betray' and move2=='cooperate':
            player1_score+=betray_cooperate
            player2_score+=cooperate_betray
        elif move1 == 'cooperate' and move2 == 'betray':
            player1_score += cooperate_betray
            player2_score += betray_cooperate
        elif move1=='betray' and move2=='betray':
            player1_score+=betray_betray
            player2_score+=betray_betray

        player1_prev_move=move1
        player2_prev_move=move2

    return player1_score, player2_score

players=[Nybegger, Badguy, TitforTat, TitForTatWithForgiveness, Joss, Friedman, TidemanChieruzzi, RandomStrategy]

objects = [cls() for cls in players]

num_of_rounds=50

results1=[]
results2=[]

for i, player1 in enumerate(objects):
    row1=[]
    row2=[]
    for j, player2 in enumerate(objects):

        player1_sc, player2_sc = play(player1, player2, num_of_rounds)
        print(player1.__class__.__name__+" score:", player1_sc)
        print(player2.__class__.__name__+" score:", player2_sc)
        row1.append(player1_sc)
        row2.append(player2_sc)
    results1.append(row1)
    results2.append(row2)
print("Results 1:")
for row in results1:
    print(row)
print("Results 2:")
for row in results2:
    print(row)
csv_file = "matrix1.csv"

with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(results1)

csv_file = "matrix2.csv"

with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(results2)




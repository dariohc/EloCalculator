__author__ = 'Dario Hermida'
import random
import matplotlib.pyplot as plt

"""
elo_calculator (rating1, results1, rating2, results2)
#ratings will be updated depending on results
#it is taken into account the distance between ratings, higher distance means higher deviations

"""
simulation_games = 50000
debug = 0

def elo_calculator(rating1, result1, rating2, result2):
    elo_in_game = rating1 + rating2
    #  elo_average = (rating1 + rating2) / 2
    #  elo factor change setups
    elo_offset = 20
    elo_increase_factor = 2.6
    elo_increase = (elo_offset + 1) * elo_increase_factor
    # winning probability for each player
    win1 = rating1 / elo_in_game
    win2 = rating2 / elo_in_game
    if result1 == 3:
        if win1 > win2:
            # player 1 is winning and is the strongest
            update1 = elo_increase * win2  # p1 wins and increase is low
            update2 = -1 * elo_increase * win2  # p2 loses and decrease is low
        else:
            # player 1 is winning and is the weakest
            update1 = elo_increase * win2  # pi wins, is weak, increase high
            update2 = -1 * elo_increase * win2  # p2 loses, is strong, decrease high
    else:
        if result2 == 3:
            if win1 > win2:
                # player 2 is winning and is the weakest
                update1 = -1 * elo_increase * win1  # p1 loses, is strong, decrease is high
                update2 = elo_increase * win1  # p2 wins, is weak, increase is high
            else:
                # player 2 is winning and is the strongest
                update1 = -1 * elo_increase * win1  # p1 loses, is weak, decrease low
                update2 = elo_increase * win1  # p2 wins, is strong, increase low
    if debug == 1:
        print('this is the update for player 1: {:.3f} with prob: {:.3f}'.format(update1, win1))
        print('this is the update for player 2: {:.3f} with prob: {:.3f}'.format(update2, win2))
    #match results accounting
    if result1 > result2:
        score1 = 5 - result2
        score2 = result2
        score_factor1 = 1 + ((score1 - 3) / 20)
        score_factor2 = 1 - (score2 / 20)
    else:
        score1 = result1
        score2 = 5 - result1
        score_factor2 = 1 + ((score2 - 3) / 20)
        score_factor1 = 1 - (score1 / 20)
    if debug == 1:
        print('score factor p1 {}, score factor p2 {}'.format(score_factor1, score_factor2))
    #stablishing correction factors for 5 to 0 points.
    # 5, 4 points small bonus
    # 3 points full gain
    # 2,1 points small bonus on lose
    # 0 points full lose
    if debug == 1:
        print('this is the Real update for player 1: {:.3f}'.format(score_factor1 * update1))
        print('this is the Real update for player 2: {:.3f}'.format(score_factor2 * update2))
    rating1 += update1
    rating2 += update2
    global maximum
    if abs(update1) > maximum: maximum = abs(update1)
    if debug == 1:
        print('this is the maximum update: {}'.format(maximum))
    return rating1, rating2

# test case for the previous function

elo1_list = []
elo2_list = []
elo1, elo2 = [2000, 1700]
aux, aux1, aux2 = [0, 0, 0]

maximum = 0

for k in range(simulation_games):
    if debug == 1:
        print('________ match number {}'.format(k+1))
    aux1, aux2 = [0, 0]
    aux1 = random.randint(0, 1)
    if aux1 == 1:
        aux1 = 3
    else:
        aux2 = 3
    if debug == 1:
        print(aux1, aux2)
    elo1, elo2 = elo_calculator(elo1, aux1, elo2, aux2)
    elo1_list.append(elo1)
    elo2_list.append(elo2)

time = range(simulation_games)
plt.plot(time, elo1_list, 'g-', time, elo2_list, 'r-')
plt.show()
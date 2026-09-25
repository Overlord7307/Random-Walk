import math
import random
import matplotlib.pyplot as plt
import time

x = 0
p = 0.5


def random_walk(xi:int, t:int, p:float):
    '''
    Returns the final position of a random walk starting from x = xi after time t (or t number of steps).

    xi (int): initial position
    t (int): total number of steps taken
    p (float): probability of walker taking a step towards the right (0 <= p <= 1)
    '''
    x = xi
    for i in range(0, t):   # Ensures t number of steps are taken
        rand_num = random.random()  # Picks a random float between 0 and 1
        if (rand_num < p):
            x += 1
        else:
            x -= 1

    return x


def P_analytical(x:int, t:int):
    '''
    Calculates the probability of finding the walker at position x after time t (or t number of steps).

    xi (int): position for which probability is calculated
    t (int): total number of steps taken
    '''
    if (abs(x) > t):
        # Since the walker takes only one step at a time, the position cannot be greater than number of steps
        return 0
    elif ((t + x) % 2 != 0):
        # If t is even, final position must also be even. If t is odd, final position must also be odd. Thus, if (t + x) is odd then P(x, t) = 0
        return 0

    # R and L are the number of right and left steps required to reach position x in time t
    R = int((t + x) / 2)
    L = t - R
    unique_paths = math.comb(t, R)  # Calculates number of ways to take exactly R number of right steps using nCr
    probability = unique_paths * (p**R) * ((1 - p)**L)  # Final probability is total number of unique paths multiplied by probability of taking each step

    return probability


def P_numerical(xi:int, t:int, p:float, N:int):
    '''
    Runs N number of random walks and returns a dictionary containing probabilities of attaining all final positions.

    xi (int): initial position
    t (int): total number of steps to be taken
    p (float): probability of taking a step to the right at every t
    N (int): number of random walks to be simulated
    '''
    ti = time.time()
    freq_dict = {}
    for i in range(0, N):
        pos = random_walk(xi, t, p)
        if (pos in freq_dict.keys()):
            freq_dict[pos] += 1
        else:
            freq_dict[pos] = 1

    prob_dict = {}
    for j in freq_dict.keys():
        prob_dict[j] = freq_dict[j] / N

    for k in range(-t, t+1):
        if (k not in prob_dict.keys()):
            prob_dict[k] = 0

    tf = time.time()
    time_elapsed = tf - ti
    print(f'Time taken for simulation: {time_elapsed} sec')

    return prob_dict


def main():
    t = 20
    prob_dict = P_numerical(x, t, p, 100000)
    x_values = prob_dict.keys()
    P_values = prob_dict.values()

    plt.figure(figsize=(16, 9))
    plt.bar(x_values, P_values, color='#000080')
    plt.xticks(range(-t, t+1, 2))
    plt.title(f'1 Dimensional Unbiased Random Walk (t = {t})')
    plt.xlabel('Position (x)')
    plt.ylabel('Probability, P(x, t)')
    plt.grid(True)
    #plt.savefig(f'1D-unbiased-random-walk_numerical_t={t}.png', dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
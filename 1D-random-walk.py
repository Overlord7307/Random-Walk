import math
import numpy as np
import random
import matplotlib.pyplot as plt
import time

x = 0
p = 0.5
N = 100000


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
    Runs N number of random walks and returns a dictionary containing probabilities of attaining all final positions. Prints time taken to run the simulation.

    xi (int): initial position
    t (int): total number of steps to be taken
    p (float): probability of taking a step to the right at every t
    N (int): number of random walks to be simulated
    '''
    ti = time.time()

    # Simulate random walk N times and store frequency of each final position in a dictionary
    freq_dict = {}
    for i in range(0, N):
        pos = random_walk(xi, t, p)
        if (pos in freq_dict.keys()):
            freq_dict[pos] += 1
        else:
            freq_dict[pos] = 1

    # Convert frequency into probability
    prob_dict = {}
    for j in freq_dict.keys():
        prob_dict[j] = freq_dict[j] / N

    for k in range(xi - t, xi + t + 1):
        if (k not in prob_dict.keys()):
            prob_dict[k] = 0

    tf = time.time()
    time_elapsed = tf - ti
    print(f'Time taken for simulation: {time_elapsed} sec')

    return prob_dict


def second_moment(t:int, p:float, N:int):
    '''
    Simulates N random walks and stores squares of the final positions. Returns average of all squares.

    t (int): total number of steps to be taken
    p (float): probability of taking a step to the right at every t
    N (int): number of random walks to be simulated
    '''
    xf_squared = []
    for i in range(0, N):
        xf = random_walk(0, t, p)
        xf_squared.append(xf**2)

    return np.mean(xf_squared)


def plot_second_moment(p:float, N:int):
    '''
    Plots the second moment as a function of t. Prints time taken to execute.
    '''
    ti = time.time()
    t_values = range(0, 101)

    y_values = []
    for i in t_values:
        y_values.append(second_moment(i, p, N))

    tf = time.time()
    print(f'Time elapsed: {tf - ti} sec')

    plt.plot(t_values, y_values, label=r'$\langle x^2 \rangle$', marker='o', color='red')

    plt.title(r'Second Moment vs Time', fontsize=14)
    plt.xlabel(r'Total Number of Steps $(t)$', fontsize=12)
    plt.ylabel(r'Second Moment of Final Position $\langle x^2 \rangle$', fontsize=12)

    plt.grid(True)
    plt.legend()
    plt.savefig('plots\\second-moment-vs-t_python.png', dpi=300, bbox_inches='tight')
    plt.show()


def gaussian(x):
    return (2 / ((2*np.pi)**0.5)) * np.exp(-(x**2) / 2)


def plot_prob(x:int, p:float):
    '''
    Plots P(x, t) vs x for t = 20, 30 and 50.
    '''
    prob_dict_20 = P_numerical(x, 20, p, 100000)
    prob_dict_30 = P_numerical(x, 30, p, 100000)
    prob_dict_50 = P_numerical(x, 50, p, 100000)

    x_20, P_20 = np.array(list(prob_dict_20.keys())) / (20**0.5), np.array(list(prob_dict_20.values())) * (20**0.5)
    x_30, P_30 = np.array(list(prob_dict_30.keys())) / (30**0.5), np.array(list(prob_dict_30.values())) * (30**0.5)
    x_50, P_50 = np.array(list(prob_dict_50.keys())) / (50**0.5), np.array(list(prob_dict_50.values())) * (50**0.5)

    x_smooth = np.linspace(-10, 10, 1000)

    plt.figure(figsize=(16, 9))
    plt.scatter(x_20, P_20, color='#0D6EFD', label='t = 20')
    plt.scatter(x_30,     P_30, color='#FFC107', label='t = 30')
    plt.scatter(x_50, P_50, color='#D90429', label='t = 50')

    plt.plot(x_smooth, gaussian(x_smooth), label='Gaussian', color='magenta', linestyle='--')

    plt.title('1-Dimensional Unbiased Random Walk (Numerical Simulation)', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel('Position (x)', fontsize=12, labelpad=10)
    plt.ylabel('Probability, P(x, t)', fontsize=12, labelpad=10)

    plt.grid(True, linestyle='--', alpha=0.5, zorder=0)
    plt.gca().set_axisbelow(True)

    plt.legend(fontsize=12, frameon=True, facecolor='white')
    plt.tight_layout()
    plt.savefig(f'plots\\1D-unbiased-random-walk_numerical_gussian-fit.png', dpi=300, bbox_inches='tight')
    plt.show()
    

def main():
    plot_second_moment(p, N)
    

if __name__ == "__main__":
    main()
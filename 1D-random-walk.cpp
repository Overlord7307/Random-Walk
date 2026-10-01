#include <fstream>
#include <iostream>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <random>
#include <chrono>
#include <utility>


int xi = 0;
double p = 0.5;
int N = 100000;


int random_walk(int xi, int t, double p, std::mt19937& gen) {
    /*
    Returns the final position of a random walk starting from x = xi after time t (or t number of steps).

    xi (int): initial position
    t (int): total number of steps taken
    p (float): probability of walker taking a step towards the right (0 <= p <= 1)
    */
    int x = xi;
    std::uniform_real_distribution<double> distrib(0.0, 1.0);

    for (int i = 0; i < t; i++) {
        double rand_num = distrib(gen);
        if (rand_num < p) {
            x++;
        } else {
            x--;
        }
    }
    return x;
}


std::unordered_map<int, double> P_numerical(int xi, int t, double p, int N) {
    /*
    Runs N number of random walks and returns an unordered map containing probabilities of attaining all final positions.

    xi (int): initial position
    t (int): total number of steps to be taken
    p (float): probability of taking a step to the right at every t
    N (int): number of random walks to be simulated
    */
    std::unordered_map<int, double> prob_dict;

    std::random_device rd;
    std::mt19937 gen(rd());

    // Maps each possible position to its frequency of occurence
    for (int i = 0; i < N; i++) {
        int pos = random_walk(xi, t, p, gen);
        prob_dict[pos]++;
    }

    // Normalize to obtain probabilities
    for (auto& [key, value] : prob_dict) {
        value = static_cast<double>(value) / N;
    }

    // Fill out remaining positions with zeroes
    for (int k = xi - t; k <= xi + t; k++) {
        if (!prob_dict.contains(k)) {
            prob_dict[k] = 0.0;
        }
    }

    return prob_dict;
}


std::pair<std::vector<int>, std::vector<double>> second_moment(double p, int N) {
    /*
    Simulates N random walks for each time step and calculates the second moment of position. Returns two vectors containing time and avg(x^2) values.

    p (float): probability of taking a step to the right at every t
    N (int): number of random walks to be simulated
    */
    
    // Random number setup
    std::random_device rd;
    std::mt19937 gen(rd());

    // Initialize vectors to store final data
    std::vector<int> t_values(101);
    std::vector<double> mean_values(101);

    // Loop over all values of t
    for (int t = 0; t < 101; t++) {
        t_values[t] = (t);

        // Perform random walk N times, sum all squares of final positions
        double square_sum = 0.0;
        for (int i = 0; i < N; i++) {
            int xf = random_walk(xi, t, p, gen);
            square_sum += xf * xf;
        }

        mean_values[t] = square_sum / N;    // Calculate and store mean of squares of final positions
    }

    return {t_values, mean_values};
}


void export_second_moment_to_csv(const std::pair<std::vector<int>, std::vector<double>>& data, const std::string& filename) {
    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file for writing!\n";
        return;
    }

    // Write CSV header
    file << "Time,SecondMoment\n";

    const auto& t_values = data.first;
    const auto& mean_values = data.second;

    // Write data rows
    for (size_t i = 0; i < t_values.size(); i++) {
        file << t_values[i] << "," << mean_values[i] << "\n";
    }

    file.close();
    std::cout << "Second moment data successfully exported to " << filename << "\n";
}


int main() {
    /*
    std::unordered_map<int, double> results = P_numerical(0, 20, p, 100000);
    std::cout << "Position | Frequency" << std::endl;
    std::cout << "--------------------" << std::endl;
    for (const auto& pair : results) {
        std::cout << pair.first << " \t | " << pair.second << std::endl;
    }
    */

    // Calculate time required to execute the function
    auto start_time = std::chrono::high_resolution_clock::now();
    auto sm_results = second_moment(p, N);
    auto end_time = std::chrono::high_resolution_clock::now();

    export_second_moment_to_csv(sm_results, "second-moment-data_cpp.csv");

    std::chrono::duration<double> duration = end_time - start_time;
    std::cout << "Time elapsed: " << duration.count() << " sec" << std::endl;
    
    return 0;
}
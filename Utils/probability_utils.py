import random
import matplotlib.pyplot as plt

def get_probabilistic_answer(probability):
    # Generate a random number between 0 and 1
    random_number = random.random()
    
    # Check if the random number is less than the given probability
    if random_number < probability:
        return 1  # Return 1 if the condition is met
    else:
        return 0  # Return 0 otherwise
    

def get_random_normal_distribution_number_biased(start, end, bias=10, std_dev=16):
    mean_value = (start + end) / 2 + bias
    std_deviation = std_dev
    # print("Mean: ", mean_value)
    # print("SD: ", std_deviation)

    random_value = int(random.gauss(mean_value, std_deviation))
    
    if random_value > end:
        random_value = get_random_normal_distribution_number_biased(start, end, bias, std_dev)
    elif random_value < start:
        random_value = get_random_normal_distribution_number_biased(start, end, bias, std_dev)
    return random_value

def check_distribution(min_value, max_value, num_samples=100000):
    results = []

    for _ in range(num_samples):
        result = get_random_normal_distribution_number_biased(min_value, max_value)
        results.append(result)

    # Plot the histogram
    plt.hist(results, bins=max_value-min_value+1, range=(min_value, max_value), density=True, alpha=0.7, color='purple')
    plt.title('Distribution Check')
    plt.xlabel('Random Values')
    plt.ylabel('Frequency')
    plt.show()
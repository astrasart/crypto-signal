# src/model.py

import json             # For loading JSON data
import os               # For file path operations
import datetime         # For converting timestamps to human-readable dates

# -------------------------------
# Function: load_crypto_data
# -------------------------------
def load_crypto_data(filepath="data/bitcoin_data.json"):
    """
    Loads cryptocurrency data from a JSON file.

    Args:
        filepath (str): The path to the JSON file that contains the crypto data.

    Returns:
        dict: A dictionary containing the loaded data.
    """
    # Open the JSON file in read mode and parse its content
    with open(filepath, "r") as file:
        data = json.load(file)
    return data

# -------------------------------
# Function: extract_price_data
# -------------------------------
def extract_price_data(data):
    """
    Extracts timestamp and price data from the JSON data.

    Args:
        data (dict): The dictionary containing crypto data (expects a 'prices' key).

    Returns:
        list: A list of tuples, each tuple containing (timestamp, price).
    """
    # The 'prices' key holds a list of [timestamp, price] pairs.
    prices = data.get("prices", [])
    # Convert each inner list to a tuple for clarity
    return [(item[0], item[1]) for item in prices]

# -------------------------------
# Function: calculate_moving_average
# -------------------------------
def calculate_moving_average(prices, window_size=5):
    """
    Calculates a simple moving average (SMA) for the price data.

    Args:
        prices (list): A list of price values (floats).
        window_size (int): The number of data points to consider in each average.

    Returns:
        list: A list of moving average values. For indices where there isn't enough
              data to form a full window, the value will be None.
    """
    moving_averages = []  # List to store computed moving averages
    for i in range(len(prices)):
        if i < window_size - 1:
            # Not enough data points to compute an average, so append None
            moving_averages.append(None)
        else:
            # Extract the current window of data points
            window = prices[i - window_size + 1 : i + 1]
            # Compute the average of the window
            avg = sum(window) / window_size
            moving_averages.append(avg)
    return moving_averages

# -------------------------------
# Function: drakes_formula
# -------------------------------
def drakes_formula(signal_strength, num_factors=1):
    """
    Placeholder function for integrating Drake's Formula.
    
    Drake's Equation originally estimates the number of extraterrestrial civilizations.
    Here, we repurpose a simplified version as a weighting factor for our buy signal.
    
    Args:
        signal_strength (float): The raw signal strength (difference between current price and moving average).
        num_factors (int): A placeholder for the number of factors affecting the signal (can be expanded later).
    
    Returns:
        float: The weighted signal strength after applying the placeholder formula.
    
    Note: This is a simplistic implementation. In a real model, you'd define and integrate
    the actual factors and calculations that make Drake's Formula meaningful in this context.
    """
    # For demonstration, we calculate a weight multiplier based on the number of factors.
    # Here, we arbitrarily increase the signal strength by 10% per factor.
    drake_weight = 1.0 + (num_factors * 0.1)
    weighted_signal = signal_strength * drake_weight
    return weighted_signal

# -------------------------------
# Function: generate_buy_signal
# -------------------------------
def generate_buy_signal(prices, moving_averages):
    """
    Generates a simple buy signal based on the latest price relative to its moving average.
    
    Args:
        prices (list): List of price values.
        moving_averages (list): List of moving average values corresponding to the prices.
    
    Returns:
        bool: True if a buy signal is generated, False otherwise.
    
    Logic:
        - Compute the difference between the latest price and its moving average.
        - Apply the placeholder Drake's formula to weight the signal.
        - If the weighted signal is positive, a buy signal is generated.
    """
    # Check if we have enough data to compute the signal
    if not prices or not moving_averages or moving_averages[-1] is None:
        return False  # Not enough data to decide
    
    # Get the most recent price and moving average
    latest_price = prices[-1]
    latest_ma = moving_averages[-1]
    
    # Calculate the raw difference (signal strength)
    signal_strength = latest_price - latest_ma

    # Adjust the signal strength using the placeholder Drake's formula
    weighted_signal = drakes_formula(signal_strength)
    
    # Debug prints to examine the values
    print("Latest Price:", latest_price)
    print("Latest Moving Average:", latest_ma)
    print("Raw Signal Strength:", signal_strength)
    print("Weighted Signal Strength:", weighted_signal)
    
    # For our simple model, a positive weighted signal triggers a buy signal
    return weighted_signal > 0

# -------------------------------
# Main Function
# -------------------------------
def main():
    """
    Main function to run the cryptocurrency analysis model.
    
    It performs the following steps:
        1. Loads the cryptocurrency data from a JSON file.
        2. Extracts timestamps and prices from the data.
        3. Calculates the moving average of the prices.
        4. Generates a buy signal based on the latest price vs. moving average.
        5. Prints the results.
    """
    # Load the cryptocurrency data from the JSON file
    data = load_crypto_data()
    
    # Extract the price data (a list of (timestamp, price) tuples)
    price_data = extract_price_data(data)
    
    # Separate the data into two lists: timestamps and prices
    timestamps, prices = zip(*price_data)
    
    # Calculate a simple moving average with a window size of 5
    moving_avg = calculate_moving_average(prices, window_size=5)
    
    # Generate a buy signal using the latest price and moving average
    buy_signal = generate_buy_signal(prices, moving_avg)
    
    # Output the latest price, moving average, and whether a buy signal is generated
    print("Latest Price:", prices[-1])
    print("Latest Moving Average:", moving_avg[-1])
    print("Buy Signal Generated:", buy_signal)
    
    # (Optional) Convert the last timestamp from milliseconds to a human-readable format
    last_timestamp = timestamps[-1] / 1000.0  # Convert milliseconds to seconds
    readable_time = datetime.datetime.fromtimestamp(last_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print("Data Timestamp:", readable_time)

# Ensure that the main function runs when this script is executed directly
if __name__ == "__main__":
    main()


import numpy as np
from scipy.optimize import curve_fit

# Define the exponential function
def exponential_func(x, a, b):
    return a * np.exp(b * x)

# Fit the exponential function to the data
def fit_exponential_underestimate(data):
    # Extract x and y values from the data points
    x_data, y_data = zip(*data)
    x_data = np.array(x_data)
    y_data = np.array(y_data)

    # Fit the exponential function to the data
    popt, _ = curve_fit(exponential_func, x_data, y_data, maxfev=10000)

    # Ensure the fitted function underestimates all data points
    def underestimating_func(x):
        y_fit = exponential_func(x, *popt)
        y_fit = np.minimum(y_fit, y_data - 1)  # Ensure the values are less than the actual values
        return np.floor(y_fit).astype(int)  # Convert to integers and floor

    return underestimating_func, popt

# Example data points (x, y)
data = [(100, 200), (125, 160), (150, 133), (175, 114), (200, 100)]

# Get the underestimating exponential function
underestimating_func, params = fit_exponential_underestimate(data)

# Print the function parameters
print(f"Exponential function parameters: a = {params[0]}, b = {params[1]}")

# Print the underestimating values for the given x data points
x_data = np.array([point[0] for point in data])
y_underestimate = underestimating_func(x_data)
print(f"Underestimating values: {y_underestimate}")

# Define the actual underestimate function for printing
def underestimate_function(x):
    return np.floor(params[0] * np.exp(params[1] * x)).astype(int)

# Print the function as a string
print(f"Underestimate function: y = floor({params[0]} * exp({params[1]} * x))")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import tkinter as tk
from tkinter import filedialog

def calculate_jerk(acceleration):
    # Calculate jerk as the derivative of acceleration
    jerk = np.gradient(acceleration)
    return jerk

def quantify_smoothness(jerk):
    # Calculate the standard deviation of jerk as a measure of smoothness
    smoothness_metric = np.std(jerk)
    return smoothness_metric

def smoothness_Calcutation_CK(pulse,time):
    # Calculate the smoothness as (integral of curve)^2/time
    # print("***********************")
    # print(len(acceleration**2),len(time))
    # print("***********************")
    
    
    Spul_value_ck = scipy.integrate.cumtrapz(pulse,time, initial=0)**2/time
    
    return Spul_value_ck.max()

def smoothness_Calcutation_CK_Cum(pulse,time):
    # Calculate the smoothness as integral of "square of derivative" of "acceleration" curve
    # print("***********************")
    # print(len(acceleration**2),len(time))
    # print("***********************")
    

    Spul_ck= (scipy.integrate.cumtrapz(pulse,time, initial=0))**2/time
    
    print("***********************")
    print("cumulative integral", Spul_ck)
    print("***********************")   
    return Spul_ck

def plot_curves(time, pulse, acceleration, jerk, Spul_value_ck,integral_of_pulse):
    # Plot the pulse, acceleration, and jerk curves
    plt.figure(figsize=(10, 6))
    plt.subplot(3, 1, 1)
    plt.plot(time, pulse, label=f"Pulse, Max: {pulse.max()} Min: {pulse.min()}")
    plt.title('Pulse Curve of '+get_file_name)
    plt.xlabel('Time')
    plt.ylabel('Pulse')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(time, integral_of_pulse, label=f"Velocity, Max: {integral_of_pulse.max()} Min: {integral_of_pulse.min()}")
    plt.title('Integral of pulse')
    plt.xlabel('Time')
    plt.ylabel('Velocity')
    plt.legend()
    
    # plt.subplot(3, 1, 2)
    # plt.plot(time, acceleration, label='Gradient of pulse')
    # plt.title('Gradient of pulse Curve')
    # plt.xlabel('Time')
    # plt.ylabel('Gradient of pulse')
    # plt.legend()

    # plt.subplot(3, 1, 3)
    # plt.plot(time, jerk, label=f"Jerk Smoothness Metric: {smoothness_metric} \nEnergy: {energy}")
    # plt.title('Jerk curve')
    # plt.xlabel('Time')
    # plt.ylabel('Jerk')
    # plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(time, Spul_ck, label=f"Spul Value CK, Max: {Spul_ck.max()}")
    plt.title('Spul_ck')
    plt.xlabel('Time')
    plt.ylabel('Spul_value_ck')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
def calculate_energy(velocity, time_step):
    # Calculate energy as the integral of velocity squared over time
    energy = np.trapz(velocity**2, dx=time_step)
    return energy


root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()


print(file_path)
print()


file_path_list=(file_path).split(("/"))
print(file_path_list)
print()

get_file_name=file_path_list[-1]

print("Seçilen Dosya :",get_file_name)
print()

# Input the path to your CSV file
# csv_file_path = "your_file.csv"
csv_file_path = get_file_name
# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Extract time and pulse data
time = df['time'].values  # Assuming 'Time' is the column name for time
pulse = df['acceleration'].values  # Assuming 'acceleration' is the column name for pulse

# Calculate acceleration and jerk
acceleration = np.gradient(pulse)
jerk = calculate_jerk(acceleration)

# Calculate smoothness metric
smoothness_metric = quantify_smoothness(jerk)


# **********************************************
#integral of pulse
integral_of_pulse=scipy.integrate.cumtrapz(pulse,time, initial=0)
# **********************************************

# Calculate energy
time_step = time[1] - time[0]
velocity = np.cumsum(acceleration) * time_step  # Velocity is the cumulative sum of acceleration
energy = calculate_energy(velocity, time_step)

print('Energy',energy)

# ******************************************

# Smoothness metric calculation
Spul_value_ck = smoothness_Calcutation_CK(pulse,time)

# Cumulative smoothness calculation
Spul_ck = smoothness_Calcutation_CK_Cum(pulse,time)

print("Spul_value_ck",Spul_value_ck)

# Print the smoothness metric
# print(f"Smoothness Metric: {smoothness_metric}")

# Plot the curves
plot_curves(time, pulse, acceleration, jerk,Spul_value_ck,integral_of_pulse)

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Scale, HORIZONTAL, StringVar, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define fuzzy variables
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')

# Membership functions
temperature['low'] = fuzz.trimf(temperature.universe, [0, 0, 20])
temperature['medium'] = fuzz.trimf(temperature.universe, [15, 25, 35])
temperature['high'] = fuzz.trimf(temperature.universe, [30, 40, 40])

humidity['low'] = fuzz.trimf(humidity.universe, [0, 0, 40])
humidity['medium'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['high'] = fuzz.trimf(humidity.universe, [60, 100, 100])

fan_speed['slow'] = fuzz.trimf(fan_speed.universe, [0, 0, 40])
fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [30, 50, 70])
fan_speed['fast'] = fuzz.trimf(fan_speed.universe, [60, 100, 100])

# Fuzzy rules
rules = [
    ctrl.Rule(temperature['low'] & humidity['low'], fan_speed['slow']),
    ctrl.Rule(temperature['low'] & humidity['medium'], fan_speed['slow']),
    ctrl.Rule(temperature['low'] & humidity['high'], fan_speed['medium']),
    ctrl.Rule(temperature['medium'] & humidity['low'], fan_speed['medium']),
    ctrl.Rule(temperature['medium'] & humidity['medium'], fan_speed['medium']),
    ctrl.Rule(temperature['medium'] & humidity['high'], fan_speed['fast']),
    ctrl.Rule(temperature['high'] & humidity['low'], fan_speed['fast']),
    ctrl.Rule(temperature['high'] & humidity['medium'], fan_speed['fast']),
    ctrl.Rule(temperature['high'] & humidity['high'], fan_speed['fast'])
]

# Control system
fan_ctrl = ctrl.ControlSystem(rules)
fan = ctrl.ControlSystemSimulation(fan_ctrl)

# GUI setup
root = Tk()
root.title("Fuzzy Fan Speed Controller")
root.geometry("1500x1200")

Label(root, text="Temperature (°C)", font=("Comic Sans", 13)).pack(pady=10, padx=10)
temp_slider = Scale(root, from_=0, to=40, orient=HORIZONTAL, length=500, resolution=1)
temp_slider.pack()

Label(root, text="Humidity (%)", font=("Comic Sans", 13)).pack(padx=10, pady=10)
humidity_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, length=500, resolution=1)
humidity_slider.pack()

result_var = StringVar()
result_label = Label(root, textvariable=result_var, font=("Comic Sans", 14), fg="white")
result_label.pack(pady=5)

# Plotting frame
plot_frame = Frame(root)
plot_frame.pack()

# Initial matplotlib figure
fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(pady=30)

def update_system(*args):
    temp_val = temp_slider.get()
    hum_val = humidity_slider.get()
    fan.input['temperature'] = temp_val
    fan.input['humidity'] = hum_val
    fan.compute()
    speed = fan.output['fan_speed']
    result_var.set(f"Calculated Fan Speed: {speed:.2f}%")
    update_plot(speed)

def update_plot(speed):
    ax.clear()
    x = fan_speed.universe
    ax.plot(x, fan_speed['slow'].mf, label='Slow', color='skyblue')
    ax.plot(x, fan_speed['medium'].mf, label='Medium', color='gray')
    ax.plot(x, fan_speed['fast'].mf, label='Fast', color='crimson')
    ax.axvline(speed, color='green', linestyle='--', linewidth=2, label=f'Output: {speed:.2f}%')
    ax.set_title('Fan Speed Membership', fontsize=12)
    ax.set_xlabel('Fan Speed (%)')
    ax.set_ylabel('Membership Degree')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper left')
    canvas.draw()

# Bind sliders to update function
temp_slider.config(command=update_system)
humidity_slider.config(command=update_system)

# Initialize display once
update_system()

# Run the app
root.mainloop()
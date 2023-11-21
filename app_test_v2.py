import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog
import webbrowser
import threading

# System mode
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('blue')

# SpeedPASEF app
app = customtkinter.CTk()
app.geometry('1280x780')
app.title('SpeedyPASEF')

# For UI elements
title = customtkinter.CTkLabel(app, text='Upload analysis.tdf files from .d folder',
                               fg_color=('#005b96'),
                               font=("Arial", 25, 'bold'),
                               corner_radius=5)
title.grid(row=0, column=0, columnspan=2, padx=40, pady=20)

# Insert my LinkedIn page
def link():
    webbrowser.open_new(r'https://www.linkedin.com/in/aline-de-lima-leite-phd-40b1312a/')

made_by = customtkinter.CTkButton(app, text="by: Aline L. Leite",
                                  font=("Arial", 10), fg_color=('transparent'),
                                  command=link)
made_by.grid(row=5, column=0, columnspan=2, padx=40, pady=20)

# Load datasets
def load_data(button, progress):
    file_path = filedialog.askopenfilename()
    if file_path:
        def load_data_task():
            con = sqlite3.connect(file_path)
            df = pd.read_sql_query(
                'select p.Frame, count(*)/f.RampTime*1000 as ddaPrecursorPerSecond from PasefFrameMsMsInfo p JOIN frames f ON p.frame = f.id group by Frame',
                con)
            con.close()

            # Create separate DataFrames for each button
            if button == file_1:
                global df1
                df1 = df
            elif button == file_2:
                global df2
                df2 = df

            progress.stop()
            progress['value'] = 100  # Update progress bar to completion
            progress.update()

        progress['value'] = 0  # Reset progress bar
        progress.start()
        # Start a thread to load data in the background
        threading.Thread(target=load_data_task).start()

# Upload tdf files Button using grid
file_1 = customtkinter.CTkButton(app, text='Analysis 1', command=lambda: load_data(file_1, progress1))
file_1.grid(row=1, column=0, padx=10, pady=10)

file_2 = customtkinter.CTkButton(app, text='Analysis 2', command=lambda: load_data(file_2, progress2))
file_2.grid(row=1, column=1, padx=10, pady=10)

# Progress bars
progress1 = Progressbar(app, orient=HORIZONTAL, mode='determinate', maximum=100)
progress1.grid(row=2, column=0, padx=5, pady=5)

progress2 = Progressbar(app, orient=HORIZONTAL, mode='determinate', maximum=100)
progress2.grid(row=2, column=1, padx=5, pady=5)

# Make the Plot for dataset 1
fig1, ax1 = plt.subplots()
ax1.set_title('File 1')
ax1.set_ylabel('Acquisition Speed (Hz)')
ax1.set_xlabel('frames')

# Make the Plot for dataset 2
fig2, ax2 = plt.subplots()
ax2.set_title('File 2')
ax2.set_ylabel('Acquisition Speed (Hz)')
ax2.set_xlabel('frames')

# Create separate plots for each DataFrame
def plot_data_1():
    if 'df1' in globals():
        ax1.scatter(df1['Frame'], df1['ddaPrecursorPerSecond'], c=df1['ddaPrecursorPerSecond'], s=5, cmap='viridis')
        plot1.draw()

def plot_data_2():
    if 'df2' in globals():
        ax2.scatter(df2['Frame'], df2['ddaPrecursorPerSecond'], c=df2['ddaPrecursorPerSecond'], s=5, cmap='viridis')
        plot2.draw()

# Create a button to plot both datasets
def plot_both_datasets():
    plot_data_1()
    plot_data_2()

plot_button = customtkinter.CTkButton(app, text='Plot', command=plot_both_datasets)
plot_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Create a frame for the plot widgets
plot_frame = Frame(app)
plot_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Plot widgets using grid inside the plot_frame
plot1 = FigureCanvasTkAgg(fig1, master=plot_frame)
plot1.get_tk_widget().grid(row=4, column=0, padx=10, pady=10)

plot2 = FigureCanvasTkAgg(fig2, master=plot_frame)
plot2.get_tk_widget().grid(row=4, column=1, padx=10, pady=10)

app.mainloop()

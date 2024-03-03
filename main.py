# IMPORTS AND DEPENDENCIES
import csv
import time
import matplotlib.pyplot as plt
import pandas as pd
import pyautogui as pag
from matplotlib.animation import FuncAnimation
import tkinter as tk

plt.style.use("ggplot")

# FUNCTIONALITIES
def choose_method():
    while True:
        method = pag.confirm("Choose Method For The Plotting System", title="INITIALIZE", buttons=["New","Default","Close"])
        if method == "New":
            new()
            default()
            break
        elif method == "Default":
            default()
            break
        elif method == "Close":
            exit()
        else:
            print("NULL methodology")
            continue

def new():
    print("NEW methodology")
    global_plotting_dialog()
    local_plotting_dialog()

def global_plotting_dialog():
    global root
    global plotno_entry;
    global rowno_entry;
    global baudrate_entry;
    global filename_entry;
    
    root = tk.Tk()
    root.title("User Information")

    plotno_label = tk.Label(root, text="No of Plots: ")
    plotno_label.grid(row=0, column=0,padx=5, pady=5)
    plotno_entry = tk.Entry(root)
    plotno_entry.grid(row=0, column=1,padx=5, pady=5)

    rowno_label = tk.Label(root, text="No of Rows: ")
    rowno_label.grid(row=1, column=0,padx=5, pady=5)
    rowno_entry = tk.Entry(root)
    rowno_entry.grid(row=1, column=1,padx=5, pady=5)

    baudrate_label = tk.Label(root, text="Plotting Rate(ms): ")
    baudrate_label.grid(row=2, column=0,padx=5, pady=5)
    baudrate_entry = tk.Entry(root)
    baudrate_entry.grid(row=2, column=1,padx=5, pady=5)

    filename_label = tk.Label(root, text="Sensor FileName(csv): ")
    filename_label.grid(row=3, column=0,padx=5, pady=5)
    filename_entry = tk.Entry(root)
    filename_entry.grid(row=3, column=1,padx=5, pady=5)


    load_button = tk.Button(root, text="Load", command=load_global)
    load_button.grid(row=4, columnspan=2,padx=5, pady=5)

    root.mainloop()

def load_global():
    global plotno
    plotno =  plotno_entry.get()
    rowno =  rowno_entry.get()
    baudrate =  baudrate_entry.get()
    filename =  filename_entry.get()
    if ".csv" not in filename:
        filename += ".csv"
    with open("setting.csv","w",newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([plotno,rowno,baudrate,filename])
    
    root.destroy()

def local_plotting_dialog():
    global list_objs
    list_objs = []
    global local_root
    local_root = tk.Tk()
    local_root.title("NEW PLOT INFO")
    for i in range(int(plotno)):
        frame = tk.Frame(local_root) 
        frame.pack() 
        
        attr_label = tk.Label(frame, text=f"Plot {i+1} Attribute: ")
        attr_label.grid(row=0, column=0+i+2,padx=5, pady=5)
        attr_entry = tk.Entry(frame)
        attr_entry.grid(row=0, column=1+i+2,padx=5, pady=5)
        list_objs.append(attr_entry)
        
        limpnt_label = tk.Label(frame, text=f"Plot {i+1} Limit Points: ")
        limpnt_label.grid(row=1, column=0+i+2,padx=5, pady=5)
        limpnt_entry = tk.Entry(frame)
        limpnt_entry.grid(row=1, column=1+i+2,padx=5, pady=5)
        list_objs.append(limpnt_entry)
        
        pltstyle_label = tk.Label(frame, text=f"Plot {i+1} Plot Style: ")
        pltstyle_label.grid(row=2, column=0+i+2,padx=5, pady=5)
        pltstyle_entry = tk.Entry(frame)
        pltstyle_entry.grid(row=2, column=1+i+2,padx=5, pady=5)
        list_objs.append(pltstyle_entry)
        
        pltcolor_label = tk.Label(frame, text=f"Plot {i+1} Plot Color: ")
        pltcolor_label.grid(row=3, column=0+i+2,padx=5, pady=5)
        pltcolor_entry = tk.Entry(frame)
        pltcolor_entry.grid(row=3, column=1+i+2,padx=5, pady=5)
        list_objs.append(pltcolor_entry)

    next_button = tk.Button(local_root, text="Next", command=next_entry)
    next_button.pack(side=tk.BOTTOM)

    local_root.mainloop()
        
        
def next_entry():
    f = open("setting.csv","a",newline="")
    csv_writer = csv.writer(f)
    for i in range(0,len(list_objs),4):
        csv_writer.writerow([
            list_objs[i].get(),
            list_objs[i+1].get(),
            list_objs[i+2].get(),
            list_objs[i+3].get(),
        ])
    f.close()
    local_root.destroy()
    print("SETTINGS.CSV UPDATED SUCCESFULLY")
        


def default():
    print("DEFAULT methodology")
    pag.confirm('Ensure That The <setting.csv> File Is Imported In The Main Directory')
    global setting
    setting = []
    f = open("setting.csv", 'r')
    csv_reader = csv.reader(f)
    for i in csv_reader:
        setting.append(i)
    f.close()
    
def plot_resultant(k):
    data = pd.read_csv(setting[0][3])
    niter = int(setting[0][0])
    rowiter = int(setting[0][1])
    coliter = int(niter/rowiter)
    
    plt.cla()
    for i in range(niter):
        plt.subplot(rowiter, coliter,i+1)
        if int(setting[i+1][1]) == 0:
            plt.plot(data[setting[i+1][0]],"o--",label=f"Channel : {setting[i+1][0]}",linewidth=1,color=setting[i+1][3])
        else:
            plt.plot(data[setting[i+1][0]][-int(setting[i+1][1]):],"o--",label=f"Channel : {setting[i+1][0]}",linewidth=1,color=setting[i+1][3])
    plt.legend(loc="upper left")
    plt.tight_layout()
    

# MAIN FUNCTION CALL
if __name__ == "__main__":
    choose_method()
    plotrate = int(setting[0][2])
    plt.figure(figsize=(16,8))
    ani = FuncAnimation(fig=plt.gcf(), func=plot_resultant,frames=100, interval = int(plotrate))
    plt.tight_layout()
    plt.show()
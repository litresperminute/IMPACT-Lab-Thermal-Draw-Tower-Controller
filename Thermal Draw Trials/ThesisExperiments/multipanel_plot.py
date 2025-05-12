import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib as mpl
import seaborn as sns
import os
import json
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 14


# === Settings ===
experiment_id = 'PETG 160C DR50 Feed Rate Testing'
log_dir = "experiment_logs"
fig_dir = "figures"
os.makedirs(fig_dir, exist_ok=True)

# === Load Data ===
csv_path = os.path.join(log_dir, f"{experiment_id}.csv")
print("Looking in:", csv_path)
json_path = os.path.join(log_dir, f"{experiment_id}_metadata.json")

df = pd.read_csv(csv_path)
with open(json_path, "r") as f:
    meta = json.load(f)

#downsample data to every 10th data point
#df = df.iloc[::10, :]

xfeedrate1 = df[(df["Time(s)"] >= 400.0) & (df["Time(s)"] <= 600.0)]["Time(s)"]
yfeedrate1 = df[(df["Time(s)"] >= 400.0) & (df["Time(s)"] <= 600.0)]["Diameter(um)"]
xfeedrate2 = df[(df["Time(s)"] >= 900.0) & (df["Time(s)"] <= 1100.0)]["Time(s)"]
yfeedrate2 = df[(df["Time(s)"] >= 900.0) & (df["Time(s)"] <= 1100.0)]["Diameter(um)"]
xfeedrate3 = df[(df["Time(s)"] >= 1200.0) & (df["Time(s)"] <= 1400.0)]["Time(s)"]
yfeedrate3 = df[(df["Time(s)"] >= 1200.0) & (df["Time(s)"] <= 1400.0)]["Diameter(um)"]
xfeedrate4 = df[(df["Time(s)"] >= 1600.0) & (df["Time(s)"] <= 1800.0)]["Time(s)"]
yfeedrate4 = df[(df["Time(s)"] >= 1600.0) & (df["Time(s)"] <= 1800.0)]["Diameter(um)"]

print(xfeedrate1)
print(yfeedrate1)
#set the limits of plots
[xmin,xmax] = [0,200]
[ymin,ymax] = [200,1200]

#Try a color from seaborn
colors = sns.color_palette("pastel6",4)

#Prepare multipanel plot
fig = plt.figure(1, figsize = (5,6))
gs = gridspec.GridSpec(4,4)
gs.update(wspace=1, hspace=0.1)

#Generate first panel
#remember, the grid spec is rows, then columns
xtr_subplot = fig.add_subplot(gs[0:1,0:4])

plt.plot(xfeedrate1,yfeedrate1,linestyle='-', marker='o', label='1 mm/min', color=colors[0], mfc='w', markersize=8)

#Define where you want ticks
xticks = np.arange(0,(xmax+1),(xmax/4))
yticks = np.arange(ymin,(ymax+1),(ymax/3))

#xticks = np.arange()
#yticks = np.arange()

plt.minorticks_on()
plt.tick_params(direction='in', which='minor', length=5, bottom=True, top=False, left=True, right=False, labelbottom=False)
plt.tick_params(direction='in', which='major', length=10, bottom=True, top=False, left=True, right=False, labelbottom=False)
plt.xticks(xticks)
plt.yticks(yticks)

#create a legend
plt.legend()

#plot limits
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)

#Generate second panel
xtr_subplot = fig.add_subplot(gs[1:2,0:4])
plt.plot(xfeedrate2,yfeedrate2,linestyle='-', marker='o', label='2 mm/min', color=colors[1], mfc='w', markersize=8)
#Define where you want ticks
xticks = np.arange(0,(xmax+1),(xmax/4))
yticks = np.arange(ymin,(ymax+1),(ymax/3))

#xticks = np.arange()
#yticks = np.arange()

plt.minorticks_on()
plt.tick_params(direction='in', which='minor', length=5, bottom=True, top=False, left=True, right=False)
plt.tick_params(direction='in', which='major', length=10, bottom=True, top=False, left=True, right=False)
plt.xticks(xticks)
plt.yticks(yticks)

#create a legend
plt.legend()

#plot limits
plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)

#Create axes labels
plt.ylabel(r'Fiber diameter ($\mu m$)', fontsize=14)
#plt.text(0,0,r'Fiber diameter ($\mu m$)', fontsize=14, rotation='vertical' )
plt.xlabel('Time (s)', fontsize=14)


xtr_subplot = fig.add_subplot(gs[2:3,0:4])
plt.plot(xfeedrate3,yfeedrate3,linestyle='-', marker='none', label='2 mm/min', color=colors[1], mfc='w', markersize=8)
plt.axhline(y=400, color='b', linestyle='--', label='target')
xtr_subplot = fig.add_subplot(gs[3:4,0:4])
plt.plot(xfeedrate4,yfeedrate4,linestyle='-', marker='none', label='2 mm/min', color=colors[1], mfc='w', markersize=8)






plt.show()
#pull data from CSV


__author__ = 'milan'

import json
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')


from smapanalysis import analyze
from sklearn.cluster import KMeans

config_file = "../data.json"

# Process and read configurations
with open(config_file) as data_file:
    conf = json.load(data_file)

activities = ["AllOpen", "AllClose", "Window50", "Window100", "MainDoor50", "MainDoor100", "SecondaryDoor50",
              "SecondaryDoor100"]
room = ["Bedroom"]

#pdf, edf = analyze.compare_activities(activities, room, conf)
#print pdf.describe()
#print edf.describe()
#pdf.plot()
#est = KMeans(n_clusters=2)
#est.fit(pdf[["Temperature_Ds18B20_AllClose"]].values)

#edf.plot(style='*')
#plt.show()

df1, df2 = analyze.peak_analysis(activities, room, conf)
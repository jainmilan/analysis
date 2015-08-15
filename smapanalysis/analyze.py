__author__ = 'milan'

import numpy
import pandas

from data_handler import data_frame
from sklearn.cluster import KMeans
from plot import scatter_plot, yy_plot

import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('fivethirtyeight')


def compare_activities(activities, room, conf):

    #sensor_tint = ["lrl1"]
    sensor_power = ["brac"]
    sensor_text = ["wuconditions"]

    #df_tint = compare_sensors(activities, room, conf, "temperature_ds18b20", sensor_tint)
    df_power = data_frame(activities, room, conf, ["power"], sensor_power)
    df_text = data_frame(activities, room, conf, ["temperature_ds18b20"], sensor_text)

    return df_power, df_text


def generate_clusters(df, clusters):
    # Preprocess data
    X = df.fillna(0).values
    X1 = X.reshape((len(X)),1)

    # Initialize and fit clustering algorithm
    est = KMeans(n_clusters=clusters)
    est.fit(X1)

    # Get learned labels
    labels = est.labels_

    return max(est.cluster_centers_), labels


def peak_analysis(activities, room, conf):
    sensors = ["power", "temperature_ds18b20"]
    locations = dict()
    locations["temperature_ds18b20"] = ["wuconditions"]
    if room[0] == "Bedroom":
        locations["power"] = ["brac"]
    else:
        locations["power"] = ["lr"]

    df = data_frame(activities, room, conf, sensors, locations)
    peaks = numpy.array([])

    fig = plt.figure(figsize=(18,12), facecolor='w', edgecolor='k')
    fig.suptitle(room[0] + " Peak Power Analysis", fontsize=14, fontweight='bold')
    idx = 1
    power_cols = filter(lambda x: 'Power' in x, df.columns)
    plots = 100*(numpy.ceil(len(power_cols)/2)+1) + 20
    results = pandas.DataFrame(index=activities)
    for column in power_cols:
        power_df = df[column]
        if len(power_df[power_df < 1500]) == 0:
            clusters = 1
        else:
            clusters = 3

        peak_value, labels = generate_clusters(power_df, clusters = clusters)
        peaks = numpy.append(peaks, peak_value)

        activity = column.split('_')[1]
        val = activity + '_Temperature'
        text_col = filter(lambda x: val in x, df.columns)

        results.loc[activity, "Peak"] = peak_value
        results.loc[activity, "Text_Avg"] = df[text_col[0]].mean()

        ax = plt.subplot(plots + idx)
        scatter_plot(power_df, labels, ax, activity)
        idx = idx + 1

    ax1 = plt.subplot(plots + idx)  # Create matplotlib axes
    results.to_csv('Results/Stats/Raw/' + room[0] + '_Summary.csv')
    yy_plot(results["Peak"], results["Text_Avg"], ax1)

    fig.tight_layout()

    plt.savefig('Results/Figures/Raw/' + room[0] + '_Plot.png')
    return results, df

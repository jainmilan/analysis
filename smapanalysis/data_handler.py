__author__ = 'milan'
import sys
import pandas
import requests

from preprocessor import clean, preprocess, get_time


def read_file(filename, index_col):
    df = pandas.read_csv(filename, index_col=index_col, na_filter=False)
    return df


def read_activities(filename="meta-info/activity.csv"):
    index_col = [0]
    activity_tags = read_file(filename, index_col)
    return activity_tags


def read_summary(filename="meta-info/summary.csv"):
    index_col=["ActivityID"]
    summary = read_file(filename, index_col)
    return summary


def get_tag(activity, room):
    summary = read_summary()
    tags = read_activities()
    x = summary[(summary['Event']==activity) & (summary['Room']==room)]
    tag = tags.loc[x.index.values[0]]
    return tag


def get_data(uuid, server, port, title, start, end):
    # URL of the dataset
    url = "http://" + server + ":" + port + "/api/data/uuid/" + uuid + "?endtime=" + str(int(end)*1000) + \
          "&starttime=" + str(int(start)*1000) + "&limit=-1"

    # Request for the data in json format
    print url

    try:
        r = requests.get(url)
    except Exception as e:
        print e
        sys.exit(1)

    archiver_data = r.json()

    if len(archiver_data[0]['Readings']) == 0:
        sys.exit(1)

    # Convert to dataframe
    df = pandas.DataFrame(archiver_data[0]['Readings'], columns=["Timestamp",title])
    df = df.set_index('Timestamp')
    df.index = pandas.to_datetime(df.index, unit='ms')
    df = df.tz_localize("UTC").tz_convert("Asia/Kolkata")

    df = clean(df, title)

    # Return series having datetimeindex to resample and further processing
    return df


def get_frame(conf, sensor, location, start, end):
    df = pandas.DataFrame()

    # UUID of the data to retrieve
    uuid = conf[sensor][location]["uuid"]
    # IP Address of the Archiver
    server = conf["archiver"]
    # Port of the Archiver
    port = conf[sensor][location]["archiver_port"]

    # Title of the column in the frame
    title = sensor.title() + "_" + location

    # Get frame for each location
    tframe = get_data(uuid, server, port, title, start, end)

    df = preprocess(tframe)
    return df


def data_frame(activities, rooms, conf, sensors, location_dict):
    df = pandas.DataFrame()
    n_cols = []
    for room in rooms:
        for activity in activities:
            for sensor in sensors:
                locations = location_dict[sensor]
                for location in locations:
                    tag = get_tag(activity, room)

                    exp_date = tag["Date"]
                    s_time = tag["Start"]
                    e_time = tag["Stop"]

                    date_frmt = conf["date_frmt"]

                    start = get_time(exp_date, s_time, date_frmt) - 30*60
                    stop = get_time(exp_date, e_time, date_frmt) + 30*60

                    df_temp = get_frame(conf, sensor, location, start, stop)
                    df_temp = df_temp.reset_index(drop=True)

                    new_col = room + "_" + activity + "_" + sensor.title() + "_" + location
                    n_cols.append(new_col)
                    df[new_col] = df_temp

    df.columns = n_cols
    return df



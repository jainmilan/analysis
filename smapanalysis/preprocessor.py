__author__ = 'milan'

import time

def preprocess(frame):
    resample_df = frame.resample('1S')
    df = resample_df.interpolate()
    df = df.dropna()
    return df


def clean(frame, title):
    dtype = title.split('_')[0].lower()
    if dtype == "power":
        frame = frame[frame[title] < 4000]
    elif dtype == "temperature":
        temp = frame[frame[title] > 15]
        frame = temp[temp[title] < 45]
    else:
        print "Unknown data type"

    return frame


def get_time(date_str, time_str, format_str):
    # Get time object from the string
    time_object = time.strptime(date_str + " " + time_str, format_str)
    # Convert to UNIX Timestamp
    epoch_time = time.mktime(time_object)
    return epoch_time


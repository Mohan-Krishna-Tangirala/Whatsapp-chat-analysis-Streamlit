import streamlit as st
import pandas as pd
from datetime import datetime
import re
import second
import matplotlib.pyplot as plt




def fetch_stats(selected_user,df):
    
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    

    num_media_messages = df[df['message'].str.contains(r'.*omitted', na=False)].shape[0]


    return num_messages, len(words), num_media_messages


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"index":"name","user":"percent"})
    return x, df

def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time

    return timeline


def week_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    

    return df['day_name'].value_counts()
        

    
def month_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heat_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]


    activity_heatmap = df.pivot_table(index="day_name", columns='period', values = 'message', aggfunc='count').fillna(0)

    return activity_heatmap


import streamlit as st
import pandas as pd
from datetime import datetime
import re
import second
import matplotlib.pyplot as plt
import seaborn as sns


st.write("Export your chart and upload...")


def preprocess(data):
    
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s[AP]M\]'

    messages = re.split(pattern,data)
    messages = re.split(pattern,data)[1:]

    dates = re.findall(pattern,data)

    converted_dates = []
    for date_str in dates:
        # Remove brackets and normalize time
        cleaned_str = date_str.strip('[]').replace('\u202f', ' ')
    
        # Parse the datetime
        dt = datetime.strptime(cleaned_str, '%d/%m/%y, %I:%M:%S %p')
    
        # Format to 24-hour time
        converted_dates.append(dt.strftime('%d/%m/%y, %H:%M'))

    df = pd.DataFrame({'user_message':messages, 'date':converted_dates})

    df['date'] = pd.to_datetime(df['date'], format = '%d/%m/%y, %H:%M')

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:   
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.apped('group_notification')
            message.append(entry[0])
        
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)


    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period




    return df



st.sidebar.title("Whatsapp chat analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess(data)

    

    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")


    selected_user = st.sidebar.selectbox("Show wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_messages = second.fetch_stats(selected_user,df)
        
        st.title("Top statistics")


        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        
        with col2:
            st.header("Total Words")
            st.title(words)
        
        with col3:
            st.header("Media shared")
            st.title(num_media_messages)


        st.title("Monthly timeline")
        timeline = second.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = 'green')
        plt.xticks(rotation = "vertical")
        st.pyplot(fig) 



        st.title("Activity map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = second.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation = "vertical")
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = second.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation = "vertical")
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            st.pyplot(fig)

        


        st.title("Weekly activity map")
        activity_heatmap = second.activity_heat_map(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_heatmap)
        st.pyplot(fig)




        # finding the busiest user in the group

        if selected_user == "Overall":
            st.title("Most busy users")
            x, new_df = second.most_busy_users(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation ="vertical")
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)

        










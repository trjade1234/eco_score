from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from gsheetsdb import connect
#from google.oauth2 import service_account3
from math import sin, cos, sqrt, atan2, radians
from datetime import datetime



#st.title('This is Eco-score!')
st.title("生态驾驶，您的绿色驾驶新体验")

#if st.sidebar.button('Back to home'):
#    st.write("  ")


#if st.sidebar.button('Loading trajectory'):
gs_id = "137n-Z1L7980e6SKL7XbqTrVO1yNRtg6QC8V6j8rCUPA"
sheetname = "carpooling_gps_processed"
gs_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gs_id, sheetname)
#st.write(gs_url)
df = pd.read_csv(gs_url, encoding = 'utf-8')
st.write(df.head())

vehid = df.vehid.unique()
        
#select a specific vehicle
#st.subheader('Choose one vehicle to visualize')
st.subheader("您想查看哪辆车")
vehoption = st.selectbox('', df.vehid.unique())
vehselected = df[df.vehid == vehoption]

#select a spcific trip of that vehicle
#st.write('This vehicle has in total ', str(len(vehselected.orderid.unique())), ' trips')
st.write('这辆车共有',str(len(vehselected.orderid.unique())), '条行程')

#st.subheader('Choose one trip to visualize')
st.subheader("您想查看哪趟行程")
tripoption = st.selectbox('', vehselected.orderid.unique())
tripselected = vehselected[vehselected.orderid == tripoption]
st.write(tripselected.head())

#st.subheader('This is the trajectory')
st.subheader("行程路线图")
map_data = pd.DataFrame(columns = ['lat', 'lon'])
map_data['lat'] = tripselected.latitude
map_data['lon'] = tripselected.longitude
st.map(map_data)

scores = 70
if st.sidebar.button('查看您的驾驶评分'):
        st.subheader(str('总评分'+str(scores)))
        my_bar = st.progress(0)
        my_bar.progress(scores + 1) #this has to be changed

if st.sidebar.button('驾驶轨迹分项分析'):
        avgspeed = tripselected['distance'].sum()/(tripselected['timediff'].sum())*3.6 #km/h
        avgacc = tripselected['acceleration'].mean()
        idleperc = 0.1
        st.subheader(str('平均速度'+str(round(avgspeed,2))+'km/h'+' 排名前50%'))
        avgspeed_bar = st.progress(0)
        avgspeed_bar.progress(50 + 1) #this has to be changed
        st.subheader(str('平均加速度'+str(round(avgacc,2))+'m/s2'+' 排名前50%'))
        avgacc_bar = st.progress(0)
        avgacc_bar.progress(60 + 1) #this has to be changed
        st.subheader(str('怠速比例'+str(idleperc*100)+'%'+' 排名前80%'))
        idleperc_bar = st.progress(0)
        idleperc_bar.progress(80 + 1) #this has to be changed

        


########################################################################################################################
##################################archived##############################################################################


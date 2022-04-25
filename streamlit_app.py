from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from gsheetsdb import connect
#from google.oauth2 import service_account3
from math import sin, cos, sqrt, atan2, radians
from datetime import datetime

#define distance function
def distance(long1, long2, lat1, lat2): #in km
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(long1)
    lat2 = radians(lat2)
    lon2 = radians(long2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

def power(speed, acc):
    ptractive = (2.76*speed+0.27*(speed**2)+1672.34*acc-23.6)
    if ptractive >= 0:
        p = 1.285*ptractive*speed + 2548.1 #watt
    else:
        p = 0.894*ptractive*speed + 3070.6 #watt
    return p


#st.title('This is Eco-score!')
st.title("生态驾驶，您的绿色驾驶新体验")

#if st.sidebar.button('Back to home'):
#    st.write("  ")


#if st.sidebar.button('Loading trajectory'):
gs_id = "1JznNtYSlTlOwmFq8baTR4Ws0r7f865wyPe2NG4m45a0"
sheetname = "sampledata"
gs_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gs_id, sheetname)
#st.write(gs_url)
df = pd.read_csv(gs_url, encoding = 'utf-8')
st.write(df.head())

vehid = df.vehid.unique()
dist = 0
df['timediff'] = 0
df['speed'] = 0
df['acceleration'] = 0
df['e_power'] = 0
for i in range(1, len(df)):
    if df['orderid'][i] == df['orderid'][i-1]:
        print((datetime.strptime(df['time'][i],"%H:%M:%S")-datetime.strptime(df['time'][i-1],"%H:%M:%S")).seconds)
        df['timediff'][i] = (datetime.strptime(df['time'][i],"%H:%M:%S")-datetime.strptime(df['time'][i-1],"%H:%M:%S")).seconds
        dist = distance(df['longitude'][i],df['longitude'][i-1],df['latitude'][i],df['latitude'][i-1])
        df['speed'][i] = dist/(df['timediff'][i]/3600)
        df['acceleration'][i] = (df['speed'][i]-df['speed'][i-1])/3.6/df['timediff'][i] #m/s2
        df['e_power'][i] = power(df['speed'][i]/3.6, df['acceleration'][i])

        
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
        dist = 0
        for i in range(1, len(tripselected)):
                dist += tripselected['speed'][i]/3.6*tripselected['timediff'][i] #meters
        avgspeed = dist/(sum(tripselected['timediff']))*3.6 #km/h
        avgacc = mean(tripselected['acceleration'])
        idleperc = 0.1
        st.subheader(str('平均速度'+str(round(avgspeed,2))+'km/h'+' 排名前50%'))
        avgspeed_bar = st.progress(0)
        avgspeed_bar.progress(50 + 1) #this has to be changed
        st.subheader(str('平均加速度'+str(round(avgacc,2))+'km/h'+' 排名前50%'))
        avgacc_bar = st.progress(0)
        avgacc_bar.progress(60 + 1) #this has to be changed
        st.subheader(str('怠速比例'+str(idleperc*100)+'%'+' 排名前80%'))
        idleperc_bar = st.progress(0)
        idleperc_bar.progress(80 + 1) #this has to be changed

        


########################################################################################################################
##################################archived##############################################################################


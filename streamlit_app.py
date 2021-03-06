from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from gsheetsdb import connect
#from google.oauth2 import service_account3
from math import sin, cos, sqrt, atan2, radians
from datetime import datetime
import pyTigerGraph as tg


#st.title('This is Eco-score!')
st.title("生态驾驶，您的绿色驾驶新体验")

#if st.sidebar.button('Back to home'):
#    st.write("  ")


#if st.sidebar.button('Loading trajectory'):
gs_id = "1JznNtYSlTlOwmFq8baTR4Ws0r7f865wyPe2NG4m45a0"
sheetname = "processed_sample"
gs_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gs_id, sheetname)
#st.write(gs_url)
df = pd.read_csv(gs_url, encoding = 'utf-8')
#st.write(df.head())

vehid = df.vehid.unique()
        
#select a specific vehicle
#st.subheader('Choose one vehicle to visualize')
st.success("您想查看哪辆车")
vehoption = st.selectbox('选择车辆编号', df.vehid.unique())
vehselected = df[df.vehid == vehoption]

#select a spcific trip of that vehicle
#st.write('This vehicle has in total ', str(len(vehselected.orderid.unique())), ' trips')
#st.markdown(str('这辆车共有'+str(len(vehselected.orderid.unique()))+'条行程'))

#st.subheader('Choose one trip to visualize')
st.success("您想查看哪趟行程")
tripoption = st.selectbox('选择行程编号', vehselected.orderid.unique())
tripselected = vehselected[vehselected.orderid == tripoption]
#st.write(tripselected.head())


col1, col2 = st.columns(2)

#st.subheader('This is the trajectory')
map_data = pd.DataFrame(columns = ['lat', 'lon'])
map_data['lat'] = tripselected.latitude
map_data['lon'] = tripselected.longitude
with col1:
        st.success("行程路线图")
        st.map(map_data)

scores = 70
with col2:
        st.success('评分状况')
if st.sidebar.button('查看您的驾驶评分'):
        with col2:
                st.markdown('**总评分状况**')
                st.write(str('总评分'+str(scores)))
                my_bar = st.progress(0)
                my_bar.progress(scores + 1) #this has to be changed

if st.sidebar.button('驾驶轨迹分项分析'):
        avgspeed = tripselected['distance'].sum()/(tripselected['timediff'].sum())*3.6 #km/h
        avgacc = tripselected['acceleration'].mean()
        idleperc = 0.1
        with col2:
                st.markdown('**分项评分状况**')
                st.write(str('平均速度'+str(round(avgspeed,2))+'km/h'+' 排名前50%'))
                avgspeed_bar = st.progress(0)
                avgspeed_bar.progress(50 + 1) #this has to be changed
                st.write(str('平均加速度'+str(round(avgacc,2))+'m/s2'+' 排名前50%'))
                avgacc_bar = st.progress(0)
                avgacc_bar.progress(60 + 1) #this has to be changed
                st.write(str('怠速比例'+str(idleperc*100)+'%'+' 排名前80%'))
                idleperc_bar = st.progress(0)
                idleperc_bar.progress(80 + 1) #this has to be changed

        


########################################################################################################################
##################################archived##############################################################################


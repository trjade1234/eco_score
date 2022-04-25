from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from gsheetsdb import connect
from google.oauth2 import service_account3

#st.title('This is Eco-score!')
st.success.title("生态驾驶，您的绿色驾驶新体验")

#if st.sidebar.button('Back to home'):
#    st.write("  ")


#if st.sidebar.button('Loading trajectory'):
gs_id = "1JznNtYSlTlOwmFq8baTR4Ws0r7f865wyPe2NG4m45a0"
sheetname = "sampledata"
gs_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gs_id, sheetname)
#st.write(gs_url)
df = pd.read_csv(gs_url, encoding = 'utf-8')
st.write(df.head())


        
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

if st.sidebar.button('查看您的驾驶评分'):
        st.subheader('总评分')
        my_bar = st.progress(0)
        my_bar.progress(70 + 1) #this has to be changed

if st.sidebar.button('驾驶轨迹分项分析'):
        distance = 0
        for i in range(1, len(tripselected)):                
                R = 6373.0
                lat1 = radians(tripselected['latitude'][i])
                lon1 = radians(tripselected['longitude'][i])
                lat2 = radians(tripselected['latitude'][i-1])
                lon2 = radians(tripselected['longitude'][i-1])
                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance += R * c
        avgspeed = distance/(len(tripselected)*3/3600)
        st.subheader(str('平均速度'+str(round(avgspeed,2))))

        


########################################################################################################################
##################################archived##############################################################################


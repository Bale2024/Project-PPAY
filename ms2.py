import pandas as pd
import streamlit as st
import plotly.express as px
import json 
import os 
import requests
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.types import VARCHAR,Integer,FLOAT,DOUBLE_PRECISION,Text,BIGINT
# Importing Data from Github repository to local machine
url ='https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
response = requests.get(url)
data = json.loads(response.content)
state_names = [i['properties']['ST_NM'] for i in data['features']]
state_names.sort()
# Dicitonary to match the state names
name_map = {'nagaland': 'Nagaland', 
            'punjab': 'Punjab', 
            'chhattisgarh': 'Chhattisgarh', 
            'gujarat': 'Gujarat', 
            'jammu-&-kashmir': 'Jammu & Kashmir', 
            'goa': 'Goa', 
            'arunachal-pradesh': 'Arunachal Pradesh', 
            'kerala': 'Kerala', 
            'delhi': 'Delhi', 
            'tamil-nadu': 'Tamil Nadu', 
            'puducherry': 'Puducherry', 'haryana': 'Haryana', 'lakshadweep': 'Lakshadweep', 'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu', 'maharashtra': 'Maharashtra', 'assam': 'Assam', 'uttar-pradesh': 'Uttar Pradesh', 'manipur': 'Manipur', 'odisha': 'Odisha', 'uttarakhand': 'Uttarakhand', 'tripura': 'Tripura', 'karnataka': 'Karnataka', 'andaman-&-nicobar-islands': 'Andaman & Nicobar', 'chandigarh': 'Chandigarh', 'jharkhand': 'Jharkhand', 'himachal-pradesh': 'Himachal Pradesh', 'andhra-pradesh': 'Andhra Pradesh', 'rajasthan': 'Rajasthan', 'madhya-pradesh': 'Madhya Pradesh', 'west-bengal': 'West Bengal', 'telangana': 'Telangana', 'mizoram': 'Mizoram', 'ladakh': 'Ladakh', 'bihar': 'Bihar', 'meghalaya': 'Meghalaya', 'sikkim': 'Sikkim' }
# 1. Extraction of Data related to Aggregated category 
Agg_trns = {'state':[],'year':[],'quarter':[],'transaction_type':[],'transaction_count':[],'transaction_amt':[]}
path_1  = r"E:\phonepay\data\aggregated\transaction\country\india\state"
agg_state_list = os.listdir(path_1)
for i in  agg_state_list:
    p_i = path_1 + "\\"+ i
    agg_year_list = os.listdir(p_i)
    for j in agg_year_list:
        p_j = p_i + "\\" + j
        agg_qrtr_list = os.listdir(p_j)
        for k in agg_qrtr_list:
            p_k = p_j + "\\" + k 
            data = open(p_k,'r')
            D = json.load(data)
            for z in D['data']['transactionData']:
                name = z['name']
                count = z['paymentInstruments'][0]['count']
                amount = z['paymentInstruments'][0]['amount']
                Agg_trns['state'].append(i)
                Agg_trns['year'].append(j)
                Agg_trns['quarter'].append(int(k.strip('.json')))
                Agg_trns['transaction_type'].append(name)
                Agg_trns['transaction_count'].append(count)
                Agg_trns['transaction_amt'].append(amount)
df_Agg_trns = pd.DataFrame(Agg_trns)
df_Agg_trns['state']= df_Agg_trns['state'].map(name_map)

import numpy as np
Agg_user = {'state':[],'year':[],'quarter':[],'User_mob_brand':[],'User_count':[],'User_percentage':[]}
path_2 = r"E:\phonepay\data\aggregated\user\country\india\state"
agg_state_list = os.listdir(path_2)
for i in  agg_state_list:
    p_i = path_2 + "\\"+ i
    agg_year_list = os.listdir(p_i)
    for j in agg_year_list:
        p_j = p_i + "\\" + j
        agg_qrtr_list = os.listdir(p_j)
        for k in agg_qrtr_list:
            p_k = p_j + "\\" + k 
            data = open(p_k,'r')
            D = json.load(data)
            try:
                for z in D['data']['usersByDevice']:
                    brand = z['brand'] 
                    count = z['count']
                    percentage = z['percentage']
                    Agg_user['state'].append(i)
                    Agg_user['year'].append(j)
                    Agg_user['quarter'].append(int(k.strip('.json')))
                    Agg_user['User_mob_brand'].append(brand)
                    Agg_user['User_count'].append(count)
                    Agg_user['User_percentage'].append(percentage)
            except:
                brand = None
                count = np.nan    
                percentage = np.nan
                Agg_user['state'].append(i)
                Agg_user['year'].append(j)
                Agg_user['quarter'].append(int(k.strip('.json')))
                Agg_user['User_mob_brand'].append(brand)
                Agg_user['User_count'].append(count)
                Agg_user['User_percentage'].append(percentage)
df_Agg_user = pd.DataFrame(Agg_user)
df_Agg_user['state']= df_Agg_user['state'].map(name_map)
# Data cleaning :
df_Agg_user.dropna(ignore_index=True, inplace=True)
# 2. Data Extraction related to Map Category:
Map_trns = {'state':[],'year':[],'quarter':[],'dist_name':[],'transaction_count':[],'transaction_amt':[]}
path_3 = r"E:\phonepay\data\map\transaction\hover\country\india\state"
Map_state_list = os.listdir(path_3)
for i in  Map_state_list:
    p_i = path_3 + "\\"+ i
    Map_year_list = os.listdir(p_i)
    for j in Map_year_list:
        p_j = p_i + "\\" + j
        Map_qrtr_list = os.listdir(p_j)
        for k in Map_qrtr_list:
            p_k = p_j + "\\" + k 
            data = open(p_k,'r')
            D = json.load(data)
            for z in D['data']['hoverDataList']:
                name = z['name']
                count = z['metric'][0]['count']
                amount = z['metric'][0]['amount']
                Map_trns['state'].append(i)
                Map_trns['year'].append(j)
                Map_trns['quarter'].append(int(k.strip('.json')))
                Map_trns['dist_name'].append(name)
                Map_trns['transaction_count'].append(count)
                Map_trns['transaction_amt'].append(amount)
df_Map_trns = pd.DataFrame(Map_trns)
df_Map_trns['state']=df_Map_trns['state'].map(name_map)
Map_user = {'state':[],'year':[],'quarter':[],'dist_name':[],'regd_users':[],'app_opens_count':[]}
path_4 = r"E:\phonepay\data\map\user\hover\country\india\state"
Map_state_list = os.listdir(path_4)
for i in  Map_state_list:
    p_i = path_4 + "\\"+ i
    Map_year_list = os.listdir(p_i)
    for j in Map_year_list:
        p_j = p_i + "\\" + j
        Map_qrtr_list = os.listdir(p_j)
        for k in Map_qrtr_list:
            p_k = p_j + "\\" + k 
            data = open(p_k,'r')
            D = json.load(data)
            for y,z in D['data']['hoverData'].items():
                name = y
                regd_users= z['registeredUsers']
                app_opens_count= z['appOpens']
                Map_user['state'].append(i)
                Map_user['year'].append(j)
                Map_user['quarter'].append(int(k.strip('.json')))
                Map_user['dist_name'].append(name)
                Map_user['regd_users'].append(regd_users)
                Map_user['app_opens_count'].append(app_opens_count)
df_Map_user = pd.DataFrame(Map_user)            
df_Map_user['state']=df_Map_user['state'].map(name_map)
# 3. Data Extraction related to Top Category:
Top_trns_dst = {'state':[],'year':[],'quarter':[],'dist_name':[],'transaction_count':[],'transaction_amt':[]}
Top_trns_pin = {'state':[],'year':[],'quarter':[],'dist_pin':[],'transaction_count':[],'transaction_amt':[]}
path_5 = r"E:\phonepay\data\top\transaction\country\india\state"
Top_state_list = os.listdir(path_5)
for i in Top_state_list:
    p_i = path_5 + "\\" + i
    Top_year_list = os.listdir(p_i)
    for j in Top_year_list:
     p_j = p_i + "\\" + j
     Top_quarter_list = os.listdir(p_j)
     for k in Top_quarter_list:
        p_k= p_j + "\\" + k
        data = open(p_k,'r')
        D = json.load(data)
        #
        for y in D['data']['districts']:
           name = y['entityName']
           count = y['metric']['count']
           amount = y['metric']['amount']
           Top_trns_dst['state'].append(i)
           Top_trns_dst['year'].append(j)
           Top_trns_dst['quarter'].append(int(k.strip('.json')))
           Top_trns_dst['dist_name'].append(name)
           Top_trns_dst['transaction_count'].append(count)
           Top_trns_dst['transaction_amt'].append(amount)
        #
        for z in D['data']['districts']:
           name = z['entityName']
           count = z['metric']['count']
           amount = z['metric']['amount']
           Top_trns_pin['state'].append(i)
           Top_trns_pin['year'].append(j)
           Top_trns_pin['quarter'].append(int(k.strip('.json')))
           Top_trns_pin['dist_pin'].append(name)
           Top_trns_pin['transaction_count'].append(count)
           Top_trns_pin['transaction_amt'].append(amount)
df_Top_trns_dst = pd.DataFrame(Top_trns_dst)  
df_Top_trns_pin = pd.DataFrame(Top_trns_pin)  
df_Top_trns_dst['state']=df_Top_trns_dst['state'].map(name_map)
df_Top_trns_pin['state']=df_Top_trns_pin['state'].map(name_map)

Top_user_dst = {'state':[],'year':[],'quarter':[],'dist_name':[],'regd_users':[]}
Top_user_pin = {'state':[],'year':[],'quarter':[],'dist_pin':[], 'regd_users':[]}
path_6 = r"E:\phonepay\data\top\user\country\india\state"
Top_state_list = os.listdir(path_6)
for i in Top_state_list:
    p_i = path_6 + "\\" + i
    Top_year_list = os.listdir(p_i)
    for j in Top_year_list:
     p_j = p_i + "\\" + j
     Top_quarter_list = os.listdir(p_j)
     for k in Top_quarter_list:
        p_k= p_j + "\\" + k
        data = open(p_k,'r')
        D = json.load(data)
        for y in D['data']['districts']:
           name = y['name']
           regd_users = y['registeredUsers']
           Top_user_dst['state'].append(i)
           Top_user_dst['year'].append(j)
           Top_user_dst['quarter'].append(int(k.strip('.json')))
           Top_user_dst['dist_name'].append(name)
           Top_user_dst['regd_users'].append(regd_users)
        for z in D['data']['districts']: 
           name = y['name']
           regd_users = y['registeredUsers']
           Top_user_pin['state'].append(i)
           Top_user_pin['year'].append(j)
           Top_user_pin['quarter'].append(int(k.strip('.json')))
           Top_user_pin['dist_pin'].append(name)
           Top_user_pin['regd_users'].append(regd_users)
df_Top_user_dst = pd.DataFrame(Top_user_dst)
df_Top_user_pin = pd.DataFrame(Top_user_pin)
df_Top_user_dst['state']=df_Top_user_dst['state'].map(name_map)
df_Top_user_pin['state']=df_Top_user_pin['state'].map(name_map)

# Establish connection with the datbase 
engine = create_engine('postgresql://postgres:7799@localhost:5433/phonepe')
conn = engine.connect()
def data_sql(df, table_name):
   df.to_sql(name=table_name, con = engine, if_exists='replace', index=False)
   engine.dispose()
# Migrating data to postgres database 
data_sql(df_Agg_trns, 'Agg_trnsn') 
data_sql(df_Agg_user, 'Aggd_user') 
data_sql(df_Map_trns, 'Map_trnsc')
data_sql(df_Map_user, 'Map_user')
data_sql(df_Top_trns_dst, 'Top_trnsd')
data_sql(df_Top_trns_pin, 'Top_trnsp')
data_sql(df_Top_user_dst, 'Top_userd')
data_sql(df_Top_user_pin, 'Top_userp')

# Streamlit App
st.set_page_config(page_title = "Phonepe", layout='wide')
 
st.title(":violet[PHONEPE PULSE DATA VISUALIZATION]")
with st.sidebar:
    options_menu = st.radio("Choose an option",("Home","Data Visualization"))
    st.image("https://images.seeklogo.com/logo-png/33/1/phonepe-logo-png_seeklogo-339867.png")
    st.write("PAY WITH PHONEPE EVERYWHERE YOU GO")
    st.image("https://www.phonepe.com/webstatic/8674/static/4a61ea7c648229cda71b85e3a5a06fca/4087d/nt_insurance.png", caption="PhonePe Logo")
#choice = st.sidebar.selectbox("Home","Data Analysis")
if options_menu == "Home":
  st.write("Project Description: Extract the phonepe data from Github Repository,store in a database and fetch from database to perfrom Data Visualization based on the queries")
  st.write("About: PhonePe is an Indian digital payment and financial services company hequartered in Bengaluru",
  "Phonepe is a Digital Wallet and Online Payment App that allows you to make Instant money transfers through UPI")
  image_url = 'https://www.phonepe.com/webstatic/8674/static/6341d1762ac4ed98d04996c9b03b5eb5/628b0/hp-banner4wt.webp'
  st.image(image_url, caption='PhonePe App', use_container_width=True)
else: 
  tab1,tab2,tab3 = st.tabs(["Aggregated", "Map", "Top"])
  with tab1:
    category = st.radio("Select a category",['transaction','user'])
    #sel_year = st.selectbox("Select a year",df_Agg_trns['year'].unique())
    #sel_quart = st.selectbox("Select a quarter",df_Agg_trns['quarter'].unique())
    #sel_year = int(sel_year)
    #sel_quart = int(sel_quart)
    years= list(range(2018,2025))
    selct_year = st.selectbox('Choose a year:',years,key='year_selectbox')
    selct_quart = st.selectbox('Choose a quarter:', ('1','2','3','4'),index=0)
    note = st.write("Hint-Please select upto 2nd quarter for 2024")
    if category == 'transaction':
        insight = st.selectbox("Choose a question ", ("1.What are the top ten states in the order of  Total Revenue for a year",
                                                      "2.Breakdown of Aggregated Transaction amount Categorically",
                                                      "3.Find the Quarterly transaction count"))
        if insight== "1.What are the top ten states in the order of  Total Revenue for a year":
            query = text('''select state, sum(transaction_amt) as TotalRevenue
                                from "Agg_trnsn"
                                where CAST("Agg_trnsn"."year" AS INTEGER) = :selct_year 
                                group by state
                                order by TotalRevenue desc
                                limit 10;''')
            df_Q1 = pd.read_sql(query,con= engine,params={'selct_year': selct_year, 'selct_quart': selct_quart})
            fig1 = px.bar(df_Q1, x='state', y ='totalrevenue',title='Top ten states by Total Revenue')  
            st.plotly_chart(fig1) 
            st.write(df_Q1) 
        elif insight=="2.Breakdown of Aggregated Transaction amount Categorically":
            df_Q2 = pd.read_sql('''select transaction_type,sum(transaction_amt) as aggregated_transaction_amount
                            from "Agg_trnsn"
                            group by transaction_type;
                            ''', con = engine)
            fig2 = px.pie(df_Q2, names = 'transaction_type', values='aggregated_transaction_amount',
                    title='Break-down of Aggregated Transaction Amount Category-wise', hover_data = ['aggregated_transaction_amount'],
                    labels = {'transaction_type':'Transaction Type',
                                'aggregated_transaction_amount':'Amount (in Rs)'})
            st.plotly_chart(fig2)
            st.write(df_Q2)
        elif insight =="3.Find the Quarterly transaction count":
            df_Q3 = pd.read_sql('''select year,quarter,count(*)as Transaction_count
                            from "Agg_trnsn"
                            group by year,quarter
                            order by year,quarter;
                            ''', con = engine) 
            df_Q3['quarter']= df_Q3['quarter'].astype(str)
            fig3 = px.bar(df_Q3, x='year',y='transaction_count', title="Transaction count Quarter-wise ",
                    labels={'quarter':'Quarter'},color = 'quarter',
                    color_discrete_sequence=px.colors.qualitative.Pastel, barmode = 'stack')
            st.plotly_chart(fig3)
            
            df_agg_trns1 = df_Agg_trns[(df_Agg_trns['year']=="2018") &(df_Agg_trns['quarter']==1)]  
            df_trns = df_agg_trns1.groupby('state')['transaction_count'].sum().reset_index()
            fig = px.choropleth(df_trns,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='state',
                color='transaction_count',
                color_continuous_scale='rainbow',
                hover_name ='state',
                title = "Transaction count across the Indian states",
                height = 700)
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)
    else:
        
        insight = "4.Find the Quarter-wise growth rate of a year- Select only the year from the first dropdown above"
        insight_sel = st.selectbox(insight,selct_year)
        query = text('''WITH Quarterly_Data AS (
                            SELECT 
                                CAST("Aggd_user"."year" AS INTEGER) as "year",
                                "Aggd_user"."quarter",
                                SUM("User_count") AS "Quarterly_Usercount"
                            FROM 
                                "Aggd_user"
                            WHERE 
                                CAST("Aggd_user"."year" AS INTEGER) = :selct_year
                            GROUP BY 
                                CAST("Aggd_user"."year" AS INTEGER),
                                "Aggd_user"."quarter"
                            )
                            SELECT 
                                "year",
                                "quarter",
                                "Quarterly_Usercount",
                                ("Quarterly_Usercount" - LAG("Quarterly_Usercount") OVER (PARTITION BY "year" ORDER BY "year", "quarter")) / NULLIF(LAG("Quarterly_Usercount") OVER (PARTITION BY "year" ORDER BY "year", "quarter"), 0)*100 AS Growth_Rate
                            FROM 
                                Quarterly_Data
                            ORDER BY 
                                "year",
                                "quarter";
                            ''')
        #with engine.connect() as conn:  
          #   result = conn.execute(query) 
           # data = result.fetchall()  
        #columns = ["year", "quarter", "Quarterly_Usercount", "Growth_Rate"] 
        #df_Q4 = pd.DataFrame(data,columns=columns)
        try:
            if 2018<=int(selct_year)<2022:
               df_Q6 = pd.read_sql(query, con=engine,params={'selct_year': selct_year})
            else:
                raise ValueError('Year out of range')
        except ValueError:
            st.warning(f"The selected year {selct_year} is out of range") 
        else:           
            fig = px.line(df_Q6, x='quarter',y='growth_rate',title='Quarterly Growth rate of Users for a year')
            st.plotly_chart(fig)
  with tab2:
    #st.write("Tab related to Map content")
    years = list(range(2018,2025))
    selct_year= st.selectbox('Choose a year:',years,key='year_selectbox1')
    option = st.radio("Choose a category:" ,['Transaction','User'])
    if option=='Transaction':
        insight = "5.Find the count of districts and revenue of all states "
        insight_sel = st.selectbox(insight,selct_year)
        query = text('''
                SELECT state,COUNT("dist_name") AS district_count,SUM(transaction_amt) AS total_revenue
                FROM "Map_trnsc"
                WHERE CAST("Map_trnsc"."year" AS INTEGER) = :selct_year 
                GROUP BY state
                ORDER BY state
                ''' )
        df= pd.read_sql(query, con=engine, params={'selct_year': selct_year})
        df_long = df.melt(id_vars='state', value_vars=['district_count', 'total_revenue'], var_name='Metrics', value_name='Count/Revenue')                       
        #fig = px.bar(df_long, x = 'state', y=['district_count','total_revenue'], title="District count and Revenue per State ",
         #           labels={'value':'Count/Revenue','variable' :'Metrics','state':'State'}, barmode = 'group',
          #          color_discrete_sequence=px.colors.qualitative.Pastel)
        fig = px.bar(df_long, x='state', y='Count/Revenue', color='Metrics', barmode='group',
              title="District Count and Revenue per State",
             labels={'Count/Revenue':'Count/Revenue', 'Metrics':'Metrics', 'state':'State'},
             color_discrete_sequence=px.colors.qualitative.Pastel)            
        st.plotly_chart(fig) 
    else:
        insight = "6.Find the district with highest app count for each state of a particular year"
        insight_sel = st.selectbox(insight,selct_year)
        query = text('''SELECT s1.state,s1.dist_name,s1.year,s1.app_opens_count
	                FROM(
	                     SELECT year,state,dist_name,app_opens_count,
                         RANK() OVER (PARTITION BY state ORDER BY app_opens_count DESC) AS rnk
                         FROM "Map_user"
                         WHERE CAST(year AS INTEGER) = :selct_year)s1
	                    where s1.rnk=1''')
        df_Q7= pd.read_sql(query,con=engine,params={'selct_year': selct_year})
        if (df_Q7['app_opens_count']<=0).all():
            st.write("Data is not Available for the selected criteria")
        else:    
            fig = px.bar(df_Q7, x='state', y='app_opens_count', color='dist_name',
                                title='District with Highest App Opens in Each State',
                                labels={'app_open_count': 'App_Open_Count'})
            st.plotly_chart(fig)
        # Check for 2018 as it contain zeros
  with tab3:
    years=list(range(2018,2025))
    selct_year= st.selectbox('Choose a year:',years,key='year_selectbox2')
    selct_quart = st.selectbox('Choose a quarter:', ('1','2','3','4'),index=0,key='quart_selectbox')
    option = st.radio("Choose a category:" ,['Transaction','User'],key='radio1')
    if option=='Transaction':
        insight = "7.Find the top ten and least ten districts based on the transaction_count"
        insight_sel = st.selectbox(insight,[selct_year,selct_quart])
        query = text('''select state,dist_name,transaction_count from "Top_trnsd"
                          where CAST(year AS INTEGER)= :selct_year and CAST(quarter AS INTEGER)= :selct_quart
                          order by transaction_count desc
                          limit 10''')
        df_top = pd.read_sql(query, con = engine, params={'selct_year':selct_year,'selct_quart':selct_quart})
        query_l = text('''select state,dist_name,transaction_count from "Top_trnsd"
                          where CAST(year AS INTEGER)= :selct_year and CAST(quarter AS INTEGER)= :selct_quart
                          order by transaction_count 
                          limit 10''') 
        df_low = pd.read_sql(query_l, con = engine, params={'selct_year':selct_year,'selct_quart':selct_quart}) 
        col1,col2=st.columns(2)                 
        if df_top.empty:
            col1.write("No data available")
        else:    
            fig=px.bar(df_top, x ='dist_name', y ='transaction_count', color = 'dist_name',
                 title='Top ten districts ') 
            col1.plotly_chart(fig)
            col1.write(df_top) 
        if df_low.empty:
            col2.write("No data available")  
        else:
            fig=px.bar(df_low, x='dist_name', y='transaction_count', color = 'dist_name',
                                     title = 'Least ten districts') 
            col2.plotly_chart(fig) 
            col2.write(df_low)                              
    else:
        insight = "8.Find the distibution of registered users across the districts of a state" 
        insight_sel = st.selectbox(insight,selct_year)  
        unique_states = df_Top_user_dst['state'].unique()
        state = st.selectbox('Choose a state;', unique_states,key='state_selectbox')
        query = text('''select state, dist_name,regd_users from "Top_userd"
                        where CAST(year AS INTEGER)= :selct_year''')
        df_user = pd.read_sql(query,con=engine,params={'selct_year':selct_year}) 
        if df_user.empty:
            st.write("No data available")
        else:
            df_state = df_user[df_user['state']==state]  
            if df_state.empty:
                st.write("No data available for the selected state") 
            else:
                fig = px.pie(df_state, values='regd_users', names = 'dist_name',
                                title = f'Registered Users in {state}',
                                labels={'registered_users':'% of registered users'})  
                fig.update_traces(textinfo = 'percent+label')
                st.plotly_chart(fig)                      

        df_regu = df_Top_user_dst[(df_Top_user_dst['year']=="2018") &(df_Top_user_dst['quarter']==1)] 
        df_cum = df_regu.groupby('state') ['regd_users'].sum().reset_index()
        fig = px.choropleth(df_cum,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='regd_users',
        color_continuous_scale='rainbow',
        hover_name ='state',
        title = "Registered Users count across the Indian states",
        height = 700)
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
                                    
          
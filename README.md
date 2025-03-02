# Project-PPAY
Introduction: PhonePe is an Indian digital payment and financial services company hequartered in Bengaluru.
              Phonepe is a Digital Wallet and Online Payment App that allows you to make Instant money transfers through UPI.

Process:
1.The project was aimed at extracting data from Github Repository,where real world transaction data frequently gets updated 
based on the years and quarter_wise.The data is cloned to the local machine where it will be stored in a specific location.
The data comprises of 36 locations including States(28) and Union Territories(8) from the year 2018 to 2024(Q2).
The data is primarly Categorised into three divisions namely Aggregated, Map and Top where two sub-divisions namely
Transaction and User are available for the classifing the data accordingly.

2.The segregated data is pushed into the personalised workbench(PostgresSQL) categorically,where the necessary tables are
created for each of the categories using SQL Alchemy.The last category(Top) is further classified district_wise and 
pin_wise.The tables are now available with the real-world transaction data to perform queries.

3.As a part of Data Visualization, the queries will be written to fetch the data from the database. With the help of Streamlit
App, where three tabs for each category are made available and the necessary visualizations like pie-chart,bargraphs,line
graphs and Choropleth map are generated using plotly library. Choropleth map is to create a Indian map where the data
of all the locations will be displayed for a better visual appeal.

4.The Streamlit App, front end application will be displaying questions where they will be filtered on parameters like 
year, quarter and state or else in a generalised fashion where entire data is considered.Thus the business insights are 
generated using the queries and the corresponding data is displayed in the front end.To name a few business insights 
include the Top ten states in order of overall transaction amount(total revenue), breakdown of total Revenue based on
the Transaction_type,Top ten and least ten districts based on the transaction_count,Districts with Highest app_open_counts
and the count of districts available for each state, Quarterly growth rate of Registered users.



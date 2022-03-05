import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('Comcast_telecom_complaints_data.csv')

df["Date"]= pd.to_datetime(df["Date"])

#Provide the trend chart for the number of complaints at daily
y = df.groupby(by=[pd.Grouper(key="Date", freq="1D")])["Status"]
graph = y.count().reset_index()

plt.plot(graph['Date'], graph['Status'], color='red')
plt.title('Number of complaints Per Day', fontsize=14)
plt.xlabel('Dates', fontsize=14)
plt.ylabel('Complaints', fontsize=14)
plt.show()

#Provide the trend chart for the number of complaints at monthly
z = df.groupby(by=[pd.Grouper(key="Date", freq="1M")])["Status"]
graph2 = z.count().reset_index()

plt.plot(graph2['Date'], graph2['Status'], color='red')
plt.title('Number of complaints per month', fontsize=14)
plt.xlabel('Dates', fontsize=14)
plt.ylabel('Complaints', fontsize=14)
plt.show()

#Provide a table with the frequency of complaint types.
freque = df.groupby(by=[pd.Grouper(key="Received Via")])["Status"]
freque = freque.count().reset_index()

#Create a new categorical variable with value as Open and Closed. Open & Pending 
#is to be categorized as Open and Closed & Solved is to be categorized as Closed
def vari(x):
    if 'Open' in x or 'Pending' in x:
        return 'Open'
    elif 'Closed' in x or 'Solved' in x:
        return 'Closed'
    
df.Status = df.Status.astype(str).apply(vari)    

#Provide state wise status of complaints in a stacked bar chart.
x = df.groupby(["State","Status"])[["Status"]].count()
x = x.rename({'Status': 'Count'}, axis=1)
x = x.reset_index()

df.groupby(["State","Status"])[["Status"]].count().unstack().plot(kind='bar', stacked=True)

#Which state has the maximum complaints
Max_complainst = df["State"].value_counts()
df["State"].value_counts().plot()

#Which state has the highest percentage of unresolved complaints
state_office = df.groupby(['State', 'Status']).agg({'Status': 'count'})
state = df.groupby(['State']).agg({'Status': 'count'})
highest_per = state_office.div(state, level='State') * 100
highest_per = highest_per.rename({'Status': 'Percent'}, axis=1)
highest_per = highest_per.reset_index()
highest_per[highest_per.Status =="Open"][["State","Percent"]].sort_values('Percent',ascending=False)

#Provide the percentage of complaints resolved till date, which were received through the Internet 
#and customer care calls.
state_office1 = df.groupby(['Received Via', 'Status']).agg({'Status': 'count'})
state1 = df.groupby(['Received Via']).agg({'Status': 'count'})
received = state_office1.div(state1, level='Received Via') * 100
received = received.rename({'Status': 'Percent'}, axis=1)
received = received.reset_index()
received[received.Status =="Closed"][["Received Via","Percent"]].sort_values('Percent',ascending=False)
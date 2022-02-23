#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)
# import datetime as dt
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score,mean_squared_error, confusion_matrix
from catboost import CatBoostRegressor
# from lightgbm import LGBMRegressor
import datetime


# In[9]:

def main():
	## Unhash this code if data is being pulled from sql database

	# import mysql.connector as sql
	# import pandas as pd

	# db_connection = sql.connect(host='localhost', database='aq_historical_data', user='root', password='sharan123')
	# db_cursor = db_connection.cursor()
	# cursor = db_connection.cursor()
	# db_cursor.execute('SELECT * FROM aq_data5')
	# table_rows = db_cursor.fetchall()
	# b = pd.DataFrame(table_rows,columns=['station','date','day','year','month','time','pm25','pm10','nox','temperature','co'])


	# In[41]:


	# b.to_csv('aqdb_data.csv',index=False)


	# In[42]:


	# a = pd.read_csv('aqdb_data.csv')


	# In[11]:


	a = pd.read_csv('2020-2022-feb13.csv') ## REading data from .csv file


	# In[12]:


	l2 = a.copy()


	# In[13]:


	l2.head()


	# In[14]:


	l2.isnull().sum()


	# In[15]:


	l2['month'] = l2.month.astype(int)
	l2['year'] = l2.year.astype(int)


	# In[16]:


	l2.head()


	# ### Preprocessing the Data

	# In[17]:


	# l2['Date'] = pd.to_datetime(l2['Date'])

	# years = []
	# yrs = l2.Date.dt.year
	# for i in yrs:
	#     years.append(i)
	# l2['Year'] = years

	hr =[]
	for i in l2.time:
		if len(i)>5:
		    hr.append(i[:-6])
		elif len(i) <=5:
		    hr.append(i[:-3])
	l2['hour'] = hr

	## if you want to have 30 min data
	# h = []
	# for i in l2.hour:
	#     if i.endswith('00'):
	#         h.append(i[1:-3]+'.0')
	#     elif i.endswith('30'):
	#         h.append(i[1:-3]+'.5')
	# l2['hour'] = h 

	l2['hour']= l2.hour.astype(int)


	# In[18]:


	l2 = l2[['station','date','day','time','year','month','hour','pm25','pm10','nox','temperature','co']]


	# In[19]:


	l2.head()


	# ### Processing Stations to Integers

	# In[20]:


	# l2.head()


	# In[21]:


	station_processed = []
	for i in l2.station:
		if i == 'Kodungaiyur_Chennai_TNPCB':
		    station_processed.append(1)
		elif i == 'Royapuram_Chennai_TNPCB':
		    station_processed.append(2)
		elif i == 'Perungudi_Chennai_TNPCB':
		    station_processed.append(3)
		elif i == 'Alandur_Bus_Depot_Chennai_CPCB':
		    station_processed.append(4)
		elif i == 'Velacheri_Res_Area_CPCB':
		    station_processed.append(5)
	l2['station'] = station_processed


	d = []
	for i in l2.day:
		if i == 'Sunday':
		    d.append(1)
		elif i == 'Monday':
		    d.append(2)
		elif i == 'Tuesday':
		    d.append(3)
		elif i == 'Wednesday':
		    d.append(4)
		elif i == 'Thursday':
		    d.append(5)
		elif i == 'Friday':
		    d.append(6)
		elif i == 'Saturday':
		    d.append(7)
	l2['day'] = d
		    


	## months 
	## 1,2 - Winter (1)
	## 3,4 - spring (2)
	## 5,6 - summer (3)
	## 7,8 - monsoon (4)
	## 9,10 - autumn (5)
	## 11,12 - pre-winter (6)


	season = []
	for i in l2.month:
		if i <= 2:
		    season.append(1)
		elif i == 3 or i == 4:
		    season.append(2)
		elif i == 5 or i == 6:
		    season.append(3)
		elif i == 7 or i == 8:
		    season.append(4)
		elif i == 9 or i == 10:
		    season.append(5)
		elif i == 11 or i == 12:
		    season.append(6)
	l2['season'] = season



	## 12 - 4 Midnight:
	## 4 - 7 - Early-Morning
	## 7 -12 - morning
	## 12 - 16 - Afternoon
	## 16 - 19 - Evening
	## 19 - 23 - Night
	pod = []
	for i in l2.hour:
		if i >= 0 and i < 4:
		    pod.append(1)
		elif i>=4 and i<7:
		    pod.append(2)
		elif i>=7 and i <12:
		    pod.append(3)
		elif i >=12 and i <16:
		    pod.append(4)
		elif i >=16 and i <19:
		    pod.append(5)
		elif i>=19 and i <= 23:
		    pod.append(6)

	l2['part_of_day'] = pod


	# In[ ]:





	# ### Dropping Date & Time feature (because of hour feature being added as an integer) 

	# In[22]:


	l2.drop(['date','time'],axis=1,inplace=True)


	# In[23]:


	l2 = l2[['station','day','month','season','year','hour','part_of_day','pm10','nox','temperature','co','pm25']]


	# In[ ]:





	# ### Preparing Test Data - 5 days of test data from current date.

	# In[25]:


	import datetime
	data = []
	stations = [1, 2, 3, 4, 5]
	dates = [datetime.datetime.now().date() + datetime.timedelta(days=i)
		     for i in range(0, 5)]
	for s in stations:
		for date in dates:
		    for time in range(0,24):
		        data.append({'station': s, 'date': date, 'hour': time})
	test_data = pd.DataFrame(data)


	# ### Custom predictions - If the predictions needs to be ran for a custom date

	# In[27]:



	# import datetime
	# data = []
	# stations = [1, 2, 3, 4, 5]
	# dates = datetime.datetime(2018, 11, 13)
	# dates = [datetime.datetime(2021,11,13).date() + datetime.timedelta(days=i)
	#          for i in range(0, 5)]
	# for s in stations:
	#     for date in dates:
	#         for time in range(0,24):
	#             data.append({'station': s, 'date': date, 'hour': time})
	# test_data = pd.DataFrame(data)


	# In[ ]:





	# In[30]:


	# test_data.head()


	# In[31]:


	#test_data = pd.read_csv('test-data-allParams-25th-5thSep-hourly.csv')
	test_data['date'] = pd.to_datetime(test_data['date'])


	months1 = []
	years1 = []
	day1 = []
	mth1 = test_data.date.dt.month
	yrs1 = test_data.date.dt.year
	dy1 = test_data.date.dt.day_name()

	for i in mth1:
		months1.append(i)
	test_data['month'] = months1

	for i in yrs1:
		years1.append(i)
	test_data['year'] = years1

	for i in dy1:
		test_data['day'] = dy1


	# hour1 =[]
	# for i in test_data.Time:
	#     if len(i) > 5:
	#         hour1.append(i[:-6])
	#     elif len(i) <=5:
	#         hour1.append(i[:-3])

	# test_data['Hour'] = hour1 

	# test_data['Hour']= test_data.Hour.astype(int)



	## months 
	## 1,2 - Winter (1)
	## 3,4 - spring (2)
	## 5,6 - summer (3)
	## 7,8 - monsoon (4)
	## 9,10 - autumn (5)
	## 11,12 - pre-winter (6)


	season = []
	for i in test_data.month:
		if i <= 2:
		    season.append(1)
		elif i == 3 or i == 4:
		    season.append(2)
		elif i == 5 or i == 6:
		    season.append(3)
		elif i == 7 or i == 8:
		    season.append(4)
		elif i == 9 or i == 10:
		    season.append(5)
		elif i == 11 or i == 12:
		    season.append(6)
	test_data['season'] = season

	pod = []
	for i in test_data.hour:
		if i >= 0 and i < 4:
		    pod.append(1)
		elif i>=4 and i<7:
		    pod.append(2)
		elif i>=7 and i <12:
		    pod.append(3)
		elif i >=12 and i <16:
		    pod.append(4)
		elif i >=16 and i <19:
		    pod.append(5)
		elif i>=19 and i <= 23.5:
		    pod.append(6)

	test_data['part_of_day'] = pod


	# In[ ]:





	# In[32]:


	d = []
	for i in test_data.day:
		if i == 'Sunday':
		    d.append(1)
		elif i == 'Monday':
		    d.append(2)
		elif i == 'Tuesday':
		    d.append(3)
		elif i == 'Wednesday':
		    d.append(4)
		elif i == 'Thursday':
		    d.append(5)
		elif i == 'Friday':
		    d.append(6)
		elif i == 'Saturday':
		    d.append('7')
	test_data['day'] = d
		    


	# In[ ]:





	# In[33]:


	test_data.head()


	# In[35]:


	l2.head()


	# In[ ]:





	# # Models

	# In[37]:


	cat = CatBoostRegressor(verbose=False)
	#lgb = LGBMRegressor()


	# # Predicting NOx

	# In[38]:


	import pickle


	# In[39]:


	nox_pred = l2.copy()
	nox_pred.drop(['pm10','temperature','co','pm25'],axis=1,inplace=True)
	nox_pred.dropna(inplace=True)

	x = nox_pred.drop('nox',1)
	y = nox_pred['nox']

	nox_test = test_data.copy()
	nox_test = nox_test[['station','date','day','month','season','year','hour','part_of_day']]
	nox_test.dropna(inplace=True)
	x_test = nox_test

	cat = cat.fit(x,y)
	cat_test_pred = cat.predict(x_test)
	pkl_file = './weight_files/nox.pkl'
	pickle.dump(cat, open(pkl_file, 'wb'))

	cat_test_pred = list(cat_test_pred)
	final_results = nox_test.copy()
	final_results['predicted_nox'] = cat_test_pred
	final_results.head()


	# In[ ]:





	# # Predicting Temperature

	# In[30]:


	# temp_pred.shape


	# In[40]:


	temp_pred = l2.copy()
	temp_pred.drop(['pm10','nox','co','pm25'],axis=1,inplace=True)

	temp_pred.dropna(inplace=True)

	x = temp_pred.drop('temperature',1)
	y = temp_pred['temperature']

	## Testing it with Test data

	temp_test = test_data.copy()
	temp_test = temp_test[['station','day','month','season','year','hour','part_of_day']]
	temp_test.dropna(inplace=True)
	x_test = temp_test

	cat = cat.fit(x,y)
	cat_test_pred = cat.predict(x_test)

	pkl_file = './weight_files/temp.pkl'
	pickle.dump(cat, open(pkl_file, 'wb'))
	cat_test_pred = list(cat_test_pred)
	final_results['predicted_temperature'] = cat_test_pred
	final_results.head()


	# In[ ]:





	# # Predicting CO

	# In[32]:


	# co_pred.shape


	# In[41]:


	co_pred = l2.copy()

	co_pred.drop(['pm10','nox','temperature','pm25'],axis=1,inplace=True)

	co_pred.dropna(inplace=True)
	co_pred.head()


	x = co_pred.drop('co',1)
	y = co_pred['co']

	### Testing it on test data

	co_test = test_data.copy()
	co_test = co_test[['station','day','month','season','year','hour','part_of_day']]
	co_test.dropna(inplace=True)
	x_test = co_test

	cat = cat.fit(x,y)
	cat_test_pred = cat.predict(x_test)
	cat_test_pred = list(cat_test_pred)

	pkl_file = './weight_files/co.pkl'
	pickle.dump(cat, open(pkl_file, 'wb'))

	final_results['predicted_co'] = cat_test_pred

	#final_results.head()


	# In[ ]:





	# # Predicting PM2.5

	# In[42]:


	pm25_pred = l2.copy()

	pm25_pred.drop(['pm10','nox','temperature','co'],axis=1,inplace=True)
	pm25_pred.dropna(inplace=True)
	x = pm25_pred.drop('pm25',1)
	y = pm25_pred['pm25']

	### Testing it on test data

	pm25_test = test_data.copy()
	pm25_test = pm25_test[['station','day','month','season','year','hour','part_of_day']]
	pm25_test.dropna(inplace=True)
	x_test = pm25_test
	cat = cat.fit(x,y)
	cat_test_pred = cat.predict(x_test)
	cat_test_pred = list(cat_test_pred)
	pkl_file = './weight_files/pm25.pkl'
	pickle.dump(cat, open(pkl_file, 'wb'))
	final_results['predicted_pm25'] = cat_test_pred
	#final_results.head()


	# In[ ]:





	# In[ ]:





	# In[43]:


	final_results.head()


	# ### Processing the predictions to user readable format

	# In[44]:


	## Date formating
	final_results['date'] = final_results['date'].astype(str)


	## Station int - str 
	sp = []
	for i in final_results.station:
		if i == 1:
		    sp.append('Kodungaiyur_Chennai_TNPCB')
		elif i == 2:
		    sp.append('Royapuram_Chennai_TNPCB')
		elif i == 3: 
		    sp.append('Perungudi_Chennai_TNPCB')
		elif i == 4: 
		    sp.append('Alandur_Bus_Depot_Chennai_CPCB')
		elif i == 5:
		    sp.append('Velacheri_Res_Area_CPCB')
	final_results['station'] = sp


	## AQI - int - str

	# 1 - good
	# 2 - Satisfactory
	# 3 - Moderate
	# 4 - Poor
	# 5 - very Poor
	# 6 - Severe
	iqa = []
	for i in final_results['predicted_pm25']:
		if i < 31:
		    iqa.append('good')
		elif i >=31 and i < 61:
		    iqa.append('satisfactory')
		elif i >= 61 and i < 91:
		    iqa.append('moderate')
		elif i >= 91 and i < 121:
		    iqa.append('poor')
		elif i >= 121 and i < 251:
		    iqa.append('very poor')
		elif i >= 251:
		    iqa.append('severe')

	final_results['predicted_aqi'] = iqa


	# 1 - good
	# 2 - Satisfactory
	# 3 - Moderate
	# 4 - Poor
	# 5 - very Poor
	# 6 - Severe

	# iqa = []
	# for i in final_results['Actual_PM2.5']:
	#     if i < 31:
	#         iqa.append('good')
	#     elif i >=31 and i < 61:
	#         iqa.append('satisfactory')
	#     elif i >= 61 and i < 91:
	#         iqa.append('moderate')
	#     elif i >= 91 and i < 121:
	#         iqa.append('poor')
	#     elif i >= 121 and i < 251:
	#         iqa.append('very poor')
	#     elif i >= 251:
	#         iqa.append('severe')
	#     else:
	#         iqa.append('Unknown')

	# final_results['Actual_AQI'] = iqa


	## part of day int - str

	## 12 - 4 Midnight:
	## 4 - 7 - Early-Morning
	## 7 -12 - morning
	## 12 - 16 - Afternoon
	## 16 - 19 - Evening
	## 19 - 23 - Night

	dop = []
	for i in final_results.part_of_day:
		if i == 1:
		    dop.append('Mid-Night')
		elif i == 2:
		    dop.append('Early-Morning')
		elif i == 3:
		    dop.append('Morning')
		elif i == 4:
		    dop.append('Afternoon')
		elif i == 5:
		    dop.append('Evening')
		elif i == 6:
		    dop.append('Night')
	final_results.part_of_day = dop


	# In[45]:


	## months 
	## 1,2 - Winter (1)
	## 3,4 - spring (2)
	## 5,6 - summer (3)
	## 7,8 - monsoon (4)
	## 9,10 - autumn (5)
	## 11,12 - pre-winter (6)

	season = []
	for i in final_results.month:
		if i <= 2:
		    season.append('Winter')
		elif i == 3 or i == 4:
		    season.append('Spring')
		elif i == 5 or i == 6:
		    season.append('Summer')
		elif i == 7 or i == 8:
		    season.append('Monsoon')
		elif i == 9 or i == 10:
		    season.append('Autumn')
		elif i == 11 or i == 12:
		    season.append('Pre-winter')
		    
	final_results['season'] = season


	hor = []
	for i in final_results.hour:
		if i == 0:
		    hor.append('00:00')
		elif i == 1:
		    hor.append('01:00')
		elif i == 2:
		    hor.append('02:00')
		elif i == 3:
		    hor.append('03:00') 
		elif i == 4:
		    hor.append('04:00')
		elif i == 5:
		    hor.append('05:00')
		elif i == 6:
		    hor.append('06:00')
		elif i == 7:
		    hor.append('07:00')
		elif i == 8:
		    hor.append('08:00')
		elif i == 9:
		    hor.append('09:00')
		elif i == 10:
		    hor.append('10:00')
		elif i == 11:
		    hor.append('11:00')
		elif i == 12:
		    hor.append('12:00')
		elif i == 13:
		    hor.append('13:00')
		elif i == 14:
		    hor.append('14:00')
		elif i == 15:
		    hor.append('15:00')
		elif i == 16:
		    hor.append('16:00')
		elif i == 17:
		    hor.append('17:00')
		elif i == 18:
		    hor.append('18:00')
		elif i == 19:
		    hor.append('19:00')
		elif i == 20:
		    hor.append('20:00')
		elif i == 21:
		    hor.append('21:00')
		elif i == 22:
		    hor.append('22:00')
		elif i == 23:
		    hor.append('23:00')
		    
	final_results['hour'] = hor


	# In[46]:


	mont = []
	for i in final_results.month:
		if i == 1:
		    mont.append('January')
		elif i == 2:
		    mont.append('February')
		elif i == 3:
		    mont.append('March') 
		elif i == 4:
		    mont.append('April')
		elif i == 5:
		    mont.append('May')
		elif i == 6:
		    mont.append('June')
		elif i == 7:
		    mont.append('July')
		elif i == 8:
		    mont.append('August')
		elif i == 9:
		    mont.append('September')
		elif i == 10:
		    mont.append('October')
		elif i == 11:
		    mont.append('November')
		elif i == 12:
		    mont.append('December')
		    
	final_results['month'] = mont
	
	print('Weights succesfully saved to ./weight_files/')


	# In[41]:


	# final_results.to_csv('ftmodel_nov18.csv',index=False)


	# In[48]:


	# import time
	# timestr = time.strftime("%Y-%m-%d - %H")
	# final_results.to_csv('./Predictions/predictions_base_-'+str(timestr)+'Hours'+'.csv', index = False)


	# In[ ]:





	# In[ ]:





	# In[49]:


	# final_grouped_date = final_results[['predicted_pm25']].groupby(final_results.date).mean()


	# In[50]:


	# print('\nDate Wise Average predictions for PM2.5')
	# print('\n')
	# print(final_grouped_date)


	# In[ ]:





	# ### Sending the predictions to the predictions table in DB

	# In[51]:


	# final_results.drop('day',axis=1,inplace=True)


	# In[46]:


	# import sqlalchemy
	# #final_results =  # The table we need to upload, here - final_grouped_date


	# database_username = 'root'
	# database_password = 'sharan123'
	# database_ip       = '127.0.0.1'
	# database_name     = 'aq_historical_data'
	# database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
	#                                                format(database_username, database_password, 
	#                                                       database_ip, database_name))
	# final_results.to_sql(con=database_connection, name='aq_predictions1', if_exists='append',index=False)


	# In[ ]:





	# In[ ]:





	# In[ ]:





	# In[ ]:





	# In[ ]:





	# In[ ]:





	# In[ ]:





	# In[ ]:





	# In[ ]:





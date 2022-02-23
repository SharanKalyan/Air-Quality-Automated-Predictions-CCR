## Importing Libraries
## Pandas and Numpy
import pandas as pd
import numpy as np

## Machine Learning Libraries
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report,r2_score,mean_squared_error, confusion_matrix
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
import pickle

## other libraries
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)
import datetime
import time


## Preparing Test Data
def main():
	print('algorithm start time :',str(datetime.datetime.now()))
	## preparing test data (5 days from current date. )
	data = []
	stations = [1, 2, 3, 4, 5]
	dates = [datetime.datetime.now().date() + datetime.timedelta(days=i) #custom pred : replace .now() with (custom_date)
		    for i in range(0, 5)]
	for s in stations:
		for date in dates:
		    for time in range(0,24):
		        data.append({'station': s, 'date': date, 'hour': time})
	test_data = pd.DataFrame(data)
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
	test_data['season'] = test_data['month'].map({1:1 , 2:1, 3:2, 4:2, 5:3,
												  6:3, 7:4, 8:4, 9:5, 10:5, 11:6, 12:6 }).astype(int)
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

	test_data['day'] = test_data['day'].map({'Sunday':1, 'Monday':2, 'Tuesday':3, 'Wednesday':4, 'Thursday':5,
		                                     'Friday':6,'Saturday':7}).astype(int)

	## Pedictions using weight files
	## NOX PRED
	nox_test = test_data.copy()
	nox_test.dropna(inplace=True)
	x_test = nox_test
	cat = pickle.load(open('./weight_files/nox.pkl' , 'rb'))
	cat_test_pred = cat.predict(x_test)
	cat_test_pred = list(cat_test_pred)
	final_results = nox_test.copy()
	final_results['predicted_nox'] = cat_test_pred
	## TEMP PRED
	temp_test = test_data.copy()
	x_test = temp_test
	cat = pickle.load(open('./weight_files/temp.pkl' , 'rb'))
	cat_test_pred = cat.predict(x_test)
	cat_test_pred = list(cat_test_pred)
	final_results['predicted_temperature'] = cat_test_pred
	## CO PRED
	co_test = test_data.copy()
	cat = pickle.load(open('./weight_files/co.pkl' , 'rb'))
	x_test = co_test
	cat_test_pred = cat.predict(x_test)
	cat_test_pred = list(cat_test_pred)
	final_results['predicted_co'] = cat_test_pred
	## PM2.5 PRED
	pm25_test = test_data.copy()
	cat = pickle.load(open('./weight_files/pm25.pkl' , 'rb'))
	x_test = pm25_test
	cat_test_pred = cat.predict(x_test)
	cat_test_pred = list(cat_test_pred)
	final_results['predicted_pm25'] = cat_test_pred

	## Processing the predictions to user readable format
	final_results['date'] = final_results['date'].astype(str)
	final_results['station'] = final_results['station'].map({1:'Kodungaiyur_Chennai_TNPCB', 2:'Royapuram_Chennai_TNPCB',
		                                                     3:'Perungudi_Chennai_TNPCB', 4:'Alandur_Bus_Depot_Chennai_CPCB',
		                                                     5:'Velacheri_Res_Area_CPCB'})
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
	final_results['part_of_day'] = final_results['part_of_day'].map({1:'Mid-Night', 2:'Early-Morning', 3:'Morning',
		                                                             4:'Afternoon', 5:'Evening', 6:'Night'})
	final_results['season'] = final_results['season'].map({1:'Winter', 2:'Winter', 3:'Spring', 4:'Spring',
		                                                  5:'Summer', 6:'Summer', 7:'Monsoon', 8:'Monsoon',
		                                                  9:'Autumn', 10:'Autumn', 11:'Pre-winter', 12:'Pre-winter'})
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
	final_results['month'] = final_results['month'].map({1:'January', 2:'February', 3:'March',4:'April',5:'May',
		                                                 6:'June',7:'July',8:'August',9:'September',10:'October',
		                                                 11:'November', 12:'December'})
	final_results['day'] = final_results['day'].map({1:'Sunday', 2:'Monday', 3:'Tuesday', 4:'Wednesday',
		                                             5:'Thursday', 6:'Friday', 7:'Saturday'})
	timestr = time.strftime("%Y-%m-%d - %H")
	final_results.to_csv('./Predictions_evals/base_models-'+str(timestr)+'Hours'+'.csv', index = False)
	final_grouped_pm25 = final_results[['predicted_pm25']].groupby(final_results.date).mean()
	final_grouped_co = final_results[['predicted_co']].groupby(final_results.date).mean()
	final_grouped_temp = final_results[['predicted_temperature']].groupby(final_results.date).mean()
	final_grouped_nox = final_results[['predicted_nox']].groupby(final_results.date).mean()
	print('Predictions successfully saved ')
	print('algorithm end time :',str(datetime.datetime.now()))

	## predictions to Database (if necessary)
	#final_results.drop('day',axis=1,inplace=True) ## as there is no day column in Database
	#import sqlalchemy
	#final_results =  # The table we need to upload, here : final_grouped_date
	#database_username = 'root'
	#database_password = 'sharan123'
	#database_ip       = '127.0.0.1'
	#database_name     = 'aq_historical_data'
	#database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
	#                                            format(database_username, database_password,
	#                                                    database_ip, database_name))
	#final_results.to_sql(con=database_connection, name='aq_predictions1', if_exists='append',index=False)

# Air-Quality-Predictions-CCR

This is an end-to-end implimentation of Machine Learning Project to Monitor and predict the Air quality Levels in the city. 

The data is collected from a Govt. source. https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing 

The data contains,
date (from jan1 2020 - feb 21 2022), station (velachery,perungudi,alandur,royapuram and kodungaiyur), time (24 data per day from 00:00 to 23:00), pm2.5 (target), pm10, nox (target), temperature (target), co (target).

Here, I hav automated the entire process of the predictions for 4 different target variables (pm2.5, nox, temperature, co). 

There are 4 suporting files that i have used. 
1. Historical_training.py
2. sceduled_training.py
3. historical_data_predictions.py
4. historical_sceduler.py

The Historical_training.py will fetch the data, train the data for 4 different target variables 
and store the weight files in the ./weight_files directory (.pkl file)

The historical_data_predictions.py file will take those weight files, do all the necessary preprocessing and predict the 4 target variables. 
(pm2.5, co, nox and temperature for every hour in the next 5 days including the current date, 360 datapoints for all the 5 stations) post that, all the post-processing will be done, and the predictions will be stored in a user readable format in ./prediction_evals directory. 

NOTE:
1. The sceduled_training.py will automate the process of training. 
This file will be running continuosly on the server and for every 30 days (or any time) the function will run automatically. 

2. The historical_sceduler.py will automate the process of predictions. 
The historical_sceduler.py will be run on the server, and the predictions will be made every 2 hours. 

3. Finally, the prediction_evals.ipynb notebook can be used to evaluate how accurate the predictions are! 

4. It is important we follow the structure of the directories. 

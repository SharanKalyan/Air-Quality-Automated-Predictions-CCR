# Air-Quality-Predictions-CCR

This is an end-to-end implimentation of Machine Learning Project to Monitor and predict the Air quality Levels in the city.

The data is collected from a Govt. source. https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing 

The data contains,
date (from jan1 2020 - feb 21 2022), station (velachery,perungudi,alandur,royapuram and kodungaiyur), time (24 data per day from 00:00 to 23:00), pm2.5 (target), pm10, nox (target), temperature (target), co (target).

Here, I have automated the entire process of the predictions for 4 different target variables (pm2.5, nox, temperature, co)

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
This file will be running continuosly on the server and for every 30 days (or any specific time interval for that matter) the function will run automatically. 

2. The historical_sceduler.py will automate the process of predictions. 
The historical_sceduler.py will be run on the server, and the predictions is set to run the predictions every 2 hours. 

3. Finally, the prediction_evals.ipynb notebook can be used to evaluate how accurate the predictions are! 

4. It is important we follow the structure of the directories. 


Here are some samples of the probable outcomes and the actuals:

# CO Predictions

![image](https://user-images.githubusercontent.com/20862520/157029950-4272244b-b079-428a-838e-0409709e24dc.png)

![image](https://user-images.githubusercontent.com/20862520/157029923-f9b7549f-b03f-450e-ac8c-3b9c7905b7a2.png)

![image](https://user-images.githubusercontent.com/20862520/157029631-963e27fa-3de0-4974-b020-dc937285814a.png)

# PM2.5 predictions
![image](https://user-images.githubusercontent.com/20862520/157030757-b7be1af6-1255-4256-b5b3-1cbf32eb779c.png)

![image](https://user-images.githubusercontent.com/20862520/157030699-1e0f7922-371a-4950-a0e9-864c2c16aff3.png)

# NOX Predictions:
![image](https://user-images.githubusercontent.com/20862520/157431536-69c93670-7c8d-4696-a81b-ba9c9ff77f1a.png)

# Temperature predictions
![image](https://user-images.githubusercontent.com/20862520/157030927-01fe7c34-3b67-44d5-bcae-50b7b5f9c213.png)


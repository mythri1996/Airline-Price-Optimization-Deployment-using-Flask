from flask import Flask, render_template,request
import pickle
import numpy as np
import pandas as pd


app = Flask(__name__)
model = pickle.load(open('flight.pkl','rb'))


@app.route('/')
def home():
    return render_template('basic.html')


@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        date_dep = request.form['Dep_Time']
        journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)
        print(date_dep, journey_day, journey_month, Dep_hour, Dep_min)
        date_arr = request.form['Arrival_Time']
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)

        Total_stops = int(request.form['stops'])
        airline = request.form['airline']
        json_data = {
            "airlines":
                {
                    'Air India': 0, 
                    'GoAir': 0, 
                    'IndiGo': 0, 
                    'Jet Airways': 0,
                    'Jet Airways Business': 0,
                    "Multiple carriers": 0, 
                    "Multiple carriers Premium economy": 0,
                    'SpiceJet': 0,
                    'Trujet': 0,
                    'Vistara': 0,
                    'Vistara Premium economy': 0
                },
            "sources":
                {
                    'Delhi': 0, 'Kolkata': 0, 'Mumbai': 0, 'Chennai': 0
                },
            "destinations":
                {
                    'Cochin': 0, 'Delhi': 0, 'New_Delhi': 0, 'Hyderabad': 0, 'Kolkata': 0
                }

        }
        if json_data:
            if 'airlines' in json_data and json_data['airlines']:
                if airline in json_data['airlines']:
                    json_data['airlines'][airline] = 1
        print(json_data)

        source = request.form["Source"]
        if json_data:
            if 'sources' in json_data and json_data['sources']:
                if source in json_data['sources']:
                    json_data['sources'][source] = 1
        destination = request.form["Destination"]
        if json_data:
            if 'destinations' in json_data and json_data['destinations']:
                if destination in json_data['destinations']:
                    json_data['destinations'][destination] = 1
        prediction = model.predict([[
            Total_stops,
            journey_day,
            journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min,
            json_data['airlines']['Air India'],
            json_data['airlines']['GoAir'],
            json_data['airlines']['IndiGo'],
            json_data['airlines']['Jet Airways'],
            json_data['airlines']['Jet Airways Business'],
            json_data['airlines']['Multiple carriers'],
            json_data['airlines']['Multiple carriers Premium economy'],
            json_data['airlines']['SpiceJet'],
            json_data['airlines']['Trujet'],
            json_data['airlines']['Vistara'],
            json_data['airlines']['Vistara Premium economy'],
            json_data['sources']['Chennai'],
            json_data['sources']['Delhi'],
            json_data['sources']['Kolkata'],
            json_data['sources']['Mumbai'],
            json_data['destinations']['Cochin'],
            json_data['destinations']['Delhi'],
            json_data['destinations']['Hyderabad'],
            json_data['destinations']['Kolkata'],
            json_data['destinations']['New_Delhi']]])
        output = round(prediction[0], 2)
        print(output)
        return render_template('basic.html', prediction_text=f"Your Flight price is Rs.{output}")
    return render_template('basic.html')


if __name__ == '__main__':
    app.run(debug=True)
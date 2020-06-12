#!/usr/bin/env python
# coding: utf-8

# In[8]:


# IMPORTING THE TKINTER MODULE
#import tkinter
from tkinter import *

# FUNCTIONS FOR MANIPULATING GUI
features = {}         # Initializing features dictionary

# Function to extract features(input data) into dictionary
def extract():
    features.clear()          # First clear the features dictionary to make room for new inputs
    
    # Variables needed/used in the function
    global date, lat, lon, burn_area
    global features
    
    # Extract features input from Tkinter entry widgets
    features['ID'] = ID1.get()
    features['area'] = Area1.get()
    features['date'] = 0
    features['lat'] = 0
    features['lon'] = 0
    features['burn_area'] = 0
    features['climate_aet'] = climate_aet1.get()
    features['climate_def'] = climate_def1.get()
    features['climate_pdsi'] = climate_pdsi1.get()
    features['climate_pet'] = climate_pet1.get()
    features['climate_pr'] = climate_pr1.get()
    features['climate_ro'] = climate_ro1.get()
    features['climate_soil'] = climate_soil1.get()
    features['climate_srad'] = climate_srad1.get()
    features['climate_swe'] = climate_swe1.get()
    features['climate_tmmn'] = climate_tmmn1.get()
    features['climate_tmmx'] = climate_tmmx1.get()
    features['climate_vap'] = climate_vap1.get()
    features['climate_vpd'] = climate_vpd1.get()
    features['climate_vs'] = climate_vs1.get()
    features['elevation'] = elevation1.get()
    features['landcover_0'] = landcover_01.get()
    features['landcover_1'] = landcover_11.get()
    features['landcover_2'] = landcover_21.get()
    features['landcover_3'] = landcover_31.get()
    features['landcover_4'] = landcover_41.get()
    features['landcover_5'] = landcover_51.get()
    features['landcover_6'] = landcover_61.get()
    features['landcover_7'] = landcover_71.get()
    features['landcover_8'] = landcover_81.get()
    features['population_density'] = population_density1.get()
    features['precipitation'] = precipitation1.get()
    
    # print(features)

# List the data fields to take the various dictionary features
fields = ['ID','area','date','lat','lon','burn_area','climate_aet','climate_def','climate_pdsi','climate_pet','climate_pr',
            'climate_ro','climate_soil','climate_srad','climate_swe','climate_tmmn','climate_tmmx','climate_vap',
            'climate_vpd','climate_vs','elevation','landcover_0','landcover_1','landcover_2','landcover_3','landcover_4',
            'landcover_5','landcover_6','landcover_7','landcover_8','population_density','precipitation']

# Function To Add features to the dataset for it's analysis
def addFeatures(file_name, dict_elements, field_names):
    # Import of necessary packages for reading the features and adding to dataset
    import csv
    from csv import DictWriter
    with open(file_name, 'a+', newline='') as write_obj:
        # create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames = field_names)
        # Add dictionary as row in the csv dataset
        dict_writer.writerow(dict_elements)
        
# Function to Analyze the dataset together with the appended features from the user input
def analyze():
    # Import of necessary variables for analysis
    global test
    global train
    global in_cols
    global target_col
    global ss
    global features
    global fields
    
    # Add the user data from the input fields stored as a dictionary to the test.csv file
    addFeatures('C:/Users/Kwabena-Kobiri/Desktop/test.csv', features, fields)
    
    # Take the ID of the input Data and display it beneath the 'ID' label in the GUI
    ID_output['text'] = features['ID']
    
    # Modules imported for Analysis
    import pandas as pd
    from sklearn.linear_model import RidgeCV
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error, r2_score

    # Reading the dataset from local machine. Change path to the location of data files on the users machine
    test= pd.read_csv('C:/Users/Kwabena-Kobiri/Desktop/test.csv', parse_dates=['date'])
    train= pd.read_csv('C:/Users/Kwabena-Kobiri/Desktop/train.csv', parse_dates=['date'])
    
    # Data split for validation
    train_all = train.copy().dropna()
    train = train_all.loc[train_all.date < '2011-01-01']
    valid = train_all.loc[train_all.date > '2011-01-01']
    # print(train.shape, valid.shape)

    # Define input and output columns
    in_cols = train.columns[6:]
    target_col = 'burn_area'
    #in_cols

    # Get our X and y training and validation sets ready
    X_train, y_train = train[in_cols], train[target_col]
    X_valid, y_valid = valid[in_cols], valid[target_col]

    # Create and fit the model
    model = RidgeCV()
    model.fit(X_train, y_train)

    # Make predictions
    preds = model.predict(X_valid)

    # Score
    #mean_squared_error(y_valid, preds)**0.5 # RMSE - should match Zindi score. Lower is better
    
    #VISUALIZE SUBMISSION FILE
    ss = pd.read_csv('C:/Users/Kwabena-Kobiri/Desktop/SampleSubmission.csv')
    #ss.head()

    # So we need to predict the burn area for each row in test. 

    # Add the same features to test as we did to train:
    #test['month'] = test.date.dt.month
    #test['year'] = test.date.dt.year
    
    #donar_train['project_submitted_datetime'] = pd.to_datetime(donar_train.project_submitted_datetime, format='%d-%m-%Y %H:%M')

    # Get predictions
    preds = model.predict(test[in_cols].fillna(0)) # fillna(0) here could be improved by examining the missing data and filling more appropriately.
    
    # Display the prediction result to the user in the 'Prediction' label on the GUI
    prediction_output['text'] = round(preds[len(preds) - 1], 5)
    
    # Add to submission dataframe
    #ss['Prediction'] = preds

    # View
    #ss.head()

    # Save ready for submission:
    #ss.to_csv('C:/Users/Kwabena-Kobiri/Desktop/SampleSubmissionOG.csv', index=False)
    
    #new = pd.read_csv('C:/Users/Kwabena-Kobiri/Desktop/SampleSubmissionOG.csv')
    #prediction_output['text'] = round(new.Prediction[1], 5)
    #prediction_output['text'] = round(new.Prediction[1], 5)

# Function To Clear All Fields on the GUI
def clear():
    #Clearing All inputs in the fields
    ID1.delete(0, END)
    Area1.delete(0, END)
    climate_aet1.delete(0, END)
    climate_def1.delete(0, END)
    climate_pdsi1.delete(0, END)
    climate_pet1.delete(0, END)
    climate_pr1.delete(0, END)
    climate_ro1.delete(0, END)
    climate_soil1.delete(0, END)
    climate_srad1.delete(0, END)
    climate_swe1.delete(0, END)
    climate_tmmn1.delete(0, END)
    climate_tmmx1.delete(0, END)
    climate_vap1.delete(0, END)
    climate_vpd1.delete(0, END)
    climate_vs1.delete(0, END)
    elevation1.delete(0, END)
    landcover_01.delete(0, END)
    landcover_11.delete(0, END)
    landcover_21.delete(0, END)
    landcover_31.delete(0, END)
    landcover_41.delete(0, END)
    landcover_51.delete(0, END)
    landcover_61.delete(0, END)
    landcover_71.delete(0, END)
    landcover_81.delete(0, END)
    population_density1.delete(0, END)
    precipitation1.delete(0, END)
    ID_output['text'] = ' '
    prediction_output['text'] = ' '
    #print(features)

#WIDGETS FOR GUI 
window = Tk()
window.title('UMOJAHACK FIRE HOTSPOT PREDICTION')
window.geometry('650x700')

#INSTRUCTION AREA
instruct = Label(window, text='ENTER DATA FOR THE VARIOUS PARAMETERS', padx='5px', pady='5px',
font=('bold', 12), bg='black', fg='white')
instruct.grid(row=0, column=1, columnspan=4, sticky=EW)

#WIDGETS ON LEFT COLUMN OF GUI
ID = Label(window, text='ID', padx='5px',pady='5px')
ID.grid(row=2, column=0, sticky=E, padx='10px')
ID1 = Entry(window)
ID1.grid(row=2, column=1, sticky=W)

area = Label(window, text='area', padx='5px',pady='5px')
area.grid(row=3, column=0, sticky=E)
Area1 = Entry(window)
Area1.grid(row=3, column=1, sticky=W)

climate_aet = Label(window, text='climate_aet', padx='5px',pady='5px')
climate_aet.grid(row=4, column=0, sticky=E)
climate_aet1 = Entry(window)
climate_aet1.grid(row=4, column=1, sticky=W)

climate_def = Label(window, text='climate_def', padx='5px',pady='5px')
climate_def.grid(row=5, column=0, sticky=E)
climate_def1 = Entry(window)
climate_def1.grid(row=5, column=1, sticky=W)

climate_pdsi = Label(window, text='climate_pdsi', padx='5px',pady='5px')
climate_pdsi.grid(row=6, column=0, sticky=E)
climate_pdsi1 = Entry(window)
climate_pdsi1.grid(row=6, column=1, sticky=W)

climate_pet = Label(window, text='climate_pet', padx='5px',pady='5px')
climate_pet.grid(row=7, column=0, sticky=E)
climate_pet1 = Entry(window)
climate_pet1.grid(row=7, column=1, sticky=W)

climate_pr = Label(window, text='climate_pr', padx='5px',pady='5px')
climate_pr.grid(row=8, column=0, sticky=E)
climate_pr1 = Entry(window)
climate_pr1.grid(row=8, column=1, sticky=W)

climate_ro = Label(window, text='climate_ro', padx='5px',pady='5px')
climate_ro.grid(row=9, column=0, sticky=E)
climate_ro1 = Entry(window)
climate_ro1.grid(row=9, column=1, sticky=W)

climate_soil = Label(window, text='climate_soil', padx='5px',pady='5px')
climate_soil.grid(row=10, column=0, sticky=E)
climate_soil1 = Entry(window)
climate_soil1.grid(row=10, column=1, sticky=W)

climate_srad = Label(window, text='climate_srad', padx='5px',pady='5px')
climate_srad.grid(row=11, column=0, sticky=E)
climate_srad1 = Entry(window)
climate_srad1.grid(row=11, column=1, sticky=W)

climate_swe = Label(window, text='climate_swe', padx='5px',pady='5px')
climate_swe.grid(row=12, column=0, sticky=E)
climate_swe1 = Entry(window)
climate_swe1.grid(row=12, column=1, sticky=W)

climate_tmmn = Label(window, text='climate_tmmn', padx='5px',pady='5px')
climate_tmmn.grid(row=13, column=0, sticky=E)
climate_tmmn1 = Entry(window)
climate_tmmn1.grid(row=13, column=1, sticky=W)

climate_tmmx = Label(window, text='climate_tmmx', padx='5px',pady='5px')
climate_tmmx.grid(row=14, column=0, sticky=E, padx='10px')
climate_tmmx1 = Entry(window)
climate_tmmx1.grid(row=14, column=1, sticky=W)

climate_vap = Label(window, text='climate_vap', padx='5px',pady='5px')
climate_vap.grid(row=15, column=0, sticky=E)
climate_vap1 = Entry(window)
climate_vap1.grid(row=15, column=1, sticky=W)

# WIDGETS ON RIGHT COLUMN OF GUI
climate_vpd = Label(window, text='         climate_vpd', padx='5px',pady='5px')
climate_vpd.grid(row=2, column=2, sticky=E)
climate_vpd1 = Entry(window)
climate_vpd1.grid(row=2, column=3, sticky=W)

climate_vs = Label(window, text='         climate_vs', padx='5px',pady='5px')
climate_vs.grid(row=3, column=2, sticky=E)
climate_vs1 = Entry(window)
climate_vs1.grid(row=3, column=3, sticky=W)

elevation = Label(window, text='         elevation', padx='5px',pady='5px')
elevation.grid(row=4, column=2, sticky=E)
elevation1 = Entry(window)
elevation1.grid(row=4, column=3, sticky=W)

landcover_0 = Label(window, text='         landcover_0', padx='5px',pady='5px')
landcover_0.grid(row=5, column=2, sticky=E)
landcover_01 = Entry(window)
landcover_01.grid(row=5, column=3, sticky=W)

landcover_1 = Label(window, text='         landcover_1', padx='5px',pady='5px')
landcover_1.grid(row=6, column=2, sticky=E)
landcover_11 = Entry(window)
landcover_11.grid(row=6, column=3, sticky=W)

landcover_2 = Label(window, text='         landcover_2', padx='5px',pady='5px')
landcover_2.grid(row=7, column=2, sticky=E)
landcover_21 = Entry(window)
landcover_21.grid(row=7, column=3, sticky=W)

landcover_3 = Label(window, text='         landcover_3', padx='5px',pady='5px')
landcover_3.grid(row=8, column=2, sticky=E)
landcover_31 = Entry(window)
landcover_31.grid(row=8, column=3, sticky=W)

landcover_4 = Label(window, text='         landcover_4', padx='5px',pady='5px')
landcover_4.grid(row=9, column=2, sticky=E)
landcover_41 = Entry(window)
landcover_41.grid(row=9, column=3, sticky=W)

landcover_5 = Label(window, text='         landcover_5', padx='5px',pady='5px')
landcover_5.grid(row=10, column=2, sticky=E)
landcover_51 = Entry(window)
landcover_51.grid(row=10, column=3, sticky=W)

landcover_6 = Label(window, text='         landcover_6', padx='5px',pady='5px')
landcover_6.grid(row=11, column=2, sticky=E)
landcover_61 = Entry(window)
landcover_61.grid(row=11, column=3, sticky=W)

landcover_7 = Label(window, text='         landcover_7', padx='5px',pady='5px')
landcover_7.grid(row=12, column=2, sticky=E)
landcover_71 = Entry(window)
landcover_71.grid(row=12, column=3, sticky=W)

landcover_8 = Label(window, text='         landcover_8', padx='5px',pady='5px')
landcover_8.grid(row=13, column=2, sticky=E)
landcover_81 = Entry(window)
landcover_81.grid(row=13, column=3, sticky=W)

population_density = Label(window, text='         population_density', padx='5px',pady='5px')
population_density.grid(row=14, column=2, sticky=E)
population_density1 = Entry(window)
population_density1.grid(row=14, column=3, sticky=W)

precipitation = Label(window, text='         precipitation', padx='5px',pady='5px')
precipitation.grid(row=15, column=2, sticky=E)
precipitation1 = Entry(window)
precipitation1.grid(row=15, column=3, sticky=W)

# BUTTONS FOR FEATURE EXTRACTION AND ANALYSIS
extract_btn = Button(window, text='Extract features', padx='5px', pady='5px', 
fg='white', bg='#1e9699', font=('bold', 11), command=extract)
extract_btn.grid(row=17, column=1, padx='10px', pady='15px')

analyze_btn = Button(window, text='Analyze features', padx='5px', pady='5px', 
fg='white', bg='#1e9688', font=('bold', 11), command=analyze)
analyze_btn.grid(row=17, column=2, padx='10px', pady='15px')

clear_btn = Button(window, text='Clear All', padx='5px', pady='5px', 
fg='white', bg='#1e9688', font=('bold', 11), command=clear)
clear_btn.grid(row=17, column=3, padx='10px', pady='15px', sticky=EW)

# ANALYSIS RESULTS
Results_text = Frame(window, relief=RAISED, bd=3, padx='5px', pady='5px', bg='#8e2de2')
Results_text.grid(row=18, column=1, columnspan=2, padx='5px', sticky=E)

ID_lbl = Label(Results_text, text='ID', padx='5px', pady='5px', 
font=('bold', 12), bg='#8e2de2', fg='white')
ID_lbl.grid(row=0, column=0, sticky=E, padx='10px')

prediction_lbl= Label(Results_text, text='Prediction', padx='10px', pady='5px', 
font=('bold', 12), bg='#8e2de2', fg='white')
prediction_lbl.grid(row=0, column=1, sticky=W, padx='15px')

Results_output = Frame(Results_text, relief=SUNKEN, bd=3, padx='5px', pady='5px', bg='#f80759')
Results_output.grid(row=1, column=0, columnspan=2, sticky=EW, padx='5px',pady='10px')

ID_output = Label(Results_output, text=' ', font=('bold', 10), bg='#f80759')
ID_output.grid(row=0, column=0, sticky=E)

prediction_output = Label(Results_output, text=' ', font=('bold', 10), bg='#f80759')
prediction_output.grid(row=0, column=1, padx='20px')

window.mainloop()


# In[ ]:





# In[ ]:





import pandas as pd
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib

class IAService:
    def __init__(self) -> None:
        pass
    def getData(self):
        return pd.read_csv('D:\Bihar 2024\csv\suivivehicule_record_v1_202410022255.csv', sep=',' ,low_memory=False)
    def toDate(self, str_time):
        return pd.to_datetime(str_time, errors='coerce')
    def setDataDate(self, df):
        df['time_diff'] = (self.toDate(df['trip_start_date']) - self.toDate(df['pick_up_time'])).dt.total_seconds()
        df['trip_start_date'] = self.toDate(df['trip_start_date'])
        df['pick_up_time'] = self.toDate(df['pick_up_time'])
        df['created_at'] = self.toDate(df['created_at'])
        return df
    def setNanOrDefaultValue(self, df):
        df['ignition'] = df['ignition'].map({'on': 1, 'off': 0})
        df['speed_measure'] = df['speed_measure'].map({'kph': 0})
        df['engineStatus'] = df['engineStatus'].map({'idling':0, 'in transit': 1, 'stopped': 2, 'in transit (ign off)':3})
        df['ignition'] = df['ignition'].fillna(-1)

        df['speed_measure'] = df['speed_measure'].fillna(-1)
        df['engineStatus'] = df['engineStatus'].fillna(-1)
        df['reason_id'] = df['reason_id'].fillna(-1)
        df['sub_reason_id'] = df['sub_reason_id'].fillna(-1)

        df['resa_trans_type'] = df['resa_trans_type'].map({'DEP': 1, 'ARV':0})
        df['resa_trans_type'] = df['resa_trans_type'].fillna(-1)
        return df

    def strEncoder(sefl, df):
        le_vehicleno = LabelEncoder()
        le_driver_oname = LabelEncoder()
        le_from_place = LabelEncoder()
        le_to_place = LabelEncoder()
        le_driver_mobile_number_place = LabelEncoder()

        # Appliquer l'encodage aux colonnes catégorielles
        df['vehicleno'] = le_vehicleno.fit_transform(df['vehicleno'].astype(str))
        df['driver_oname'] = le_driver_oname.fit_transform(df['driver_oname'].astype(str))
        df['FromPlace'] = le_from_place.fit_transform(df['FromPlace'].astype(str))
        df['ToPlace'] = le_to_place.fit_transform(df['ToPlace'].astype(str))
        df['driver_mobile_number'] = le_driver_mobile_number_place.fit_transform(df['driver_mobile_number'].astype(str))
        return df

    def preparationData(self, df):
        df = self.setDataDate(df)
        df = self.setNanOrDefaultValue(df)
        df = self.strEncoder(df)

    def filtreData(self, df):
        df_filtered = df[df['status'].isin([0, 1, 5])]
        X = df_filtered[['difftimepickup', 'speed', 'engineStatus', 'time_diff', 'odometer', 'ignition',
        'vehicleno', 'driver_oname', 'driver_mobile_number', 'FromPlace','ToPlace']]
        y = df_filtered['status']

        X_clean = X.dropna()
        y_clean = df['status'].loc[X_clean.index]
        return X_clean, y_clean

    def createModeles(self,df):  
        self.preparationData (df) 
        X_clean, y_clean = self.filtreData(df)
        X_train, X_test, y_train, y_test = train_test_split(X_clean, y_clean, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        joblib.dump(model, 'data/randomForestClassifier-models-v1.pkl')

        y_pred = model.predict(X_test)

        print("Accuracy:", accuracy_score(y_test, y_pred))
        print(classification_report(y_test, y_pred))
        print( (y_test, y_pred))
        return accuracy_score(y_test, y_pred)

    def loadModeleSupervisé(self, X_to_predict):
        X = self.prepareDataToPredict(X_to_predict)
        X.info()
        modelJob = joblib.load('D:/mautourco-suivi-vehicule/data/randomForestClassifier-models-v1.pkl')
        y_pred = modelJob.predict_proba(X)
        print("Propabilité " , y_pred)
        return y_pred
    
    def prepareDataToPredict(self, data):
        new_trip_data = pd.DataFrame([{
            'difftimepickup': float(data.difftimepickup) if data.difftimepickup is not None else 0.0,
            'speed': float(data.speed) if data.speed is not None else 0.0 ,
            'engineStatus': data.engineStatus,  # Si c'est toujours la même valeur, inutile d'utiliser random.choice
            'time_diff': random.uniform(-3600, 3600),
            'odometer': float(data.odometer) if data.odometer is not None else 0.0,
            'ignition': data.ignition,  # Même raison pour l'ignition
            'vehicleno': data.vehicleno,
            'driver_oname': data.driver_oname,
            'driver_mobile_number': data.driver_mobile_number,
            'FromPlace': data.FromPlace,
            'ToPlace': data.ToPlace
        }])

        new_trip_data['ignition'] = new_trip_data['ignition'].map({'on': 1, 'off': 0})
        new_trip_data['engineStatus'] = new_trip_data['engineStatus'].map({'idling':0, 'in transit': 1, 'stopped': 2, 'in transit (ign off)':3})
        new_trip_data['ignition'] = new_trip_data['ignition'].fillna(-1)

        # Utilisation d'un seul objet LabelEncoder
        label_encoder = LabelEncoder()

        # Colonnes à encoder
        columns_to_encode = ['vehicleno', 'driver_oname', 'driver_mobile_number', 'FromPlace', 'ToPlace']

        # Encodage de toutes les colonnes spécifiées
        for col in columns_to_encode:
            new_trip_data[col] = label_encoder.fit_transform(new_trip_data[col].astype(str))

        new_trip_data.head()
        return new_trip_data

        

    def mapDataX(self, data):
        pass








        

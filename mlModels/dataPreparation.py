import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

CALCULATED_COLUMNS = [
    'AVG_RATING',
    'ACTIVITY_ORIENTED_INVESTMENT',
    'INTERACTION_ORIENTED_INVESTMENT',
    'COURSE_ACCESS_CONNECTION_ORIENTED_INVESTMENT',
    'COURSE_ACCESS_COUNT_ORIENTED_INVESTMENT',
    'ENGAGEMENT'
]

def prepData(filepath):
    data = pd.read_csv(filepath, sep=';', on_bad_lines='warn')
    dropUselessColumns(data)
    handleTimeTypeVariables(data)
    handleMissingData(data)
    labelTarget(data)
    features = data.drop('DIFFICULTY', axis=1)
    target = data['DIFFICULTY']
    scaledFeatures = scaling(features)
    X_res, y_res = equilibrate(scaledFeatures, target)
    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def dropUselessColumns(data):
    # toutes les colonnes dont la valeur peux dépendre d'une autre colonne est supprimée pour éviter les redondances
    data.drop(columns=CALCULATED_COLUMNS, inplace=True)
    return

def handleTimeTypeVariables(data):
    new_columns = []
    for col in data.columns:
        if 'SUBMISSION' in col or 'ACCESS' in col:
            day_col = data[col].dt.day
            month_col = data[col].dt.month
            hour_col = data[col].dt.hour
            minute_col = data[col].dt.minute
            new_columns.append(day_col.rename(f"{col}_day"))
            new_columns.append(month_col.rename(f"{col}_month"))
            new_columns.append(hour_col.rename(f"{col}_hour"))
            new_columns.append(minute_col.rename(f"{col}_minute"))
            data.drop(columns=[col], inplace=True)
    data = pd.concat([data] + new_columns, axis=1)
    return


def handleMissingData(data):
    data.fillna(-1, inplace=True)
    return

def labelTarget(data):
    label_enc = LabelEncoder()
    data['DIFFICULTY'] = label_enc.fit_transform(data['DIFFICULTY'])
    data = pd.get_dummies(data)
    return

def scaling(data):
    scaler = MinMaxScaler()
    return scaler.fit_transform(data)

def normalize(data):
    scaler = StandardScaler()
    return scaler.fit_transform(data)

def equilibrate(X, y):
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X, y)
    return X_res, y_res

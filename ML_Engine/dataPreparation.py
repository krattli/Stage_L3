import pandas as pd
import numpy as np
from typing import Tuple, List, cast

from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

USELESS_COLUMNS = [
    'ACADEMIC_Y',
    'COURSE_NAME',
    'AVG_RATING',
    'ACTIVITY_ORIENTED_INVESTMENT',
    'INTERACTION_ORIENTED_INVESTMENT',
    'COURSE_ACCESS_CONNECTION_ORIENTED_INVESTMENT',
    'COURSE_ACCESS_COUNT_ORIENTED_INVESTMENT',
    'ENGAGEMENT',
    'RATING_S5Q1',
    'RANK_S3Q1',
]

def prepData(filepath:str) -> Tuple[ np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[str]]:
    data = pd.read_csv(filepath, sep=';', on_bad_lines='warn')
    data = dropUselessColumns(data)                # toutes les colonnes dont la valeur peux dépendre d'une autre colonne est supprimée pour éviter les redondances
    data = handleTimeTypeVariables(data)           # les variables temporelles sont séparées en plusieurs autres colonnes (mois, jour, heure, minute)
    data = labelTarget(data, 'PUBLIC')
    data = labelTarget(data, 'DIFFICULTY')
    data = cleanComas(data)                        # dans le csv, les nombres à virgule sont pas reconnus par python pour être converites en float, on doit donc les remplacer
    data = handleMissingData(data)                 # les données manquantes sont remplaées par -1
    #data = pd.get_dummies(data)
    print(data.columns)
    features, target = chooseTarget(data, 'DIFFICULTY')
    scaledFeatures = scaling(features)
    X_res, y_res = equilibrate(scaledFeatures, target)
    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)
    return np.asarray(X_train), np.asarray(X_test), np.asarray(y_train), np.asarray(y_test), features.columns.tolist()

def dropUselessColumns(data):
    data.drop(columns=USELESS_COLUMNS, inplace=True)
    return data

def handleTimeTypeVariables(data):
    new_columns = []
    for col in data.columns:
        if 'FIRST' in col or 'LAST' in col:
            data[col] = data[col].str.strip()
            data[col] = data[col].str.replace(r'[-]', '', regex=True)
            try:
                data[col] = pd.to_datetime(data[col], errors='coerce')
                if pd.api.types.is_datetime64_any_dtype(data[col]):
                    day_col = data[col].dt.day
                    month_col = data[col].dt.month
                    hour_col = data[col].dt.hour
                    minute_col = data[col].dt.minute
                    new_columns.append(day_col.rename(f"{col}_day"))
                    new_columns.append(month_col.rename(f"{col}_month"))
                    new_columns.append(hour_col.rename(f"{col}_hour"))
                    new_columns.append(minute_col.rename(f"{col}_minute"))
                    data.drop(columns=[col], inplace=True)
            except Exception as e:
                print(f"Erreur lors de la conversion de {col}: {e}")
    data = pd.concat([data] + new_columns, axis=1)
    return data


def handleMissingData(data:pd.DataFrame) -> pd.DataFrame:
    data.fillna(-1, inplace=True)
    return data

def labelTarget(data:pd.DataFrame, targetLabel:str) -> pd.DataFrame:
    label_enc = LabelEncoder()
    data[targetLabel] = data[targetLabel].str.strip()
    data[targetLabel] = label_enc.fit_transform(data[targetLabel])
    return data

def cleanComas(data:pd.DataFrame) -> pd.DataFrame:
    for col in data.columns:
        if data[col].dtype == 'object':
            data[col] = data[col].str.replace(',', '.', regex=True)
    return data

def chooseTarget(data:pd.DataFrame, targetLabel:str) -> Tuple[pd.DataFrame, np.ndarray]:
    features = data.drop(targetLabel, axis=1)
    target = cast(pd.Series, data[targetLabel]) # nécéssaire, sinon pyright ne comprends pas que data[targetLabel] renvoie un objet de type pd.Series
    return features, np.asarray(target)


def scaling(data:pd.DataFrame) -> np.ndarray:
    scaler = MinMaxScaler()
    return scaler.fit_transform(data)

def normalize(data:pd.DataFrame) -> pd.DataFrame:
    scaler = StandardScaler()
    return scaler.fit_transform(data)

def equilibrate(X:np.ndarray, y:np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    smote = SMOTE(random_state=42)
    result = smote.fit_resample(X, y)
    return np.asarray(result[0]), np.asarray(result[1])

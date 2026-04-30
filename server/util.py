import json
import pickle
import warnings
from pathlib import Path

import numpy as np

__locations = None
__data_columns = None
__model = None
_ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"

def get_estimated_price(location, sqft, bhk, bath):
    load_saved_artifacts()

    location = (location or "").strip().lower()
    try:
        loc_index = __data_columns.index(location)
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="X does not have valid feature names",
            category=UserWarning,
        )
        predicted_price = __model.predict([x])[0]

    return round(predicted_price, 2)


def load_saved_artifacts():
    global __data_columns
    global __locations
    global __model

    if __data_columns is not None and __model is not None:
        return

    columns_path = _ARTIFACTS_DIR / "columns.json"
    model_path = _ARTIFACTS_DIR / "banglore_home_prices_model.pickle"

    with columns_path.open("r", encoding="utf-8") as f:
        __data_columns = json.load(f)["data_columns"]
        __locations = __data_columns[3:]

    with model_path.open("rb") as f:
        __model = pickle.load(f)

def get_location_names():
    load_saved_artifacts()
    return __locations


def get_data_columns():
    load_saved_artifacts()
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2)) # other location
    print(get_estimated_price('Ejipura', 1000, 2, 2))  # other location

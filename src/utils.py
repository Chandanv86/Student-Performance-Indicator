import os
import sys
import numpy as np 
import pandas as pd
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
from src.logger import logging

# def save_object(file_path, obj):
#     """
#     Ye function kisi bhi Python object ko ek specific path pr 
#     Pickle (.pkl) file banakar save karne ke kaam aata hai.
#     """
#     try:
#         # 1. Directory Path nikalna
#         dir_path = os.path.dirname(file_path)

#         # 2. Agar directory exist nhi karti, toh use bana dena
#         os.makedirs(dir_path, exist_ok=True)

#         # 3. Object ko Binary Write ('wb') mode mein save karna
#         # 'dill' ya 'pickle' dono ka logic same hai, pr dill zyada powerful hai
#         with open(file_path, "wb") as file_obj:
#             pickle.dump(obj, file_obj)
        
#         logging.info(f"Object successfully saved at: {file_path}")
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj) # Ya dill.dump
    except Exception as e:
        raise CustomException(e, sys)
    except Exception as e:
        # Agar permissions issue ho ya space na ho, toh exception raise karna
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    """
    In-depth Model Evaluation function:
    1. Har model ko uthayega.
    2. GridSearchCV se best parameters dhoondhega.
    3. Model ko train (fit) karega.
    4. Test data pr score (R2 Score) calculate karega.
    """
    try:
        report = {}

        # Hum 'models' dictionary ki keys (names) pr loop chala rahe hain
        for i in range(len(list(models))):
            model_name = list(models.keys())[i]
            model = list(models.values())[i]
            para = param[model_name]

            # --- HYPERPARAMETER TUNING  ---
            # GridSearchCV ka kaam hai best parameters dhoondhna.
            # cv=3 ka matlab hai data ko 3 baar shuffle karke check karna.
            # n_jobs=-1 matlab computer ke saare processors use karna speed ke liye.
            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            # Best parameters milne ke baad model ko un settings pr set karna
            model.set_params(**gs.best_params_)
            
            # Asli training yahan ho rahi hai best settings ke saath
            model.fit(X_train, y_train)

            # Prediction karna Train aur Test data dono pr
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            # Performance check (R2 Score nikalna)
            # Hum report mein sirf 'test_model_score' rakh rahe hain kyunki wahi asli test hai
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    """
    Pickle file ko wapas load karne ke liye (Prediction ke waqt kaam aayega).
    """
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)

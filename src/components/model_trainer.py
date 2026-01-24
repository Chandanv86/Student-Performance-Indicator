import os
import sys
from dataclasses import dataclass

# Essential Algorithms
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models # evaluate_models -> utils 

@dataclass
class ModelTrainerConfig:
    """
    Configuration Class: Ye batati hai ki jab hamara 'Best Model' mil jayega,
    toh uski Pickle (.pkl) file kha save hogi.
    """
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        # Config object create kiya taaki model path access ho sake
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        """
        Ye main function hai jo transformed arrays ko uthayega,
        multiple models ko train karega, aur best model select karega.
        """
        try:
            logging.info("Train aur Test input data ko split kar rahe hain")
            
            # 1. Array ko X aur y mein baantna
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            # 2. Dictionary of Models: 
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            # 3. Hyperparameters (Params): 
            params = {
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                },
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Gradient Boosting": {
                    'learning_rate': [.1, .01, .05, .001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Linear Regression": {},
                "XGBRegressor": {
                    'learning_rate': [.1, .01, .05, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "AdaBoost Regressor": {
                    'learning_rate': [.1, .01, 0.5, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }

            # 4. Evaluation: Utils function ko call kiya jo 'Hyperparameter Tuning' karke report dega
            model_report: dict = evaluate_models(
                X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                models=models, param=params
            )

            # 5. Best Model dhundna report mein se
            best_model_score = max(sorted(model_report.values()))

            # Best model ka naam nikalna dictionary keys se
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            # 6. Threshold Check: Agar accuracy 60% se kam hai toh model reject
            if best_model_score < 0.6:
                raise CustomException("Koi bhi best model nhi mila jiske acceptable accuracy ho")
            
            logging.info(f"Best model mil gaya: {best_model_name} with score: {best_model_score}")

            # 7. Model ko save karna (Pickle file banana)
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            # Final Prediction check on test data
            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)

            return r2_square

        except Exception as e:
            raise CustomException(e, sys) 
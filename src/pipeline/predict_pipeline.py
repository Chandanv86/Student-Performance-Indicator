import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object # Humne utils mein load_object pehle hi bana liya tha

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        """
        Layman: Raw data ko uthao, preprocessor se saaf karo, aur model se prediction lo.
        Deep Dive: Loading serialized objects and performing inference.
        """
        try:
            model_path = 'artifacts/model.pkl'
            preprocessor_path = 'artifacts/preprocessor.pkl'

            # Objects ko load karna (Deserialization)
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            # Data ko scale/encode karna
            data_scaled = preprocessor.transform(features)

            # Final Prediction
            preds = model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    """
    Ye class HTML form ke inputs ko ek DataFrame mein convert karne ke liye hai.
    Variables exactly wahi hone chahiye jo training ke waqt the.
    """
    def __init__(self, gender: str, race_ethnicity: str, parental_level_of_education: str,
                 lunch: str, test_preparation_course: str, reading_score: int, writing_score: int):
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)
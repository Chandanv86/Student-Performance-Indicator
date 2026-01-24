import os
import sys
import pandas as pd
# --- FUTURE USE: Agar Database use karna ho toh niche wali libraries install aur uncomment karein ---
# import pymongo # MongoDB se connect karne ke liye library
# import mysql.connector # SQL se connect karne ke liye library
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import CustomException

# --- Step 1: Configuration ---
@dataclass
class DataIngestionConfig:
    """
    Yha hum decide kar rahe hain ki local file ya database se data aane ke baad 
    usse local 'artifacts' folder mein kha save karna hai.
    """
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "raw.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    """
    ========================================================================================
    FUTURE USE INSTRUCTIONS (DATABASE INGESTION):
    Agar aapko MongoDB ya SQL se data uthana hai, toh:
    1. Upar waale imports ko uncomment karein.
    2. Niche diye gaye functions ko uncomment karein.
    3. 'initiate_data_ingestion' method ke andar 'df = pd.read_csv' wali line ko comment karein
       aur 'df = self.get_data_from_mongodb()' ya SQL waale function ko call karein.
    ========================================================================================
    """

    # def get_data_from_mongodb(self):
    #     """
    #     NoSQL Database (MongoDB) se data fetch karne ka logic.
    #     """
    #     try:
    #         logging.info("MongoDB se data fetch karne ki process start ho rahi hai")
    #         mongo_client_url = "YOUR_MONGODB_CONNECTION_STRING"
    #         client = pymongo.MongoClient(mongo_client_url)
    #         db = client['database_name']
    #         collection = db['collection_name']
    #         cursor = collection.find()
    #         df = pd.DataFrame(list(cursor))
    #         if "_id" in df.columns:
    #             df.drop(columns=["_id"], inplace=True)
    #         return df
    #     except Exception as e:
    #         raise CustomException(e, sys)

    # def get_data_from_sql(self):
    #     """
    #     Relational Database (MySQL/PostgreSQL) se data fetch karne ka logic.
    #     """
    #     try:
    #         logging.info("SQL database se data fetch karne ki process start ho rahi hai")
    #         connection = mysql.connector.connect(host="localhost", user="root", password="password", database="db_name")
    #         query = "SELECT * FROM table_name"
    #         df = pd.read_sql_query(query, connection)
    #         connection.close()
    #         return df
    #     except Exception as e:
    #         raise CustomException(e, sys)

    # --- MAIN INITIATION METHOD (LOCAL SOURCE FOCUS) ---
    def initiate_data_ingestion(self):
        """
        Ye main gate hai jo local CSV file ko read karke split aur save karta hai.
        """
        logging.info("Data Ingestion process started from local source")
        try:
            # --- LOCAL SOURCE READING ---
            # Hum direct 'notebook/data/stud.csv' se data utha rahe hain.
            # Agar file khaheen aur hai toh yha path change karein.
            df = pd.read_csv(os.path.join('notebook', 'data', 'stud.csv'))
            
            logging.info('Local dataset ko successfully dataframe mein load kar liya gaya hai')

            # Artifacts folder banana agar nhi hai toh (mkdir -p logic)
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Raw data ko backup ke liye artifacts mein save karna
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")
            
            # Data split: 80% Training ke liye aur 20% Testing ke liye
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Split huye datasets ko save karna
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion process complete. Local data split aur save ho gaya hai.")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            # Agar file nhi milti ya koi syntax error hai toh CustomException trigger hoga
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj = DataIngestion()
    # Ab yha koi source pass karne ki zarurat nhi hai, ye by-default local file hi uthayega
    train_path, test_path = obj.initiate_data_ingestion()
    print(f"Data ingestion successful. Files saved at:\n{train_path}\n{test_path}")
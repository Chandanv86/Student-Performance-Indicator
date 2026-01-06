import logging # Ye main library hai jo messages ko record karne ke kaam aati hai
import os # Operating System library taaki hum folders aur paths ke saath khel sakein
from datetime import datetime # Har log file ko unique time dene ke liye

# 1. Sabse pehle hum log file ka ek unique naam decide karte hain.
# datetime.now() current time leta hai aur strftime use ek specific format mein badal deta hai.
# Isse fayda ye hota hai ki har baar jab aap project run karoge, ek nayi file banegi pr puraani delete nhi hogi.
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# 2. Ab hum batate hain ki ye file kha pr save honi chahiye.
# os.getcwd() current project directory ka path uthata hai.
# os.path.join use 'logs' folder aur hamare 'LOG_FILE' naam ke saath merge (join) kar deta hai.
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# 3. Yha pr hum check karte hain ki kya 'logs' naam ka folder already exist karta hai?
# os.makedirs folder banata hai. exist_ok=True ka matlab hai ki agar folder pehle se hai, 
# toh crash nhi hona hai, bas use hi use kar lena hai.
os.makedirs(os.path.dirname(logs_path), exist_ok=True)

# 4. Ye hai sabse important part: Basic Configuration.
# Yha hum decide karte hain ki log dikhega kaisa aur kha save hoga.
logging.basicConfig(
    filename=logs_path, # Saara record is path wali file mein jayega
    # format mein: 
    # asctime -> Time kab hua
    # lineno -> Code ki kis line se message aaya
    # name -> Kaunsa module (file) chal raha hai
    # levelname -> Info hai ya Error
    # message -> Asli message jo humne likha hai
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    # level=logging.INFO ka matlab hai ki sirf zaruri Information aur Errors record honi chahiye.
    level=logging.INFO,
)

# 5. Ye hai Testing Block.
# __name__ == "__main__" ensure karta hai ki ye code sirf tabhi chale jab hum 'logger.py' ko 
# directly run karein. Jab hum ise kisi doosre module mein import karenge, toh ye line execute nhi hogi.
if __name__ == "__main__":
    logging.info("Logging has started successfully! Folder bhi ban gaya hai aur file bhi.")
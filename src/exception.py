import sys

def error_message_detail(error, error_detail: sys):
    # 1. sys.exc_info() humein ek tuple deta hai: (type, value, traceback)
    # Humein sirf 'traceback' (exc_tb) chahiye, isliye pehle 2 ko '_' (ignore) kar diya.
    _, _, exc_tb = error_detail.exc_info()

    # 2. exc_tb (Traceback object) ke paas poori kundli hoti hai
    # 'tb_frame' se hum frame mein enter karte hain aur 'f_code.co_filename' se file ka name nikalte hain.
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    # 3. 'tb_lineno' se exactly line number mil jata hai kha crash hua.
    line_number = exc_tb.tb_lineno

    # 4. Ab sabko ek clean 'String' format mein saja dete hain.
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, line_number, str(error)
    )

    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        # 1. 'super()' call karke hum Python ki basic Exception class ko initialize karte hain.
        # Taaki ye ek "Real" error ki tarah behave kare.
        super().__init__(error_message)

        # 2. Humne jo upar function banaya tha, use call karke detailed message yha store kar liya.
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
    
    def __str__(self):
        # Jab koi is error ko print karega ya log mein dekhega,
        # toh use hamara detailed message dikhega.
        return self.error_message
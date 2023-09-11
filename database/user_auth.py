import os
from dotenv import load_dotenv

class UserAuth:
    '''
    This class is to access the username and password stored in env file
    '''
    def __init__(self):
        load_dotenv()
        self.__user_name = os.environ.get('DATABASE_USER_NAME')
        self.__password = os.environ.get('DATABASE_PASSWORD')
        pass

    def getUserName(self):
        return self.__user_name
    
    def getPassword(self):
        return self.__password

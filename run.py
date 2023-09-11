from getpass import getpass
import os
from api_server.flask_server import runFlaskApp
from scrapper.scrape_data import scrapeData


def printInitial():
    print("Hello, Welcome to Maharashtra Property ETL Pipeline")
    print("This module includes a python script which scrapes top 50 properties in Bandra region of Andheri, Mumbai Suburbs for year 2023")
    print("==============================================")
    print("Note: Please make sure your system has a postgresql account")
    checkEnvVariable()


def checkEnvVariable():
    res = os.path.isfile('.env')
    if not res:
        user=input("Username to access postgresql:")
        pas=getpass("Passward for {}:".format(user))
        

        with open(".env", "w") as f:
            f.write("DATABASE_USER_NAME={}\n".format(user))
            f.write("DATABASE_PASSWORD={}".format(pas))
    

    print("User saved!")
    print("=================================")


if __name__ == '__main__':
    printInitial()

    print("Starting Scrapping data")
    print("Please NOTE:")
    print("The browser will open for scrapping, only manual thing")
    print("**Entering Captcha** (No need to click submit button)")
    print("**Starting Google Translate from extension bar**")

    res = input("Plese enter y to continue, q to exit ").lower()

    while True:
        if res=='y':
            scrapeData()
            runFlaskApp()
            break
        elif res=='q':
            break
        else:
            res = input("Plese enter y to continue, q to exit ").lower()
            continue




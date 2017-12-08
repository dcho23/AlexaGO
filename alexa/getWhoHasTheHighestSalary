import sys
import pymysql
import logging
# import json
# import urllib2


rds_host  = "gadb.czvdmt1ncqds.us-east-2.rds.amazonaws.com"
db_username = "root"
db_password = "password"
db_name = "ece4813"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(event)

    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.981176af-6d4a-427b-b05e-1f6a994d69b6"): 
        raise ValueError("Invalid Application ID")

    conn = pymysql.connect(rds_host, 
        user=db_username, 
        passwd=db_password, 
        db=db_name, 
        port=3306, 
        connect_timeout=15,
        cursorclass=pymysql.cursors.DictCursor)


    with conn.cursor() as cur:
        cur.execute("SELECT Name, Salary FROM People WHERE Salary = (SELECT Max(Salary) FROM People)")
        x = cur.fetchone() 
        name = str(x['Name'])
        salary = str(x['Salary'])
        # cur.execute("SELECT MAX(Salary) FROM People WHERE Title = 'PROFESSOR'")
        # x = cur.fetchone() 

    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": name + " has the highest salary of " + salary 
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": ""
                }
            },
            "shouldEndSession": True
        },
        "sessionAttributes": {}
    }
        
        

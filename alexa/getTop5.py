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

    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.bdf221d3-049a-4269-8485-ea229dde019b"): 
        raise ValueError("Invalid Application ID")

    conn = pymysql.connect(rds_host, 
        user=db_username, 
        passwd=db_password, 
        db=db_name, 
        port=3306, 
        connect_timeout=15,
        cursorclass=pymysql.cursors.DictCursor)


    with conn.cursor() as cur:
        cur.execute("SELECT Organization,count(Organization) as count FROM People WHERE Salary > 100000 GROUP BY Organization ORDER BY count DESC LIMIT 5;")
        x = cur.fetchall() 
        
        result = ""
        for i in x:
            result += str(i['Organization']) + ", "


    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "The top five schools that have the most employees making over one hundred thousand are " + result 
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
        
        
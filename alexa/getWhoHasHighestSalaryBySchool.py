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

    # if (event['session']['application']['applicationId'] != "amzn1.ask.skill.7ff2c569-3910-4bf6-a412-a142754b74fc"): 
    #     raise ValueError("Invalid Application ID")

    if (event['session']['application']['applicationId'] == "amzn1.ask.skill.770b4aab-187f-4391-9925-38c9f1afe1c2"): 
        org = "Georgia Institute of Technology"
    elif (event['session']['application']['applicationId'] == "amzn1.ask.skill.8f5a60cc-3ad9-4708-9baf-899ff2e31377"): 
        org = "University of Georgia"
    elif (event['session']['application']['applicationId'] == "amzn1.ask.skill.aa78f4d7-574d-47ca-b3c2-cd58ab15f003"): 
        org = "Georgia State University"
    elif (event['session']['application']['applicationId'] == "amzn1.ask.skill.5c0cbdc7-4c20-4859-be2d-44cb8eb300a9"): 
        org = "Georgia Southern University"
    elif (event['session']['application']['applicationId'] == "amzn1.ask.skill.93f74927-fb1f-48be-a10a-7a23779a1ad6"): 
        org = "Kennesaw State University"
    elif (event['session']['application']['applicationId'] == "amzn1.ask.skill.9e3537e0-0f49-4f85-b954-eb24dfbff53d"): 
        org = "Valdosta State University"
    else: 
        raise ValueError("Invalid Application ID")


    conn = pymysql.connect(rds_host, 
        user=db_username, 
        passwd=db_password, 
        db=db_name, 
        port=3306, 
        connect_timeout=15,
        cursorclass=pymysql.cursors.DictCursor)


    with conn.cursor() as cur:
        result = "SELECT Name, Salary FROM People WHERE Salary = (SELECT Max(Salary) FROM People WHERE Organization = '%s')" % (org)
        # logger.info(result)
        cur.execute(result)
        x = cur.fetchone() 
        name = str(x['Name'])
        salary = str(x['Salary'])

    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": name + " has the highest salary of " + salary + " at " + org
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
        
        
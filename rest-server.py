from __future__ import print_function
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect
import database
import requests
import json

app = Flask(__name__)
#get global database instant (use it when you want it, it's here for example)
connection = database.get_connection()

@app.route("/home", methods=['GET'])
def homePage():
    return render_template('home.html')


@app.route("/", methods=['GET'])
def home():
    results = requests.get('https://cwzopgcs8c.execute-api.us-east-1.amazonaws.com/prod/getsum').json()
    return render_template('nt.html',l=results[0],y=results[1],t='Total Salary Distributions for University Organizations from 2010 to 2017')

@app.route("/organizationSalary/<int:year>", methods=['GET'])
def piO(year): 
    payload = {
		"year": year
    }
    salary = requests.post('https://cwzopgcs8c.execute-api.us-east-1.amazonaws.com/prod/getsumyear',data=json.dumps(payload)).json()
    yy = 'Total Salary Distributions for University Organizations from ' + str(year)
    return render_template('nt.html',l=salary[0],y=salary[1],t=yy)

@app.route("/OrganizationBreakdown", methods=['GET'])
def OrgBreak():
    out = requests.get('https://cwzopgcs8c.execute-api.us-east-1.amazonaws.com/prod/getOrgBreak').json()
    results = out[0]
    orgs = out[1]
    return render_template('indB.html',l=results,y=orgs,t="Salary Breakdown By Title")

@app.route("/OrganizationBreakdownInd/<organization>", methods=['GET'])
def OrgBreakInd(organization):
	payload = {
		"organization": organization
	}
	out = requests.post('https://cwzopgcs8c.execute-api.us-east-1.amazonaws.com/prod/getOrgBreakInd',data=json.dumps(payload)).json()
	results = out[0]
	orgs = out[1]
	yy = "Salary Break Down For "+ organization
	return render_template('indB.html',l=results,y=orgs,t=yy)

@app.route("/OrganizationBreakdownComp/<organization>/<organization2>", methods=['GET'])
def OrgBreakIndComp(organization,organization2):
	payload = {
		"organization": organization,
		"organization2": organization2
	}
	out = requests.post('https://cwzopgcs8c.execute-api.us-east-1.amazonaws.com/prod/getOrgBreakIndComp',data=json.dumps(payload)).json()
	results = out[0]
	results2 = out[1]
	yy = "Salary Break Down For "+ organization
	zz= "Salary Break Down For "+ organization2
	return render_template('compareP.html',l=results,y=results2,t=yy,u=zz)

@app.route("/OrganizationBreakdownCompBar/<organization>/<organization2>/<int:bars>/<int:year>", methods=['GET'])
def OrgBreakCompBar(organization,organization2,bars,year):
	payload = {
		"organization": organization,
		"organization2":organization2,
		"bars":bars,
		"year":year
	}
	print(payload)
	out = requests.post('https://cwzopgcs8c.execute-api.us-east-1.amazonaws.com/prod/getOrgBreakCompBar',data=json.dumps(payload)).json()
	results = out[0]
	results2 = out[1]
	yy = "Salary Break Down For "+ organization +": Top - "+str(bars) + " in "+ str(year)
	zz= "Salary Break Down For "+ organization2 +": Top - "+str(bars) + " in "+ str(year)
	return render_template('barPCompare.html',l=results,y=results2,t=yy,u=zz)

@app.route("/OrganizationBreakdownBar/<organization>/<int:bars>/<int:year>", methods=['GET'])
def OrgBreakBar(organization,bars,year):
	payload = {
		"organization":organization,
		"bars":bars,
		"year":year
	}
	out = requests.post('https://cwzopgcs8c.execute-api.us-east-1.amazonaws.com/prod/getOrgBreakBar',data=json.dumps(payload)).json()
	results=out[0]
	orgs=out[1]
	ly = [2010,2011,2012,2013,2014,2015,2016]
	yy = "Salary Break Down For "+ organization+" in " + str(year)
	return render_template('barP.html',l=results,t=yy,listYears=ly,oo=orgs,numBars=range(1,101))

@app.route("/page1", methods=['GET','POST'])
def page1():
	if (request.method == 'GET'):
		with connection.cursor() as cursor:
			salary = requests.get("https://cwzopgcs8c.execute-api.us-east-1.amazonaws.com/prod/salary").json()
			colors = []
			for i in range(len(salary)):
				if (i % 5 == 0):
					colors.append("bar primary")
				elif (i % 5 == 1):
					colors.append("bar alert")
				elif (i % 5 == 2):
					colors.append("bar success")
				elif (i % 5 == 3):
					colors.append("bar warning")
				else:
					colors.append("bar secondary")
			salary = zip(colors,salary)
			maxSal = 0
			for item in salary:
				if (item[1]['Average'] > maxSal):
					maxSal = item[1]['Average']
			titles = requests.get("https://cwzopgcs8c.execute-api.us-east-1.amazonaws.com/prod/title").json()
			year = ['2010 - 2016']
		return render_template('page1.html', salaries=salary, maxSal=maxSal, titles=titles, year=year)
	else:
		titles = request.form.getlist('selectedTitle')
		year = request.form.getlist('selectedYear')
		payload = {
			"titles": titles,
			"year": year
		}
		result = json.dumps(payload)
		salary = requests.post("https://cwzopgcs8c.execute-api.us-east-1.amazonaws.com/prod/getSelectedAvgSalary",data=json.dumps(payload)).json()
		year = "2010 - 2016"
		colors = []
		for i in range(len(salary)):
			if (i % 5 == 0):
				colors.append("bar primary")
			elif (i % 5 == 1):
				colors.append("bar alert")
			elif (i % 5 == 2):
				colors.append("bar success")
			elif (i % 5 == 3):
				colors.append("bar warning")
			else:
				colors.append("bar secondary")
		salary = zip(colors,salary)
		# print(salary)
		maxSal = 0
		for item in salary:
			if (item[1]['Average'] > maxSal):
				maxSal = item[1]['Average']
		titles = requests.get("https://cwzopgcs8c.execute-api.us-east-1.amazonaws.com/prod/title").json()
	return render_template('page1.html', salaries=salary, maxSal=maxSal, titles=titles, year=year)

@app.route("/page3", methods=['GET', 'POST'])
def page3():
    if (request.method == 'GET'):
        SchoolList = ['GEORGIA INSTITUTE OF TECHNOLOGY', 'GEORGIA STATE UNIVERSITY',
         'KENNESAW STATE UNIVERSITY', 'UNIVERSITY OF GEORGIA', 'GEORGIA SOUTHERN UNIVERSITY',
          'VALDOSTA STATE UNIVERSITY']
        payload = {
            "SchoolList": SchoolList
        }
        AllSchoolBudgetList = requests.post('https://cwzopgcs8c.execute-api.us-east-1.amazonaws.com/prod/getschoolbudgets', data = json.dumps(payload)).json()
        return render_template('page3.html', schoolBudget = AllSchoolBudgetList, schools = SchoolList)

    else:
        SchoolList = request.form.getlist("school")
        numToAdd = 6 - len(SchoolList)
        payload = {
            "SchoolList": SchoolList
        }
        AllSchoolBudgetList = requests.post('https://cwzopgcs8c.execute-api.us-east-1.amazonaws.com/prod/getschoolbudgets', data = json.dumps(payload)).json()
        for x in range (0, numToAdd):
            #AllSchoolBudgetList.append([0,0,0,0,0,0,0])
            SchoolList.append('-')
        return render_template('page3.html', schoolBudget = AllSchoolBudgetList, schools = SchoolList)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        connection.close()

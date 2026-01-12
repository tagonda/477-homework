# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request
from .utils.database.database  import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
db = database()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/<page>')
def route(page):
	return render_template(page)

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data)

@app.route('/processfeedback', methods=['POST'])
def processfeedback():
	# Get form data
	feedback_data = request.form
	
	name = feedback_data.get('name')
	email = feedback_data.get('email')
	comment = feedback_data.get('comment')
	
	# Insert feedback into database
	db.insertRows(
		table='feedback',
		columns=['name', 'email', 'comment'],
		parameters=[[name, email, comment]]
	)
	
	# Fetch all feedback from database
	all_feedback = db.query("SELECT * FROM feedback ORDER BY comment_id DESC")
	
	# Render the feedback page
	return render_template('processfeedback.html', feedback=all_feedback)
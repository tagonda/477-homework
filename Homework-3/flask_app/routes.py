# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    """Decorator to require login for specific routes"""
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
    """Get the current user's email from session (decrypted) or return 'Unknown'"""
    if 'email' in session:
        # Decrypt the email from the session
        return db.reversibleEncrypt('decrypt', session['email'])
    return 'Unknown'

@app.route('/login')
def login():
    """Render the login page"""
    return render_template('login.html', user=getUser())

@app.route('/logout')
def logout():
    """Log out the user by removing email from session"""
    session.pop('email', default=None)
    return redirect('/')

@app.route('/processlogin', methods=["POST", "GET"])
def processlogin():
    """Process login credentials and authenticate user"""
    # Extract form fields from the request
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    
    # Get email and password from form
    email = form_fields.get('email', '')
    password = form_fields.get('password', '')
    
    # Authenticate the user using the database utility
    auth_result = db.authenticate(email, password)
    
    # Check if authentication was successful
    if auth_result:
        # Store encrypted email in session
        session['email'] = db.reversibleEncrypt('encrypt', email)
        return json.dumps({'success': 1})
    else:
        # Authentication failed
        return json.dumps({'success': 0})


#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
    """Render the chat page (requires login)"""
    return render_template('chat.html', user=getUser())

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Handle when a user joins the chat room"""
    join_room('main')
    user = getUser()
    
    # Determine message style based on user role
    if user == 'owner@email.com':
        style = 'width: 100%;color:blue;text-align: right'
    else:
        style = 'width: 100%;color:grey;text-align: left'
    
    # Broadcast to everyone in the room (including sender)
    emit('status', {'msg': user + ' has entered the room.', 'style': style}, room='main', broadcast=True)

@socketio.on('text', namespace='/chat')
def text(message):
    """Handle when a user sends a text message"""
    user = getUser()
    
    # Determine message style based on user role
    if user == 'owner@email.com':
        style = 'width: 100%;color:blue;text-align: right'
    else:
        style = 'width: 100%;color:grey;text-align: left'
    
    # Broadcast to everyone in the room (including sender)
    emit('message', {'msg': user + ': ' + message['msg'], 'style': style}, room='main', broadcast=True)

@socketio.on('left', namespace='/chat')
def left(message):
    """Handle when a user leaves the chat room"""
    user = getUser()
    
    # Determine message style based on user role
    if user == 'owner@email.com':
        style = 'width: 100%;color:blue;text-align: right'
    else:
        style = 'width: 100%;color:grey;text-align: left'
    
    # Broadcast to everyone in the room BEFORE leaving
    emit('status', {'msg': user + ' has left the room.', 'style': style}, room='main', broadcast=True)
    
    # Now leave the room
    leave_room('main')


#######################################################################################
# RESUME/FEEDBACK ROUTES
#######################################################################################

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


#######################################################################################
# OTHER ROUTES
#######################################################################################
@app.route('/')
def root():
    """Redirect root to home page"""
    return redirect('/home')

@app.route('/home')
def home():
    """Render the home page"""
    print(db.query('SELECT * FROM users'))
    fun_fact = "When I'm not coding, I love playing video games! Some of my favorites include the Mother series, the Persona series, the Animal Crossing series, and the Pokémon series."
    return render_template('home.html', user=getUser(), fun_fact=fun_fact)

@app.route('/projects')
def projects():
    """Render the projects page"""
    return render_template('projects.html', user=getUser())

@app.route('/piano')
def piano():
    """Render the piano page"""
    return render_template('piano.html', user=getUser())

@app.route("/static/<path:path>")
def static_dir(path):
    """Serve static files"""
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    """Add headers to prevent caching"""
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
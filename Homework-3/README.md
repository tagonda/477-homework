# Web Application Development: Homework 3




## Purpose

The purpose of this assignment is to provide hands-on experience with basic security, authentication and asyncryonous communication technologies for your web application, including:

1. Session management,
2. Password encryption and user authentication and,
3. Asynchronous communication technologies.



## Assignment Goals

Your high-level goal in this assignment is to extend your webpage from Homework 2 to include:

1. **An Authentication System**:  allowing user authentication, and restricted access to certain components of your application.
2. **A Chat System**: allowing you and a guest user of your web application to engage in a live text-based conversation. 

Your implementation should satisfy both the General Requirements, and Specific Requirements detailed in the sections below;  to help you grasp the overarching goal and requirements more concretely, [see the Homework overview video](https://youtu.be/NZzUMxTJKr4). Please note; your implementation does not have to look identical to the example solution. As long as you achieve the Specific and General requirement below, your assignment is complete.



## General Requirements

As a general requirement, we would like you to following good programming practice, this includes (but is not limited to):

* All code should be commented, organized, and thoughtfully structured.
* Don't mix `HTML`, `CSS`, and `Javascript` in single files.
* `Jinja` should be used to minimize redundancies in HTML.
* `SQL` tables should use forign keys when appropriate, and contain comments at both the row, and the table level.

Please see the General Requirements section of the [assignment rubric](documentation/rubric.md) for other elements of good programming practice that we'd like you you to pay attention to.



## Specific Requirements

For each of the three assignment goals listed above, we provide a section that outlines the specific requirements associated with that goal, below: 



#### 1. Authentication System Requirements 

For this portion of the assignment, you will generate the authentication system for your web application; this will involve two main tasks:  

1. **Extend the database utility to support sensitive data storage and authentication** by extending/completing the following code:

   * **`createUser(email, password, role)`**: Should create database entries for your users given an email, password and role (`guest`, or `owner`). The function should only add a user to the database if they do not already exists (i.e. if there is no matching email). The password of the user should be encrypted using [Scrypt](https://docs.python.org/3/library/hashlib.html) before being stored; you may use the `onewayEncrypt` function provided in the utility. The function should also return information about the success or failure of user creation.

   * **`authenticate(email, password)`**: Should check if a given email and encrypted password combination exist in the database. The function should  return information about the success or failure of the authentication.

2. **Enabling login and logout functionality for your application** by extending/completing the following code:

   * **`@app.route('/login')`**:  Should render the `login.html` template. The HTML template should contain two inputs that capture the email and password of the user, as well as a button that submits the credentials for authentication to `@app.route('/processlogin')`  using an asynchronous POST request via [AJAX](https://flask.palletsprojects.com/en/2.0.x/patterns/jquery/). If `@app.route('/processlogin')` indicates that the authentication was a failure this should be noted on the page; more specifically, your page must dynamically show how many times the authentication attempt has failed. If the authentication is a success, the user should be redirected to `/home`.

   * **`@app.route('/processlogin')`**:  Should be configured to process a POST request containing credentials for authentication. More sepcifically, the tool should extract the credentials from the request, and check if the user's email and password match a value in a the database using the `authenticate` method from the database utility. If the authentication is successful, the user's session should be updated to contain an encrypted version of their email; see below for an example:

   ```python
   session['email'] = db.reversibleEncrypt('encrypt', form_fields['email']) 
   ```

   The status of the authentication should be be returned as a JSON object to the AJAX handler in `login.html` for further action; see below for an example:

   ```
   return json.dumps(status)
   ```

   * **`@app.route('/logout')`**:  Should remove the `email` field from the session using [session.pop](https://pythonbasics.org/flask-sessions/) and redirect the user back to `/home`.

   * **`templates\shared\layout.html`**: The navigation bar should be updated to include a login/logout option. More specifically, when a user is logged in, they should see the option to logout; conversely, when a user is logged out, they should see the option to login.



#### 2. Chat System Requirements 

For this portion of the assignment, you will write code creates a live chat system in your web application. This will involve two tasks:  

1. **Complete the chat.html template** by adding HTML, CSS and JavaScript that allows users to see ongoing messages, enter their own messages, and leave the chat. The template already contains a functional implemention of `socket.io` for streaming messages in real time from the Client's interactions with `chat.html` to the `def joined(message)` in `routes.py`.  More specific requirements follow:

   * <u>Room Entry</u>: all users in the chat should see a message indicating when a given user "has entered the room"; this component was already completed for you. 
   * <u>Message Entry:</u> all users in the chat should see the messages entered by all other users.
   * <u>Room Derture:</u> all users in the chat should see the messages indicating when a user has "left the room". There should be a button on the page that allows the user to leave the chat.
   * <u>Message Styling:</u> all messages related to the site owner should be in blue and right justified; all other messages should be grey and left-justified.

2. **Add SocketIO processors in routes.py:** by writing any additonal  `@socketio.on(...)` decorated functions to `emit` data back to `chat.html`

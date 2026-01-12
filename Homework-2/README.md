# Web Application Development: Homework 2



## Purpose

The purpose of this assignment is to provide you with hands-on experience with backend development including:

1. [Python Flask](https://flask.palletsprojects.com/en/2.0.x/) - a backend for your web application.
2. [MySQL](https://www.mysql.com/) - a relational database to store and retrieve data for your application.
3. [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) - a tools for generating dynamic HTML content.



## Assignment Goals

Your high-level goal in this assignment is to extend your professional webpage from Homework 1 to include:

1. **A Database**:  allowing you to store persistent information used by your web application.
1. **A Resume page**: providing a HTML version of your Resume (rather than a .pdf). 
2. **A Feedback form**:  Allowing visitors to provide feedback anywhere on your web application.

Your implementation should satisfy both the General Requirements, and Specific Requirements detailed in the sections below. Please note; your implementation does not have to look identical to the example solution. As long as you achieve the Specific and General requirement below, your assignment is complete.



## General Requirements

As a general requirement, we would like you to follow good programming practice, this includes (but is not limited to):

* All code should be commented, organized, and thoughtfully structured.
* Don't mix `HTML`, `CSS`, and `Javascript` in single files.
* `SQL` tables should use foreign keys when appropriate, and contain comments at both the row, and the table level.

Please see the General Requirements section of the [assignment rubric](documentation/rubric.md) for other elements of good programming practice that we'd like you you to pay attention to.



## Specific Requirements

For each of the three assignment goals listed above, we provide a section that outlines the specific requirements associated with that goal, below: 



#### 1. Database requirements

For this portion of the assignment, you will specify a database that allows you to store information used by your web application. This will involve three tasks:  

1. **Specify several database tables** by adding `.sql` files to `database/create_tables` folder; more specifically you will create:

   * **`experiences.sql`**: contains the `CREATE TABLE` statement for the `experiences` table, which describes all the experiences you had at each position in the `positions` table ; the table should contain the following columns:

     * `experience_id`: the primary key, and unique identifier for each experience
     * `position_id`: a foreign key that references  `positions.position_id` 
     * `name`: the name of the experience.
     * `description`: a description of the experience.
     * `hyperlink`: a link where people can learn more about the experience.
     * `start_date`: the state date of the experience.
     * `end_date`: the end date of the experience.

   * **`skills.sql`**: contains the `CREATE TABLE` statement for the `skills` table, which describes all skills associated with each of the experiences in the `experiences` table ; the table should contain the following columns:

     * `skill_id`:  the primary key, and unique identifier for each skill
     * `experience_id`: a foreign key that references  `experiences.experience_id` 
     * `name`: the name of the skill
     * `skill_level`: the level of the skill; 1 being worst, 10 being best.

   * **`feedback.sql`**: contains the `CREATE TABLE` statement for the `feedback` table, which contains user feedback about your website; the table should contain the following columns:

     * `comment_id`: the primary key, and unique identifier for each comment.

     * `name`: the commentators name

     * `email`:  the commentators email

     * `comment`:  The text of the comment

       

2. **Specify the initial data that will populate your tables** by adding `.csv` files to `database/initial_data`; more specifically, you will create (or update):

   1. **`institutions.csv`**: contains data that will be ported into the `institutions` table on initialization of the app.

   2. **`positions.csv`**: contains data that will be ported into the `positions` table on initialization of the app.

   3. **`experiences.csv`**: contains data that will be ported into the `experiences` table on initialization of the app.

   4. **`skills.csv`**:  contains data that will be ported into the `skills` table on initialization of the app.

      

3. **Extend the [database utility](flask_app/utils/database/database.py)** by adding functions that create tables, insert data, and fetch resume data; more specifically, you will populate the following empty function in the database utility:

   1. **`createTables()`**: should create all tables in your database by executing each of the  `.sql` files in `database/create_tables`, and populating them with the initial data provided in `database/initial_data`. Note that `createTables()` is called in `__init__.py` and will therefore be executed upon creation of your application.

   2. **`insertRows()`**: should insert rows into a given table; more specifically, the function should take the table name, a list of column names, and a list of parameter lists (i.e. a list of lists) and execute the appropriate `INSERT` query.

   3. **`getResumeData()`**: should return a nested `dict` that hierarchically represents the complete data  contained in the `institutions`, `positions`, `experiences`, and `skills` tables. Tables should be nested according to their foreign key dependencies. Here's an example of what the the returned data should look like:

      ```json
      {1: {'address': 'NULL',
              'city': 'East Lansing',      
             'state': 'Michigan',
              'type': 'Academia',
               'zip': 'NULL',
        'department': 'Computer Science',
              'name': 'Michigan State University',
         'positions': {1: {'end_date'        : None,
                           'responsibilities': 'Teach classes; mostly NLP and Web design.',
                           'start_date'      : datetime.date(2020, 1, 1),
                           'title'           : 'Instructor',
                           'experiences': {1: {'description' : 'Taught an introductory course ... ',
                                                  'end_date' : None,
                                                 'hyperlink' : 'https://gitlab.msu.edu',
                                                      'name' : 'CSE 477',
                                                    'skills' : {},
                                                'start_date' : None
                                              },
                                           2: {'description' : 'introduction to NLP ...',
                                                  'end_date' : None,
                                                  'hyperlink': 'NULL',
                                                  'name'     : 'CSE 847',
                                                  'skills': {1: {'name'        : 'Javascript',
                                                                 'skill_level' : 7},
                                                             2: {'name'        : 'Python',
                                                                 'skill_level' : 10},
                                                             3: {'name'        : 'HTML',
                                                                 'skill_level' : 9},
                                                             4: {'name'        : 'CSS',
                                                                 'skill_level' : 5}},
                                                  'start_date': None
                                              }
                                          }
                          }
                      }
          }
      }
      ```

      

#### 2. Resume page requirements

For this portion of the assignment, you will write code that generates a dynamic HTML version of your Resume. This will involve two tasks:  

1. **Complete the `resume.html` template** by adding html and jinja statements that dynamically transform the data returned by `getResumeData()` into a dynamic, and <u>mobile friendly</u> resume page; more specifically, your resume page should:
   * <u>For each institution</u>, display:
     * `name` of the institution; this should be left justified.
     * location information for the institution (`department`,`address`, `city` etc.); this should be right justified. 
     * <u>For each affiliated position,</u> display:
       * `title`; this should be left justified
       * `start_date` and `end_date`; this should be right justified.
       * `responsibilities` of the position.
       * <u>For each affiliated experience,</u> display: 
         * `name` of the experience; this should be a hyperlink if the `hyperlink` field is not NULL.
         * `description` of the experience
         * <u>For each affiliated skill, display</u>:
           * `name` of the skill. 
2. **Be mindful of your styling**; while I have not specified specific constraints on the styling here, the content should:
* Look good on both mobile and desktop screens.
  
* Only display a field if it is not `"NULL"` or `None`
  
* Denote the hierarchical relationships in the source data using font-sizes, colors, bullets, etc.



#### 3. Feedback form requirements

For this portion of the assignment, you will generate a feedback form that allows users to send feedback on your site from anywhere in your web application; this will involve three  tasks:

1. **Add an html feedback form** to the `layout.html` template (along with any supporting CSS and JavaScript). The form should contain:

   *  `action` attribute that sends the data to the `/processfeedback` route in `routes.py`.
   *  `method`, and `enctype` attributes that specify a [POST request](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST).
   * The form should contain four `<input>` elements:
     * `name`: a text field that captures the name.
     * `email`: a text field that captures the email.
     * `comment`:  a text field that captures the comment.
     * `submit`: a button that submits the form.
   * The form should be styled such that:
     * the `position` of the form centers it in the screen, even as a user scrolls up or down.
     * the `display` of the form makes it initially invisible.

2. **Add a button that toggles the visibility of the feedback form** to the `layout.html` template. More specifically;

   * When the button is pressed the form should become visible.

   * The button to toggle the feedback form should show up on every page of your application and should always be visible.

3. **Process and store the feedback:**

   * In `routes.py`,  add a route and function to handle the feedback data submitted by the users. Within the route, access the submitted data via `request.form`. It should look something like this:

     ```python
     @app.route('/processfeedback', methods = ['POST'])
     def processfeedback():
     	feedback = request.form
     ```

   * within the `/processfeedback` route, add code that:

     * Inserts the form data into the `feedback` table within the database.

     * Extract all feedback from the `feedback` table
     * Render a template `processfeedback.html` that transform the feedback data into a dynamic, and <u>mobile friendly</u> feedback page; 

     

#### 4. OPTIONAL: Create a Favicon for your website

Visit [this website](https://favicon.io/logo-generator/) to quickly generate a favicon for your site. Add this line to your HTML head; note that the value of the `href` attribute should be the location of the favicon, which may differ from what I'm showing below.

```HTML
<link rel="shortcut icon" href="static/main/images/favicon.ico">
```

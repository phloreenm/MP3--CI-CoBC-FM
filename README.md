![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)




## ** ** 




# **The idea behind 'Restaurant Manager'**

The idea of developing this web application is a result of a discussion I had with a friend of mine, about his need to use a tool to organize the flow in the activity of his restaurant. We've sketched on paper some ideas and we concluded to a simple application, for the beginning, to see how it would work in real life. Basically the app should perform as a tool both for the employees in their daily duties, but also for the managers, which could verify daily reports of the events had place during the day.

Being a web application would allow any active employee to access it with just a smartphone, tablet or a laptop and proceed with his tasks. The access to the dashboard would be done though a login page. 

# **Features**
I designed three levels of Role-based Access Control:
- **System Administrator** or the 'admin' role:
  - Is the owner of the app providing the services to its clients (restaurant owners)
  - Has the right to CRUD:
    - New Restaurant managers in the users' list
- **Restaurant Manager** or 'manager' role:
  - Has the right to CRUD:
    - Restaurant's employees
    - Daily tasks
    - Hazards procedures
    - Create new forms
- **Employee** or 'user' role:
  - Has the right to:
    - Read:
      - Daily Tasks
      - Hazard Procedures
      - Submit/Fil Daily Tasks Predefined Forms

Obviously the application has the potential to be developed even further to match other business models or to incorporate even more capabilities, but in future releases.

# **Application feasibility**
'Restaurant Manager' is a tool designed to simplify and improve daily tasks, practical and user-friendly, that simplifies and streamlines daily tasks for restaurant managers and their employees. With its intuitive interface and useful features, it offers a feasible solution for managing specific aspects of a restaurant's operations, from employee task assignments to hazard procedures and daily reports management.


# **Needed to be installed**
- The ```env.py``` file is read using the ```dotenv``` library in Python. This library allows you to load environment variables from a file named .env located in the same directory as your Python script.
```pip install python-dotenv```

# ** Deployment **
To install all dependencies listed in the requirements.txt type in terminal: ```pip install -r requirements.txt```


# ** Code refactoring **
- In a future release of the project's code, I shall approach the object oriented paradigm to represent the database persistence in objects/classes. This way the necessary code will be less.+

---

Welcome USER_NAME,

This is the Code Institute student template for Gitpod. We have preinstalled all of the tools you need to get started. It's perfectly ok to use this template as the basis for your project submissions.

You can safely delete this README.md file, or change it for your own project. Please do read it at least once, though! It contains some important information about Gitpod and the extensions we use. Some of this information has been updated since the video content was created. The last update to this file was: **September 1, 2021**

## Gitpod Reminders

To run a frontend (HTML, CSS, Javascript only) application in Gitpod, in the terminal, type:

`python3 -m http.server`

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

To run a backend Python file, type `python3 app.py`, if your Python file is named `app.py` of course.

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

In Gitpod you have superuser security privileges by default. Therefore you do not need to use the `sudo` (superuser do) command in the bash terminal in any of the lessons.

To log into the Heroku toolbelt CLI:

1. Log in to your Heroku account and go to *Account Settings* in the menu under your avatar.
2. Scroll down to the *API Key* and click *Reveal*
3. Copy the key
4. In Gitpod, from the terminal, run `heroku_config`
5. Paste in your API key when asked

You can now use the `heroku` CLI program - try running `heroku apps` to confirm it works. This API key is unique and private to you so do not share it. If you accidentally make it public then you can create a new one with _Regenerate API Key_.

------

## **Credits**
- [Tilig's password generator](https://www.tilig.com/password-generator?network=g)
- [Materialize Library](https://materializecss.com/)
- [MongoDB Compass](https://www.mongodb.com/try/download/compass)
- [MongoDB Shell](https://www.mongodb.com/try/download/shell)
- [Materialize Register Page Sample](https://codepen.io/HaldunA/pen/eJxRPG)
- [Flask flash() method – How to Flash Messages in Flask?](https://www.askpython.com/python-modules/flask/flask-flash-method)
- [Used registration and login procedures from Code Institute Flask Mini Project](https://github.com/Code-Institute-Solutions/TaskManagerAuth/tree/main/02-UserAuthenticationAndAuthorization/04-login_functionality)
- [materialize CSS](https://materializecss.com/collections.html)
- [User access in Flask](https://blog.teclado.com/learn-python-defining-user-access-roles-in-flask/)
- [Hide Flash Flash messages](https://stackoverflow.com/questions/21993661/css-auto-hide-elements-after-5-seconds/21994053#21994053)
- [Favicon source](https://pngtree.com/element/down?id=NDE3MTMxNg==&type=1&time=1680618631&token=MjcwZjRjNzlkNmY5MjEzMzkwOGQyYWYzMjQzYTU5YWI=)
- [Remove unnecessary whitespace from Jinja rendered template](https://stackoverflow.com/questions/35775207/remove-unnecessary-whitespace-from-jinja-rendered-template)
- [Jinja Whitespace](https://python-web.teclado.com/section11/lectures/02_jinja_whitespace_control/)
- [Web Dev - Using Flask to Show Which Navbar Link is Active](https://www.youtube.com/watch?v=sIGPwvd-nTk)
### **Media**
- Cards:
  - [Employees icon: Restaurant Waiter Png vectors by Lovepik.com](https://lovepik.com/images/png-restaurant-waiter.html)
  - [Employees icon](https://www.publicdomainpictures.net/pictures/240000/nahled/restaurant-employee.jpg)
  - [Manager icon](https://cdn2.iconfinder.com/data/icons/business-finance-135/64/manager-1024.png)
  - [Administrator icon](https://icons.iconarchive.com/icons/aha-soft/free-large-boss/512/Admin-icon.png)
  - [Modal base code SOURCE](https://materializecss.com/modals.html#!)
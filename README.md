![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)




## ** ** 




# **The idea behind 'Restaurant Manager'**

The idea of developing this web application is a result of a discussion I had with a friend of mine, about his need to use a tool to organize the flow in the activity of his restaurant. We've sketched on paper some ideas and we concluded to a simple application, for the beginning, to see how it would work in real life. Basically the app should perform as a tool both for the employees in their daily duties, but also for the managers, which could verify daily reports of the events had place during the day.

Being a web application would allow any active employee to access it with just a smartphone, tablet or a laptop and proceed with his tasks. The access to the dashboard would be done though a login page. 

# **Features**
I designed three levels of Role-based Access Control:
- **System Administrator** or the 'admin' role:
  - Is the owner of the app providing the services to its clients (restaurant owners)
  - Has the right to C.R.U.D.:
    - Sys Admin in the users' list (can't delete himself, but only edit his details, except the username)
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



---

---

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
- [Get the values of the selected radio inputs in Flask](https://www.reddit.com/r/flask/comments/g5qwgw/how_can_i_get_the_value_of_the_selected_radio/)
### **Media**
- Cards:
  - [Employees icon: Restaurant Waiter Png vectors by Lovepik.com](https://lovepik.com/images/png-restaurant-waiter.html)
  - [Employees icon](https://www.publicdomainpictures.net/pictures/240000/nahled/restaurant-employee.jpg)
  - [Manager icon](https://cdn2.iconfinder.com/data/icons/business-finance-135/64/manager-1024.png)
  - [Administrator icon](https://icons.iconarchive.com/icons/aha-soft/free-large-boss/512/Admin-icon.png)
  - [Modal base code SOURCE](https://materializecss.com/modals.html#!)
### **Information**
- Cards:
  - [Food Standards Agency UK](https://www.food.gov.uk/)
  - [Temperature control: hot food](https://www.bromley.gov.uk/leaflet/261478/12/751/d#:~:text=When%20you%20are%20cooking%20food,it%20is%20overcooked%20or%20heated.)

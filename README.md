# API Webserver

## Football Statistics App

### Summary of Problem and Solution

This web application is designed to provide statistics and information about Australian Rules Football teams, players and results. This is solving the problem of tracking and storing data of sporting teams and their players. This data and information includes statistics for individual players, teams, the matches they play and the performances by players for each match. This is a problem as this data provides many insights to many different fields within the industry as well as third-party industries that rely on this information.

 for use by the following:

- Management of players within the sport. Management can track players performance based on average performance to gain insight into the value of the individual player. This can be used to determine a monetary value to pay a player.
- Recruitment can use these statistics to calculate whether a player is required within a team or undesired. Future prospects can be found by analysing statistics of players and determining whether that skill is required within a particular team.
- Medical and physio department gain can insight into the health of players and help to determine adequate training regeims for individual players.
- Gambling and other outcome based industries can use these statistics to produce bets and predict future outcomes for odds of games.
- The Australian Football League can use the results to formulate a ladder to rank the teams in order of Wins/Losses across the season in order to determine who is the best team.

Without tracking and relating these statistics, these insights into the information would be impossible to accurately analyse and produce performance and results outcomes for these relevant industries.

Users of the application will be able to log in and view all results and statistics of all teams, players and matches. Only Administrators can modify/manipulate data within the application.

### Database system

The database system to be implemented for this application will be PostgreSQL, which is an open-sourced relational database managment system. As it is open-sourced it is cost effective and easy to find information relating to the database model with an expansive libraries for functionality. PostgreSQL is ACID compliant which guarentees transactions with the database are valid and the data maintains integrity. This database management system works well with a relational database model which will be used to store the data in predefined structure called tables. This will allow definition of constraints to records to ensure validity of data as well as the ability to relate various tables with each other to analyse information efficiently. PostgreSQL will use Structured Query Language to interact and access the database through the use of queries which can accuratley and efficiently manipulate data in the desired manner.
PostgreSQL is a suitable choice as it supports many different features relating to performance, security and programming. The Object Relational Mapper SQLAlchemy can be used with PostgreSQL to validate and sanitise the data, Python language can be used to write the code for operation of the application.
PostgreSQL supports common datatypes such as numeric, boolean and Date/time types which will be used in the application as well as the ability to work well with JSON objects in storing relational data.

Drawbacks of PostgreSQL include the fact that it focuses on features relating to compatability over speed/performance. Comparible to other database management systems such as MySQL, PostgreSQL is slower and less efficient as the size of the Data increases as when querying a table is will start with the first row(record) of a table and make its way through. As PostgreSQL is open-sourced which allows it to be feature-rich, it does not come with a warranty or liability protection as it is not owned by any one company compared to propriety software which has full copyright control.

### Object Relational Mapping

*Functionality*- ORM or object relational mapper is used to interact with and application and database. This has the benefit of Queries to the databae being able to be written in the programming language of your choice, in this case Python, but can be any depending on your application. The ORM supports the conversion of objects in programming languages to compatible types for the use of storing the information in databases. This otherwise incompatible interaction is useful as it allows for efficient, repeatable and consistent manipulation of data without excess conversion code into the native language of the database, in this case SQL.

*Productivity* - To convert and store information in the database, structures called **models** are set up which define how the data is expected to be stored in the database. By setting up this structure the information being converted will be consistant, reliable and maintain integrity. As you only set up a model once, repeat code is avoided, validation of data is maintained and updates or corrections are easily maintainable. By not repeating yourself in code productivity is increased.

*Maintainability* - By using these models the underlying SQL code is guarenteed to be correct (once initialized correctly) which negates the need to have complete comprehension of the SQL language. This also allows you to change the underlying database without disruption as the outputing code is genereated by the ORM. Because these models use Object oriented models, you can extend and inherit from the classes which further reduces code and improves maintainability. This preperation and sanitising of the data also prevents SQL injection by not accepting direct code into the database.

*Design* - The use of models gives the application greater architecture by seperating concerns. Models can be stored in seperate files which again increases maintainability, readability and ease of development potential of the application.

One drawback of an ORM is that performance can be sacrificed. Although the code generated by the conversion of data is accurate, quite often it can be more complex than necessary which causes a slower performance. This is because ORMs are designed to cover a broad range of date-use scenarious and account for that through complex conversion.

### Entity Relation Diagram

![ERD](/docs/ERD.png)

### Database Relations

- **Users**: is an entity that that contains data relating to the users of the database. This table has attributes(columns) of User_id, Name, email, password and if a user is an administrator or not. It has a primary key of User_id and relates to no other tables as it is a seperate concern.
- **Players**: is an entity that contains data for all players in the database. This table has attributes(columns) of Player_id, Name, Age, Position, Height, Weight, Salary and Team. The primary key is the Player_id and contains Foreign key of Team. This is a Many(mandatory)-to-One(mandatory) relationship as One team has Many players. A player MUST relate to a team and a team MUST have multiple players. The Primary Key of Player_id is a Foreign Key in the Performances table and relates to this table in a One(mandatory)-to-Many(optional) relationship as One Player will have Many Performances. A Performance MUST relate to a player but a player may not have ANY performances.
- **Teams**: is an entity containing data relating to each team in the database. This table has attributes(columns) of Team_id, home ground, wins, losses and ladder position. It has a Primary Key of Team_id that is a foreign key in Scores as One(mandatory)-to-Many(mandatory) relationship as One team has many scores, a Score must be related to a team and a team must have a score for a Match.
- **Matches**: is an entity containing data relating to each match that is played. This table has attributes(columns) of Match_id, date, and location. The primary key of match_id is a foreign key in Scores and relates in a One(mandatory) to Many(mandatory) relationship as one Match must have and has multiple scores. This Primary Key is also a foreign key in Performances table in a One(mandatory) to many(mandatory) relationship as One match must have many performances.
- **Scores** is an entity containing the attribute score of One team in a match. It is a JOINING table between Teams and Matches as Teams have many matches and Matches have many teams. Scores has a primary key of Scores_id and contains Foreign keys of Team_id and Match_id.
- **Performances**: is an entity containing the data of One player in One Match. It is a JOINING table between Matches and Players as a Match has many performances from Many players. Performances has a Primary key of Performance_id and contains attributes of Goals,Behinds, Disposals and injuries. It also contains Foreign Keys of Match_id which it has a many-to-one relationship and Player_id which also has a Many to one relationship as previously described.

### Model relations

The model a class of SQLalchemy defines the table in the database with each attribute(column) datatype being defined as well as which values are nullable or allowed to be undefined. This also has statements which include which model and value to populate when referencing as well as action required when parent element is deleted.

The Schema , a class of Marshmallow, defines how to load/unload incoming data from requests. Each attribute that is to be loaded when the Schema is referenced is defined here. Nested Schemas are defined here as well to define how they are returned.

- **Users**: The User model defines the attributes as the following
  
```py
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
```

The User model has no relations to any other models.

The User Schema loads/unloads the following attributes when accepting data from a request

```py
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin')
        ordered = True
```


- **Players**: The Player model defines the attributes as the following.
  
```py
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height_cm = db.Column(db.Integer, nullable=False)
    weight_kg = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String, nullable=False)
    salary_per_year = db.Column(db.Integer, nullable=False)
```

As Player_id is a foreign key in Performances and the relationship is stated in the model. The value of performances states the relationship to the **Performance** model and back populates the **performance** value from the corresponding table. In this case delete all records associated.

```py
performances = db.relationship('Performance', back_populates='player', cascade= 'all, delete')
```

As the Team_id attribute in is a Foreign_key in the Player model it is stated here. The value of **team** states to reference the Team model and populate the players value in the associated table when referenced.

```py
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id') , nullable=False)
    team = db.relationship('Team', back_populates='players')
```

The following attributes are loaded when the PlayerSchema is referenced.

```py
class Meta:
    fields = ('id', 'name', 'age', 'height_cm', 'weight_kg', 'position', 'salary_per_year', 'team', 'team_id')
    ordered = True
```

As team is a nested list of fields related to the team Schema it is defined here which elements to load when PlayerSchema is called.

```py
team = fields.Nested('TeamSchema', only=['id', 'name'])
```

- **Teams**: The Team model defines the attributes as the following.
  
```py
id = db.Column(db.Integer, primary_key=True)
name = db.Column(db.String, nullable=False)
home_ground = db.Column(db.String, nullable=False)
wins = db.Column(db.Integer, nullable=False)
losses = db.Column(db.Integer, nullable=False)
ladder_position = db.Column(db.String, nullable=False)
```

As Team_id is a foreign key in Players and Scores the relationship is stated in the model. the value of players states the relationship to the **Player** model and back populates the **team** value from the corresponding table. In this case delete all records associated. The same relationship is defined for **scores**.

```py
players = db.relationship('Player', back_populates='team', cascade= 'all, delete')
scores = db.relationship('Score', back_populates='team', cascade= 'all, delete')

```

The following attributes are loaded when the TeamSchema is referenced.

```py
class Meta:
    fields = ('id', 'name', 'home_ground', 'wins', 'losses', 'ladder_position' ,'players')
    ordered = True
```

As players is a nested list of players related to the team, elements of the Player Schema are nested within the TeamSchema when called.

```py
players = fields.List(fields.Nested('PlayerSchema', only=['name', 'id', 'position']))
```

- **Performances**: The Performance model defines its attributes as the following:

```py
    id = db.Column(db.Integer, primary_key=True)
    goals = db.Column(db.Integer, nullable=False)
    behinds = db.Column(db.Integer, nullable=False)
    disposals = db.Column(db.Integer, nullable=False)
    injuries = db.Column(db.String, nullable=True)
```

The attributes of **player_id** and **match_id** are foreign keys from Player and Match models respectively. The relationship is defined that the value of **player** and **match** represent the Player and Match models and populate the performance value in the correspondng tables. These relationships are defined as following:

```py
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    player = db.relationship('Player', back_populates='performances')
    match = db.relationship('Match', back_populates='performances')

```

The Performance Schema contains nested fields of **player** and **match** which loads the corresponding attributes of the Schemas when Performance Schema is loaded. The Performance Schema has the following attributes loaded.

```py
    class Meta:
        fields= ('id', 'player', 'match', 'goals', 'behinds', 'disposals', 'injuries','player_id','match_id')
        ordered = True
```

- **Matches**: The Match model defines its attribute as the following:

```py
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    location = db.Column(db.String, nullable=False)
```

The Match_id primary key is a foreign Key in Scores and Performances models and so the relationship is defined in the model. the value of scores identifies the relationship to the Score model and populates the match data when called, upon deletion of the parent table the child records are also deleted. The same applies to the performances relationship.

```py
    scores = db.relationship('Score', back_populates='match', cascade= 'all, delete')
    performances = db.relationship('Performance', back_populates='match', cascade= 'all, delete')
```

The Match Schema has a nested attribute of **scores** which loads attributes of the Score Schema in when the Match Schema is loaded.

```py
    scores = fields.List(fields.Nested('ScoreSchema', exclude=['match']))
    class Meta:
        fields = ('id', 'date', 'location' ,'scores')
```

- **Scores**: The Score model defines its attribute as the following:

```py
id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)

```

The attributes of **team_id** and **match_id** are foreign keys from the corresponding tables and are defined here.

```py
    team = db.relationship('Team', back_populates='scores')
    match = db.relationship('Match', back_populates='scores')
```

The Score Schema contains attributes of team and match which are nested fields of the corresponding Schemas. The attribute loaded when the schema is called are the following.

```py
class Meta:
        fields= ('id', 'score', 'team', 'match', 'team_id', 'match_id')
        ordered = True
```

### Project Management

This project is managed by the use of Agile Methodology. This involves the use of constant iteration over functionality of the application ensuring quality and performance requirements are met. This methodology encourages working software over comprehensive documentation and responding to change over following a rigid plan.

To implement this Agile method this project will use the tool Kanban Boards. Kandban boards are designed to maximise efficiency of workflow by providing a visual framework to assist is reaching project goals. Each project requirement and step is broken down into seperate *Tickets* to indentify which goals need to be completed. These Tickets represent a **User Story**  or requirement to be met, they are given priority statuses to see which ones are more important than the others and which ones will take more time than others. Dates of completion are added to Tickets to guarentee timing requirements are being met and work flow is accomplished.

Tickets are arranged into **columns** which represent the workflow of the project and give a simple visual order to tasks to be completed. Tickets in these columns are marked To-Do, In-Progress or Completed.

The Kandban boards will be used throughout the life-cycle of the project as it can be reprioritised, reassigned and updated as needed which makes it more flexible.

For keeping track of updates and version control to the project a Github repository is used. This allows for commiting of current versions and retraceablity to previous versions if needed. 

### KanBan Board and Rrepository

https://trello.com/b/hbSCNNPr/football-api

https://github.com/code-ry/football_API

### Third Party Services

- **Marshmallow**: is an ORM framework librarys that converts complex datatypes such as objects to and from Python datatypes. This is used in the API to convert incoming request data into usable and consistant data types to be used to access and manipulate the database. In this project we use the Schemas that Marshmallow creates to convert the data into desired structure when accepting incoming data.

- **SQLAlchemy**: is and ORM and database toolkit written in the python language. It provides an interface to generate and execute database code without having to write the SQL code manually. This has the benefit of having realiable, consistant and maintainable code in the program as the code is generated and guarenteed to be accurate. SQLAlchemy provides methods for use of all CRUD operations that can be written in python code and outputs SQL queries.

- **Bcrypt**: is a password-hashing function that is used to enrypt the user inputs of passwords into a hexidecimal string to be stored in the database. As the Hash is one way it cannot be easily decrypted and provides security to the application.

- **JWT**: JSON web tokens are used in this application to provide security and a method to authenticate users of the platform. Authentication verifies the credentials of a user and issues a token to be used by the user while accessing information. The token consists of a Header, Payload and Signiture which outsputs a stringnthat can be passed to authenticate a user. Whenever a User wishes to access information through the API the token can be checked for validity.

### API Endpoint Documentation

#### Authentication Endpoints

**Error returns**

- When an expected body is received empty or wrong format
A 400 error code is returned with the required message in JSON format
- When a user fail to provide valid username/password
A 401 error code is returned with the required message in JSON format
- When a URL was not found on server
A 404 error code is returned with the required message in JSON format
- When a value is entered outside of range or invalid.
A 400 error code is returned with the required message in JSON format
- When a required field is not present.
A Key error occurs and 400 code returned with the required message in JSON format
- When an invalid input has been entered into a field.
A Validation Error occurs and 400 code returned with the required message in JSON format

**auth/register/**

- Methods: POST
- Arguments: None
- Description: Validates and adds a User to the database.
- Authentication : None
- Authorization : None
- Request Body:
  
```py
{
    "name": "John Doe",
    "email": "john.doe@gmail.com",
    "password": "aA123456#"
}
```

- Response Body:
  
```py
{
    "id": 4,
    "name": "John Doe",
    "email": "john.doe@gmail.com",
    "is_admin": false
}
```

**auth/login/**

- Methods: POST
- Arguments: None
- Description: Verifies a valid user using email and password, returns a token
- Authentication : None
- Authorization : None
- Request Body:
  
```py
{
    "email": "john.doe@gmail.com",
    "password": "aA123456#"
}
```

- Response Body:
  
```py
{
    "email": "john.doe@gmail.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODIzNTg4MiwianRpIjoiOGI2MDNhNGMtOTY0Ni00MTQ1LThjOWItZTg0YWJjMjc4ZjE0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQiLCJuYmYiOjE2NjgyMzU4ODIsImV4cCI6MTY2ODMyMjI4Mn0.IA9KdDEbXiGtJs3_mVW8XneiMdQB_CwB0lL1DiiKEAc",
    "is_admin": false
}
```

#### User Endpoints

**users/**

- Methods: GET
- Arguments: None
- Description: Returns a list of all users
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
None

- Response Body:
  
```py
[
    {
        "id": 1,
        "name": "Ryan Bussey",
        "email": "admin@football.com",
        "is_admin": true
    },
    {
        "id": 2,
        "name": "Joe Blow",
        "email": "joeblow@gmail.com",
        "is_admin": false
    }
]
```

**users/<int:id>/**

- Methods: GET
- Arguments: Integer (representing user_id)
- Description: Returns a single users data
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
None

- Response Body:
  
```py
{
    "id": 2,
    "name": "Joe Blow",
    "email": "joeblow@optus.com",
    "is_admin": false
}
```

**users/<int:id>/**

- Methods: PUT/PATCH
- Arguments: Integer (representing user_id)
- Description: Modifies the data of the specified user in the argument
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
```py
{
    "email": "blob@optus.com",
    "name": "Ryano",
    "is_admin": true
}
```

- Response Body:
  
```py
{
    "id": 2,
    "name": "Ryano",
    "email": "blob@optus.com",
    "is_admin": true
}
```

**users/<int:id>/**

- Methods: DELETE
- Arguments: Integer (representing user_id)
- Description: Deletes the specified user in the argument
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
None

- Response Body:
  
```py
{
    "message": "User Ryano deleted successfully"
}
```

#### Player Endpoints

**players/**

- Methods: GET
- Arguments: None
- Description: Returns a list of all players
- Authentication : bearer token in Authorization header
- Authorization : None
- Request Body:
  
None

- Response Body:

```py 
[
    {
        "id": 2,
        "name": "Andy Brayshaw",
        "age": 26,
        "height_cm": 160,
        "weight_kg": 63,
        "position": "Midfield",
        "salary_per_year": 200000,
        "team": {
            "id": 1,
            "name": "Fremantle Dockers"
        }
    },
    {
        "id": 5,
        "name": "Gary Ablett",
        "age": 25,
        "height_cm": 160,
        "weight_kg": 75,
        "position": "Half-Back",
        "salary_per_year": 400000,
        "team": {
            "id": 3,
            "name": "Geelong Cats"
        }
    },

...


]
```

**players/<int:id>/**

- Methods: GET
- Arguments: Integer (representing player_id)
- Description: Returns a single players data
- Authentication : bearer token in Authorization header
- Authorization : None
- Request Body:
  
None

- Response Body:
  
```py
{
    "id": 2,
    "name": "Andy Brayshaw",
    "age": 26,
    "height_cm": 160,
    "weight_kg": 63,
    "position": "Midfield",
    "salary_per_year": 200000,
    "team": {
        "id": 1,
        "name": "Fremantle Dockers"
    },
    "team_id": 1
}
```

**players/<int:id>/performances/**

- Methods: GET
- Arguments: Integer (representing player_id)
- Description: Returns a list of all single players' performances
- Authentication : bearer token in Authorization header
- Authorization : None
- Request Body:
  
None

- Response Body:
  
```py
[
    {
        "player": {
            "name": "Nat Fyfe",
            "id": 1
        },
        "match": {
            "location": "Fremantle Oval",
            "id": 1,
            "date": "2022-01-01"
        },
        "goals": 6,
        "behinds": 5,
        "disposals": 25,
        "injuries": "Broken Shoulder"
    },
    {
        "player": {
            "name": "Nat Fyfe",
            "id": 1
        },
        "match": {
            "location": "Subiaco Oval",
            "id": 2,
            "date": "2022-06-05"
        },
        "goals": 5,
        "behinds": 7,
        "disposals": 30,
        "injuries": null
    },
    {
        "player": {
            "name": "Nat Fyfe",
            "id": 1
        },
        "match": {
            "location": "The Cattery, GMHBA Stadium",
            "id": 3,
            "date": "2022-08-01"
        },
        "goals": 1,
        "behinds": 2,
        "disposals": 4,
        "injuries": null
    }
]
```

**players/<int:id>/**

- Methods: PUT/PATCH
- Arguments: Integer (representing player_id)
- Description: Modifies the data of the specified player in the argument
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
```py
{
    "age": 28,
    "height_cm": 180
}
```

- Response Body:
  
```py
{
    "id": 2,
    "name": "Andy Brayshaw",
    "age": 28,
    "height_cm": 180,
    "weight_kg": 63,
    "position": "Midfield",
    "salary_per_year": 200000,
    "team": {
        "id": 1,
        "name": "Fremantle Dockers"
    },
    "team_id": 1
}
```

**player/<int:id>/'**

- Methods: DELETE
- Arguments: Integer (representing player_id)
- Description: Deletes the specified player in the argument
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
None

- Response Body:
  
```py
{
    "message": "Player Andy Brayshaw deleted successfully"
}
```

#### Team Endpoints

**teams/**

- Methods: GET
- Arguments: None
- Description: Returns a list of all teams
- Authentication : bearer token in Authorization header
- Authorization : None
- Request Body:
  
None

- Response Body:

```py
[
    {
        "id": 1,
        "name": "Fremantle Dockers",
        "home_ground": "Fremantle Oval",
        "wins": 2,
        "losses": 0,
        "ladder_position": "1st",
        "players": [
            {
                "name": "Nat Fyfe",
                "id": 1,
                "position": "Midfield"
            },
            {
                "name": "Andy Brayshaw",
                "id": 2,
                "position": "Midfield"
            }
        ]
    },
    {
        "id": 3,
        "name": "Geelong Cats",
        "home_ground": "The Cattery, GMHBA Stadium",
        "wins": 1,
        "losses": 1,
        "ladder_position": "2nd",
        "players": [
            {
                "name": "Gary Ablett",
                "id": 5,
                "position": "Half-Back"
            },
            {
                "name": "Tom Hawkins",
                "id": 6,
                "position": "Full-Forward"
            }
        ]
    },

...


]

```

**teams/<int:id>/**

- Methods: GET
- Arguments: Integer (representing team_id)
- Description: Returns a single teams data
- Authentication : bearer token in Authorization header
- Authorization : None
- Request Body:
  
None

- Response Body:
  
```py
{
    "id": 1,
    "name": "Fremantle Dockers",
    "home_ground": "Fremantle Oval",
    "wins": 2,
    "losses": 0,
    "ladder_position": "1st",
    "players": [
        {
            "name": "Nat Fyfe",
            "id": 1,
            "position": "Midfield"
        },
        {
            "name": "Andy Brayshaw",
            "id": 2,
            "position": "Midfield"
        }
    ]
}
```

**teams/<int:id>/'**

- Methods: PUT/PATCH
- Arguments: Integer (representing team_id)
- Description: Modifies the data of the specified team in the argument
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
```py
{
    "home_ground": "Fremantle Oval",
    "wins": 4,
    "losses": 2
}
```

- Response Body:
  
```py
{
    "id": 1,
    "name": "Fremantle Dockers",
    "home_ground": "Fremantle Oval",
    "wins": 4,
    "losses": 2,
    "ladder_position": "1st",
    "players": [
        {
            "name": "Nat Fyfe",
            "id": 1,
            "position": "Midfield"
        },
        {
            "name": "Andy Brayshaw",
            "id": 2,
            "position": "Midfield"
        }
    ]
}
```

**teams/<int:id>/'**

- Methods: DELETE
- Arguments: Integer (representing team_id)
- Description: Deletes the specified team in the argument
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
None

- Response Body:
  
```py
{
    "message": "team Fremantle Dockers deleted successfully"
}
```

#### Performances Endpoints

**performances/**

- Methods: GET
- Arguments: None
- Description: Returns a list of all performances
- Authentication : bearer token in Authorization header
- Authorization : None
- Request Body:
  
None

- Response Body:

```py
[
    {
        "player": {
            "name": "Josh Kennedy",
            "id": 4
        },
        "match": {
            "date": "2022-04-15",
            "id": 4,
            "location": "The Cattery, GMHBA Stadium"
        },
        "goals": 6,
        "behinds": 5,
        "disposals": 25,
        "injuries": "Torn Hamstring"
    },
    {
        "player": {
            "name": "Gary Ablett",
            "id": 5
        },
        "match": {
            "date": "2022-08-01",
            "id": 3,
            "location": "The Cattery, GMHBA Stadium"
        },
        "goals": 5,
        "behinds": 7,
        "disposals": 30,
        "injuries": null
    }

...


]

```

**performances/<int:id>/**

- Methods: GET
- Arguments: Integer (representing performance_id)
- Description: Returns a single performance data
- Authentication : bearer token in Authorization header
- Authorization : None
- Request Body:
  
None

- Response Body:
  
```py
{
    "player": {
        "name": "Gary Ablett",
        "id": 5
    },
    "match": {
        "date": "2022-08-01",
        "id": 3,
        "location": "The Cattery, GMHBA Stadium"
    },
    "goals": 5,
    "behinds": 7,
    "disposals": 30,
    "injuries": null
}
```

**performances/<int:id>/'**

- Methods: PUT/PATCH
- Arguments: Integer (representing performance_id)
- Description: Modifies the data of the specified performance in the argument
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
```py
{
    "behinds": 12,
    "disposals": 50,
}
```

- Response Body:
  
```py
{
    "player": {
        "name": "Gary Ablett",
        "id": 5
    },
    "match": {
        "date": "2022-08-01",
        "id": 3,
        "location": "The Cattery, GMHBA Stadium"
    },
    "goals": 5,
    "behinds": 12,
    "disposals": 50,
    "injuries": null
}
```

**performances/<int:id>/'**

- Methods: DELETE
- Arguments: Integer (representing performance_id)
- Description: Deletes the specified performance in the argument
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
None

- Response Body:
  
```py
{
    "message": "performance 5 deleted successfully"
}
```

#### Matches Endpoints

**matches/**

- Methods: GET
- Arguments: None
- Description: Returns a list of all matches
- Authentication : bearer token in Authorization header
- Authorization : None
- Request Body:
  
None

- Response Body:

```py
[
    {
        "location": "The Cattery, GMHBA Stadium",
        "date": "2022-08-01",
        "scores": [
            {
                "id": 5,
                "score": 96,
                "team": {
                    "name": "Fremantle Dockers",
                    "id": 1
                }
            },
            {
                "id": 6,
                "score": 95,
                "team": {
                    "name": "Geelong Cats",
                    "id": 3
                }
            }
        ],
        "id": 3
    },
    {
        "location": "Subiaco Oval",
        "date": "2022-06-05",
        "scores": [
            {
                "id": 3,
                "score": 106,
                "team": {
                    "name": "Fremantle Dockers",
                    "id": 1
                }
            },
            {
                "id": 4,
                "score": 18,
                "team": {
                    "name": "West Coast Eagles",
                    "id": 2
                }
            }
        ],
        "id": 2
    },


...


]

```

**matches/<int:id>/**

- Methods: GET
- Arguments: Integer (representing match_id)
- Description: Returns a single match data
- Authentication : bearer token in Authorization header
- Authorization : None
- Request Body:
  
None

- Response Body:
  
```py
{
    "location": "Fremantle Oval",
    "date": "2022-01-01",
    "scores": [
        {
            "id": 1,
            "score": 63,
            "team": {
                "name": "Fremantle Dockers",
                "id": 1
            }
        },
        {
            "id": 2,
            "score": 26,
            "team": {
                "name": "West Coast Eagles",
                "id": 2
            }
        }
    ],
    "id": 1
}
```

**matchs/<int:id>/'**

- Methods: PUT/PATCH
- Arguments: Integer (representing match_id)
- Description: Modifies the data of the specified match in the argument
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
```py
{
    "location": "The Cattery GMHBA Stadium",
    "date": "22/12/2022"
}
```

- Response Body:
  
```py
{
    "location": "The Cattery GMHBA Stadium",
    "date": "2022-12-22",
    "scores": [
        {
            "id": 1,
            "score": 63,
            "team": {
                "name": "Fremantle Dockers",
                "id": 1
            }
        },
        {
            "id": 2,
            "score": 26,
            "team": {
                "name": "West Coast Eagles",
                "id": 2
            }
        }
    ],
    "id": 1
}
```

**matches/<int:id>/'**

- Methods: DELETE
- Arguments: Integer (representing match_id)
- Description: Deletes the specified match in the argument
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
None

- Response Body:
  
```py
{
    "message": "match 2 deleted successfully"
}
```

**matches/<int:id>/performances/**

- Methods: GET
- Arguments: Integer (representing player_id)
- Description: Returns a list of all single match performances
- Authentication : bearer token in Authorization header
- Authorization : None
- Request Body:
  
None

- Response Body:
  
```py
[
    {
        "id": 3,
        "player": {
            "name": "Nat Fyfe",
            "id": 1
        },
        "match": {
            "date": "2022-08-01",
            "location": "The Cattery, GMHBA Stadium",
            "id": 3
        },
        "goals": 1,
        "behinds": 2,
        "disposals": 4,
        "injuries": null
    },
    {
        "id": 6,
        "player": {
            "name": "Gary Ablett",
            "id": 5
        },
        "match": {
            "date": "2022-08-01",
            "location": "The Cattery, GMHBA Stadium",
            "id": 3
        },
        "goals": 5,
        "behinds": 7,
        "disposals": 30,
        "injuries": null
    }
]
```

#### Score Endpoints

**scores/**

- Methods: GET
- Arguments: None
- Description: Returns a list of all scores
- Authentication : bearer token in Authorization header
- Authorization : None
- Request Body:
  
None

- Response Body:

```py
[
    {
        "id": 5,
        "score": 96,
        "team": {
            "name": "Fremantle Dockers",
            "id": 1
        },
        "match": {
            "id": 3,
            "date": "2022-08-01",
            "location": "The Cattery, GMHBA Stadium"
        }
    },
    {
        "id": 6,
        "score": 95,
        "team": {
            "name": "Geelong Cats",
            "id": 3
        },
        "match": {
            "id": 3,
            "date": "2022-08-01",
            "location": "The Cattery, GMHBA Stadium"
        }
    },

...


]

```

**score/<int:id>/**

- Methods: GET
- Arguments: Integer (representing score_id)
- Description: Returns a single score data
- Authentication : bearer token in Authorization header
- Authorization : None
- Request Body:
  
None

- Response Body:
  
```py
{
    "id": 6,
    "score": 95,
    "team": {
        "name": "Geelong Cats",
        "id": 3
    },
    "match": {
        "id": 3,
        "date": "2022-08-01",
        "location": "The Cattery, GMHBA Stadium"
    }
}
```

**performances/<int:id>/'**

- Methods: PUT/PATCH
- Arguments: Integer (representing score_id)
- Description: Modifies the data of the specified performance in the argument
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
```py
{
    "score": 95
}
```

- Response Body:
  
```py
{
    "id": 6,
    "score": 117,
    "team": {
        "name": "Geelong Cats",
        "id": 3
    },
    "match": {
        "id": 3,
        "date": "2022-08-01",
        "location": "The Cattery, GMHBA Stadium"
    }
}
```

**scores/<int:id>/'**

- Methods: DELETE
- Arguments: Integer (representing score_id)
- Description: Deletes the specified score in the argument
- Authentication : bearer token in Authorization header
- Authorization : is_admin: True
- Request Body:
  
None

- Response Body:
  
```py
{
    "message": "score 8 deleted successfully"
}
```

# API Webserver

## Football Statistics App

### Summary

This web application is designed to provide statistics and information about Australian Rules Football teams, players and results. This is solving the problem of tracking performance of sporting teams and their players for use by the following:

- Management of players within the sport. Management can track players performance based on average performance to gain insight into the value of the individual player. This can be used to determine a monetary value to pay a player.
- Recruitment can use these statistics to calculate whether a player is required within a team or undesired. Future prospects can be found by analysing statistics of players and determining whether that skill is required within a particular team.
- Medical and physio department gain can insight into the health of players and help to determine adequate training regeims for individual players.
- Gambling and other outcome based industries can use these statistics to produce bets and predict future outcomes for odds of games.
- The Australian Football League can use the results to formulate a ladder to rank the teams in order of Wins/Losses across the season in order to determine who is the best team.

Without tracking and relating these statistics, these insights into the information would be impossible to accurately analyse and produce performance and results outcomes for these relevant industries.

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

The entity of Player will contain records of data relating to players Name, Age, playing position and Team they play for. The attribute of Team in Player will be a Foreign Key to the entity of Team. The Entity of Player is related to the entity of Team in a one(Mandatory)-to-many(Mandatory) relationship as 1 Team has many players, but a player can only have one team but must belong to one.

The entity of Performance stores data about the performance of a certain player in a certain Match by recording the amount of goals, behinds and disposals. It contains Foreign Keys relating to the Player ID and Match ID to relate the tables of each. Performance is a Many(Mandatory) to One(Mandatory) relationship with Player as a player can have multiple performances but must play in the match to have a performance. Performance is related to Match in a One-to-Many relationship and a Match has multiple performances but The Performance must only relate to One Player and One Match.

The entity of Team contains the data of each Team Name, Location, Total Wins and Ladder position. Team is related to Match in a one to many relationship as one team can have many matches but a match refers to 2 **unique** teams.

The entity of Match contains data of individual Matches Date, Teams playing (identified through foreign their foreign keys, and their relevant scores for that match. Match is related to Team as many to one as one team can have multiple matches but only 2 unique teams per match. Match is related to Performance one(mandatory)-to-many(mandatory) as one match must have multiple performances and performances must be related to at least one match.

### Project Management

This project is managed by the use of Agile Methodology. This involves the use of constant iteration over functionality of the application ensuring quality and performance requirements are met. This methodology encourages working software over comprehensive documentation and responding to change over following a rigid plan.

To implement this Agile method this project will use the tool Kanban Boards. Kandban boards are designed to maximise efficiency of workflow by providing a visual framework to assist is reaching project goals. Each project requirement and step is broken down into seperate *Tickets* to indentify which goals need to be completed. These Tickets represent a **User Story**  or requirement to be met, they are given priority statuses to see which ones are more important than the others and which ones will take more time than others. Dates of completion are added to Tickets to guarentee timing requirements are being met and work flow is accomplished.

Tickets are arranged into **columns** which represent the workflow of the project and give a simple visual order to tasks to be completed. Tickets in these columns are marked To-Do, In-Progress or Completed.

The Kandban boards will be used throughout the life-cycle of the project as it can be reprioritised, reassigned and updated as needed which makes it more flexible.

### KanBan Board

https://trello.com/b/hbSCNNPr/football-api

### API Endpoint Documentation

### Model relations

### Third Party Services
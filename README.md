# flask_project

Insert sample data into the "users" table. 

INSERT INTO user (name, email, role) VALUES ('Sona', 'sonal@gmail.com', 'tester');


Retrieve all users from the "users" table. 

SELECT * FROM `user`;


Retrieve a specific user by their ID

SELECT * FROM `user` WHERE id='1';



Retrieve a specific user by their Role

SELECT * FROM `user` WHERE role = 'developer';

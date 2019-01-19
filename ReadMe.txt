-----SECURED INSTANT POINT TO POINT MESSAGING APPLICATION
-----THIS APPLICATION IS FOR TWO USERS NAMELY ALICE AND BOB
-----OUR MESSAGING APPLICATION USES PYTHON AND REDIS

-----Required Tools:
1. Python3.x
2. Redis2.4.6

----To download and install redis
1. Dowload Redis2.4.6 from https://github.com/rgl/redis/downloads
2. Navigate to the folder where redis was downloaded
3. Double click the "redis-server". This will start the redis service in the backend.

-----To install python packages 
Packages in Python:
during program execution, If prompted for the below packages, install them using below command in command prompt by navigating to the python program folder

	pip install <package-name>

1. flask
2. flask_socketio 
3. redis
4. random
5. string
6. json
7. SimpleCache
8. chillkat: This package is included with the project folder. To install this package type following command in the command prompt within python program folder
	
	python installChilkat.py


-----To execute the Application
1. Navigate to the folder where python.exe is available and place the project contents.
2. Open command promt. 
3. Navigate to the python program folder.
4. Execute the following command to run the application

	python main.py

5. The promt will give you the hostname and port number to open the application in browser

	127.0.0.1:5000

6. To open Alice login paste the following in the web browser

	127.0.0.1:5000\AliceLoginPage

7. To open Bob login paste the following in the web browser

	127.0.0.1:5000\BobLoginPage

8. Enter the user credentials as specified below to login

	Alice credentials: User name: alice
		            password: cs@5173
	Bob credentials:  User name: bob
		           password: cs@5173

9. Chat box for users will be opened in the respective browser.
10. Type message in the Alice chat box and hit send button.
11. Go to Bob browser page, you willl see the message received in Bob chat box.
12. You can also upload image from any of the user and hit send so that it can be received by other user.
13. Logout of the application for both user when required.
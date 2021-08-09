# sqlite_injection_lab :syringe: :syringe:

This is the sqlite blind injection lab for beginners.

![alt text](https://i.imgur.com/zYWptdn.png)

This lab is ctf style lab. You can submmit the flag you get from challenges. There are only 6 challenges and only boolean based blind injection challenges. 

![alt_text](https://i.imgur.com/af9aTm5.png)

Sorry for too many css files as I am training my front-end skill but I am still too bad in it :neutral_face: :neutral_face: .

You can reset the database. And if you don't like the default flag, you can customize the flag.
Please do not store any important data into challenge database. It will be deleted when you reset the database.

![alt_text](https://i.imgur.com/L2ttqgS.png)

Hope you enjoy the lab :cowboy_hat_face: :cowboy_hat_face: .

Feel free to dm me at [DISCORD](https://discord.com/users/604681695064490015) if you have trouble in solving challenges. Your feedback are welcome.

# Requirements
Flask
`pip intall Flask`

sqlite3
`pip install pysqlite3`

# Set-up

It is recommanded to run the lab in virtual environment.

`pip3 install virtualenv`

`cd YOUR_LAB_DIR`

`python3 -m venv venv`


On windows: `set FLASK_APP=app.py` then `flask run` or `flask run --host=0.0.0.0 -p YOUR_PORT`

On linux: `export FLASK_APP=app.py` then `flask run` or `flask run --host=0.0.0.0 -p YOUR_PORT`

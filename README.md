# Password Manager Online

## Instructions
### MAIN.PY 
Open the file main.py and toggle the comment of the line 6.
The fuction _generate_key()_ will print a new personal secret key (**copy only what is between the quotes**. Ex: b'___secretkey___' ).
That key is crucial for the password manager. Once lost is impossible to recover the data encrypted.
After getting the key you can toggle the comment line again or simply delete the line.

### FUNCTIONS.PY
After creating an account and a database in _MongoDB Atlas_, copy the connection string that is provided after selecting the database: <br>
**Overview** > **Connect** > **Compass** <br>
Don´t forget to replace the field _<password>_ with your password. <br>
Open the file functions.py and add the connection string to the constant variable in line 8.

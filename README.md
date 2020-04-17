# Dashboard

## Installing Packages
Using pip, install the following packages:
* pymongo
* flask

## Setting Up Your Dashboard
* Visit https://ipstack.com/, sign up for a free account
  * Navigate to your dashboard and find  your API access key
  * Copy and paste your key into the text file named **"ipstack_geolocation_key.txt"** inside the API folder
* Visit https://openweathermap.org/, sign up for a free account
  * Click on the API tab and click on the subscibe button under the **"Current weather data"** option
  * In the free column, click on **"Get API key and Start"**
  * An email will be sent with your API key called an "APPID"
  * Copy and paste your key into the text file named **"openweathermap_key.txt"**
* Visit https://www.mongodb.com/, sign up for a free account
  * Create a new cluster
  * Create a new database called **"Dashboard"**
  * Create a new collection in your database called **"Dashboard"** as well
  * Go back to your clusters and click on the **"Connect"** button for your newly created database
  * Click the option called **"Connect using MongoDB Compass"**
  * Do not worry about any options and copy the MongoDB Compass connection string
    * The string should start with look something like: **"mongodb+srv://<username>:<password>@dashboard..."**
    * You need to replace <username> and <password> with your username and password respectively. The username field may be already filled out
  * Copy and paste your connection string with your filled in credentials into the text file named **"mongo_connection_string.txt"**

* Visit https://developers.google.com/calendar/quickstart/python, and follow the step provided
  * The quickstart.py file mentioned in the instructions are provided in the repo, however, the file may be outdated so be sure to check with the website for any changes
  * If the quickstart.py script ran successfully, a token.pickle file should be created in the directory
  
 * Before starting the dashboard, run the **create_db_structure.py** script to setup your database structure
 
## Usage
* Run the db_updater.py file **then** the app.py file
* The dashboard should now be running on your http://localhost/

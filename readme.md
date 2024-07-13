# Todo Assesment

## Setup project localy
### Steps
1. git clone git@github.com:Ahmed712441/Todo-assessment.git
2. [optional] create and activate virtual environment (py -3 -m venv venv) (.\venv\scripts\activate). Note: this commands create and activate virtual env on Windows only
3. run pip install -r requirements.txt
4. create a .env file , .env file must contain this variables
    1. DEBUG=1 to run in debug mode
    2. DOMAINS=localhost:8000,localhost
    3. AUTH0_DOMAIN , your auth0 domain ( ex: dev-u.us.auth0.com)
    4. API_IDENTIFIER , The audience you defined when creating auth0 API
    5. AUTH0_CLIENT_ID , your auth0 client id
    6. AUTH0_CLIENT_SECRET , your auth0 client secret
    7. MONGO_DB_HOST , your mongodb connection string ( ex: mongodb+srv://USER:PASSWORD@CLUSTER_URL/ )

5. run python manage.py migrate
6. run python manage.py runserver ( then the api will be active and running at http://localhost:8000/ you shouldn't call the api at http://127.0.0.1:8000/ if you want to do so change DOMAINS env variable to 'localhost:8000,localhost,127.0.0.1,127.0.0.1:8000' )

## Google Cloud deploy
### Steps
1. create a google cloud project
2. enable billing for the project
3. Enable the Secret Manager, and Cloud Build APIs.
4. Install the Google Cloud CLI. ( https://cloud.google.com/sdk/docs/install )
5. run gcloud init to initialize google cloud cli with your google account and select the project that you created in step 1
6. run gcloud app create ( initialize app engine and select the deployable region )
7. git clone git@github.com:Ahmed712441/Todo-assessment.git
8. you need to store your env file secretly on google cloud so run gcloud secrets create django_settings --data-file .env ( you can exclude DOMAINS,DEBUG as they aren't considered secrets they will be placed as normal env variables in app engine )
9. run gcloud secrets versions access latest --secret django_settings ( acknowledge that your secrets is uploaded successfully )
10. run gcloud secrets add-iam-policy-binding django_settings \
    --member serviceAccount:$PROJECT_ID@appspot.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor   ( this command add new policy to the default serviceAccount for google cloud engine in this project to allow cloud engine to access secrets you created in previous step )
11. run python manage.py collectstatic ( to collect staticfiles)
11. run gcloud app deploy to deploy your app then get the url of the deployed (ex: https://assesment-todo-429214.lm.r.appspot.com/ )
12. update the env_variables sections in app.yaml file in your project to be 
    ```
    env_variables:
    # This setting is used in settings.py to configure your ALLOWED_HOSTS
        DOMAINS: YOUR_APP_DOMAIN ( ex: assesment-todo-429214.lm.r.appspot.com )
    ```
13. redeploy your app after changes run gcloud app deploy
14. Now your api is active and runing
15. [optional] gcloud app deploy command don't delete old deployment versions but add new ones so to clean up the first deployment version you created to get the url. run:
    1. gcloud app versions list
    2. copy versionID for all versions with TRAFFIC_SPLIT 0.00
    3. gcloud app versions delete VERSION_ID VERSION_ID

## API endpoints description
### Authentication endpoints
| Endpoint  | Description |
| ------------- |:-------------:|
| POST /user/register/     | create a new user account, inputs: email,name,and password      |
| POST /user/login/      | login user, inputs: email,and password returns access_token and refresh_token     |
| POST /user/refresh/      | refresh users access_token to return new one without needing for re-login, inputs: refresh_token |
### Todo Model
| Field  | Type |
| ------------- |:-------------:|
| title     | string      |
| description      | string     |
| status      | CHOICES ( "Done","Pending","Canceled","Active" ) |
| due_date      | DateTime |
| user      | RelatedField to User Table |
| _id      | Auto-generated id |
### Todo endpoints
| Endpoint  | Description |
| ------------- |:-------------:|
| POST /todo/   | create new todo ( need authenticated user ), inputs: title,description,due_date,status      |
| GET /todo/      | list the todos of requesting user has pagination ( need authenticated user ), no inputs needed    |
| PUT /todo/$TODO_ID/      | update todo, include fields you want to update other fields are not necessary, inputs: title,description,due_date,status ( need todo owner )   |
| DELETE /todo/$TODO_ID/      | delete todo, no inputs needed ( need todo owner ) |
| GET /todo/$TODO_ID/      | retrieve individual todo, no inputs needed ( need todo owner ) |
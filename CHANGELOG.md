## 0.1.0 (2023-09-21)

### Feat

- **main**: Connect uvicorn to 0.0.0.0. Add Documentations
- **config**: Add reconnect ENV variables. Fix type casting error of env variables
- **components/db_api**: Add Reconnect to db logic
- **routes**: Add auto_response for tests. Document timer routes and fix some issues
- **route/timer**: Implement the full sql and routes logics for set and get timer
- **routes**: Create the basic RestAPI Server and the routes for the timer
- **app_config**: Create the app_config object that collects env variables for the application
- **RestAPI_Objects**: Define the structure and vlidation of the request and response objects the RestAPI

### Fix

- **config**: Fix typo in row 25
- **db_api**: Move the create table to the main __error_handler__. Delete error code in the __del__ function

### Refactor

- **classes**: Extract TimerInformation from the db_api component to independed class
- **db_api**: Create connection to sql server, create the project db if not existing
- **project**: Creat the project base folder structure

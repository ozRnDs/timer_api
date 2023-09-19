# Overview
The timer api component is part of the timer_project.

The component's responsibility is to supply a REST API interface to the system.
The Interface enables the following actions:
1. Register new timed task to the service
2. Question existing tasks

Multiple components (pods) can work simultaneously. However, the components need external load-balancer to be fully scalable.

## Rest API
### Swagger
The component includes a swagger interface at route: http://*{component_name/component_ip}*/docs
### Basic Routes
1. POST /timer/

   1. Request Body: The time from now to invoke the specified url
        ```json
        {
            "hours": {int},
            "minutes": {int},
            "seconds": {int},
            "url": {str}
        }
        ```
    1. Response Body: The timer id and time left in seconds to invoke it
        ```json
        {
            "id": {UUID as str},
            "time_left": {int}
        }
        ```
2. GET /timer/{timer_id}
    1. Request Query: The timer's id
        
        timer_id must be UUID
    1. Response Body: The timer's full status and time left to invoke it
        ```json
        {
            "id": {UUID as str},
            "status": {waiting/failed/done},
            "time_left": {int}
        }
        ```

## Component Logic
1. _(INITIALIZE)_ The component will try to create connection to the set MySQL Server.
1. _(INITIALIZE)_ If the database or table in the server don't exist, the component will create them.
1. The component will launch a uvicorn server for the Rest Api.

## Environment Variables

| Environment Variable Name | Description | Optional/Mandatory |Notes |
| -- | -- | -- | -- |
| DB_HOST | The MySQL Server's host address (ip/dns/service name) | Mandatory |The MySQL port should be 3306 in order to enable the component to connect. |
| DB_USER | The user name the component should log to the MySQL Server | Mandatory | **For production should be passed through secrets** |
| DB_PASSWORD | The password for the MySQL Server| Mandatory | **For production should be passed through secrets** |
| DB_NAME | The name of the project DB | Optional | Default: _timer_db_ |
| RETRY_NUMBER | Number of retries the service will do before self shutdown | Optional | Default: _10_ |
| RECONNECT_WAIT_TIME | Number of seconds to wait between reconnect retries | Optional | Default: _1_ |

# Quick Start
## System Compose
The component is containerized using docker. It should be deployed using the timer_project compose file with the other components of the system.
## Component Docker
The component can be deployed using docker command:
```bash
export COMPONENT_NAME=timer_api_1
export DB_HOST=timer-api
export DB_USER=root
export DB_PASSWORD=1234
export IMAGE_NAME=timer_api
export IMAGE_TAG=0.0.1
export REST_PORT=80
docker run -d --rm --name $COMPONENT_NAME -e DB_HOST=$DB_HOST -e DB_USER=$DB_USER -e DB_PASSWORD=$DB_PASSWORD -p $REST_PORT:5000 $IMAGE_NAME:$IMAGE_TAG
```
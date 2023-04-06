**API Documentation:**

This API provides functionality for user registration, login, password reset, and email verification. The API is implemented using the Flask web framework, Flask-RESTful extension, Flask-SQLAlchemy extension, and email. Message module. The API can be tested using the Python requests library or any other RESTful API client.

Base URL:

Endpoints:

/register - POST method
/login - POST method
/forgot-password - POST method
/reset-password - POST method
Parameters:

username - string - required - email of the user
password - string - required - password of the user
secret_code - string - required for reset-password endpoint
Response format:
The API returns a JSON object as a response to all endpoints. In case of an error, the response will have an "error" key, and in case of success, the response will have a "message" key.

Endpoint Usage Examples:

**/register:**
This endpoint is used to register a new user.
Example usage:

Request:
`POST /register?username=user@example.com&password=mysecretpassword`

Response:

`{
"message": "User registered successfully",
"token": "rygtfcedxswzaq1234567890poiuytrewqas"
}`

**/login:**
This endpoint is used to log in a user.
Example usage:

Request:
`POST /login?username=user@example.com&password=mysecretpassword`

Response:
`{
"message": "Logged in successfully",
"token": "rygtfcedxswzaq1234567890poiuytrewqas"
}
`
**/forgot-password:**
This endpoint is used to send an email containing a secret code to the user.
Example usage:

Request:
`POST /forgot-password?username=user@example.com`

Response:
`{
"message": "Email sent successfully"
}`

**/reset-password:**
This endpoint is used to reset the password of a user.
Example usage:

Request:
`POST /reset-password?username=user@example.com&password=newsecretpassword&secret_code=rygtfced`

Response:
`{
"message": "Password reset successfully"
}`

Bought tiket

Endpoint
The API endpoint for the buyTicket resource is /buy-ticket.

Parameters
The buyTicket resource expects the following headers:

token: A token generated when the user logs in to the system.
date: The date of the movie show in the format 'YYYY-MM-DD'.
title: The title of the movie.
time: The time of the movie show in the format 'HH:MM'.
number: The number of the seat the user wants to purchase.
username: The username of the user making the purchase.
Response
The buyTicket resource returns a JSON response that contains a message field and a data field if the ticket purchase was successful.

The message field contains a string that describes the outcome of the ticket purchase. The possible messages are:

Ticket bought successfully: The ticket purchase was successful.
Seat not found: The specified seat is not available for purchase.
Time not found: The specified movie show time is not available for the specified movie.
Title not found: The specified movie title is not available on the specified date.
Date not found: The specified date is not available for any movie.
The data field contains a dictionary with the following fields:

date: The date of the movie show in the format 'YYYY-MM-DD'.
title: The title of the movie.
time: The time of the movie show in the format 'HH:MM'.
number: The number of the seat the user purchased.
id: A unique identifier for the ticket.
Example usage
Here is an example of how to use the buyTicket API class:

```
import requests

# Set the API endpoint URL
url = 'http://localhost:5000/buy-ticket'

# Set the headers
headers = {
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJhZG1pbiIsInBhc3N3b3JkIjoiYmFkbWluIiwiaWF0IjoxNTE2MjM5MDIyfQ.kG-PxH-kWnX9kTxp6gNEFYyRMT6OWaUJ7fU3qMjmzgQ',
    'date': '2023-04-07',
    'title': 'Avengers: Endgame',
    'time': '19:00',
    'number': '7',
    'username': email
}

# Send a POST request to the API endpoint
response = requests.post(url, headers=headers)

# Print the response
print(response.json())
```

Answer /buyTicket
`{
    "message": "Ticket bought successfully",
    "data": {
        "date": "2023-04-08",
        "title": "Avengers: Endgame",
        "time": "20:00",
        "number": 3,
        "id": "MjM4NzE4NTM2OTQ="
    }
}`

Aviable metods for schedule

```for day /getDay?date=2023-04-08

for all /fullSchedule
```
My tikets /getTikets?username=email

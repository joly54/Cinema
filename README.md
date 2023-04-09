**API Documentation:**

This API provides functionality for user registration, login, password reset, and email verification. The API is implemented using the Flask web framework, Flask-RESTful extension, Flask-SQLAlchemy extension, and email. Message module. The API can be tested using the Python requests library or any other RESTful API client.

Endpoints:

Login: /login  
Register: /register  
Forgot Password: /forgot-password  
Reset Password: /reset-password  
Get Day: /getDay  
Full Schedule: /fullSchedule  
Buy Ticket: /buyTicket  
Display Tickets: /displayTikets  
Get Tickets: /getTikets  
Confirm Email: /confirmEmail  
Is Email Confirmed: /isEmailConfirmed  
Check Token: /checkToken  
Resend Email Validation Code: /resendEmailValidationCode


Base URL: `testaccjgh.pythonanywhere.com`

**/login:**
This endpoint is used to authenticate a user and generate a session token.
Example usage:

Request:
`POST /login?username=user@example.com&password=mysecretpassword`

Response:

On successful authentication, the server will return an HTTP 200 response with a JSON body containing a success message, the user's session token, and the timestamp at which the session token will expire:
`
{
    "message": "Logged in successfully",
    "token": "rygtfcedxswzaq1234567890poiuytrewqas",
    "validDue": 1671234567
}
`
If the authentication fails due to invalid credentials, the server will return an HTTP 400 response with a JSON body containing an error message:
`
{
    "message": "Wrong username or password"
}
`
Note that the session token is also returned in a cookie named token, which should be stored by the client and sent along with subsequent requests to protected resources.

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

**/isEmailConfirmed:**
This endpoint is used to check if a user's email address has been confirmed.
Example usage:

Request:
`GET /isEmailConfirmed?username=user@example.com`

Response:

If the user's email address has been confirmed, the server will return an HTTP 200 response with a JSON body containing a success message:
`
{
    "message": "Email confirmed"
}
`
If the user's email address has not been confirmed, the server will return an HTTP 200 response with a JSON body containing an error message:
`
{
    "message": "Email not confirmed"
}
`
If the specified username does not correspond to a registered user, the server will return an HTTP 404 response with a JSON body containing an error message:

`
{
    "message": "User not found"
}
`

**/confirmEmail:**
This endpoint is used to confirm a user's email address.
Example usage:

Request to get validation code:
`GET /confirmEmail?username=user@example.com`

Response:

If the server successfully sends an email containing the validation code to the specified email address, it will return an HTTP 200 response with a JSON body containing a success message:

`
{
    "message": "Email sent successfully"
}
`
Request to check email confirmation status:
`GET /confirmEmail?username=user@example.com&code=-1`

Response:

If the user's email address has been confirmed, the server will return an HTTP 200 response with a JSON body containing a success message:

`
{
    "message": "Email confirmed"
}
`
If the user's email address has not been confirmed, the server will return an HTTP 200 response with a JSON body containing an error message:

`
{
    "message": "Email not confirmed"
}
`
Request to confirm email:
`GET /confirmEmail?username=user@example.com&code=123456`

Response:

If the validation code is correct and the email is successfully confirmed, the server will return an HTTP 200 response with a JSON body containing a success message:

`
{
    "message": "Email confirmed"
}
`
If the validation code is incorrect, the server will return an HTTP 400 response with a JSON body containing an error message:

`
{
    "message": "Wrong code"
}
`
If the specified username does not correspond to a registered user, the server will return an HTTP 404 response with a JSON body containing an error message:

`
{
    "message": "User not found"
}
`
If the user's email address has already been confirmed, the server will return an HTTP 400 response with a JSON body containing an error message:

`
{
    "message": "Email already confirmed"
}
`

**/forgotPassword:**
This endpoint is used to send a password reset email to a user.
Example usage:

Request:
`POST /forgotPassword?username=user@example.com`

Response:

If the specified username corresponds to a registered user and the email is successfully sent, the server will return an HTTP 200 response with a JSON body containing a success message:

`
{
    "message": "Email sent successfully"
}
`
If the specified username does not correspond to a registered user, the server will return an HTTP 404 response with a JSON body containing an error message:

`
{
    "message": "User not found"
}
`

**/resetPassword:**
This endpoint is used to reset a user's password using a secret code.
Example usage:

Request:
`POST /resetPassword?username=user@example.com&password=newpassword&secret_code=abcdefg12345`

Response:

If the specified username corresponds to a registered user, the secret code matches the user's secret code, and the password is successfully updated, the server will return an HTTP 200 response with a JSON body containing a success message:

`
{
    "message": "Password reset successfully"
}
`
If the specified username does not correspond to a registered user, the server will return an HTTP 404 response with a JSON body containing an error message:

`
{
    "message": "User not found"
}
`
If the specified secret code does not match the user's secret code, the server will return an HTTP 400 response with a JSON body containing an error message:

`
{
    "message": "Wrong secret code"
}
`

**/getDay:**
This endpoint is used to retrieve the day of the week for a given date.
Example usage:

Request:
`GET /getDay?date=2023-04-09`

Response:

If the specified date is valid and corresponds to a day of the week, the server will return an HTTP 200 response with a JSON body containing the day of the week:

`
{
    "message": "success",
    "day": list of films
}
`
If the specified date is not valid or does not correspond to a day of the week, the server will return an HTTP 404 response with a JSON body containing an error message:

`
{
    "message": "Date not found"
}
`

**/fullSchedule**
Same as previous but for full schedule

Class buyTicket(Resource):

This class is a resource that handles the purchasing of a ticket by a user.

Methods:

post(): This method handles the POST request to buy a ticket. It expects the following headers:

`token: A string representing the user's authentication token.
date: A string representing the date of the movie.
title: A string representing the title of the movie.
time: A string representing the time of the movie.
number: An integer representing the number of the seat the user wants to purchase.
username: A string representing the username of the user.
`
Responses:

Returns a JSON response with the following fields:
`
message: A string representing the status of the ticket purchase.
data: A dictionary representing the ticket information if the ticket was bought successfully. The dictionary contains the following fields:
date: A string representing the date of the movie.
title: A string representing the title of the movie.
time: A string representing the time of the movie.
number: An integer representing the number of the seat purchased.
id: A string representing the unique ID of the ticket.
urltoqr: A string representing the URL of the QR code for the ticket.
`
Possible message responses are:
`
User not found: The username in the request headers does not correspond to an existing user in the database.
Wrong token or session expired: The authentication token in the request headers is incorrect or has expired.
Email not confirmed: The user has not confirmed their email address.
Date not found: The specified date in the request headers does not exist in the system.
Title not found: The specified movie title in the request headers does not exist on the specified date.
Time not found: The specified movie time in the request headers does not exist for the specified movie title on the specified date.
Seat not found: The specified seat number in the request headers is not available for purchase.
Ticket bought successfully: The ticket was purchased successfully and the data field contains the ticket information.
`

**/getTikets:**
This endpoint is used to get all tickets bought by a particular user.
Example usage:

Request:
`GET /getTikets?username=user@example.com&token=rygtfcedxswzaq1234567890poiuytrewqas`

Response:
`
{ "message": "success", "tikets": [ { "date": "2023-04-15", "title": "Movie Title", "time": "15:00", "number": 5, "id": "HJUYT67T98HG54FJ", "urltoqr": "http://baseurl.com/tikets/HJUYT67T98HG54FJ.png" }, { "date": "2023-04-16", "title": "Another Movie Title", "time": "19:00", "number": 2, "id": "DFE789YHJ786DFR45", "urltoqr": "http://baseurl.com/tikets/DFE789YHJ786DFR45.png" } ] }
`
In the example above, the API returns all tickets bought by the user with username "user@example.com" and token "rygtfcedxswzaq1234567890poiuytrewqas". The response contains a list of tickets, where each ticket has a date, title, time, number, id, and a URL to the QR code image of the ticket.

/checkToken:

This endpoint is used to check the validity of a token.

Example usage:

Request:
`GET /checkToken?username=user@example.com&token=rygtfcedxswzaq1234567890poiuytrewqas`

Response:

If the token is valid and not expired, the response will be:

`
{
"message": "Token valid"
}
`
If the token is not valid or expired, the response will be:

`
{
"message": "Token not valid"
}
`
Note that the token validity is determined by comparing the input token and the token stored in the database with the corresponding username. If the username or the stored token in the database is not found, the response will be:

`
{
"message": "User not found"
}
`

**/resendEmailValidationCode:**

This endpoint is used to resend the validation code to a user's email in case they didn't receive it or it expired.

Example usage:

Request:
`GET /resendEmailValidationCode?username=user@example.com`

Response:

If the user is found and their email is not confirmed, a new validation code will be generated and sent to the user's email. The response will be:

`
{
"message": "Email sent successfully"
}
`
If the user is not found, the response will be:

`
{
"message": "User not found"
}
`
If the user's email is already confirmed, the response will be:

`
{
"message": "Email already confirmed"
}
`
Note that the sendValidationCode function is a custom function that sends an email to the user's email address containing the validation code. The get_random_string(16) function is also a custom function that generates a random string of length 16.

**/buyManyTikets:**

This endpoint is used to buy multiple tickets for a movie screening.

Example usage:

Request(in headers):

`
POST /buyManyTikets
token: rygtfcedxswzaq1234567890poiuytrewqas
date: 2023-04-15
title: The Avengers
time: 15:00
number: [A1, A2, A3]
username: user@example.com
`
Response:

If the user is found, their token is valid and their email is confirmed, and the movie screening details are valid, the specified tickets will be bought and the response will be:

`
{
"message": "Ticket bought successfully",
"data": [
    {
    "username": "user@example.com",
    "date": "2023-04-15",
    "title": "The Avengers",
    "time": "15:00",
    "number": "A1",
    "id": "abcd1234efgh5678",
    "urltoqr": "https://example.com/tikets/abcd1234efgh5678.png"
    },
    {
    "username": "user@example.com",
    "date": "2023-04-15",
    "title": "The Avengers",
    "time": "15:00",
    "number": "A2",
    "id": "ijkl9012mnop3456",
    "urltoqr": "https://example.com/tikets/ijkl9012mnop3456.png"
    },
    {
    "username": "user@example.com",
    "date": "2023-04-15",
    "title": "The Avengers",
    "time": "15:00",
    "number": "A3",
    "id": "qrst7890uvwx2345",
    "urltoqr": "https://example.com/tikets/qrst7890uvwx2345.png"
    }
    ]
}
`
If the user is not found, the response will be:

`
{
"message": "User not found"
}
`
If the user's token is invalid or their session has expired, the response will be:

`
{
"message": "Wrong token or session expired"
}
`
If the user's email is not confirmed, the response will be:

`
{
"message": "Email not confirmed"
}
`
If the movie screening details are invalid, the response will be:

`
{
"message": "Date not found"
}
`
Note that the sendManyTikets function is a custom function that sends an email to the user's email address containing the purchased tickets as attached QR codes. The get_random_string(16) function is also a custom function that generates a random string of length 16


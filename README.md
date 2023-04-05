**API Documentation:**

This API provides functionality for user registration, login, password reset, and email verification. The API is implemented using the Flask web framework, Flask-RESTf ul extension, Flask-SQLAlchemy extension, and email. Message module. The API can be tested using the Python requests library or any other RESTf ul API client.

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
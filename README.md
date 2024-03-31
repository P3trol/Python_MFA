# Python_MFA
A multifactor authentication application developed in python

As part of my university course I was tasked with the creation of a multi-factor authentication project, the three levels of authentication chosen were Login with username and encrypted password, one-time password and a captcha.

The project was coded in python with the flask framework used for the front end. The database chosen was SQLite, in the database stored are the username, first name, last name, email, encrypted password using sha-256, and the OTP secret key.

Flask was chosen due to the login page library and the current user library, these would help with the ease of use in the creation of this project, instead of having to store cookies.

The otp functionality uses the library pyotp for the creation of a time-based one-time password. The captcha is generated on the backend in the python .random function and then stored in a variable then using the captcha library to create a static image that is checked against the variable.


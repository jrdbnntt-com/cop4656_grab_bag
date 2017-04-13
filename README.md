COP4656 Group Project 2: Grab Bag (django server)
=================================================

This is the backend for the project hosted on a live server.

The base url for all requests is "https://gb.jrdbnntt.com/".

# Technical components
* Session management
* User accounts & authentication 
* Django administration web interface
* Authenticated JSON-based REST API
* Push Notifications (sent via [Firebase Cloud Messaging (FCM)](https://firebase.google.com/docs/cloud-messaging/))
* PostgreSQL Database (managed by Django's Models)
* Cron Job Scheduling

# Development
## Database Connection
There is a PostgreSQL 9.5 database hosted on a private server for the app. In development, you will want to set up an SSH tunnel for the database port.

Example:  `ssh -nNT -L 5432:localhost:5432 user@example.com`

# API Routes
## Testing Routes `/api/test/*`
* GET `/api/test/get/simple_get_test` - Returns sample response for testing
    - Response
        + `some_integer` (int)
        + `some_string` (string)
        + `some_boolean` (boolean)
        + `some_json` (string[])
* POST `/api/test/simple_post_test` - Sample post request for testing
    - Request
        + `some_integer` (int, 0 <= x <= 100)
    - Response
        + `some_message` (string) - Should contain a message with `req.some_integer`
# Cybersecurity

## A sample project that shows some common flaws in cybersecurity and how to fix them

This is a project for the Cyber-Security course of the university of Helsinki.

### Link:

[https://github.com/Juggern4ut/cyberSecurityProjectMeier]()

### Installation:

No further installation is required, you can start the server by running the command `python manage.py runserver` and view it on [http:127.0.0.1:8000]()

## FLAW 1:

### Location of the flaw

exact source link pinpointing flaw 1...

### Description of the flaw

This application allows a logged in user to post a text unto his or her profile page like one may find in popular social media platforms like Facebook or twitter, however the input of the field is not sanitized correctly and allows an attacker to execute SQL-Queries using SQL-Injections.

### How to fix it

By saitizing the Input, we can ensure that SQL-Injections can be prevented. To further harden our application we can also use `execute` instead of `executescript` since it allows only a single query to run.

## FLAW 2:

### Location of the flaw

exact source link pinpointing flaw 2...

### description of the flaw

This example social media platform also allows users to send messages to each other. Since the content of the messages are not validated, a malicious user might try an attack by using cross site scripting to gain access to cookies from the recieving user.

### How to fix it

To prevent XSS we have to ensure that no script tags can be sent using the chat. This can be done by parsing out the `<script>` tags from any user input.

## FLAW 3:

exact source link pinpointing flaw 3...

description of flaw 3...

how to fix it...

## FLAW 4:

exact source link pinpointing flaw 4...

description of flaw 4...

how to fix it...

## FLAW 5:

exact source link pinpointing flaw 5...

description of flaw 5...

how to fix it...

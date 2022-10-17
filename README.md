# Cybersecurity

## A sample project that shows some common flaws in cybersecurity and how to fix them

This is a project for the Cyber-Security course of the university of Helsinki. It shows a dummy social media application where users can send messages to eachother, create posts and upload images. The application handles a basic friend system. (Note: Who is a friend to who is hardcoded into the database). However there are several security flaws that are listed below and ways or ideas on how to fix them. In the code, the flaws are marked with comments and the fixes are all commented out. To check the fixes just comment out everything in the flaw and uncomment everything in the fix.

### Link:

[https://github.com/Juggern4ut/cyberSecurityProjectMeier]()

### Installation:

No further installation is required, you can start the server by running the command `python manage.py runserver` and view it on [http:127.0.0.1:8000]()

## FLAW 1:

### Location of the flaw

https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/views.py#L69

### Description of the flaw

This application allows a logged in user to post a text unto his or her profile page like one may find in popular social media platforms like Facebook or twitter, however the input of the field is not sanitized correctly and allows an attacker to execute SQL-Queries using SQL-Injections.

### How to fix it

By saitizing the Input, we can ensure that SQL-Injections can be prevented. To further harden our application we can also use `execute` instead of `executescript` since it allows only a single query to run. An even better solution would be to use models. This solution is shown by the commented out code below the flaw.

## FLAW 2:

### Location of the flaw

https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/views.py#L52

### Description of the flaw

This example social media platform also allows users to send messages to each other. Since the content of the messages are not validated, a malicious user might try an attack by using cross site scripting to gain access to cookies from the recieving user.

### How to fix it

To prevent XSS we have to ensure that no script tags can be sent using the chat. This can be done by parsing out the `<script>` tags from any user input. FOr an even better solution we can use BeautifulSoup to parse out all the tags and be left with only text between the html-tags.

## FLAW 3:

### Location of the flaw

https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/views.py#L92

### Description of the flaw

In the application, a user should be able to look at all the posts of another user but only if they have them in their friend list, but since the views are not checked, a user can access the posts of every other user by manipulating the URL.

### How to fix it

Before returning all the posts of a user we have to make sure that they are allowed to look at them. Check out the commented out code below the flaw to see how the fix can be implemented.

## FLAW 4:

### Location of the flaw

https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/views.py#L27

### Description of the flaw

In the application users have the possibility to upload an image with their post that show up on their profile. Since we fixed in flaw 3 that users that are not friends cannot see each others posts we might assume that the images are safe too. But a clever attacker might realize that he can directly download images by manipulating the URL again.

### How to fix it

When the user tries to access an image directly via the url we need to make sure that the logged in user is allowed to access that image.

## FLAW 5:

### Location of the flaw

https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/views.py#L47
https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/views.py#L67

### Description of the flaw

When a user adds a post, uploads an image or sends a message to another user, the server will have to process that request, edit the database and maybe also save a uploaded file. A malicious user could use this for a denial of service attack (DoS) by sending thousends of post requests to generate data on the server.

### How to fix it

There are many ways to make a denial of service attack more difficult. In this fix the library `django-ratelimit` is used which allows the developer to set a limit to certain views so that they cannot be called an unlimited amount of time.

In this fix only the views that handle post requests have a rate limit set. In a productive system it might also make sense to limit the other views aswell. Using the same technique we could also limit the login attempts to prevent brute force attacks aswell.

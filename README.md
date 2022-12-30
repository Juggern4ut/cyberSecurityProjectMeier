# Cybersecurity

## A sample project that shows some common flaws in cybersecurity and how to fix them

This is a project for the Cyber-Security course of the university of Helsinki. It shows a dummy social media application where users can send messages to eachother, create posts and upload images. The application handles a basic friend system. (Note: Who is a friend to who is hardcoded into the database). However there are several security flaws that are listed below and ways or ideas on how to fix them. In the code, the flaws are marked with comments and the fixes are all commented out. To check the fixes just comment out everything in the flaw and uncomment everything in the fix.

### Link:

[https://github.com/Juggern4ut/cyberSecurityProjectMeier]()

### Installation:

One of the flaws requires the package "django-ratelimit" to be installed, you can do so by running the following command: `pip install django-ratelimit`. Other than that no further installation is required, you can start the server by running the command `python manage.py runserver` and view it on [http:127.0.0.1:8000]()

Logins for the frontend are:

- admin:admin
- bob:squarepants
- alice:redqueen

#### Problems with using this porject

If any problems or unexpected behaviour occur when trying to use this project, send an email to lukas.meier@helsinki.fi

## FLAW 1:

### Location of the flaw

https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/views.py#L69

### Description of the flaw

This application allows a logged in user to post a text unto his or her profile page like one may find in popular social media platforms like Facebook or Twitter, however the input of the field is not sanitized correctly and allows an attacker to execute SQL-Queries using SQL-Injections. We can verify this huge security flaw by logging in as any user and create a new post with any SQL-Injection. For example: `this is my post'); INSERT INTO pages_post (author_id, content) VALUES (1, 'Im the admin and i stink!`

### How to fix it

By saitizing the Input, we can ensure that SQL-Injections can be prevented. To further harden our application we can also use `execute` instead of `executescript` since it allows only a single query to run. An even better solution would be to use models. This solution is shown by the commented out code below the flaw.

## FLAW 2:

### Location of the flaw

https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/templates/pages/chat.html#L31

### Description of the flaw

This example social media platform also allows users to send messages to each other. Due to bad configuration we passed the `|safe` template filter to the template exposing our application to XSS-Attacks. Since the content of the messages are not validated, a malicious user might try an attack by using cross site scripting to gain access to cookies from the recieving user. To verify this problem, we can log in as any user and go to the chat view with any of his/her friends. If we now send a message containing a `<script>`-tag and send it, it will be executed when the recieving user opens the chat page.

### How to fix it

To prevent XSS we have to ensure that no script tags can be sent using the chat. The easiest way is to just remove the `|safe` filter from the template. Now all tags will be parsed out automatically. Another solution could be to manually parsing out the `<script>` tags from any user input or we could use BeautifulSoup to parse out all the tags and be left with only text between the html-tags. For this project, we will go with the simpelest solution and just remove the `|safe` filter.

## FLAW 3.1:

### Location of the flaw

https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/views.py#L92

### Description of the flaw

In the application, a user should be able to look at all the posts of another user but only if they have them in their friend list, but since the views are not checked, a user can access the posts of every other user by manipulating the URL. A user that looks at the url might also quuickly realize that the user-ids are simply incrementing numbers, so guessing the url is not hard either. To verify this Problem we can simply login as bob and visit the profile of the admin user directly by going to `/profile/1` even though the admin is not in bobs friend list. Here are the ids of the users: admin = 1, bob = 2, alice = 3.

### How to fix it

Before returning all the posts of a user we have to make sure that they are allowed to look at them. Check out the commented out code below the flaw to see how the fix can be implemented. To futher increase the security the user ids also should not simply increment but be something random so users can not just 'guess' a valid profile URL.

## FLAW 3.2:

### Location of the flaw

https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/views.py#L27

### Description of the flaw

In the application users have the possibility to upload an image with their post that show up on their profile. Since we fixed in flaw 3 that users that are not friends cannot see each others posts we might assume that the images are safe too. But a clever attacker might realize that he can directly download images by manipulating the URL again. To verify this Problem we can once again login as bob and visit the url `/image/3` and download a image of the admin.

### How to fix it

When the user tries to access an image directly via the url we need to make sure that the logged in user is allowed to access that image. This solution is implemented in the commented out code below the flaw.

## FLAW 4:

https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/templates/pages/chat.html#L44
https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/views.py#L49

### Description of the flaw

If requests are not protected agains cross site request forgery (CSRF) a malicous user might be able to create a link to a website that if opened by the already logged in victim will send a request to our application. Since we do not check for the origin of the request, we assume it is legit and execute it.

### How to fix it

Luckily django forces us to use the '{% csrf_token}' in forms that use 'unsafe' methods (as defined here: https://datatracker.ietf.org/doc/html/rfc7231.html#section-4.2.1) But it doesn't do so for 'safe' methods such as GET. Now GET methods should by design not cause any side effects. So no data on the server side should be changed by it. If we can not (or have any other reason not to) stick to that rule, we have to make sure to add the csrf_token to the form as to prive the origin of the request and prevent a CSRF-Attack. In this example flaw, it would also make sense to switch the form in the chat to action type "POST" since there is no particular reason not to do so.

## FLAW 5:

### Location of the flaw

https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/views.py#L47
https://github.com/Juggern4ut/cyberSecurityProjectMeier/blob/master/server/pages/views.py#L67

### Description of the flaw

When a user adds a post, uploads an image or sends a message to another user, the server will have to process that request, edit the database and maybe also save a uploaded file. A malicious user could use this for a denial of service attack (DoS) by sending thousends of post requests to generate data on the server.

### How to fix it

There are many ways to make a denial of service attack more difficult. In this fix the library `django-ratelimit` is used which allows the developer to set a limit to certain views so that they cannot be called an unlimited amount of time.

In this fix only the views that handle post requests have a rate limit set. In a productive system it might also make sense to limit the other views aswell. Using the same technique we could also limit the login attempts to prevent brute force attacks aswell.

## Disclaimer

This is only a demo project that is meant to display common security flaws. The focus has been put on the five flaws listed above and not on the usability or correctnes of the application. Do not use any of this code in a productive system.

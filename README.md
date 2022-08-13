# Charity
This project is a Django project to connect charity to benefactor or vice versa.


After installing the libraries in the requirements, you can run the project with the runserver command in Django commands.
<p> first you must create a database and makemigrations data then first run commands : <b> python manage.py migrate</b> and <b>python manage.py makemigrations </b></p>
<p> second for manage your site you must create a superuser with command : <b>python manage.py createsuperuser </b></p>   
<p> you must after download this project create a captcha google and wirte <b>RECAPTCHA_PUBLIC_KEY</b> and <b>RECAPTCHA_PRIVATE_KEY</b> in settings.py <p>
<p>for run project you must run command: <b>python manage.py runserver</b></p>  

After the implementation of the project, you must register on the site and then complete your profile with the title you want to be on the site.


If you are on the site as a charity, you can define missions and put them on the site so that charitable people can see and request to do them if they like, and after your request, you can accept or reject.
The missions you register can be seen in your profile section in the relevant field, and if a charity requests cooperation, you can accept or reject it from the same section.


If you are on the site as a philanthropist, you can see charity missions and request pending items for cooperation with the charity.
The missions you request can be seen in your profile section.



This project consists of three apps:<br>
<ul>
<li>about_us</li>
<li>accounts</li>
<li>charities</li>
</ul>
<br>
<h3>app about_us : </h3>
<p>This app includes parts of the template that are home and about us, and north of the footer and header </p>
<h3> app accounts: </h3>
<p>This app is related to users and the templates related to the user, such as user registration or login or logout or changing the password, are related to the user.
</p>
<h3> app charities: </h3>
<p>This app contains sections related to a benefactor and a charity and their related templates</p>
<p>
This project is my first Django project and it is a Django template and I really enjoyed doing it.
In fact, it is similar to a real project rather than a real project and it can definitely be better than this.</p>

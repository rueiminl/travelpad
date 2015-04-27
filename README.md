site: http://ec2-52-10-143-249.us-west-2.compute.amazonaws.com

# team27
15-437/15-637 repo for chunninc

prerequisite:
	1. install apache2, mysql, python, django, mod-wsgi, ...
	1.1 pip install pillow 		(used when uploading photos)
	2. cp github to /var/www/travelpad (or ln -s)
	3. new file travelpad.conf
		> a2ensite travelpad.conf
	4. edit settings.py 'read_default_file' = your mysql user/password configuration file
	format:
	[client]
	database = travelpad
	user = root
	password = xxx
	default-character-set = utf8
	5. python manage.py migrate
	6. restart apache2 by: /etc/init.d/apache2 reload
	or just debug by > python manage.py runserver

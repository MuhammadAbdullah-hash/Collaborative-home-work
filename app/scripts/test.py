'''
	This is script file  used to run scripts  / python files in django enviroment
	Steps to make it working are as follows : 
		1) add "django_extensions" in your INSTALLED APPS in setting.py
		2) Make a folder in your app with directory structure as follows : 
			project-root
				your app
					scripts
						__init__.py , <your script.py>
		3) open cmd and type "manage.py runscript <your script.py>"
	
	Note : 
		Runscript doesnt give specific errors
		It has general errors like if there is an import error it would simply say : 
			" No (valid) module for script 'test.py' found                                                                                                
			Try running with a higher verbosity level like: -v2 or -v3                                                                                  
			CommandError: An error has occurred running scripts. See errors above. "
		For imports it doesnt take reletive path to modules it takes full path for exmpale : 
			from . models import <YOUR MODEL> ------> Wrong way 
			from <yourapp>.models import <YOUR MODEL> ------------> Correct way
'''

from app.models import New_user


def run():
	obj = New_user.objects.filter( name = 'quddus-34' ) 
	print(obj[0].id)
	# print( obj[0].id )
	# for j in New_user.objects.all():
	# 	print(j.get_attr)


run()


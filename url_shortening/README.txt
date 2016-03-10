# UrlShortening
1. Make sure that Python is installed on your system. If not then download and install from www.python.org. Install Python version 2.7
2. Set the following paths in the PATH environment variable :
	- C:\Python27\
	- C:\Python27\Scripts\
	- C:\Python27\Lib\site-packages\
4. To install Python packages on your computer, Setuptools is needed. Download the latest version of Setuptools for your Python version at		  	 https://pypi.python.org/pypi/setuptools#windows-powershell-3-or-later
3. If pip is not installed in your computer then open a command prompt and type easy_install pip
4. Then enter pip install django. You can verify by typing  django-admin --version that django has successfully installed
5. Once all these setups are complete go to the folder containing this project in the command prompt. 
6. Go inside the url_shortening folder and then type python manage.py runserver
7. This will start the server and you can access the application in your web browser using http://localhost:8000/my_shortener.com or http://127.0.0.1:8000/my_shortener.com
8. To close the server from the command prompt used CTRL + C
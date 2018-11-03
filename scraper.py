from bs4 import BeautifulSoup
import requests
import lxml  

def login(username, password):

	session_requests=requests.session()
	session_requests.post('https://www.spoj.com/login', data={
		'login_user': username,
		'password': password
		})
	yield session_requests

username = imput("Enter username : ")
password = input("Enter password : ")
with login(username, password) as session:
	

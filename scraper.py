from bs4 import BeautifulSoup
import requests
import lxml  
from contextlib import contextmanager
from getpass import getpass

lang = {'C': '.c', 'C++': '.cpp', 'CPP14': '.cpp', 'JAVA': '.java',
		'PYTHON3': '.py', 'PYPY': '.py', 'C++ 4.3.2': '.cpp', 'CPP': '.cpp',
		'PYTHON': '.py', 'TEXT': '.txt'
		}


@contextmanager
def login(username, password):

	session_requests=requests.session()
	session_requests.post('https://www.spoj.com/login', data={
		'login_user': username,
		'password': password
		})
	yield session_requests

def solved_problem_set(soup):
	solved_problems=set()
	tab = soup.find('table', class_='table')
	for tr in soup.find('table', class_='table'):
		for tr in tab.find_all('tr'):
			for td in tab.find_all('td'):
				if td.a.text != '':
					solved_problems.add(td.a.text)
	return solved_problems


def get_sol_id(newsoup):
	for tr in newsoup.find_all('tr'):
		check=tr.find('td', class_='statusres text-center')
		if check['status']==15:
			td=tr.find('td', class_='statustext text-center').a.text
			return td

def get_ac_lang(newsoup):
	for tr in newsoup.find_all('tr'):
		check=tr.find('td', class_='statusres text-center')
		if check['status']==15:
			td=tr.find('td', class_='slang text-center').a.text
			return td 

if __name__ == '__main__':
	username = raw_input("Enter username : ")
	password = getpass("Enter password : ")
	with login(username, password) as session:
		myacc=session.get('https://www.spoj.com/myaccount')
		soup=BeautifulSoup(myacc.text, "lxml")
		solved_problems=solved_problem_set(soup)
		for problem in solved_problems:
			probstatus="https://www.spoj.com/status/"+problem+","+username
			newsoup=BeautifulSoup(probstatus.text, "lxml")
			print (problem+" : \n")
			acid=get_sol_id(newsoup)
			aclang=get_ac_lang(newsoup)
			filename=problem+lang[aclang]
			print ("Downloading "+filename+" ...\n")
			with open(filename, "w") as solution:
				solution.write(session.get('https://www.spoj.com/files/src/save/{sol_id}'.format(sol_id=acid)).text)

		

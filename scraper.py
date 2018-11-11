from bs4 import BeautifulSoup
import requests
import lxml  
from contextlib import contextmanager
from getpass import getpass
import sqlite3
import csv



csv_file = open('problems.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['problem_name', 'language_used'])


conn = sqlite3.connect('problems.db')
c=conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS prob1 (
problem_name varchar2,
language_used varchar2
)""")

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
		check = tr.find('td', class_='statusres text-center')
		if check != None and check['status'] == '15':
			acid = tr.find('td', class_='statustext').text
			return acid.strip()

def get_ac_lang(newsoup):
	for tr in newsoup.find_all('tr'):
		check = tr.find('td', class_='statusres text-center')
		if check != None and check['status'] == '15':
			aclang=tr.find('td', class_='slang').find('span').text
			return aclang.strip()

if __name__ == '__main__':
	username = raw_input("Enter username : ")
	password = getpass("Enter password : ")
	print("\n")
	check = raw_input("Download solutions ? (yes/y OR no/n) : ")
	print("\n")

	if(check == "no" or check == 'n' or check == 'N' or check == 'NO'):
		with login(username, password) as session:
			myacc=session.get('https://www.spoj.com/myaccount')
			soup=BeautifulSoup(myacc.text, "lxml")
			solved_problems=solved_problem_set(soup)
			print(solved_problems)
			for problem in solved_problems:
				probstatus=session.get("https://www.spoj.com/status/"+problem+","+username)
				newsoup=BeautifulSoup(probstatus.text, "lxml")
				print (problem+" : \n")
				acid=get_sol_id(newsoup)
				aclang=get_ac_lang(newsoup)
				filename = problem + lang[aclang]
				temp=""
				langused=""
				langused=aclang
				temp=problem
				csv_writer.writerow([temp, langused])
				c.execute("INSERT INTO prob1 VALUES (?, ?)", (temp, langused))
				conn.commit()
	else:
		with login(username, password) as session:
			myacc=session.get('https://www.spoj.com/myaccount')
			soup=BeautifulSoup(myacc.text, "lxml")
			solved_problems=solved_problem_set(soup)
			print(solved_problems)
			for problem in solved_problems:
				probstatus=session.get("https://www.spoj.com/status/"+problem+","+username)
				newsoup=BeautifulSoup(probstatus.text, "lxml")
				print (problem+" : \n")
				acid=get_sol_id(newsoup)
				aclang=get_ac_lang(newsoup)
				filename = problem + lang[aclang]
				temp=""
				langused=""
				langused=aclang
				temp=problem
				csv_writer.writerow([temp, langused])
				c.execute("INSERT INTO prob1 VALUES (?, ?)", (temp, langused))
				conn.commit()
				print ("Downloading "+filename+" ...\n")
				with open(filename, "w") as solution:
					solution.write(session.get('https://www.spoj.com/files/src/save/{sol_id}'.format(sol_id=acid)).text)


	csv_file.close()
	c.execute("SELECT * from prob1")
	print(c.fetchall())

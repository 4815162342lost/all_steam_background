#!/usr/bin/python3
import requests
import sqlite3
import sys
import time
from bs4 import BeautifulSoup
import math
import os
from PyQt5.QtWidgets import *

steam_app=QApplication(sys.argv)
window=QWidget()
window.setWindowTitle("Program for downloading Steam Background")
window.resize(400,200)

menu_bar=QMenuBar(window)
menu_bar.setFixedSize(2000,25)
menu_file=menu_bar.addMenu('&File')

def window_close():
	db_backrounds.commit()
	window.close()

#button_start.clicked.connect(start)
exitButton = QAction('Exit', window)
exitButton.setShortcut('Ctrl+Q')
exitButton.setStatusTip('Exit application')
exitButton.triggered.connect(window_close)
menu_file.addAction(exitButton)

chose_games=QComboBox(window)
chose_games.addItem("A-C")
chose_games.addItem("D-F")
chose_games.addItem("G-I")
chose_games.addItem("J-L")
chose_games.addItem("M-O")
chose_games.addItem("P-R")
chose_games.addItem("S-U")
chose_games.addItem("V-X")
chose_games.addItem("Y-Z")
chose_games.addItem("0-9")
chose_games.move(170,30)

label_chose_games=QLabel(window)
label_chose_games.setText("Games name starterd on ...")
label_chose_games.move(0,35)

label0=QLabel(window)
label0.setText("Download files on:")
label0.move(0,60)

radio0=QRadioButton("On one directory", window)
radio0.move(0, 80)
radio0.click()

radio1=QRadioButton("On games directory", window)
radio1.move(150, 80)

bar = QProgressBar(window)
bar.resize(400,20)
bar.setMinimum=(0)
bar.move(0,100)

button_start=QPushButton("Start", window)
button_start.move(130, 150)

def start():
	urls=("http://www.steamcardexchange.net/index.php?showcase-filter-ac", "http://www.steamcardexchange.net/index.php?showcase-filter-df", 
	"http://www.steamcardexchange.net/index.php?showcase-filter-gi", "http://www.steamcardexchange.net/index.php?showcase-filter-jl", 
	"http://www.steamcardexchange.net/index.php?showcase-filter-mo", "http://www.steamcardexchange.net/index.php?showcase-filter-pr", 
	"http://www.steamcardexchange.net/index.php?showcase-filter-su", "http://www.steamcardexchange.net/index.php?showcase-filter-vx", 
	"http://www.steamcardexchange.net/index.php?showcase-filter-yz", "http://www.steamcardexchange.net/index.php?showcase-filter-09")

	game_link=get_games_link(urls[chose_games.currentIndex()])
	games_count=len(game_link)
	bar.setMaximum(int(games_count))
	current_game_count=1
	file_end=urls[chose_games.currentIndex()][len(urls[chose_games.currentIndex()])-2:len(urls[chose_games.currentIndex()])]
	if radio1.isChecked()==True:
		for url in game_link:
			get_backgrounds_link_and_downloading_on_game_path(url)
			current_game_count+=1
			bar.setValue(current_game_count)

	else:
		create_path("Backgrounds_"+str(file_end))
		for url in game_link:
			get_backgrounds_link_and_downloading_on_backgrounds_path(url, file_end)
			print(current_game_count,"games background downloading from", games_count)
			current_game_count+=1
			bar.setValue(current_game_count)

big_counter=0
def get_games_link(url):
	"""Function for return link to games"""
	r=requests.get(url)
	game_link0=[]
	if r.status_code == 200:
		soup=BeautifulSoup(r.text, "html.parser")
		for game_list in soup.find_all(class_="showcase-game-item"):
			game_link=game_list.a.get("href")
			game_link0.append(game_link)
	return game_link0

def get_backgrounds_link_and_downloading_on_game_path(url):
	"""Function for extract background url"""
	url="http://www.steamcardexchange.net/"+url
	r=requests.get(url)
	if r.status_code==200:
		soup=BeautifulSoup(r.text, "html.parser")
		game_name=soup.find(class_="game-title").h1.string
		path=create_path(game_name)
		counter=0
		for background in soup.find_all(class_="showcase-element-container background"):
			for background_link in background.find_all(class_="element-link-right"):
				url=background_link.get("href")
				save_file(url,counter,path,game_name)
				counter+=1
				
def get_backgrounds_link_and_downloading_on_backgrounds_path(url,file_end):
	url="http://www.steamcardexchange.net/"+url
	r=requests.get(url)
	global big_counter
	counter=big_counter
	if r.status_code==200:
		soup=BeautifulSoup(r.text, "html.parser")
		game_name=soup.find(class_="game-title").h1.string
		for background in soup.find_all(class_="showcase-element-container background"):
			for background_link in background.find_all(class_="button-blue market"):
				url=background_link.get("href")
				store_link=url.replace("(Profile Background)","")
				counter+=1
			for background_link in background.find_all(class_="element-link-right"):
				url=background_link.get("href")
				save_file(url, big_counter, "Backgrounds_"+file_end,game_name)
				big_counter+=1
	if counter!=big_counter:
		print("Counter brocken. Fix it.")
		big_counter=counter+2

def save_file(url, number, path,game_name):
	"""Function for download file and save to disk"""
	if add_to_db(game_name, url)!=False:
		try:
			r=requests.get(url)
			if r.status_code==200:
				path=path+"/"+str(number)
				f=open(str(path)+".jpg", "wb")
				f.write(r.content)
				f.close
			else:
				error_to_log(url,1,game_name)
		except requests.exceptions.ConnectionError:
			error_to_log(url,1,game_name)

def error_to_log(url, type,game_name):
	"""Function for save errors on log file"""
	if type==1:
		print("Game: ", game_name, "Server not avaliable. ", "\n", url, sep='')
		time.sleep(5)
	if type==0:
		print("Path",url,"exists")
		return 0
	f=open("error.log", "a")
	f.write("Game: "+str(game_name)+"\n"+str(url)+"\n")
	f.close

def create_path(path_name):
	"""Function foe create path"""
	pwd=os.getcwd()
	if os.path.exists(pwd+"/"+path_name)==False:
		os.mkdir(pwd+"/"+path_name)
	else:
		error_to_log(path_name,0, None)
	return pwd+"/"+path_name

def add_to_db(game_name, url):
	"""Function to add record on db"""
	global counter_my
	cursor.execute("select exists(select url from backgrounds where url=?)", (url,))
	need_add=cursor.fetchone()[0]
	if need_add==0:
		cursor.execute("insert into backgrounds values (?,?)", (url, game_name))
		if counter_my==10:
			db_backrounds.commit()
			counter_my=0
		counter_my+=1
	else:
		return False

counter_my=0
button_start.clicked.connect(start)
db_backrounds=sqlite3.connect("./backgrounds.db")
cursor=db_backrounds.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables=[row[0] for row in cursor.fetchall()]
if "backgrounds" in tables:
	print("Table backgrounds exists")
else:
	cursor.execute("create table backgrounds (url text, game_name text, uniqUE(url));")
window.show()
steam_app.exec_()

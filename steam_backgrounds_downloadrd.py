#!/usr/bin/python3
import requests
import sys
import time
from bs4 import BeautifulSoup
import math
import os

big_counter=0
def get_games_link(url):
	"""Function for return link to games"""
	r=requests.get(url)
	game_link0=[]
	if r.status_code == 200:
		soup=BeautifulSoup(r.text)
		for game_list in soup.find_all(class_="showcase-game-item"):
			game_link=game_list.a.get("href")
			game_link0.append(game_link)
	return game_link0

def get_backgrounds_link_and_downloading_on_game_path(url):
	"""Function for extract background url"""
	url="http://www.steamcardexchange.net/"+url
	r=requests.get(url)
	if r.status_code==200:
		soup=BeautifulSoup(r.text)
		game_name=soup.find(class_="game-title").h1.string
		path=create_path(game_name)
		counter=0
		for background in soup.find_all(class_="showcase-element-container background"):
			for background_link in background.find_all(class_="element-link-right"):
				url=background_link.get("href")
				save_file(url,counter,path)
				counter+=1
				
def get_backgrounds_link_and_downloading_on_backgrounds_path(url):
	url="http://www.steamcardexchange.net/"+url
	r=requests.get(url)
	global big_counter
	counter=big_counter
	if r.status_code==200:
		soup=BeautifulSoup(r.text)
		for background in soup.find_all(class_="showcase-element-container background"):
			for background_link in background.find_all(class_="button-blue market"):
				url=background_link.get("href")
				store_link=url.replace("(Profile Background)","")
				save_background_link_to_steam_trade_store(store_link, counter)
				counter+=1
			for background_link in background.find_all(class_="element-link-right"):
				url=background_link.get("href")
				save_file(url, big_counter,"Backgrounds")
				big_counter+=1
	if counter!=big_counter:
		print("Counter brocken. Fix it.")
		big_counter=counter+2

def save_background_link_to_steam_trade_store(link,number):
	f=open("list_link.log","a")
	f.write(str(number)+"\n"+str(link)+"\n")
	f.close

def save_file(url, number, path):
	"""Function for download file and save to disk"""
	try:
		r=requests.get(url)
		if r.status_code==200:
			path=path+"/"+str(number)
			f=open(str(path), "wb")
			f.write(r.content)
			f.close
		else:
			error_to_log(url,1, game_name)
	except requests.exceptions.ConnectionError:
		error_to_log(url,1, game_name)

def error_to_log(url, type, game_name):
	"""Function for save errors on log file"""
	if type==1:
		print("Server not avaliable. ", "Game: ", game_name, "\n", url, sep='')
		time.sleep(5)
	if type==0:
		print("Path",url,"exists","\n")
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
		error_to_log(path_name,0,None)
	return pwd+"/"+path_name

def chose_games_and_path():
	"""Function for chose path and games"""
	urls=("http://www.steamcardexchange.net/index.php?showcase-filter-ac/", "http://www.steamcardexchange.net/index.php?showcase-filter-df", 
	"http://www.steamcardexchange.net/index.php?showcase-filter-gi", "http://www.steamcardexchange.net/index.php?showcase-filter-jl", 
	"http://www.steamcardexchange.net/index.php?showcase-filter-mo", "http://www.steamcardexchange.net/index.php?showcase-filter-pr", 
	"http://www.steamcardexchange.net/index.php?showcase-filter-su", "http://www.steamcardexchange.net/index.php?showcase-filter-vx", 
	"http://www.steamcardexchange.net/index.php?showcase-filter-yz", "http://www.steamcardexchange.net/index.php?showcase-filter-09")
	chose=input("Enter 1 to download from A to C, 2 -- D-F, 3 -- G-I, 4 -- J-L, 5 -- M-O, 6 -- P-R, 7 -- S-U, 8 -- V-X, 9 -- Y-Z, 0 -- 0-9\n")
	try:
		if 0<int(chose)<10:
			url=urls[int(chose)-1]
		elif int(chose)==0:
			url=urls[9]
		else:
			print("Enter correct number!")
			exit(1)
	except ValueError:
		print("Enter correct number!")
		exit(1)
	path_chose=input("Enter 1 to downloading files to each path, 2 -- to one path.\n")
	if path_chose!="1" and path_chose!="2":
		print("Enter correct number!")
		exit(1)
	if path_chose=="2":
		path_chose="Backgrounds"
	chose_and_path_list=[url, path_chose]
	return chose_and_path_list
		
def start():
	"""Main function"""
	create_path("Backgrounds")
	url_and_path_list=[]
	url_and_path_list=chose_games_and_path()
	game_link=get_games_link(url_and_path_list[0])
	games_count=len(game_link)
	current_game_count=1
	if url_and_path_list[1]!="Backgrounds":
		for url in game_link:
			get_backgrounds_link_and_downloading_on_game_path(url)
			print(current_game_count,"games background downloading from", games_count)
			current_game_count+=1
	else:
		for url in game_link:
			get_backgrounds_link_and_downloading_on_backgrounds_path(url)
			print(current_game_count,"games background downloading from", games_count)
			current_game_count+=1
start()

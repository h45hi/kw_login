from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import os, time, random

URL='https://portal.csm.co.in'
login_time=datetime(year=2020, month=9, day=30, hour=8, minute=40, second=0)
logoff_time=datetime(year=2020, month=9, day=30, hour=19, minute=30, second=0)
cur_time=datetime.now()

class kw_login:

	def __init__(self,username,password):
		self.username = username
		self.password = password
		self.bot = webdriver.Chrome()
		self.bot.maximize_window()

	def kw_v6_login(self):
		bot = self.bot
		bot.get(URL)
		time.sleep(random.randrange(3,6))
		signin_btn = bot.find_element_by_link_text('Sign In').click()
		time.sleep(random.randrange(3,6))
		username = bot.find_element_by_id("login")
		username.send_keys(self.username)
		time.sleep(random.randrange(3,6))
		password = bot.find_element_by_id("password")
		password.send_keys(self.password)
		time.sleep(random.randrange(3,6))
		password.send_keys(Keys.RETURN)

	def kw_v5_login(self):
		bot = self.bot
		time.sleep(random.randrange(8,14))
		dashboard_menu = bot.find_element_by_xpath("/html/body/header/nav/ul[1]/li/a").click()
		time.sleep(random.randrange(5,8))
		kwv5_menu = bot.find_element_by_link_text('Kwantify V5').click()
		return bot

	def get_open_window_status(self):
		bot = self.bot
		time.sleep(40)
		active_urls = []
		opened_windows = bot.window_handles
		for i, window in enumerate(opened_windows):
			bot.switch_to.window(opened_windows[i])
			try:
				if 'google' in bot.current_url:
					bot.switch_to.frame(opened_windows[i])
			except NoSuchElementException as e:
				pass

		return {'url': bot.command_executor._url, 'session_id': bot.session_id}

	def kw_v5_logout(self):
		bot = self.bot
		time.sleep(random.randrange(3,6))
		opened_windows = bot.window_handles
		for i,windows in enumerate(opened_windows):
			time.sleep(random.randrange(2,5))
			bot.switch_to.window(opened_windows[i])
			if 'csmpl' in bot.current_url:
				signout_btn = bot.find_element_by_xpath('//*[@id="nvBarNd"]/div[1]/a').click()

	def kw_v6_logout(self):
		bot = self.bot
		time.sleep(random.randrange(3,6))
		dropdown = bot.find_element_by_xpath('//*[@id="top_menu"]/li[5]/a').click()
		time.sleep(random.randrange(2,5))
		signout_menu = bot.find_element_by_xpath('//*[@id="o_logout"]').click()
		return bot

if __name__ == "__main__":
	try:
		if os.path.exists('./secrets.py'):
			from secrets import kw_username, kw_password
			k = kw_login(kw_username,kw_password)
			if login_time.time() <= cur_time.time():
				k.kw_v6_login()
				time.sleep(random.randrange(8,14))
				resp = k.kw_v5_login()
			if logoff_time.time() <= cur_time.time():
				time.sleep(random.randrange(5,10))
				k.kw_v5_logout()
				time.sleep(random.randrange(5,10))
				resp = k.kw_v6_logout()
			resp.quit()
		else:
			raise ImportError('Please check if you have secrets file in same directory as this one.')
	except ImportError as e:
		print(e)



### For using existing browser
# bot_dict = k.get_open_window_status()
# print("BOT DICT", bot_dict)
# if bot_dict.get('url') != False:
# 	old_bot = webdriver.Remote(command_executor=bot_dict.get('url'),desired_capabilities={})
# 	old_bot.session_id = bot_dict.get('session_id')
# 	body = old_bot.find_element_by_tag_name("body")
# 	body.send_keys(Keys.CONTROL + 't')
# 	old_bot.get("https://twitter.com/")
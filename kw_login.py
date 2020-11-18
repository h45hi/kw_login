from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from datetime import datetime
from getopt import getopt
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
		time.sleep(random.randrange(6,10))
		# check_in = bot.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/div/div/div/div[2]/div/div/div[3]/div/div[1]/div/div/div').click()
		return bot

	"""Needed incase of task reporting"""
	def kw_v5_login(self):
		bot = self.bot
		time.sleep(random.randrange(8,14))
		dashboard_menu = bot.find_element_by_xpath("/html/body/header/nav/ul[1]/li/a").click()
		time.sleep(random.randrange(5,8))
		kwv5_menu = bot.find_element_by_link_text('Kwantify V5').click()

	def get_tab(self, tab_key=None):
		bot = self.bot
		time.sleep(random.randrange(3,6))
		opened_windows = bot.window_handles
		for i,windows in enumerate(opened_windows):
			time.sleep(0.5)
			bot.switch_to.window(opened_windows[i])
			if tab_key in bot.current_url:
				return opened_windows[i]

	def get_task_links(self):
		bot = self.bot
		csm_tab = self.get_tab(tab_key='DashboardStandardv1')
		bot.switch_to.window(csm_tab)
		time.sleep(random.randrange(2,5))
		project_mgmt = bot.find_element_by_xpath("//*[@id='sidebar-left']/ul/li[4]/a").click()
		time.sleep(random.randrange(2,5))
		project_monitor = bot.find_element_by_xpath("//*[@id='sidebar-left']/ul/li[4]/ul/li/a").click()
		time.sleep(random.randrange(2,5))
		project_task = bot.find_element_by_xpath("//*[@id='sidebar-left']/ul/li[4]/ul/li/ul/li[3]/a").click()
		bot.switch_to.frame(bot.find_element_by_xpath('//*[@id="iFr"]'))
		time.sleep(random.randrange(2,5))
		task_links = [link.get_attribute('href') for link in bot.find_elements_by_tag_name('a')\
		 				if 'TaskReporting' in link.get_attribute('href')]
		return task_links

	def report_project_task(self, links):
		bot = self.bot
		for link in links:
			bot.execute_script(f'''window.open("{link}","_blank");''')
			task_tab = self.get_tab(tab_key='TaskReporting')
			bot.switch_to.window(task_tab)
			""" Set Task Status as completed """
			task_sts = Select(bot.find_element_by_id('selStatus'))
			task_sts.select_by_value('2')
			""" Set From Time as 9:00 AM """
			bot.find_element_by_id('txtFromTime').click()
			bot.find_element_by_xpath('//*[@id="frmTask"]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[4]/td[3]/span[1]/ul/li[37]').click()
			""" Set To Time as 5:00 PM """
			bot.find_element_by_id('txtToTime').click()
			bot.find_element_by_xpath('//*[@id="frmTask"]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[5]/td[3]/span[1]/ul/li[69]').click()
			""" Set To Remark """
			remark = bot.find_element_by_id('txtARemarks')
			remark.send_keys('completed')
			""" Click on Submit button """
			bot.find_element_by_id('btnSubmit').click()
			alert_obj = bot.switch_to.alert
			alert_obj.accept()
			bot.close()
			task_tab = self.get_tab(tab_key='framepage.aspx')
			bot.switch_to.window(task_tab)

	def kw_v6_logout(self):
		bot = self.bot
		time.sleep(random.randrange(6,10))
		check_in = bot.find_element_by_xpath('//div[@class="csm-checkout"]').click()
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
				resp = k.kw_v6_login()
				k.kw_v5_login()
			# if logoff_time.time() <= cur_time.time():
			# 	time.sleep(random.randrange(5,10))
			# 	resp = k.kw_v6_logout()
			task_links = k.get_task_links()
			if len(task_links)>0:
				k.report_project_task(task_links)
		else:
			raise ImportError('Please check if you have secrets file in same directory as this one.')
	except ImportError as e:
		print(e)
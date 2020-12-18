from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time, random, argparse

URL='https://portal.csm.co.in'

my_parser = argparse.ArgumentParser(allow_abbrev=False)
my_parser.add_argument('--username', action='store', type=str, required=True, metavar='', help='Username for logging in portal')
my_parser.add_argument('--password', action='store', type=str, required=True, metavar='', help='Password for logging in portal')
my_parser.add_argument('--browser', action='store', type=str, required=True, metavar='', help='Broswer of choice[Chrome/Firefox]')
my_parser.add_argument('--check_in', action='store_true',
						help='Willing to check in, include this flag if want to set as true, default:False *Optional')
my_parser.add_argument('--log_out', action='store_true', 
						help='Willing to log out, include this flag if want to set as true, default:False *Optional')
my_parser.add_argument('--report_task', action='store_true',
						help='Willing to report task, include this flag if want to set as true, default:False *Optional')
args = my_parser.parse_args()

class kw_login:

	def __init__(self,username,password):
		self.username = username
		self.password = password
		self.bot = webdriver.Chrome() if args.browser.lower() == 'chrome' else webdriver.Firefox()
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
		if args.check_in:
			check_in = bot.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/div/div/div/div[2]\
													/div/div/div[3]/div/div[1]/div/div/div').click()
		time.sleep(random.randrange(3,6))
		return bot

	"""Needed incase of task reporting"""
	def kw_v5_login(self):
		bot = self.bot
		time.sleep(random.randrange(8,14))
		dashboard_menu = bot.find_element_by_xpath("/html/body/header/nav/ul[1]/li/a").click()
		time.sleep(random.randrange(5,8))
		kwv5_menu = bot.find_element_by_link_text('Kwantify V5').click()

	""" Needed to wish all (Birthday/Year of Service/Well Wishes/Anniversary) """
	def kw_wish_all(self):
		bot = self.bot
		self.kw_v5_login()
		csm_tab = self.get_tab(tab_key='DashboardStandardv1')
		bot.switch_to.window(csm_tab)
		time.sleep(random.randrange(3,6))
		bot.execute_script("window.scrollBy(0,100)")
		bot.switch_to.frame(bot.find_element_by_xpath('//*[@id="34"]/div/iframe'))
		# Switching to birthday frame
		wish_ids = ["birthdayId", "yearOfServiceId", "wellWishesId", "anniversaryId"]
		for wish_id in wish_ids:
			wish_btn = bot.find_element_by_id(wish_id)
			print(f'{wish_id} having count {wish_btn.get_attribute("innerHTML")}')
			if int(wish_btn.get_attribute("innerHTML")) > 1:
				wish_btn.click()
				time.sleep(random.randrange(1,3))
				bot.switch_to.window(csm_tab)
				# Switching to wish modal
				bot.switch_to.frame(bot.find_element_by_xpath('//*[@id="myFrame"]'))
				bot.execute_script("window.scrollBy(0,document.scrollingElement.scrollHeight)")
				time.sleep(random.randrange(1,3))
				# Clicking on wish all button
				bot.find_element_by_xpath('//*[@id="btnWishToAll"]').click()
				bot.switch_to.window(csm_tab)
				# Close modal
				time.sleep(random.randrange(1,3))
				bot.find_element_by_xpath('//*[@id="myModal"]/div[1]/button').click()
				time.sleep(random.randrange(1,3))
				bot.switch_to.frame(bot.find_element_by_xpath('//*[@id="34"]/div/iframe'))
			if int(wish_btn.get_attribute("innerHTML")) == 1:
				wish_btn.click()
				time.sleep(random.randrange(1,3))
				bot.switch_to.window(csm_tab)
				bot.switch_to.frame(bot.find_element_by_xpath('//*[@id="myFrame"]'))
				bot.execute_script("window.scrollBy(0,document.scrollingElement.scrollHeight)")
				time.sleep(random.randrange(1,3))
				bot.find_element_by_xpath('//*[@id="1618"]/div[2]/div[2]/button[2]').click()
				bot.switch_to.window(csm_tab)
				time.sleep(random.randrange(1,3))
				bot.find_element_by_xpath('//*[@id="myModal"]/div[1]/button').click()
				time.sleep(random.randrange(1,3))
				bot.switch_to.frame(bot.find_element_by_xpath('//*[@id="34"]/div/iframe'))


	""" Switch to specific tab depending on tab_key """
	def get_tab(self, tab_key=None):
		bot = self.bot
		time.sleep(random.randrange(3,6))
		opened_windows = bot.window_handles
		for i,windows in enumerate(opened_windows):
			time.sleep(0.5)
			bot.switch_to.window(opened_windows[i])
			if tab_key in bot.current_url:
				return opened_windows[i]

	""" Get all assigned task links """
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

	""" Iterate through task links and report task """
	def report_project_task(self, links):
		bot = self.bot
		for link in links:
			bot.execute_script(f'''window.open("{link}","_blank");''')
			task_tab = self.get_tab(tab_key='TaskReporting')
			bot.switch_to.window(task_tab)
			# Set Task Status as completed
			task_sts = Select(bot.find_element_by_id('selStatus'))
			task_sts.select_by_value('2')
			time_selection = '//*[@id="frmTask"]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/table/tbody/tr[4]/td[3]/span[1]/ul/'
			# Set From Time as 9:00 AM
			bot.find_element_by_id('txtFromTime').click()
			bot.find_element_by_xpath(time_selection+'li[37]').click()
			# Set To Time as 5:00 PM
			bot.find_element_by_id('txtToTime').click()
			bot.find_element_by_xpath(time_selection+'li[69]').click()
			# Set To Remark
			remark = bot.find_element_by_id('txtARemarks')
			remark.send_keys('completed')
			# Click on Submit button & close current tab
			bot.find_element_by_id('btnSubmit').click()
			alert_obj = bot.switch_to.alert
			alert_obj.accept()
			bot.close()
			# Switch back to task table page
			task_tab = self.get_tab(tab_key='framepage.aspx')
			bot.switch_to.window(task_tab)

	def kw_v6_logout(self):
		bot = self.bot
		check_out = bot.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/div/div/div/div[2]\
												/div/div/div[3]/div/div[2]/div/div/div').click()
		time.sleep(random.randrange(3,6))
		user_dropdown = bot.find_element_by_xpath('/html/body/header/nav/ul[3]/li[3]/a').click()
		time.sleep(random.randrange(2,5))
		signout_menu = bot.find_element_by_xpath('/html/body/header/nav/ul[3]/li[3]/div/a[3]').click()
		time.sleep(random.randrange(2,5))
		return bot

if __name__ == "__main__":
	k = kw_login(args.username, args.password)
	resp = k.kw_v6_login()
	if args.check_in:
		k.kw_wish_all()
	if args.report_task:
		k.kw_v5_login()
		task_links = k.get_task_links()
		if len(task_links) > 0:
			k.report_project_task(task_links)
	if args.log_out:
		time.sleep(random.randrange(5,10))
		resp = k.kw_v6_logout()
	resp.quit()

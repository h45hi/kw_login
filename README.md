# kw_login

This is a personal tool to carry out daily tasks in internal portal i.e. Kwantify. It has different features like logging in, wishing employees and task reporting.
In order to use this script follow below steps

## Web Driver
After installing python dependencies, web-driver are needed to interact with browsers.
For running script in chrome, download [driver](https://sites.google.com/a/chromium.org/chromedriver/).
For running script in firefox, download [driver](https://github.com/mozilla/geckodriver/releases).
Please remember to place driver in location
### For Linux
```bash
$ venv/bin
```
### For Windows
```bash
$ venv\Scripts
```
## Command line Flags
In order for script to carry out different tasks it needs various flags.
```bash
$ python kw_login.py --help
```
### Output
```bash
usage: kw_login.py [-h] --username  --password  --browser  [--check_in] [--log_out] [--report_task]

optional arguments:
  -h, --help     show this help message and exit
  --username     Username for logging in portal
  --password     Password for logging in portal
  --browser      Broswer of choice[Chrome/Firefox]
  --check_in     Willing to check in, include this flag if want to set as true, default:False *Optional
  --log_out      Willing to log out, include this flag if want to set as true, default:False *Optional
  --report_task  Willing to report task, include this flag if want to set as true, default:False *Optional
```
Sample Command
```bash
$ python kw_login.py --username johndoe --password helloworld --browser chrome --check_in
```

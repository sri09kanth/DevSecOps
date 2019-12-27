from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import subprocess
import sys
import random
import string

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def bash_command(cmd):
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')

myusername = randomString(8)
mypassword = randomString(12)

if len(sys.argv) < 3:
    print 'Provide the ip address to do DAST scan!'
    print 'Provide the output location of html report!'
    sys.exit(1)

driver = webdriver.Remote("http://"+sys.argv[1]+":4444/wd/hub", DesiredCapabilities.CHROME)

driver.get("http://"+sys.argv[1]+":10007/login")

registerbutton = driver.find_element_by_xpath("/html/body/div/div/div/form/center[3]/a")
registerbutton.click()
print("we're at: " + driver.current_url)

print("creating a user..")
username = driver.find_element_by_name("username")
password1 = driver.find_element_by_name("password1")
password2 = driver.find_element_by_name("password2")

username.clear()
username.send_keys(myusername)
password1.clear()
password1.send_keys(mypassword)
password2.clear()
password2.send_keys(mypassword)
password2.send_keys(Keys.RETURN)
login = driver.find_element_by_xpath('/html/body/div/div/div/center[2]/h4')
assert "Login" in login.text

print("created user")

driver.get("http://"+sys.argv[1]+":10007/login")
print("we're at: " + driver.current_url)
username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")
username.clear()
username.send_keys(myusername)
password.clear()
password.send_keys(mypassword)
password.send_keys(Keys.RETURN)
header = driver.find_element_by_xpath("/html/body/div/div/div[1]/h1")
assert "Last gossips" in header.text
print("logged in!")

nikto_string = "STATIC-COOKIE="
cookies_list = driver.get_cookies()
for cookie in cookies_list:
    nikto_string+= '\"' + cookie['name'] + '\"='
    nikto_string+= '\"'+ cookie['value'] + '\"'
bash_command("cp ~/nikto-config.txt ~/new-nikto-config.txt")
bash_command("echo '" + nikto_string +"' >> ~/new-nikto-config.txt")
bash_command("/var/jenkins_home/nikto-master/program/nikto.pl -ask no -config ~/new-nikto-config.txt -Format html -h http://"+sys.argv[1]+":10007/gossip -output "+ sys.argv[2])
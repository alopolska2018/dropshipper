from selenium import webdriver
import time

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False)
profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)")
driver = webdriver.Firefox(profile)
driver.get("https://login.aliexpress.com/?from=sm")
time.sleep(100)
cookies = { c["name"]: c["value"] for c in driver.get_cookies() }
print(cookies)
driver.delete_all_cookies()
driver.quit()

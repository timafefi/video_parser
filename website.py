import logging
from seleniumwire import webdriver  # Import from seleniumwire  
from selenium.webdriver.common.by import By


class WebClient:
    def __init__(self, username, password, LogsObj):
        self.credentials = {'usr': username, 'pswd': password}
        self.driver = self.setupdriver()
        self.logged_in = False
        self.Logs = LogsObj

    def setupdriver(self):
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.add_argument('--headless')
        return  webdriver.Firefox(options=fireFoxOptions)

    def login(self):
        loginpage = 'https://ru.pastrycampus.com/login/index.php'
        self.driver.get(loginpage)
        login = self.driver.find_element(By.ID, "username")
        login.clear()
        login.send_keys(self.credentials['usr'])
        passwd = self.driver.find_element(By.ID, "password")
        passwd.clear()
        passwd.send_keys(self.credentials['pswd'])
        btn = self.driver.find_element(By.ID, "loginbtn").click()
        if self.driver.current_url == loginpage:
            self.Logs.log("Invalid login or password", 'red')
            return -1
        self.logged_in = True
        return 0

    def close(self):
        self.driver.close()


    def get_url_and_filename(self, url):
        if not url:
            self.Logs.log("Empty Url. Falling back", 'red')
        if not self.logged_in:
            self.Logs.log(f"Logging into '{self.credentials['usr']}'", 'blue')
            f = self.login()
            if f == -1:
                return ['Error']
        self.Logs.log(f"getting video source information for\n {url}", 'blue')
        self.driver.get(url)
        self.driver.find_element(By.CLASS_NAME, "vjs-swarmify-play-button").click()
        self.driver.wait_for_request('https://video-node.swarmcdn.com/')
        for request in reversed(self.driver.requests):
            if 'video-node.swarmcdn.com' in request.url and '.mp4' in request.url:
                videohttp = request.url.split('?')[0]
                break
        name = self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div[1]/div[2]/section/div[1]/h2")
        self.Logs.log(f"Found download link for {name}", 'blue')
        return [videohttp, name.text]




if __name__ == '__main__':
    WC = WebClient('tatianafil', 'Samantha2014')
    WC.get_url_and_filename('https://ru.pastrycampus.com/mod/page/view.php?id=12866')

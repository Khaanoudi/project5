import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TickerChartLogin:
    def __init__(self):
        self.base_url = "https://www.tickerchart.net"
        self.session = requests.Session()
        
    def login_api(self, username: str, password: str):
        """Login using direct API call"""
        login_url = f"{self.base_url}/api/v1/auth/login"
        
        payload = {
            "username": username,
            "password": password
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            response = self.session.post(login_url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            if 'token' in data:
                self.session.headers.update({
                    "Authorization": f"Bearer {data['token']}"
                })
                return data['token']
            
        except requests.exceptions.RequestException as e:
            print(f"Login failed: {e}")
            return None

    def login_selenium(self, username: str, password: str):
        """Login using Selenium for browser automation"""
        driver = webdriver.Chrome()
        try:
            # Navigate to login page
            driver.get(f"{self.base_url}/ar/login")
            
            # Wait for login form elements
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = driver.find_element(By.NAME, "password")
            login_button = driver.find_element(By.CLASS_NAME, "login-button")
            
            # Fill in credentials
            username_field.send_keys(username)
            password_field.send_keys(password)
            
            # Click login
            login_button.click()
            
            # Wait for successful login
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "user-profile"))
            )
            
            # Get cookies and token
            cookies = driver.get_cookies()
            for cookie in cookies:
                self.session.cookies.set(cookie['name'], cookie['value'])
            
            # Extract token from localStorage if needed
            token = driver.execute_script("return localStorage.getItem('TC_TOKEN');")
            
            return token
            
        except Exception as e:
            print(f"Login failed: {e}")
            return None
            
        finally:
            driver.quit()

# Usage example
def main():
    login_manager = TickerChartLogin()
    
    # Method 1: Direct API login
    token = login_manager.login_api(
        username="your_username",
        password="your_password"
    )
    
    if token:
        print("API Login successful!")
        print(f"Token: {token}")
    
    # Method 2: Browser automation login
    token = login_manager.login_selenium(
        username="your_username",
        password="your_password"
    )
    
    if token:
        print("Browser Login successful!")
        print(f"Token: {token}")

    return login_manager.session  # Return authenticated session for further use

# Full example with market data
class TickerChartClient:
    def __init__(self, username: str, password: str):
        self.login_manager = TickerChartLogin()
        self.session = None
        self.token = None
        self.authenticate(username, password)
    
    def authenticate(self, username: str, password: str):
        """Login and set up authenticated session"""
        self.token = self.login_manager.login_api(username, password)
        if self.token:
            self.session = self.login_manager.session
        else:
            raise Exception("Authentication failed")
    
    def get_market_data(self, symbol: str):
        """Get market data for a symbol"""
        if not self.session:
            raise Exception("Not authenticated")
            
        url = f"{self.login_manager.base_url}/api/v1/market/data"
        params = {"symbol": symbol}
        
        response = self.session.get(url, params=params)
        return response.json()
    
    def get_portfolio(self):
        """Get user portfolio"""
        if not self.session:
            raise Exception("Not authenticated")
            
        url = f"{self.login_manager.base_url}/api/v1/portfolio"
        response = self.session.get(url)
        return response.json()

# Usage
if __name__ == "__main__":
    client = TickerChartClient(
        username="your_username",
        password="your_password"
    )
    
    # Get market data
    data = client.get_market_data("1010.TAD")
    print("Market Data:", data)
    
    # Get portfolio
    portfolio = client.get_portfolio()
    print("Portfolio:", portfolio)

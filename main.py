import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import exceptions 
import random
import time



class PokeonTCGClient():

    def __init__(self, creds, codes, file):
        self.creds = creds
        self.codes = codes
        self.file = file

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('no-sandbox')
        self.driver = webdriver.Chrome(chrome_options)
        self.driver.implicitly_wait(10)
        self.wait_driver = WebDriverWait(self.driver, timeout=10)

    def start(self):

        self.login()

        if self.codes or self.file:
            self.submit_code_loop()

        print('Succesfully Procesed All Codes')

        self.stop()

    def stop(self):
        print('Closing Application')
        self.driver.quit()

    def submit_code_loop(self):

        self.input_box = self.wait_driver.until(lambda d: d.find_element(by=By.ID, value="code"))
        self.submit_button = self.wait_driver.until(lambda d: d.find_element(by=By.XPATH, value="//button[@data-testid='verify-code-button']"))
        
        if args.codes:
            self.submit_codes(args.codes)

        if self.file is not None:
            self.submit_codes(self.parse_file())


    def submit_codes(self, codes):
            for i, code in enumerate(codes, 1):
                redeemed = False
                print(f'Iteration {i}')
                print(f'Current Code {code}')
                self.input_box.send_keys(code)
                self.submit_button.click()

                while True:
                    # Give the Browser a Chance to Update
                    time.sleep(1.5)
                    # Wait Until Submit is disabled and text is clear
                    if self.submit_button.get_property('disabled') == False \
                        and self.input_box.text == "":
                        break

                # Currently Pokemon Go Accepts 10 codes at a time
                if i % 10 == 0:
                    print('Starting Code Redemption')
                    self.redeem_codes()
                    redeemed = True
            
            if redeemed == False:
                print('Starting Code Redemption')
                self.redeem_codes()    

    def get_invalid_rows(self):
        invalid_cells = []
        div_table = self.driver.find_element(by=By.XPATH, value="//div[@class='RedeemModule_loadingWrapper__2mZ-x']")
        rows = div_table.find_element(by=By.TAG_NAME, value='tbody').find_elements(by=By.TAG_NAME, value='tr')

        for row in rows:
            cells = row.find_elements(by=By.TAG_NAME, value='td')
            final_cell = cells[-1]
            image = final_cell.find_element(by=By.TAG_NAME, value='img')
            if 'invalid' in image.get_attribute("src").lower():
                invalid_cells.append(final_cell)
        return invalid_cells

    def redeem_codes(self):

        # Get All X's and Clear Them
        # Get Table First
        try:

            invalid_cells = self.get_invalid_rows()
            if len(invalid_cells) >= 10:
                print('Clearing Table')
                clear_button = self.driver.find_element(by=By.XPATH, value="//button[@data-testid='button-clear-table']")
                clear_button.click()
                time.sleep(1.25)
            elif len(invalid_cells) > 0:
                for cell in invalid_cells:
                    print('Deleting Entry')
                    cell.click()
                    time.sleep(0.75)
            else:
                redeem_button = self.driver.find_element(by=By.XPATH, value="//button[@data-testid='button-redeem']")
                if redeem_button.get_property('disabled') == False:
                    redeem_button.click()
                    time.sleep(2.5)
            return
        except exceptions.StaleElementReferenceException as e:
            self.redeem_codes()


    def parse_file(self):

        file_type = self.file.split('.')[-1]
        codes = []

        if file_type == "txt":
            with open(args.file, 'r', encoding='utf-8') as file:
                codes += [x.replace('\n',"") for x in file.readlines()]
                print(codes)
            
        else:
            raise NotImplementedError("txt is the only file type implemented")
        
        return codes


    def login(self):

        self.driver.get("https://redeem.tcg.pokemon.com/en-us/")
        user_name_box = self.wait_driver.until(lambda d: d.find_element(by=By.NAME, value="email"))
        password_box = self.wait_driver.until(lambda d: d.find_element(by=By.NAME, value="password"))

        login_button = self.wait_driver.until(lambda d: d.find_element(by=By.ID, value="accept"))
        time.sleep(random.triangular(0.5, 2))
        user_name_box.send_keys(self.creds["username"])
        password_box.send_keys(self.creds["password"])
        login_button.click()
        time.sleep(random.triangular(1.5, 2))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Automatically Submit Codes')
    parser.add_argument('username', type=str,
                        help='Pokemon Trainer Account Usernmae')
    parser.add_argument('password', type=str,
                        help='Pokemon Trainer Account Password')
    parser.add_argument('--codes', '-c', type=list, default=[],
                        nargs='*', help='List of Pokemon TCG Codes to Redeem')
    parser.add_argument('-file', '-f', type=str, default=None,
                        help='Path to File containing Pokemon TCG Codes')
    args = parser.parse_args()

    PokeonTCGClient(
        creds = {"username" : args.username, "password": args.password},
        codes = args.codes,
        file = args.file
    ).start()

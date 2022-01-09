import unittest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
import warnings


class XKomBasket(unittest.TestCase):
    """
    A test suite containing three test cases for selected functionalities of the cart of the x-kom.pl online store
    """

    def setUp(self):
        """
        Preparation of the test environment
        """
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(
            "https://www.x-kom.pl/p/421690-pendrive-pamiec-usb-corsair-64gb-survivor-stealth-usb-30.html")

    def testcase1_add_and_remove_product_from_basket(self):
        """
        Test case # 1
        1) Adding a product to the basket, followed by verification if there is one item in the basket.
        2) Removal of the product from the basket and checking if the basket is empty.
        """
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # 1. Click "Add to Cart"
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Dodaj do koszyka"]'))).click()

        # 2. Click "Go to Cart"
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Przejdź do koszyka'))).click()

        # 3. Download the quantity of the product in the basket and assign it to the variable
        basket_value = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.Select-value-label'))).text

        # 4. Check if there is 1 selected product in the cart
        self.assertEqual(basket_value, "1", "In basked should be 1 product, but currently is: {}.".format(basket_value))

        # 5. Remove the product from the cart
        driver.find_element_by_xpath('//button[@title="Usuń z koszyka"]').click()

        # 6. Click on the basket in the upper right corner
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Koszyk")]'))).click()

        # 7. Make an assertion whether the basket is empty and the following message is displayed correctly: "Your basket is empty"
        notification = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//h2[contains(text(),"Twój koszyk jest pusty")]'))).text
        self.assertEqual(notification, "Twój koszyk jest pusty", "Basket is not empty")

    def testcase2_add_more_than_1000_products_to_basket(self):
        """
        Test case # 2
        Checking the behavior of the system when adding more than 999 items to the cart.
        It is not possible to enter more than 999 items in the cart.
        """
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # 1. Click "Add to Cart"
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Dodaj do koszyka"]'))).click()

        # 2. Click "Go to Cart"
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Przejdź do koszyka'))).click()

        # 3. Select the option from the drop-down list that allows you to enter any quantity of the product
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="Select-arrow-zone"]'))).click()
        element = driver.find_element_by_xpath('//div[@class="Select-input"]')
        action = ActionChains(driver)
        action.move_to_element_with_offset(element, 2, 300).click().perform()

        # 4. Generate a random number greater than 999 (range 1000-1000000)
        invalid_product_amount = random.randint(1000, 1000000)
        print("\nAdding {} products to basket".format(invalid_product_amount))

        # 5. Change the quantity of the product in the cart from 1 to a randomly generated number in the range 1000-1000000
        amount_input = driver.find_element_by_xpath('//input[@type="number"]')
        amount_input.send_keys(invalid_product_amount)

        # 6. Download the quantity of products from the basket and assign to the variable
        value_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type*="number"]')))
        basket_value = int(value_field.get_attribute("value"))

        # 7. Check if there are less than 999 products in your cart
        print("In basket is {} pieces of product".format(basket_value))
        self.assertLessEqual(basket_value, 999,
                             "In basket is more then 999 products. Currently {}.".format(basket_value))

    def testcase3_check_total_value_in_basket_for_randomly_generated_amount_of_product(self):
        """
        Test case # 3
        Adding a random amount of product from 1 to 999 to the cart.
        Calculating if the final order value in the cart is correct.
        """
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # 1. Get the price of the product
        product_price = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="n4n86h-4 edNVst"]'))).text

        # 2. Convert product price from text to float (example from 139,00 zł to 139.00)
        product_price = float(product_price.split(" ")[0].replace(",", "."))

        # 3. Generate a random number of products between 1 - 999
        product_amount = random.randint(1, 999)
        print("\nAdding {} products to basket".format(product_amount))

        # 4. Calculate the expected order value for a random quantity of the product
        expected_total_value = product_amount * product_price

        # 5. Convert the expected order value from float to string (example from 72141.0 to 72 141,00 zł)
        str_expected_total_value = "{:.2f} zł".format(expected_total_value)
        first_part, second_part = str_expected_total_value.split(".")
        first_part_separated = ' '.join([first_part[::-1][i:i + 3] for i in range(0, len(first_part), 3)])[::-1]
        str_expected_total_value = "{},{}".format(first_part_separated, second_part)
        print("Expected total value: {}".format(str_expected_total_value))

        # 6. Select the option from the drop-down list that allows you to enter any quantity of the product
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="Select-arrow-zone"]'))).click()
        element = driver.find_element_by_xpath('//div[@class="Select-input"]')
        action = ActionChains(driver)
        action.move_to_element_with_offset(element, 2, 300).click().perform()

        # 7. Change the quantity of the product in the cart from 1 to a randomly generated number between 1 and 999
        amount_input = driver.find_element_by_xpath('//input[@type="number"]')
        amount_input.send_keys(product_amount)

        # 8. Click "Add to Cart"
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Dodaj do koszyka"]'))).click()

        # 9. Click "Go to Cart"
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Przejdź do koszyka'))).click()

        # 10. Get the order value from the cart
        total_amount = wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="pvj85d-3 dcOESF"]'))).text
        print("Total value in basket: {}".format(total_amount))

        # 11. Check if the value of the order in the basket is correctly calculated
        self.assertEqual(str_expected_total_value, total_amount,
                         "Total value is not properly calculated. Expected: {}, current: {}".format(
                             str_expected_total_value, total_amount))

    def tearDown(self):
        """
        Clean up the test environment after each test case has been run.
        Close the browser with self.driver.close ().
        """
        self.driver.close()
        warnings.simplefilter("ignore", ResourceWarning)


if __name__ == "__main__":
    unittest.main(verbosity=2)

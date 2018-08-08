import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from functions import parse_order_date, parse_delivery_date_string, parse_total

def get_order_history_years(driver):
    """Goes to Orders page, get all available years of history
    """
    driver.get('https://www.amazon.ca/gp/your-account/order-history')

    list_items = driver.find_element_by_css_selector(".a-dropdown-container")

    years = []
    for item in list_items.find_elements_by_tag_name("option"):
        year = item.text
        if len(year) == 4:
            years.append(int(year))

    return years

def sign_in(driver, email, password):
    # Signs into Amazon
    driver.get("https://www.amazon.ca/gp/sign-in.html")

    driver.find_element_by_name('email').send_keys(EMAIL)
    try:
        driver.find_element_by_id('continue').click()
    except:
        pass

    driver.find_element_by_name('password').send_keys(PASSWORD)
    driver.find_element_by_id('signInSubmit').click()

##################################################
# Selenium webscraping
##################################################

# Parse input parameters for email/password
if len(sys.argv) != 3:
    print("Enter your name and password as parameters.\nE.g. > python amazon_order_history.py name@email.com Password1")
    sys.exit()
else:
    _, EMAIL, PASSWORD = sys.argv

    
driver = webdriver.Firefox()

sign_in(driver, EMAIL, PASSWORD)
years = get_order_history_years(driver)

outfile = open("history.csv", "w")
outfile.write("OrderDate,OrderTotal,OrderNumber,Status,DeliveredDate\n")

for year in years:
    driver.get('https://www.amazon.ca/gp/your-account/order-history?opt=ab&digitalOrders=1&unifiedOrders=1&returnTo=&orderFilter=year-%s' % year)

    while True:
        # Find all orders on the page
        orders_container = driver.find_element_by_id("ordersContainer")
        orders = orders_container.find_elements_by_class_name("a-box-group")

        # Extract info and items for each order
        for order in orders:
            order_date = order.find_element_by_class_name('a-span3')
            order_date = order_date.find_element_by_class_name("value").text
            order_date = parse_order_date(order_date)

            order_total = order.find_element_by_class_name('a-span2')
            order_total = order_total.find_element_by_class_name('value').text
            order_total = parse_total(order_total)

            order_number = order.find_element_by_class_name("a-col-right")
            order_number = order_number.find_element_by_class_name("value").text

            order_shipments = order.find_elements_by_class_name("shipment")

            for shipment in order_shipments:
                try:
                    delivered = shipment.find_element_by_class_name("a-size-medium")
                    status, delivered_date = parse_delivery_date_string(delivered.text)

                    outfile.write(f'"{order_date}","{order_total}","{order_number}","{status}","{delivered_date}"\n')
                except NoSuchElementException:
                    pass

        # Go to next page, if exists
        try:
            next_page_button = driver.find_element_by_class_name("a-last")

            if 'a-disabled' in next_page_button.get_attribute('class'):
                # If next page button is disabled, break out of loop
                break
            else:
                next_page_button.click()
        except NoSuchElementException:
            break

outfile.close()

from datetime import datetime
import re

# My functions
def parse_order_date(date):
    return datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")


def parse_delivery_date_string(date_string):

    # Search extracted string for possible delivered keywords
    prefixes_list = ['Delivered', 'Was expected', 'Expected by']
    prefixes_regex = "(" + "|".join(prefixes_list) + ")"

    match = re.search(prefixes_regex, date_string)

    # If string has delivered keywords, parse date
    if match:
        status = match.group()
        extracted_date = date_string[match.end()+1:]

        try:
            parsed_date = datetime.strptime(extracted_date, "%b %d, %Y").strftime("%Y-%m-%d")
            return status, parsed_date
        except ValueError:
            pass

    return date_string, ''

def parse_total(total):
    return float(total[5:])

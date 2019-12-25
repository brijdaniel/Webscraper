"""
If the log file fails, then this code can be used to build a pseudo log file from the terminal output
TODO INCOMPLETE!!
"""
import re


def build_log(log_file):
    # Open txt file containing terminal output, filter down to successful lines for the 50th page of a suburb
    with open(log_file, 'r') as file:
        lines = file.read().splitlines()
        successes = [line for line in lines if re.search('SUCCESS', line)]
        suburbs = [line for line in successes if re.search(r'50', line)]

    # Extract the suburb name from these lines
    # 'of (.+?)\\.' means find the substring that is between 'of ' and '.' ? means be greedy, ie all find all chars,
    # and \\ if because . needs to be escaped
    suburb_list = [re.search('of (.+?)\\.', suburb).group(1) for suburb in suburbs]

    url_base = 'https://www.realestate.com.au/'
    url_list = []

    # Iterate through list of suburbs, replace spaces with + and generate URL format
    for suburb in suburb_list:
        suburb = suburb.replace(' ', '+')
        combined_url = url_base + 'sold' + '/in-' + suburb + ',+sa/list-'
        url_list.append(combined_url)



if __name__ == '__main__':
    log_file = 'C:/Users/Brij/PycharmProjects/Webscraper/Logs/temp.txt'
    build_log(log_file)
import urllib, re
from dateutil import parser
from datetime import datetime as dtm

# string required to standardize date format
DATE_FORMAT_STRING = "%m/%d/%Y"
TIME_FORMAT_STRING = "%H:%M:%S"
DATE_TIME_FORMAT_STRING = DATE_FORMAT_STRING + " " + TIME_FORMAT_STRING

def getTime(string_format):
    time = (dtm.now()).strftime(string_format)
    return time

def getDate(string_format):
    date = (dtm.now()).strftime(string_format)
    return date

# Takes a base url and a relative url and returns an absolute url
def getAbsoluteUrl(baseUrl, relativeUrl):
    return urllib.parse.urljoin(baseUrl, relativeUrl)

def remove_html_tags(text):
    """Remove html tags from a string"""
    try:
        if text != None:
            str(text)
            clean = re.compile('<.*?>')
            return re.sub(clean, '', text)
        else:
            pass
    except:
        pass

def remove_newline_tab(text):
    return text.replace('\n', ' ').replace('\t', '').replace('\r', '').replace('\xa0',' ').replace('&amp;','').replace('\"','').replace('[1]','').replace('[2]','').replace('[3]','').replace('[4]','').replace('[5]','').replace('[6]','').replace('[7]','').replace('[8]','').replace('[9]','').replace('[10]','')

def extractDatefromString(text):
    try:
        date = parser.parse(text, fuzzy=True)
        return date.isoformat(timespec='milliseconds')
    except:
        pass

def image_url_handler(url):
    
    if url == None:
        return " "
    else:
        return 'https:'+ url
    
def ifEmptyVariable(text):
    if text == '':
        return "None"
    else:
        return text

def remove_style_tags(text):
    # Remove content with <style> tags
    text = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', text, flags=re.IGNORECASE)
    return text

def split_data(string):
    if ',' in string:
        return str(string).replace(' ', '').split(',')
    if ';' in string:
        return str(string).replace(' ', '').split(';')
    else:
        return split_member_names(string)

def get_wiki_id(link):
    
    pattern = r'/Q(\d+)'
    match = re.search(pattern, link)
    return int(match.group(1))

def split_member_names(members_string):

    members_list = str(members_string).split()
    full_names_list = []
    i = 0
    while i < len(members_list):
        if i+1 < len(members_list):
            full_names_list.append(members_list[i] + " " + members_list[i+1])
            i += 2
        else:
            full_names_list.append(members_list[i])
            i += 1
    
    return full_names_list

def string_to_lowercase(text):
    return str(text).lower()

# Prints the log in console
def printInfo(msg):
    print(getDate(DATE_FORMAT_STRING) + ' ' +
          getTime(TIME_FORMAT_STRING) + ' INFO: ' + str(msg))
    
# Prints the log in console with Red Error
def printError(msg):
    CRED = '\033[91m'
    CEND = '\033[0m'
    print(CRED + getDate(DATE_FORMAT_STRING) + ' ' +
          getTime(TIME_FORMAT_STRING) + ' ERROR: ' + str(msg) + CEND)


# Prints the log in console with Green Success
def printSuccess(msg):
    CGREEN = '\033[92m'
    CEND = '\033[0m'
    print(CGREEN + getDate(DATE_FORMAT_STRING) + ' ' +
          getTime(TIME_FORMAT_STRING) + ' SUCCESS: ' + str(msg) + CEND)
    
def remove_white_spaces(text):
    return ' '.join(str(text).split())
import sys
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException

def read_file_newline_stripped(file_path):
    with open(file_path) as f:
        content = [word.strip() for word in f if word.strip() != '']
    return content

def append_file(file_name, content):
    with open(file_name, "a") as myfile:
        myfile.write(content + '\n')

def crawl(driver_path, binary_path, log_extraction_script, websites_to_crawl, page_load_timeout=10, file_write_timeout=4):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--no-sandbox')  
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('--chrome-binary=' + binary_path)
    chrome_options.binary_location = binary_path

    driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)
    driver.set_page_load_timeout(page_load_timeout)    
    for url_to_open in websites_to_crawl:
        try:
            print('Opening URL: ' + url_to_open)
            append_file('crawl.log', url_to_open)
            driver.get('http://127.0.0.1:8000/' + url_to_open)
            time.sleep(file_write_timeout)
            try:
                driver.execute_script(log_extraction_script)
            except BaseException as ex:
                print('[Main Frame] Something went wrong: ' + str(ex))
                pass
            time.sleep(1)

        except BaseException as ex:
            print('Something went wrong: ' + str(ex))
            pass
        finally:
            driver.quit()
            driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)
            driver.set_page_load_timeout(page_load_timeout)    


def main():
    driver_path = sys.argv[1]
    binary_path = sys.argv[2]
    original_url_file = sys.argv[3]
    url_file = sys.argv[3]
    original_websites_to_crawl = read_file_newline_stripped(original_url_file)
    websites_to_crawl = read_file_newline_stripped(url_file)

    while True:
        # driver_path = '/mnt/drive/work/adgraph/chromedriver' 
        # tested with ChromeDriver version 2.44
        # binary_path = '/media/umar/Elements/chromium_binary/chromium/src/out/Default/chrome'
        log_extraction_script = "document.createCDATASection('NOTVERYUNIQUESTRING');"

        crawl(driver_path, binary_path, log_extraction_script, websites_to_crawl)
        # logs will be stored in `rendering_stream` in home directory

        crawl_log = read_file_newline_stripped('crawl.log')
        if original_websites_to_crawl[-1] == crawl_log[-1]:
            print('All files crawled. Exiting now.')
            break
        else:
            websites_to_crawl = original_websites_to_crawl[original_websites_to_crawl.index(crawl_log[-1]):]

if __name__ == '__main__':
    main()
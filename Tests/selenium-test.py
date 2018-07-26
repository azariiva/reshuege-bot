from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get('https://rus-ege.sdamgia.ru/search')

elem = browser.find_element_by_name('search')  # Find the search box
elem.send_keys('(1)... (2)Например, в Голландии, Бельгии городское население составляет 90% всего населения. (3)Фактически эти страны превратились в города-государства. (4)К этому близки и другие крупные индустриальные страны. (5)Не исключение и наша страна: за последние десять лет процесс урбанизации достиг высокого уровня. (6)... можно сказать, что городская среда становится главной средой обитания человечества.' + Keys.RETURN)

sleep(5)

try:
    elem = browser.find_element_by_class_name('prob_maindiv')
    print(elem.text)
except Exception as err:
    print(err)
    

browser.quit()

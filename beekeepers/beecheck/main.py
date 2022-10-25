import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os, sys, time
import pickle
from selenium.webdriver.chrome.options import Options
import json

URL = 'https://ne.beecheck.org/map'

def main():
    driver = webdriver.Chrome()
    driver.set_window_rect(50,50,1600,1000)
    driver.get(URL)
    canvas = driver.find_element_by_id('map_canvas')

    pins = driver.find_elements_by_css_selector('marker')
    print(len(pins))
    sys.exit()
    # height = 704
    # width = 1600
    # action = webdriver.common.action_chains.ActionChains(driver)
    # for x in range(width):
    #     print(x)
    #     for y in range(height):
    #         print(y)
    #         action.move_to_element_with_offset(canvas, x,y).click().perform()


def main2():
    options = Options()
    options.headless = True

    browser = webdriver.Chrome(options=options)

    browser.get(URL)

    # https://apimirror.com/javascript/errors/cyclic_object_value
    jss = '''const getCircularReplacer = () => {
      const seen = new WeakSet();
      return (key, value) => {
        if (typeof value === "object" && value !== null) {
          if (seen.has(value)) {
            return;
          }
          seen.add(value);
        }
        return value;
      };
    };
    //https://stackoverflow.com/a/10455320/454773
    return JSON.stringify(driftwatch_map.data, getCircularReplacer());
    '''

    js_data = json.loads(browser.execute_script(jss))
    browser.close()
if __name__ == '__main__':
    main2()
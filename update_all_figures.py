import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

from tqdm import tqdm
from loguru import logger
from git import Repo
import glob


def find_by_css(driver, css_selector):
    return driver.find_elements(By.CSS_SELECTOR, css_selector)


def find_collapsed_folders(driver):
    return find_by_css(driver, "i.fa.fa-angle-right.fa-fw.file-tree-expand-icon")


def find_linked_figures(driver):
    return find_by_css(driver, "i.fa.fa-external-link-square.fa-rotate-180.linked-file-highlight")

def click_refresh(driver):
    find_by_css(driver, 'i.fa.fa-refresh.fa-fw')[0].click()
    
    
def refresh_figures_in_overleaf():
    logger.info("Refreshing figures in overleaf")
    options = Options()
    profile = FirefoxProfile("/home/pepijn/.mozilla/firefox/bps8ai8k.default-release")
    options.profile = profile
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")

    driver = webdriver.Firefox(options=options, service=Service(executable_path=GeckoDriverManager().install()))
    driver.get("https://www.overleaf.com/project/656a348f5874d8af8dacde27")
    time.sleep(3)
    driver.implicitly_wait(1)

    folders = find_collapsed_folders(driver)
    if not any(folders):
        logger.warning("No collapsed folders found. Is overleaf logged in in Firefox?")
    while any(folders):
        for folder in folders:
            folder.click()
            time.sleep(0.3)
        folders = find_collapsed_folders(driver)
    logger.info("All folders expanded")
    
    for linked_figure in tqdm(find_linked_figures(driver), desc="Updating figures"):
        linked_figure.click()
        time.sleep(1)
        
        last_updated = driver.find_element(By.CSS_SELECTOR, '[file="file"]').text
        click_refresh(driver)
        time.sleep(2)
        
        if last_updated == driver.find_element(By.CSS_SELECTOR, '[file="file"]').text:
            print("Figure already not updated, trying again, text was: ", last_updated)
            click_refresh(driver)
            time.sleep(2)

    driver.close()
    logger.info("Done refreshing figures in overleaf")

def commit_and_push():
    logger.info("Committing and pushing")
    repo = Repo("./")
    files_to_add = glob.glob("**/*.drawio", recursive=True)
    files_to_add.extend(glob.glob("**/*.pdf", recursive=True))
    
    if any(files_to_add):    
        repo.index.add(files_to_add)
        
        repo.index.commit("Update figures")
        origin = repo.remote(name='origin')
        origin.push(refspec=repo.active_branch, force=False).raise_if_error()
        logger.info(f"Done committing and pushing: {repo.head.commit}")
    else:
        logger.info("No files to add, exiting")

def main():
    commit_and_push()
    refresh_figures_in_overleaf()

if __name__ == "__main__":
    main()

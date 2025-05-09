import os
import requests
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from config import PAIRS, YEAR

def get_histdata_filename(pair, year, month):
    """
    Generate the expected filename format from HistData
    """
    return f"HISTDATA_COM_ASCII_{pair.upper()}_M1{year}{month:02d}.zip"

def get_histdata_url(pair, year, month):
    """
    Generate the URL for HistData downloads
    """
    return f"https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/{pair.upper()}/{year}/{month:02d}"

def download_with_selenium(pair, year, month):
    """
    Handle the download with Selenium using direct link strategy.
    """
    options = webdriver.ChromeOptions()
    download_dir = os.path.abspath("downloads")
    
    # Set up Chrome options for downloads
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Go to initial page
        url = get_histdata_url(pair, year, month)
        print(f"Navigating to: {url}")
        driver.get(url)
        sleep(2)

        # Step 2: Submit the initial form to get to the download page
        try:
            print("Looking for download form...")
            form = wait.until(EC.presence_of_element_located((By.ID, "download_form")))
            print("Found form, submitting...")
            form.submit()
            sleep(3)
        except Exception as e:
            print(f"Error with form: {e}")
            raise e

        # Step 3: On the download page, need to handle the file_down form
        try:
            # Click the download link which triggers the form
            download_link = wait.until(EC.presence_of_element_located((By.ID, "a_file")))
            print("Found download link, clicking...")
            
            # Execute the form submission directly using JavaScript
            script = '''
                document.getElementById('file_down').submit();
                return true;
            '''
            driver.execute_script(script)
            print("Submitted download form...")
            sleep(15)  # Wait for download to complete
            
        except Exception as e:
            print(f"Error with download form: {e}")
            # Try alternative method - direct form submission
            try:
                file_form = driver.find_element(By.ID, "file_down")
                if file_form:
                    print("Found download form, submitting directly...")
                    file_form.submit()
                    sleep(15)
            except Exception as inner_e:
                print(f"Error with alternative download method: {inner_e}")
                raise inner_e

    except Exception as e:
        print(f"\nError during download process: {e}")
        # Save screenshot and page source
        try:
            driver.save_screenshot(f"error_screenshot_{pair}_{year}{month:02d}.png")
            with open(f"error_page_{pair}_{year}{month:02d}.html", 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("Saved error screenshot and page source")
        except:
            pass
        raise e
    
    finally:
        driver.quit()

    # Verify the download with longer wait time
    base_filename = get_histdata_filename(pair, year, month)
    base_name = base_filename[:-4]  # Remove .zip extension
    
    # Check for possible variations of the filename
    possible_files = [
        os.path.join(download_dir, base_filename),
        os.path.join(download_dir, f"{base_name} (1).zip"),
        os.path.join(download_dir, f"{base_name} (2).zip"),
        os.path.join(download_dir, f"{base_name} (3).zip")
    ]
    
    # Wait longer for the file to appear (some downloads might be slower)
    max_wait = 45
    start_time = time.time()
    while time.time() - start_time < max_wait:
        for file_path in possible_files:
            if os.path.exists(file_path):
                print(f"✅ Successfully verified {os.path.basename(file_path)}")
                return True
        sleep(1)
    
    print(f"❌ No matching files found for {base_filename}")
    return False

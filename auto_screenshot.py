from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

# Setup Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# Open your Streamlit app
driver.get("http://localhost:8501")  

# Wait longer for Streamlit to fully load
time.sleep(8)

try:
    # Click Temperature Prediction tab
    temp_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-baseweb='tab'][contains(., 'Temperature Prediction')]"))
    )
    temp_tab.click()
    print("✅ Clicked Temperature Prediction tab")
    time.sleep(3)
    
    # Scroll down to see dropdowns
    driver.execute_script("window.scrollTo(0, 300)")
    time.sleep(2)
    
    # ========== SCREENSHOT 1: IMD Classical ==========
    print("📸 Taking screenshot 1: IMD Classical dropdown")
    
    # Find all select dropdowns
    all_selects = driver.find_elements(By.XPATH, "//div[@data-baseweb='select']")
    print(f"Found {len(all_selects)} select dropdowns")
    
    if len(all_selects) >= 2:
        # Click the Classical Algorithm dropdown (index 1, after Data Source)
        driver.execute_script("arguments[0].scrollIntoView(true);", all_selects[1])
        time.sleep(1)
        driver.execute_script("arguments[0].click();", all_selects[1])
        time.sleep(2)
        driver.save_screenshot("1_imd_classical_dropdown.png")
        print("✅ Saved: 1_imd_classical_dropdown.png")
        
        # Press ESC to close dropdown
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(2)
    
    # ========== SCREENSHOT 2: IMD Quantum ==========
    print("📸 Taking screenshot 2: IMD Quantum dropdown")
    
    # Re-find elements (Streamlit may have re-rendered)
    all_selects = driver.find_elements(By.XPATH, "//div[@data-baseweb='select']")
    
    if len(all_selects) >= 3:
        # Click the Quantum Algorithm dropdown
        driver.execute_script("arguments[0].scrollIntoView(true);", all_selects[2])
        time.sleep(1)
        driver.execute_script("arguments[0].click();", all_selects[2])
        time.sleep(2)
        driver.save_screenshot("2_imd_quantum_dropdown.png")
        print("✅ Saved: 2_imd_quantum_dropdown.png")
        
        # Press ESC
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(2)
    
    # ========== SWITCH TO NCMRWF ==========
    print("🔄 Switching to NCMRWF data source")
    
    # Re-find Data Source dropdown
    all_selects = driver.find_elements(By.XPATH, "//div[@data-baseweb='select']")
    driver.execute_script("arguments[0].scrollIntoView(true);", all_selects[0])
    time.sleep(1)
    driver.execute_script("arguments[0].click();", all_selects[0])
    time.sleep(1)
    
    # Click NCMRWF option
    ncmrwf_option = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'NCMRWF')]"))
    )
    ncmrwf_option.click()
    print("✅ Selected NCMRWF")
    time.sleep(4)  # Wait for UI to update
    
    # ========== SCREENSHOT 3: NCMRWF Classical ==========
    print("📸 Taking screenshot 3: NCMRWF Classical dropdown")
    
    # Re-find all dropdowns
    all_selects = driver.find_elements(By.XPATH, "//div[@data-baseweb='select']")
    
    if len(all_selects) >= 2:
        driver.execute_script("arguments[0].scrollIntoView(true);", all_selects[1])
        time.sleep(1)
        driver.execute_script("arguments[0].click();", all_selects[1])
        time.sleep(2)
        driver.save_screenshot("3_ncmrwf_classical_dropdown.png")
        print("✅ Saved: 3_ncmrwf_classical_dropdown.png")
        
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(2)
    
    # ========== SCREENSHOT 4: NCMRWF Quantum ==========
    print("📸 Taking screenshot 4: NCMRWF Quantum dropdown")
    
    # Re-find all dropdowns
    all_selects = driver.find_elements(By.XPATH, "//div[@data-baseweb='select']")
    
    if len(all_selects) >= 3:
        driver.execute_script("arguments[0].scrollIntoView(true);", all_selects[2])
        time.sleep(1)
        driver.execute_script("arguments[0].click();", all_selects[2])
        time.sleep(2)
        driver.save_screenshot("4_ncmrwf_quantum_dropdown.png")
        print("✅ Saved: 4_ncmrwf_quantum_dropdown.png")
    
    print("\n🎉 All screenshots captured successfully!")
    print("📂 Files saved in: D:\\QML_UI\\QML\\weather_prediction_of_all_doing_changes\\")

except Exception as e:
    print(f"❌ Error: {e}")
    driver.save_screenshot("error_screenshot.png")
    print("Saved error screenshot for debugging")

finally:
    time.sleep(2)
    driver.quit()
    print("✅ Browser closed")
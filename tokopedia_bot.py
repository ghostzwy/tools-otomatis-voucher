import time
import random
import string
import os
import sys
from datetime import datetime, timedelta

# --- DRIVER MANAGER ---
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager 
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService 
from selenium.webdriver.firefox.options import Options as FirefoxOptions 

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==========================================
# 1. SETUP PROFIL BROWSER
# ==========================================
base_path_edge = r"C:\Users\danan\AppData\Local\Microsoft\Edge\User Data" 
base_path_brave = r"C:\Users\danan\AppData\Local\BraveSoftware\Brave-Browser\User Data"
base_path_firefox = r"C:\Users\danan\AppData\Roaming\Mozilla\Firefox\Profiles"

profiles = {
    "1": {"type": "edge", "path": base_path_edge, "profile": "Default",   "name": "Edge 1 - Heirbiglow (English/AMPM)"},
    "2": {"type": "edge", "path": base_path_edge, "profile": "Profile 1", "name": "Edge 2 - Ciara Indonesia (English/AMPM)"},
    "3": {"type": "firefox", "path": base_path_firefox, "profile": "jtkkxnwv.default-release", "name": "Firefox - Harnisch (Indo/24H)"},
    "4": {"type": "edge", "path": base_path_edge, "profile": "Profile 5", "name": "Edge 4 - Ciara Malaysia (English/AMPM)"},
    "5": {"type": "brave", "path": base_path_brave, "profile": "Default", "name": "Brave - Heirbikids (English/AMPM)"},
}

# ==========================================
# 2. START BROWSER (DEBUG MODE)
# ==========================================
def start_browser(choice):
    selected = profiles.get(choice)
    if not selected: return None

    # Auto Kill
    print(f"🔪 Mematikan proses {selected['type']} lama...")
    try:
        if selected['type'] == 'edge': os.system("taskkill /F /IM msedge.exe >nul 2>&1")
        elif selected['type'] == 'firefox': os.system("taskkill /F /IM firefox.exe >nul 2>&1")
        elif selected['type'] == 'brave': os.system("taskkill /F /IM brave.exe >nul 2>&1")
    except Exception as e:
        print(f"⚠️ Gagal kill process (Abaikan): {e}")
        
    time.sleep(2) 

    print(f"🚀 Gas buka {selected['name']}...")
    
    # --- EDGE ---
    if selected['type'] == 'edge':
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument(f"user-data-dir={selected['path']}")
        options.add_argument(f"profile-directory={selected['profile']}")
        options.add_experimental_option("detach", True)
        options.add_argument("--log-level=3")
        
        try:
            print("   🔧 Sedang install/cek Edge Driver...")
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
            print("   ✅ Edge Berhasil Terbuka!")
            
        except Exception as e:
            print(f"\n❌ ERROR FATAL EDGE: {e}")
            print("💡 Tips: Coba update Edge manual, atau hapus folder 'msedgedriver' lama.")
            return None

    # --- FIREFOX ---
    elif selected['type'] == 'firefox':
        options = FirefoxOptions()
        full_path = os.path.join(selected['path'], selected['profile'])
        options.add_argument("-profile")
        options.add_argument(full_path)
        
        try:
            print("   🔧 Sedang install/cek Gecko Driver...")
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            print("   ✅ Firefox Berhasil Terbuka!")
            
        except Exception as e:
            print(f"\n❌ ERROR FATAL FIREFOX: {e}")
            return None
        
    # --- BRAVE ---
    elif selected['type'] == 'brave':
        options = ChromeOptions()
        options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        options.add_argument(f"user-data-dir={selected['path']}")
        options.add_argument(f"profile-directory={selected['profile']}")
        options.add_experimental_option("detach", True) 
        options.add_argument("--log-level=3")
        
        try:
            print("   🔧 Sedang install/cek Chrome Driver (Brave)...")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            print("   ✅ Brave Berhasil Terbuka!")
            
        except Exception as e:
            print(f"\n❌ ERROR FATAL BRAVE: {e}")
            return None
    
    driver.maximize_window()
    return driver

# ==========================================
# 3. FUNGSI ISI TEXT (UNIVERSAL)
# ==========================================
def fill_input_xpath(driver, xpath, value, description):
    try:
        elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        time.sleep(0.5)
        
        # Cara hapus bersih: Klik -> Ctrl+A -> Backspace
        elem.click()
        elem.send_keys(Keys.CONTROL + "a")
        elem.send_keys(Keys.BACKSPACE)
        time.sleep(0.2)
        elem.send_keys(value)
        elem.send_keys(Keys.ENTER) 
        print(f"   ✅ {description} diisi: {value}")
        return True
    except Exception as e:
        print(f"   ⚠️ Gagal isi {description}: {e}")
        return False

# ==========================================
# 4. LOGIKA UTAMA (DUAL LANGUAGE SUPPORT)
# ==========================================
def run_tiktok(driver, search_target, new_name, new_code, raw_tgl_start, browser_choice):
    
    # --- A. SETUP FORMAT WAKTU ---
    dt_start = datetime.strptime(f"{raw_tgl_start}", "%d-%m-%Y")
    dt_end = dt_start + timedelta(days=25)

    is_english = False
    
    if browser_choice == '3': 
        # === FIREFOX (INDONESIA) ===
        print("🇮🇩 Mode: INDONESIA (24 Jam)")
        is_english = False
        date_start_str = dt_start.strftime("%d/%m/%Y")
        date_end_str = dt_end.strftime("%d/%m/%Y")
        time_start_str = "06:00"
        time_end_str = "23:59"
        xpath_start_label = "Waktu mulai"
        xpath_end_label = "Waktu selesai"
        
    else:
        # === EDGE & BRAVE (INGGRIS) ===
        print("🇺🇸 Mode: ENGLISH (AM/PM)")
        is_english = True
        date_start_str = dt_start.strftime("%m/%d/%Y")
        date_end_str = dt_end.strftime("%m/%d/%Y")
        time_start_str = "06:00 AM"
        time_end_str = "11:59 PM"
        xpath_start_label = "Start time"
        xpath_end_label = "End time"

    # --- B. BUKA WEBSITE & SEARCH ---
    url_tiktok = "https://seller-id.tiktok.com/marketing/promotion/tools/voucher/list" 
    driver.get(url_tiktok)
    print("⏳ Loading TikTok Shop...")
    time.sleep(5) 

    print(f"🔎 Mencari Voucher: '{search_target}'")
    try:
        # Input Search
        fill_input_xpath(driver, "//input[contains(@placeholder, 'Filter')]", search_target, "Search Box")
        time.sleep(3) 

        # Klik Dropdown Action
        dropdown_btn = driver.find_element(By.XPATH, "//tbody/tr[1]//button[contains(@class, 'theme-arco-btn-icon-only')]")
        driver.execute_script("arguments[0].click();", dropdown_btn)
        time.sleep(1)

        # Klik Duplicate
        dup_xpath = "//li[contains(text(), 'Duplicate') or contains(text(), 'Duplikasi')]"
        driver.find_element(By.XPATH, dup_xpath).click()
        print("   ✅ Tombol Duplikat diklik!")
        
    except Exception as e:
        print(f"❌ Gagal Search/Duplikat: {e}")
        print("⚠️ Pastikan kamu sudah LOGIN MANUAL di browser ini!")
        return

    print("⏳ Nunggu form edit kebuka...")
    time.sleep(5)

    # --- C. ISI FORMULIR (SESUAI BAHASA) ---
    print(f"📝 Mengisi Data Baru ({'English' if is_english else 'Indo'})...")

    # 1. GANTI NAMA VOUCHER
    xpath_name = "//label[contains(text(),'Promotion name') or contains(text(),'Nama promosi')]/../..//input"
    fill_input_xpath(driver, xpath_name, new_name, "Nama Voucher")

    # 2. GANTI KODE VOUCHER
    xpath_code = "//input[@maxlength='5']" 
    fill_input_xpath(driver, xpath_code, new_code, "Kode Voucher")

    # 3. ISI TANGGAL & JAM
    # Start Time
    xpath_date_start = f"//label[contains(., '{xpath_start_label}')]/../..//div[contains(@class, 'date-picker')]//input"
    fill_input_xpath(driver, xpath_date_start, date_start_str, "Tgl Mulai")
    
    xpath_time_start = f"//label[contains(., '{xpath_start_label}')]/../..//div[contains(@class, 'time-picker')]//input"
    fill_input_xpath(driver, xpath_time_start, time_start_str, "Jam Mulai")

    time.sleep(1)

    # End Time
    xpath_date_end = f"//label[contains(., '{xpath_end_label}')]/../..//div[contains(@class, 'date-picker')]//input"
    fill_input_xpath(driver, xpath_date_end, date_end_str, "Tgl Selesai")
    
    xpath_time_end = f"//label[contains(., '{xpath_end_label}')]/../..//div[contains(@class, 'time-picker')]//input"
    fill_input_xpath(driver, xpath_time_end, time_end_str, "Jam Selesai")

    print("\n✋ BERHENTI DULU. Cek manual di browser, lalu klik Submit sendiri ya.")

# ==========================================
# 5. MENU UTAMA
# ==========================================
if __name__ == "__main__":
    print("\n=== BOT TIKTOK SHOP (DEBUG MODE) ===")
    
    search_target = input("1. Nama Voucher Lama (yg mau dicari/duplikat): ")
    if not search_target: search_target = "Diskon 25rb"

    new_name = input("2. Nama Voucher BARU: ")
    if not new_name: new_name = "Diskon Spesial"

    new_code = input("3. Kode Voucher BARU (5 Digit): ")
    if not new_code: new_code = "TEST1"

    print("\n4. Tanggal Mulai (DD-MM-YYYY)")
    raw_tgl = input("   Ketik Tanggal (Misal 12-12-2025): ")
    if not raw_tgl: raw_tgl = datetime.now().strftime("%d-%m-%Y")

    print("\n5. Pilih Browser:")
    for k, v in profiles.items(): print(f"   {k}. {v['name']}")
    pilihan = input("   Nomor Browser: ")

    driver = start_browser(pilihan)

    if driver:
        try:
            run_tiktok(driver, search_target, new_name, new_code, raw_tgl, pilihan)
        except Exception as e:
            print(f"❌ Error Runtime: {e}")
        finally:
            print("\n✅ Script Selesai.")
    else:
        print("\n❌ Gagal membuka browser. Cek pesan error di atas.")
import time
import random
import string
import os
import sys
from datetime import datetime, timedelta

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

# --- TAMBAHKAN KEMBALI IMPORT DRIVER MANAGER UNTUK FIREFOX/BRAVE FALLBACK ---
from webdriver_manager.firefox import GeckoDriverManager 
from webdriver_manager.chrome import ChromeDriverManager


# ==========================================
# 1. SETUP PROFIL BROWSER
# ==========================================
base_path_edge = r"C:\Users\danan\AppData\Local\Microsoft\Edge\User Data" 
base_path_brave = r"C:\Users\danan\AppData\Local\BraveSoftware\Brave-Browser\User Data"
base_path_firefox = r"C:\Users\danan\AppData\Roaming\Mozilla\Firefox\Profiles"

profiles = {
    "1": {"type": "edge", "path": base_path_edge, "profile": "Default",   "name": "Edge 1 - HERB25SEN"}, 
    "2": {"type": "edge", "path": base_path_edge, "profile": "Profile 1", "name": "Edge 2 - Ciara Indonesia"},
    "3": {"type": "firefox", "path": base_path_firefox, "profile": "jtkkxnwv.default-release", "name": "Firefox - Harnisch"},
    "4": {"type": "edge", "path": base_path_edge, "profile": "Profile 5", "name": "Edge 4 - Ciara Malaysia"}, 
    "5": {"type": "brave", "path": base_path_brave, "profile": "Default", "name": "Brave - Heirbikids"},
}

# ==========================================
# 2. START BROWSER (DRIVER FALLBACK)
# ==========================================
def start_browser(choice):
    selected = profiles.get(choice)
    if not selected: return None

    # Auto Kill
    print(f"🔪 Matiin proses {selected['type']} lama...")
    try:
        if selected['type'] == 'edge': os.system("taskkill /F /IM msedge.exe >nul 2>&1")
        elif selected['type'] == 'firefox': os.system("taskkill /F /IM firefox.exe >nul 2>&1")
        elif selected['type'] == 'brave': os.system("taskkill /F /IM brave.exe >nul 2>&1")
    except Exception as e:
        print(f"⚠️ Gagal kill process (Abaikan): {e}")
        
    time.sleep(2) 

    print(f"🚀 OTW buka {selected['name']}...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # --- EDGE ---
    if selected['type'] == 'edge':
        driver_path = os.path.join(current_dir, "msedgedriver.exe")
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument(f"user-data-dir={selected['path']}")
        options.add_argument(f"profile-directory={selected['profile']}")
        options.add_experimental_option("detach", True)
        options.add_argument("--log-level=3")
        
        if not os.path.exists(driver_path):
            print("\n❌ ERROR: File 'msedgedriver.exe' TIDAK DITEMUKAN di folder script!")
            return None
        
        try:
            print("   🔧 Pakai driver LOKAL: msedgedriver.exe")
            service = EdgeService(driver_path)
            driver = webdriver.Edge(service=service, options=options)
        except Exception as e:
            print(f"❌ Yah gagal buka Edge. Error: {e}")
            return None

    # --- FIREFOX (FALLBACK AUTO-DOWNLOAD) ---
    elif selected['type'] == 'firefox':
        driver_path = os.path.join(current_dir, "geckodriver.exe")
        options = FirefoxOptions()
        full_path = os.path.join(selected['path'], selected['profile'])
        options.add_argument("-profile")
        options.add_argument(full_path)
        
        try:
            if os.path.exists(driver_path):
                print("   🔧 Pakai driver LOKAL: geckodriver.exe")
                service = FirefoxService(driver_path)
            else:
                print("   🌐 Driver LOKAL tidak ada. Auto-download Geckodriver (butuh internet)...")
                service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
        except Exception as e:
            print(f"❌ Gagal buka Firefox: {e}")
            return None
        
    # --- BRAVE (FALLBACK AUTO-DOWNLOAD) ---
    elif selected['type'] == 'brave':
        driver_path = os.path.join(current_dir, "chromedriver.exe")
        options = ChromeOptions()
        options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        options.add_argument(f"user-data-dir={selected['path']}")
        options.add_argument(f"profile-directory={selected['profile']}")
        options.add_experimental_option("detach", True) 
        options.add_argument("--log-level=3")
        
        try:
            if os.path.exists(driver_path):
                print("   🔧 Pakai driver LOKAL: chromedriver.exe")
                service = ChromeService(driver_path)
            else:
                print("   🌐 Driver LOKAL tidak ada. Auto-download Chromedriver (butuh internet)...")
                service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"❌ Gagal buka Brave: {e}")
            return None
    
    driver.maximize_window()
    return driver

# ==========================================
# 3. FUNGSI ISI TEXT (UNIVERSAL)
# ==========================================
def fill_input_xpath(driver, xpath, value, description):
    try:
        elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        time.sleep(0.5)
        
        elem.click()
        elem.send_keys(Keys.CONTROL + "a")
        elem.send_keys(Keys.BACKSPACE)
        time.sleep(0.2)
        elem.send_keys(value)
        elem.send_keys(Keys.ENTER) 
        print(f"   ✅ {description}: {value}")
        return True
    except Exception as e:
        print(f"   ⚠️ Gagal isi {description}: {e}")
        return False

# ==========================================
# 4. LOGIKA UTAMA TIKTOK
# ==========================================
def run_tiktok(driver, search_target, new_name, new_code, raw_tgl_start, browser_choice):
    
    # --- A. SETUP FORMAT WAKTU ---
    dt_start = datetime.strptime(f"{raw_tgl_start}", "%d-%m-%Y")
    dt_end = dt_start + timedelta(days=25)
    
    # Deteksi Format Berdasarkan Browser Choice
    if browser_choice == '4': 
        # === EDGE 4 (CIARA MALAYSIA / AM/PM) ===
        print("🇲🇾 Mode: MALAYSIA (AM/PM - MM/DD/YYYY)")
        date_start_str = dt_start.strftime("%m/%d/%Y") # MM/DD/YYYY
        date_end_str = dt_end.strftime("%m/%d/%Y")
        time_start_str = "06:00 AM"
        time_end_str = "11:59 PM"
        xpath_start_label = "Start time" 
        xpath_end_label = "End time" 
        
    else:
        # === INDONESIA GRUP (24H / DD/MM/YYYY) ===
        # Meliputi Edge 1, Edge 2, Firefox, Brave
        print("🇮🇩 Mode: INDONESIA (24 Jam)")
        date_start_str = dt_start.strftime("%d/%m/%Y") # DD/MM/YYYY
        date_end_str = dt_end.strftime("%d/%m/%Y")
        time_start_str = "06:00"
        time_end_str = "23:59"
        
        # Label disesuaikan
        if browser_choice == '3':
            # Firefox (Indo)
            xpath_start_label = "Waktu mulai" 
            xpath_end_label = "Waktu selesai"
        else:
            # Edge 1, Edge 2, Brave (Biasanya English di form meskipun domain ID)
            xpath_start_label = "Start time" 
            xpath_end_label = "End time"


    # --- B. BUKA WEBSITE & SEARCH ---
    url_tiktok = "https://seller-id.tiktok.com/marketing/promotion/tools/voucher/list" 
    driver.get(url_tiktok)
    
    print("⏳ Nunggu halaman TikTok siap...")
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Filter')]")))
    except:
        print("❌ Gagal memuat halaman utama TikTok.")
        return
    
    # 1. SEARCH & DUPLIKAT
    print(f"🔎 Mencari Voucher: '{search_target}'")
    try:
        # Input Search Box (Bilingual placeholder search)
        search_xpath = "//input[contains(@placeholder, 'Filter') or contains(@placeholder, 'Filter berdasarkan')]"
        if not fill_input_xpath(driver, search_xpath, search_target, "Search Box"):
            return
        
        # Tekan ENTER
        driver.find_element(By.XPATH, search_xpath).send_keys(Keys.ENTER)
        print("   ✅ Enter ditekan. Nunggu hasil filter (5 detik)...")
        time.sleep(5) 
        
        # Explicit Wait untuk memastikan BARIS PERTAMA
        row_with_target = f"//tbody/tr[1][contains(., '{search_target}')]"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, row_with_target)))
        print("   ✅ Hasil filter ditemukan di baris pertama.")

        # Klik Tombol Panah Dropdown
        dropdown_xpath = "//tbody/tr[1]//button[contains(@class, 'theme-arco-btn-icon-only')]"
        dropdown_btn = driver.find_element(By.XPATH, dropdown_xpath)
        driver.execute_script("arguments[0].click();", dropdown_btn)
        time.sleep(1)

        # Klik Duplicate
        dup_xpath = "//li[contains(text(), 'Duplicate') or contains(text(), 'Duplikasi')]"
        driver.find_element(By.XPATH, dup_xpath).click()
        print("   ✅ Tombol Duplikat diklik!")
        
    except Exception as e:
        print(f"❌ Gagal Search/Duplikat: {e}")
        print("⚠️ Pastikan nama voucher lama BENAR dan sudah ada di halaman list!")
        return

    print("⏳ Nunggu halaman edit kebuka (5 detik)...")
    time.sleep(5)

    # --- C. ISI FORMULIR ---
    print(f"📝 Mengisi Data Baru...")

    # 1. GANTI NAMA VOUCHER
    xpath_name = "//label[contains(text(),'Promotion name') or contains(text(),'Nama promosi')]/../..//input"
    fill_input_xpath(driver, xpath_name, new_name, "Nama Voucher")

    # 2. GANTI KODE VOUCHER
    xpath_code = "//input[@maxlength='5']" 
    fill_input_xpath(driver, xpath_code, new_code, "Kode Voucher")

    # 3. ISI TANGGAL & JAM
    
    # Start Time - Tanggal
    xpath_date_start = f"//label[contains(., '{xpath_start_label}')]/../..//div[contains(@class, 'date-picker')]//input"
    fill_input_xpath(driver, xpath_date_start, date_start_str, "Tgl Mulai")
    
    # Start Time - Jam
    xpath_time_start = f"//label[contains(., '{xpath_start_label}')]/../..//div[contains(@class, 'time-picker')]//input"
    fill_input_xpath(driver, xpath_time_start, time_start_str, "Jam Mulai")

    time.sleep(1)

    # End Time - Tanggal
    xpath_date_end = f"//label[contains(., '{xpath_end_label}')]/../..//div[contains(@class, 'date-picker')]//input"
    fill_input_xpath(driver, xpath_date_end, date_end_str, "Tgl Selesai")
    
    # End Time - Jam
    xpath_time_end = f"//label[contains(., '{xpath_end_label}')]/../..//div[contains(@class, 'time-picker')]//input"
    fill_input_xpath(driver, xpath_time_end, time_end_str, "Jam Selesai")

    print("\n✋ BERHENTI DULU. Cek manual di browser, lalu klik Submit sendiri ya.")

# ==========================================
# 5. MENU UTAMA
# ==========================================
if __name__ == "__main__":
    print("\n=== BOT TIKTOK SHOP (FINAL TIME FIX) ===")
    
    search_target = input("1. Nama Voucher Lama (yg mau dicari/duplikat): ")
    if not search_target: search_target = "Diskon 25rb"

    new_name = input("2. Nama Voucher BARU: ")
    if not new_name: new_name = "Diskon Spesial"

    new_code = input("3. Kode Voucher BARU (5 Digit): ")
    if not new_code: new_code = "TEST1"

    print("\n4. Tanggal Mulai (DD-MM-YYYY)")
    raw_tgl = input("   Ketik Tanggal (Misal 15-12-2025): ")
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
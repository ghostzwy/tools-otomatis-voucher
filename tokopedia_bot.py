import time
import random
import string
import os
import sys

# --- Import Library Selenium & Driver Manager ---
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
from selenium.webdriver.common.action_chains import ActionChains

# ==========================================
# 1. SETUP PROFIL BROWSER (SAMA PERSIS KAYA SHOPEE)
# ==========================================
base_path_edge = r"C:\Users\danan\AppData\Local\Microsoft\Edge\User Data" 
base_path_brave = r"C:\Users\danan\AppData\Local\BraveSoftware\Brave-Browser\User Data"
base_path_firefox = r"C:\Users\danan\AppData\Roaming\Mozilla\Firefox\Profiles"

profiles = {
    # Edge 1: Heirbiglow
    "1": {"type": "edge", "path": base_path_edge, "profile": "Default",   "name": "Edge 1 - Heirbiglow"},
    # Edge 2: Ciara Indonesia
    "2": {"type": "edge", "path": base_path_edge, "profile": "Profile 1", "name": "Edge 2 - Ciara Indonesia"},
    # Firefox: Harnisch
    "3": {"type": "firefox", "path": base_path_firefox, "profile": "jtkkxnwv.default-release", "name": "Firefox - Harnisch"},
    # Edge 4: Ciara Malaysia
    "4": {"type": "edge", "path": base_path_edge, "profile": "Profile 5", "name": "Edge 4 - Ciara Malaysia"},
    # Brave: Heirbikids
    "5": {"type": "brave", "path": base_path_brave, "profile": "Default", "name": "Brave - Heirbikids"},
}

# ==========================================
# 2. FUNGSI NYALAIN BROWSER
# ==========================================
def start_browser(choice):
    selected = profiles.get(choice)
    if not selected:
        print("❌ Pilihan browser gak ada bro!")
        return None

    # AUTO KILL
    print(f"🔪 Matiin proses {selected['type']} dulu biar aman...")
    if selected['type'] == 'edge':
        os.system("taskkill /F /IM msedge.exe >nul 2>&1")
    elif selected['type'] == 'firefox':
        os.system("taskkill /F /IM firefox.exe >nul 2>&1")
    elif selected['type'] == 'brave':
        os.system("taskkill /F /IM brave.exe >nul 2>&1")
    time.sleep(2) 

    print(f"🚀 Gas buka {selected['name']}...")
    load_timeout = 20
    
    # --- EDGE ---
    if selected['type'] == 'edge':
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument(f"user-data-dir={selected['path']}")
        options.add_argument(f"profile-directory={selected['profile']}")
        options.add_experimental_option("detach", True) 
        options.add_argument("--log-level=3") 
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        try:
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        except: return None

    # --- FIREFOX ---
    elif selected['type'] == 'firefox':
        options = FirefoxOptions()
        full_profile_path = os.path.join(selected['path'], selected['profile'])
        options.add_argument("-profile")
        options.add_argument(full_profile_path)
        try:
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        except: return None
        
    # --- BRAVE ---
    elif selected['type'] == 'brave':
        options = ChromeOptions()
        options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        options.add_argument(f"user-data-dir={selected['path']}")
        options.add_argument(f"profile-directory={selected['profile']}")
        options.add_experimental_option("detach", True) 
        options.add_argument("--log-level=3")
        try:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        except: return None
    
    driver.set_page_load_timeout(load_timeout)
    driver.maximize_window()
    return driver

# ==========================================
# 3. LOGIKA TIKTOK SHOP (SESUAI HTML)
# ==========================================
def run_tiktok(driver, target_name):
    # Link Voucher TikTok (Pastikan ini bener)
    url_tiktok = "https://seller-id.tiktok.com/marketing/promotion/tools/voucher/list" 
    
    print("\n--- 🎵 MASUK TIKTOK SHOP ---")
    driver.get(url_tiktok)
    
    print("⏳ Nunggu loading halaman...")
    time.sleep(5) 

    # 1. SEARCH VOUCHER
    print(f"🔎 Nyari voucher: '{target_name}'")
    try:
        # XPath sesuai HTML yang Mas Danang kirim (placeholder='Filter by promotion name')
        search_xpath = "//input[@placeholder='Filter by promotion name']"
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_xpath)))
        
        search_box.click()
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.BACKSPACE)
        search_box.send_keys(target_name)
        time.sleep(1)
        search_box.send_keys(Keys.ENTER)
        print("   ✅ Udah diketik & Enter. Nunggu filter...")
        time.sleep(3)
        
    except Exception as e:
        print(f"   ❌ Gagal di kotak Search: {e}")
        return

    # 2. KLIK DROPDOWN (PANAH DI KOLOM ACTION)
    print("🖱️ Nyari tombol Dropdown...")
    try:
        # Cari baris tabel yang ada nama vouchernya, terus cari tombol dropdown di baris itu
        # HTML tombol: <button data-tid="m4b_dropdown_button" ...>
        row_xpath = f"//tr[contains(., '{target_name}')]//button[@data-tid='m4b_dropdown_button']"
        
        dropdown_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, row_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_btn)
        time.sleep(1)
        
        dropdown_btn.click()
        print("   ✅ Dropdown kebuka!")
        time.sleep(1)
        
        # 3. KLIK MENU 'DUPLICATE' / 'DUPLIKASI'
        print("   👀 Klik menu Duplicate...")
        # Menu biasanya muncul di layer atas (bukan di dalam tabel), kita cari text-nya aja
        duplicate_xpath = "//li[contains(text(), 'Duplicate') or contains(text(), 'Duplikasi')]"
        dup_menu = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, duplicate_xpath)))
        dup_menu.click()
        print("   ✅ MENU DUPLICATE DIKLIK!")
        
        print("\n⏳ Lagi loading halaman edit...")
        time.sleep(5)
        
        # --- STOPPOINT ---
        print("\n🛑 STOP DULU MAS!")
        print("Sekarang form Edit Voucher pasti udah kebuka.")
        print("Tolong kirimkan HTML (Inspect Element) dari:")
        print("1. Kolom **Nama Voucher**")
        print("2. Kolom **Kode Voucher** (Claim Code)")
        print("3. Kolom **Tanggal Mulai & Selesai** (Penting, karena TikTok beda sama Shopee)")
        print("4. Tombol **Submit/Konfirmasi** di bawah")
        
    except Exception as e:
        print(f"   ❌ Gagal klik duplikat: {e}")

# ==========================================
# 4. MENU UTAMA
# ==========================================
if __name__ == "__main__":
    print("\n=== BOT TIKTOK SHOP (CONFIG SAMA KAYA SHOPEE) ===")
    
    target = input("Nama Voucher yang mau diduplikat (Cth: Diskon 25rb): ")
    if not target: target = "Diskon 25rb"

    print("\nPilih Browser:")
    for k, v in profiles.items(): print(f"   {k}. {v['name']}")
    pilihan = input("Nomor Browser: ")

    driver = start_browser(pilihan)

    if driver:
        try:
            run_tiktok(driver, target)
        except Exception as e:
            print(f"❌ Error: {e}")
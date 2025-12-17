import time
import random
import string
import re
from datetime import datetime, timedelta
import os

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

# ==========================================
# 1. SETUP PROFIL BROWSER (BASECAMP)
# ==========================================
base_path_edge = r"C:\Users\danan\AppData\Local\Microsoft\Edge\User Data" 
base_path_brave = r"C:\Users\danan\AppData\Local\BraveSoftware\Brave-Browser\User Data"
base_path_firefox = r"C:\Users\danan\AppData\Roaming\Mozilla\Firefox\Profiles"

profiles = {
    "1": {"type": "edge", "path": base_path_edge, "profile": "Default",   "name": "Edge 1 - HERB25SEN"},
    "2": {"type": "edge", "path": base_path_edge, "profile": "Profile 1", "name": "Edge 2 - Ciara Indonesia"},
    "3": {"type": "firefox", "path": base_path_firefox, "profile": "jtkkxnwv.default-release", "name": "Firefox - Harnisch"},
    "4": {"type": "edge", "path": base_path_edge, "profile": "Profile 4", "name": "Edge 4 - Ciara Malaysia"},
    "5": {"type": "brave", "path": base_path_brave, "profile": "Default", "name": "Brave - Heirbikids"},
}

# ==========================================
# 2. FUNGSI NYALAIN BROWSER (THE ENGINE)
# ==========================================
def start_browser(choice):
    selected = profiles.get(choice)
    if not selected:
        print("❌ Waduh, pilihan browsernya ga ada di menu, bang!")
        return None

    if selected['type'] == 'edge':
        print("🔪 Matiin paksa Edge dulu biar fresh...")
        try: os.system("taskkill /F /IM msedge.exe >nul 2>&1")
        except: pass
    elif selected['type'] == 'firefox':
        print("🔪 Matiin paksa Firefox dulu...")
        try: os.system("taskkill /F /IM firefox.exe >nul 2>&1")
        except: pass
    elif selected['type'] == 'brave':
        print("🔪 Matiin paksa Brave dulu...")
        try: os.system("taskkill /F /IM brave.exe >nul 2>&1")
        except: pass
        
    time.sleep(2)

    print(f"🚀 OTW buka {selected['name']}...")
    print(f"📂 Pake folder profil: {selected['profile']}")
    load_timeout = 60
    
    if selected['type'] == 'edge':
        local_edge_driver = os.path.join(os.path.dirname(os.path.abspath(__file__)), "msedgedriver.exe")
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument(f"user-data-dir={selected['path']}")
        options.add_argument(f"profile-directory={selected['profile']}")
        options.add_experimental_option("detach", True) 
        options.add_argument("--log-level=3") 
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        try:
            if os.path.exists(local_edge_driver):
                driver = webdriver.Edge(service=EdgeService(local_edge_driver), options=options)
            else:
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        except Exception as e:
            print(f"❌ Yah gagal buka Edge: {e}")
            return None

    elif selected['type'] == 'firefox':
        options = FirefoxOptions()
        full_profile_path = os.path.join(selected['path'], selected['profile'])
        if not os.path.exists(full_profile_path): return None
        options.add_argument("-profile")
        options.add_argument(full_profile_path)
        try:
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        except: return None
        
    elif selected['type'] == 'brave':
        options = ChromeOptions()
        options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        options.add_argument(f"user-data-dir={selected['path']}")
        options.add_argument(f"profile-directory={selected['profile']}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu") 
        options.add_experimental_option("detach", True) 
        options.add_argument("--log-level=3")
        options.add_argument("--disable-blink-features=AutomationControlled")
        try:
            driver_manual_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
            if os.path.exists(driver_manual_path):
                service = ChromeService(executable_path=driver_manual_path)
            else:
                driver_downloaded = ChromeDriverManager(driver_version="143.0.7499.40").install()
                service = ChromeService(driver_downloaded)
            driver = webdriver.Chrome(service=service, options=options)
        except: return None
    
    driver.set_page_load_timeout(load_timeout)
    driver.maximize_window()
    return driver

# ==========================================
# 3. ALAT BANTU (SUPPORT SYSTEM)
# ==========================================
def tutup_popup(driver):
    print("🔒 Coba tutup popup/notifikasi kalau ada...")
    try:
        close_btns = driver.find_elements(By.XPATH, 
            "//button[contains(@class,'close')] | "
            "//div[contains(@class,'close')] | "
            "//span[text()='×'] | "
            "//button[contains(text(),'Nanti') or contains(text(),'Later')] | "
            "//button[contains(text(),'Tutup') or contains(text(),'Close')] | "
            "//button[contains(text(),'OK')]"
        )
        for btn in close_btns:
            if btn.is_displayed():
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(1)
    except: pass

def pindah_ke_tab_shopee(driver, browser_choice):
    if browser_choice == '4':
        target_url = "https://seller.shopee.com.my/portal/marketing/vouchers/list"
    else:
        target_url = "https://seller.shopee.co.id/portal/marketing/vouchers/list"
    
    print(f"🔎 Menuju halaman voucher: {target_url}")
    try:
        if "shopee" in driver.current_url.lower(): 
            return
        for tab in driver.window_handles:
            driver.switch_to.window(tab)
            if "shopee" in driver.current_url.lower():
                print(f"✅ Tab Shopee sudah ditemukan: {driver.title}")
                return
        driver.get(target_url)
        if browser_choice == '4':
            print("   Malaysia loading lambat, kasih napas 5 detik...")
            time.sleep(5)
    except Exception as e:
        print(f"⚠️ Gagal buka URL: {e}")
        driver.get(target_url)

def generate_kode_suffix(length=3):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

# ==========================================
# 4. LOGIKA KALENDER — 2 ARRAY + FIX SEMUA SINGKATAN BULAN
# ==========================================
def robot_klik_kalender_shopee(driver, element_id, target_date_obj, target_time_str):
    print(f"   🗓️ Otw setting {element_id.upper()}: {target_date_obj.strftime('%d-%m-%Y')} {target_time_str}")
    
    # ARRAY 1: Singkatan bulan
    SHORT_MONTHS = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Mei": 5, "Jun": 6,
        "Jul": 7, "Ags": 8, "Agu": 8, "Aug": 8,
        "Sep": 9, "Sept": 9, "Okt": 10, "Oct": 10,
        "Nov": 11, "Des": 12, "Dec": 12
    }
    
    # ARRAY 2: Nama lengkap
    FULL_MONTHS = {
        "January":1, "February":2, "March":3, "April":4, "May":5, "June":6,
        "July":7, "August":8, "September":9, "October":10, "November":11, "December":12
    }
    
    month_map = {**SHORT_MONTHS, **FULL_MONTHS}

    try:
        try:
            driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(0.5)
        except: pass

        xpath_target = f"//div[@id='{element_id}']//input"
        wrapper = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_target)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", wrapper)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", wrapper)
        time.sleep(1.0) 

        tgt_d = int(target_date_obj.day)
        tgt_y = int(target_date_obj.year)
        tgt_m = target_date_obj.month
        
        for _ in range(50):
            try:
                visible_headers = [h for h in driver.find_elements(By.CLASS_NAME, "date-box") if h.is_displayed()]
                if not visible_headers:
                    print("      ⚠️ Header kalender ga nongol!")
                    break
                
                header_elem = visible_headers[-1]
                header_text = header_elem.text.strip()
                
                found_year = re.search(r'\d{4}', header_text)
                if not found_year: break
                curr_y_int = int(found_year.group())
                
                found_month = re.search(r'^[A-Za-z]+', header_text)
                if not found_month: break
                curr_m_str = found_month.group()
                curr_m_int = month_map.get(curr_m_str, 0)

                if curr_m_int == 0:
                    print(f"      ⚠️ Bulan tidak dikenali: {curr_m_str}")
                    break

                active_panel = driver.find_elements(By.CLASS_NAME, "eds-react-date-picker__header")[-1]
                nav_btns = active_panel.find_elements(By.XPATH, ".//div[contains(@class, 'btn-arrow-default')]")
                
                if len(nav_btns) < 4: break

                btn_prev_year  = nav_btns[0]
                btn_prev_month = nav_btns[1]
                btn_next_month = nav_btns[2]
                btn_next_year  = nav_btns[3]

                if curr_y_int > tgt_y:
                    driver.execute_script("arguments[0].click();", btn_prev_year)
                    time.sleep(0.3)
                    continue 
                elif curr_y_int < tgt_y:
                    driver.execute_script("arguments[0].click();", btn_next_year)
                    time.sleep(0.3)
                    continue

                if curr_m_int > tgt_m:
                    driver.execute_script("arguments[0].click();", btn_prev_month)
                    time.sleep(0.3)
                    continue
                elif curr_m_int < tgt_m:
                    driver.execute_script("arguments[0].click();", btn_next_month)
                    time.sleep(0.3)
                    continue
                
                print(f"      ✅ Kalender udah pas di: {header_text}")
                break
            except: break

        # Klik tanggal
        try:
            all_cells = driver.find_elements(By.XPATH, f"//div[contains(@class,'eds-react-date-picker__table-cell') and text()='{tgt_d}']")
            valid_cell = None
            for cell in all_cells:
                if cell.is_displayed() and "out-of-range" not in cell.get_attribute("class"):
                    valid_cell = cell
            
            if valid_cell:
                driver.execute_script("arguments[0].click();", valid_cell)
                print(f"      ✅ Tanggal {tgt_d} berhasil diklik.")
            else:
                print(f"      ❌ Gagal klik tanggal {tgt_d}.")
        except: pass

        # Set jam & menit
        h, m = target_time_str.split(':')
        print(f"      ⏰ Otw set jam ke: {h}:{m}")
        
        try:
            h_str = f"{int(h):02d}"
            jam_els = driver.find_elements(By.XPATH, f"//div[contains(@class,'time-box') and text()='{h_str}']")
            for el in jam_els:
                if el.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({behavior:'instant', block:'center'});", el)
                    time.sleep(0.3)
                    driver.execute_script("arguments[0].click();", el)
                    break
        except: pass

        try:
            m_str = f"{int(m):02d}" 
            menit_els = driver.find_elements(By.XPATH, f"//div[contains(@class,'time-box') and text()='{m_str}']")
            for el in reversed(menit_els):
                if el.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({behavior:'instant', block:'center'});", el)
                    time.sleep(0.3)
                    driver.execute_script("arguments[0].click();", el)
                    break
        except: pass

        # Konfirmasi kalender
        time.sleep(1)
        try:
            popup_xpath = "//div[contains(@class, 'eds-react-date-picker__btn-wrap')]//button"
            confirm_btns = driver.find_elements(By.XPATH, popup_xpath)
            clicked = False
            for btn in reversed(confirm_btns):
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
                    print("      ✅ Tombol Konfirmasi Kalender DIKLIK.")
                    clicked = True
                    time.sleep(1)
                    break
            if not clicked:
                driver.find_element(By.TAG_NAME, "body").click()
        except: pass

    except Exception as e:
        print(f"      ❌ Error di kalender: {e}")

# ==========================================
# 5. LOGIKA UTAMA SHOPEE (THE BRAIN)
# ==========================================
def run_shopee_full(driver, diskon_angka, tgl_mulai_str, jam_mulai_str, len_suffix, crm_number, browser_choice):
    
    print("\n--- 🛒 GASKEUN DUPLIKAT VOUCHER SHOPEE ---")
    
    obj_mulai = datetime.strptime(tgl_mulai_str, "%d-%m-%Y")
    obj_akhir = obj_mulai + timedelta(days=25)
    jam_akhir_str = "23:59"
    
    print(f"📅 Start: {tgl_mulai_str} {jam_mulai_str}")
    print(f"📅 End  : {obj_akhir.strftime('%d-%m-%Y')} {jam_akhir_str}")

    pindah_ke_tab_shopee(driver, browser_choice)
    
    tutup_popup(driver)
    time.sleep(3)
    tutup_popup(driver)

    # TUNGGU HALAMAN SIAP — CEPAT & PINTAR
    print("Nunggu halaman voucher siap...")
    try:
        WebDriverWait(driver, 30).until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'My Vouchers') or contains(text(),'No vouchers')]")),
                EC.presence_of_element_located((By.XPATH, "//table//th"))
            )
        )
        print("Halaman voucher sudah siap (cepat!)")
    except:
        print("   Masih loading, lanjut aja...")
    
    # Target voucher
    if browser_choice in ['1', '5']:
        target_text = f"Voucher Claim {diskon_angka}000"
    elif browser_choice == '2':
        target_text = f"Diskon {diskon_angka}%"
    elif browser_choice in ['3', '4']:
        target_text = f"Diskon {diskon_angka}rb"
    else:
        print("❌ Browser tidak dikenali.")
        return

    print(f"🔎 Mencari voucher: '{target_text}'")

    # Scroll sampai ketemu
    for i in range(15):
        driver.execute_script("window.scrollBy(0, 700);")
        time.sleep(random.uniform(1.3, 2.1))
        if driver.find_elements(By.XPATH, f"//tr[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{target_text.lower()}')]"):
            print("   🎯 Voucher target sudah kelihatan!")
            break
    time.sleep(2)

    # Klik Duplikat
    duplicate_text = "Duplicate" if browser_choice == '4' else "Duplikat"
    xpath_row = f"//tr[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{target_text.lower()}')]"
    row = driver.find_element(By.XPATH, xpath_row)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
    time.sleep(1)
    driver.find_element(By.XPATH, f"{xpath_row}//button[.//span[contains(text(),'{duplicate_text}')]]").click()
    print(f"✅ Tombol {duplicate_text} berhasil diklik!")

    time.sleep(8)
    tutup_popup(driver)

    # Ganti kode
    suffix = generate_kode_suffix(len_suffix)
    kode_baru = f"{diskon_angka}{suffix}"
    kode_input = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//input[@maxlength='5']")))
    kode_input.click()
    kode_input.send_keys(Keys.CONTROL + "a")
    kode_input.send_keys(Keys.DELETE)
    kode_input.send_keys(kode_baru)
    print(f"⌨️ Kode baru: {kode_baru}")

    # Ganti nama
    if browser_choice in ['2', '4']:
        nama_baru = f"Diskon {diskon_angka}% (CRM {crm_number})" if browser_choice == '2' else f"Diskon {diskon_angka}rb (CRM {crm_number})"
        nama_input = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "(//input[@type='text'])[1]")))
        nama_input.click()
        nama_input.send_keys(Keys.CONTROL + "a")
        nama_input.send_keys(Keys.DELETE)
        nama_input.send_keys(nama_baru)
        print(f"🔧 Nama diganti: {nama_baru}")

    elif browser_choice == '3':
        nama_baru = f"Diskon {diskon_angka}rb (HARN{kode_baru})"
        nama_input = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "(//input[@type='text'])[1]")))
        nama_input.click()
        nama_input.send_keys(Keys.CONTROL + "a")
        nama_input.send_keys(Keys.DELETE)
        nama_input.send_keys(nama_baru)
        print(f"🔧 Nama diganti: {nama_baru}")

    else:
        print("ℹ️ Nama voucher dibiarkan tetap (HERB/Heirbikids)")

    time.sleep(2)

    # Set tanggal
    robot_klik_kalender_shopee(driver, "startDate", obj_mulai, jam_mulai_str)
    time.sleep(3)
    driver.find_element(By.TAG_NAME, "body").click()
    time.sleep(2)
    robot_klik_kalender_shopee(driver, "endDate", obj_akhir, "23:59")

    print("\n✋ SELESAI 100%! Semua sudah diisi otomatis.")
    print("   Tinggal cek sebentar, lalu klik tombol CONFIRM/SIMPAN (merah) manual ya bang!")
    print("   Botnya sekarang sudah super stabil dan akurat!")

# ==========================================
# 6. MENU UTAMA
# ==========================================
if __name__ == "__main__":
    print("\n=== 🤖 BOT DUPLIKAT VOUCHER SHOPEE - EDISI ANAK SENJA V11 (FINAL & FULL) 🤖 ===\n")
    
    crm_input = input("1. Nomor CRM Hari Ini (misal: 179): ").strip() or "000"

    angka = input("2. Angka Diskon (25/50/90): ").strip() or "25"
    
    print("\n3. Tanggal Mulai (DD-MM-YYYY)")
    raw_tgl = input("   Ketik tanggal (contoh: 18-12-2025): ").strip() or datetime.now().strftime("%d-%m-%Y")
    
    raw_jam = input("4. Jam Mulai (contoh: 08:00): ").strip() or "00:00"

    try:
        len_suffix = int(input("5. Panjang kode acak (2/3/4 huruf): ").strip())
    except:
        len_suffix = 3

    print("\n6. Pilih Akun/Browser:")
    for k, v in profiles.items():
        print(f"   {k}. {v['name']}")
    pilihan_browser = input("   Masukkan nomor: ").strip()

    driver = start_browser(pilihan_browser)
    if driver:
        try:
            run_shopee_full(driver, angka, raw_tgl, raw_jam, len_suffix, crm_input, pilihan_browser)
            print("\n✅ Script selesai. Browser tetap terbuka untuk konfirmasi manual.")
        except KeyboardInterrupt:
            print("\n⛔ Dibatalkan manual.")
        except Exception as e:
            print(f"\n❌ Error tak terduga: {e}")
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
from selenium.webdriver.common.action_chains import ActionChains

# ==========================================
# 1. SETUP PROFIL BROWSER
# ==========================================
base_path_edge = r"C:\Users\danan\AppData\Local\Microsoft\Edge\User Data" 
base_path_brave = r"C:\Users\danan\AppData\Local\BraveSoftware\Brave-Browser\User Data"
base_path_firefox = r"C:\Users\danan\AppData\Roaming\Mozilla\Firefox\Profiles"

profiles = {
    "1": {"type": "edge", "path": base_path_edge, "profile": "Default",   "name": "Edge - Utama (Personal)"},
    "2": {"type": "edge", "path": base_path_edge, "profile": "Profile 1", "name": "Edge - Profile 2 (Fixed)"},
    "3": {"type": "firefox", "path": base_path_firefox, "profile": "jtkkxnwv.default-release", "name": "Firefox - Utama"},
    
    # --- PERBAIKAN DISINI: DIGANTI JADI 'Profile 4' ---
    "4": {"type": "edge", "path": base_path_edge, "profile": "Profile 4", "name": "Edge - Profile 4 (Target)"},
    
    "5": {"type": "brave", "path": base_path_brave, "profile": "Default", "name": "Brave Browser"},
}

# ==========================================
# 2. FUNGSI NYALAIN BROWSER
# ==========================================
def start_browser(choice):
    selected = profiles.get(choice)
    if not selected:
        print("❌ Pilihan browser gak ada bro!")
        return None

    if selected['type'] == 'edge':
        print("🔪 Membersihkan sisa proses Edge dulu...")
        try:
            os.system("taskkill /F /IM msedge.exe >nul 2>&1")
        except: pass
        time.sleep(2) 

    print(f"🚀 Lagi buka {selected['name']}...")
    print(f"📂 Menggunakan Folder: {selected['profile']}") # Debug info
    load_timeout = 20
    
    if selected['type'] == 'edge':
        local_edge_driver = os.path.join(os.path.dirname(os.path.abspath(__file__)), "msedgedriver.exe")
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument(f"user-data-dir={selected['path']}")
        options.add_argument(f"profile-directory={selected['profile']}")
        options.add_experimental_option("detach", True) 
        options.add_argument("--log-level=3") 
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if os.path.exists(local_edge_driver):
            driver = webdriver.Edge(service=EdgeService(local_edge_driver), options=options)
        else:
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

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
# 3. ALAT BANTU (HELPER)
# ==========================================
def pindah_ke_tab_shopee(driver):
    print("🔎 Lagi nyari tab Shopee...")
    try:
        if "shopee.co.id" in driver.current_url.lower(): return
        for tab in driver.window_handles:
            driver.switch_to.window(tab)
            if "shopee.co.id" in driver.current_url.lower():
                print(f"✅ Sip, tab ketemu: {driver.title}")
                return
        driver.get("https://seller.shopee.co.id/portal/marketing/vouchers/list")
    except:
        driver.get("https://seller.shopee.co.id/portal/marketing/vouchers/list")

def generate_kode_suffix(length=3):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

# ==========================================
# 4. LOGIKA KALENDER (NAVIGATOR 3.4 - POSITIONAL CLICK)
# ==========================================
def robot_klik_kalender_shopee(driver, element_id, target_date_obj, target_time_str):
    print(f"   🗓️ SETTING {element_id.upper()}: {target_date_obj.strftime('%d-%m-%Y')} {target_time_str}")
    
    # Mapping Bulan Shopee INDONESIA
    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Mei": 5, "Jun": 6,
        "Jul": 7, "Ags": 8, "Agu": 8, "Sep": 9, "Okt": 10, "Nov": 11, "Des": 12
    }

    try:
        # 0. RESET FOKUS
        try:
            driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(0.5)
        except: pass

        # 1. BUKA POPUP KALENDER
        xpath_target = f"//div[@id='{element_id}']//input"
        wrapper = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_target)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", wrapper)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", wrapper)
        time.sleep(1.0) 

        # Target Data
        tgt_d = int(target_date_obj.day)
        tgt_y = int(target_date_obj.year)
        tgt_m = target_date_obj.month
        
        # 2. NAVIGASI TAHUN & BULAN (POSITIONAL)
        for _ in range(50):
            try:
                # Cari header di popup yang AKTIF
                visible_headers = [h for h in driver.find_elements(By.CLASS_NAME, "date-box") if h.is_displayed()]
                if not visible_headers:
                    print("      ⚠️ Gak nemu header kalender!")
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

                # Cari Grup Tombol Navigasi di popup aktif
                active_panel = driver.find_elements(By.CLASS_NAME, "eds-react-date-picker__header")[-1]
                nav_btns = active_panel.find_elements(By.XPATH, ".//div[contains(@class, 'btn-arrow-default')]")
                
                if len(nav_btns) < 4:
                    print("      ⚠️ Tombol navigasi kurang lengkap!")
                    break

                btn_prev_year  = nav_btns[0] # <<
                btn_prev_month = nav_btns[1] # <
                btn_next_month = nav_btns[2] # >
                btn_next_year  = nav_btns[3] # >>

                # --- BANDINGKAN TAHUN ---
                if curr_y_int > tgt_y:
                    print(f"      ⏪ Tahun {curr_y_int} > {tgt_y}. Mundur Tahun...")
                    driver.execute_script("arguments[0].click();", btn_prev_year)
                    time.sleep(0.5)
                    continue 
                elif curr_y_int < tgt_y:
                    print(f"      ⏩ Tahun {curr_y_int} < {tgt_y}. Maju Tahun...")
                    driver.execute_script("arguments[0].click();", btn_next_year)
                    time.sleep(0.5)
                    continue

                # --- BANDINGKAN BULAN ---
                if curr_m_int > tgt_m:
                    print(f"      ⬅️ Bulan {curr_m_str} > Target. Mundur Bulan...")
                    driver.execute_script("arguments[0].click();", btn_prev_month)
                    time.sleep(0.5)
                    continue
                elif curr_m_int < tgt_m:
                    print(f"      ➡️ Bulan {curr_m_str} < Target. Maju Bulan...")
                    driver.execute_script("arguments[0].click();", btn_next_month)
                    time.sleep(0.5)
                    continue
                
                print(f"      ✅ Kalender Pas: {header_text}")
                break

            except Exception as e: 
                print(f"Navigasi Error: {e}")
                break

        # 3. KLIK TANGGAL
        try:
            # Cari sel tanggal (1-31) di tabel yang visible
            all_cells = driver.find_elements(By.XPATH, f"//div[contains(@class,'eds-react-date-picker__table-cell') and text()='{tgt_d}']")
            valid_cell = None
            for cell in all_cells:
                # Pastikan tanggal yang aktif (bukan tanggal bulan lalu/depan yg samar)
                if cell.is_displayed() and "out-of-range" not in cell.get_attribute("class"):
                    valid_cell = cell
            
            if valid_cell:
                driver.execute_script("arguments[0].click();", valid_cell)
                print(f"      ✅ Tanggal {tgt_d} diklik.")
            else:
                print(f"      ❌ Gagal nemu tanggal {tgt_d}.")
        except: pass

        # 4. SET JAM & MENIT
        h, m = target_time_str.split(':')
        print(f"      ⏰ Set waktu: {h}:{m}")
        
        try: # Jam
            h_str = f"{int(h):02d}"
            jam_els = driver.find_elements(By.XPATH, f"//div[contains(@class,'time-box') and text()='{h_str}']")
            for el in jam_els:
                if el.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({behavior:'instant', block:'center'});", el)
                    time.sleep(0.3)
                    driver.execute_script("arguments[0].click();", el)
                    break
        except: pass

        try: # Menit
            m_str = f"{int(m):02d}" 
            menit_els = driver.find_elements(By.XPATH, f"//div[contains(@class,'time-box') and text()='{m_str}']")
            # Menit biasanya kolom kanan (index terakhir di list elements)
            found_menit = False
            for el in reversed(menit_els):
                if el.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({behavior:'instant', block:'center'});", el)
                    time.sleep(0.3)
                    driver.execute_script("arguments[0].click();", el)
                    found_menit = True
                    break
            if not found_menit: print(f"      ⚠️ Gagal klik menit {m_str}")
        except: pass

        # 5. KLIK KONFIRMASI (SCOPE SPESIFIK: POPUP ONLY)
        time.sleep(1)
        try:
            popup_xpath = "//div[contains(@class, 'eds-react-date-picker__btn-wrap')]//button"
            confirm_btns = driver.find_elements(By.XPATH, popup_xpath)
            clicked = False
            for btn in reversed(confirm_btns):
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
                    print("      ✅ Konfirmasi Kalender (Kecil) DIKLIK.")
                    clicked = True
                    time.sleep(1)
                    break
            
            if not clicked:
                print("      ⚠️ Tombol konfirmasi popup gak nemu, klik body...")
                driver.find_element(By.TAG_NAME, "body").click()

        except Exception as e:
            print(f"      ❌ Gagal konfirmasi: {e}")

    except Exception as e:
        print(f"      ❌ Error Kalender: {e}")

# ==========================================
# 5. LOGIKA UTAMA SHOPEE
# ==========================================
def run_shopee_full(driver, diskon_angka, tgl_mulai_str, jam_mulai_str, len_suffix, crm_number, browser_choice):
    
    print("\n--- 🛒 GASKEUN PROSES SHOPEE ---")
    
    obj_mulai = datetime.strptime(tgl_mulai_str, "%d-%m-%Y")
    obj_akhir = obj_mulai + timedelta(days=25)
    jam_akhir_str = "23:59"
    
    print(f"📅 Start: {tgl_mulai_str} {jam_mulai_str}")
    print(f"📅 End  : {obj_akhir.strftime('%d-%m-%Y')} {jam_akhir_str}")

    pindah_ke_tab_shopee(driver)
    
    print("⏳ Nunggu tabel voucher muncul...")
    time.sleep(5) 
    
    # --- FIREFOX: ZOOM OUT WAJIB ---
    if browser_choice == '3':
        print("🔭 Mode Firefox: Zoom Out 80% & Cari 'rb'...")
        driver.execute_script("document.body.style.zoom = '80%'")
        target_text = f"Diskon {diskon_angka}rb" 
    elif browser_choice == '5': 
        print("🔭 Mode Brave: Cari 'Voucher Claim'...")
        target_text = f"Voucher Claim {diskon_angka}000"
    else:
        target_text = f"Diskon {diskon_angka}%"

    print("⬇️ Scroll ke bawah dikit...")
    driver.execute_script("window.scrollBy(0, 800);") 
    time.sleep(2)

    print(f"🔎 Mencari Voucher dengan tulisan: '{target_text}'...")

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{target_text}')]")))
        xpath_fix = f"//tr[contains(., '{target_text}')]//button[span[contains(text(),'Duplikat')]]"
        dup_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath_fix)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dup_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", dup_btn)
        print(f"✅ BERHASIL klik Duplikat (HTML Fix).")
    except:
        print(f"⚠️ Tombol langsung gak mempan, coba cari tombol 'Last Column'...")
        try:
            xpath_row = f"//tr[contains(., '{target_text}')]"
            row = driver.find_element(By.XPATH, xpath_row)
            last_col = row.find_element(By.XPATH, ".//td[last()]")
            btns = last_col.find_elements(By.TAG_NAME, "button")
            found_dup = False
            for b in btns:
                if "Duplikat" in b.text or "Duplikat" in b.get_attribute('innerHTML'):
                    driver.execute_script("arguments[0].click();", b)
                    print("✅ Sip, ketemu tombol Duplikat di kolom terakhir.")
                    found_dup = True
                    break
            if not found_dup: return
        except Exception as e:
            print(f"❌ Gagal Total Duplikat. Error: {e}")
            return

    print("⏳ Nunggu halaman edit kebuka...")
    time.sleep(5) 
    
    suffix = generate_kode_suffix(len_suffix)
    kode_voucher_input = f"{diskon_angka}{suffix}"
    
    # --- RENAME LOGIC ---
    if browser_choice == '1':
        nama_baru = f"Diskon {diskon_angka}% (CRM {crm_number})"
        print(f"🔧 [Edge Utama] Ganti nama jadi: '{nama_baru}'...")
        try:
            wait = WebDriverWait(driver, 10)
            xpath_nama = "(//input[@type='text'])[1] | //input[@placeholder='Nama Voucher']"
            nama_input = wait.until(EC.presence_of_element_located((By.XPATH, xpath_nama)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nama_input)
            driver.execute_script("arguments[0].value = '';", nama_input)
            nama_input.send_keys(Keys.CONTROL + "a")
            nama_input.send_keys(Keys.BACKSPACE)
            nama_input.send_keys(nama_baru)
            print(f"✅ Nama Voucher beres.")
        except: pass
    elif browser_choice == '2':
        nama_baru = f"Diskon {diskon_angka}% (CRM {crm_number})"
        print(f"🔧 [Edge Profile 2] Ganti nama jadi: '{nama_baru}'...")
        try:
            wait = WebDriverWait(driver, 10)
            xpath_nama = "(//input[@type='text'])[1] | //input[@placeholder='Nama Voucher']"
            nama_input = wait.until(EC.presence_of_element_located((By.XPATH, xpath_nama)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nama_input)
            driver.execute_script("arguments[0].value = '';", nama_input)
            nama_input.send_keys(Keys.CONTROL + "a")
            nama_input.send_keys(Keys.BACKSPACE)
            nama_input.send_keys(nama_baru)
            print(f"✅ Nama Voucher beres.")
        except: pass
    elif browser_choice == '3':
        nama_baru = f"Diskon {diskon_angka}rb (HARN{kode_voucher_input})"
        print(f"🔧 [Firefox] Ganti nama jadi: '{nama_baru}'...")
        try:
            wait = WebDriverWait(driver, 10)
            xpath_nama = "(//input[@type='text'])[1] | //input[@placeholder='Nama Voucher']"
            nama_input = wait.until(EC.presence_of_element_located((By.XPATH, xpath_nama)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nama_input)
            driver.execute_script("arguments[0].value = '';", nama_input)
            nama_input.send_keys(Keys.CONTROL + "a")
            nama_input.send_keys(Keys.BACKSPACE)
            nama_input.send_keys(nama_baru)
            print(f"✅ Nama Voucher beres.")
        except: pass
    elif browser_choice == '4':
        nama_baru = f"Diskon {diskon_angka}% (CRM {crm_number})"
        print(f"🔧 [Edge Profile 5] Ganti nama jadi: '{nama_baru}'...")
        try:
            wait = WebDriverWait(driver, 10)
            xpath_nama = "(//input[@type='text'])[1] | //input[@placeholder='Nama Voucher']"
            nama_input = wait.until(EC.presence_of_element_located((By.XPATH, xpath_nama)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nama_input)
            driver.execute_script("arguments[0].value = '';", nama_input)
            nama_input.send_keys(Keys.CONTROL + "a")
            nama_input.send_keys(Keys.BACKSPACE)
            nama_input.send_keys(nama_baru)
            print(f"✅ Nama Voucher beres.")
        except: pass
    elif browser_choice == '5':
        # --- BRAVE: Voucher Claim 25000 ---
        nama_baru = f"Voucher Claim {diskon_angka}000"
        print(f"🔧 [Brave] Ganti nama jadi: '{nama_baru}'...")
        try:
            wait = WebDriverWait(driver, 10)
            xpath_nama = "(//input[@type='text'])[1] | //input[@placeholder='Nama Voucher']"
            nama_input = wait.until(EC.presence_of_element_located((By.XPATH, xpath_nama)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nama_input)
            driver.execute_script("arguments[0].value = '';", nama_input)
            nama_input.send_keys(Keys.CONTROL + "a")
            nama_input.send_keys(Keys.BACKSPACE)
            nama_input.send_keys(nama_baru)
            print(f"✅ Nama Voucher beres.")
        except: pass

    # --- INPUT KODE ---
    print(f"⌨️ Input Kode: {kode_voucher_input}")
    try:
        wait = WebDriverWait(driver, 10)
        inp_kode = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@maxlength='5']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", inp_kode)
        inp_kode.click()
        inp_kode.send_keys(Keys.CONTROL + "a")
        inp_kode.send_keys(Keys.BACKSPACE)
        inp_kode.send_keys(kode_voucher_input) 
        print(f"   ✅ Kode masuk.")
    except: pass

    time.sleep(1)
    
    # --- ISI TANGGAL (NAVIGATOR 3.4) ---
    # 1. Start Date
    robot_klik_kalender_shopee(driver, "startDate", obj_mulai, jam_mulai_str)
    
    # JEDA PENTING
    print("   🛑 Tutup popup dulu biar aman...")
    time.sleep(2) 
    try: driver.find_element(By.TAG_NAME, "body").click()
    except: pass
    time.sleep(1)

    # 2. End Date
    robot_klik_kalender_shopee(driver, "endDate", obj_akhir, jam_akhir_str)

    print("\n✋ BERHENTI DULU BRO. Silakan CEK MANUAL, lalu klik tombol Konfirmasi (Merah Besar) sendiri ya.")

# ==========================================
# 6. MENU UTAMA
# ==========================================
if __name__ == "__main__":
    print("\n=== BOT AUTO VOUCHER (PROFILE 4 FIX) ===")
    
    crm_input = input("1. Masukkan Nomor CRM Hari Ini (cth: 169): ")
    if not crm_input: crm_input = "000"

    angka = input("2. Masukkan Angka Diskon (25/50/90): ") or "25"
    
    print("\n3. Tanggal Mulai (DD-MM-YYYY)")
    print("   Contoh: 29-11-2025")
    raw_tgl = input("   Ketik Tanggal: ") or datetime.now().strftime("%d-%m-%Y")
    
    raw_jam = input("4. Jam Mulai (cth 08:00): ") or "00:00"

    try:
        len_suffix = int(input("5. Mau kode acak berapa huruf? (2/3): "))
    except:
        len_suffix = 3

    print("\n6. Pilih Browser:")
    for k, v in profiles.items(): print(f"   {k}. {v['name']}")
    pilihan_browser = input("   Nomor Browser: ")

    driver = start_browser(pilihan_browser)

    if driver:
        try:
            run_shopee_full(driver, angka, raw_tgl, raw_jam, len_suffix, crm_input, pilihan_browser)
            print("\n✅ Script Selesai. Browser sengaja dibiarin kebuka.")
        except KeyboardInterrupt:
            print("\n⛔ Yah kok distop paksa (Ctrl+C)? Yaudah browser tetep kebuka kok.")
        except Exception as e:
            print(f"\n❌ Waduh Error: {e}")
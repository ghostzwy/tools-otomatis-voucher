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
# 1. SETUP PROFIL BROWSER (BASECAMP)
# ==========================================
# Ini path sakti biar bot-nya pinter, pake otak browser asli kamu.
base_path_edge = r"C:\Users\danan\AppData\Local\Microsoft\Edge\User Data" 
base_path_brave = r"C:\Users\danan\AppData\Local\BraveSoftware\Brave-Browser\User Data"
base_path_firefox = r"C:\Users\danan\AppData\Roaming\Mozilla\Firefox\Profiles"

# Daftar akun perang kita nih:
profiles = {
    # Edge 1: Si Heirbiglow (CARI 25000)
    "1": {"type": "edge", "path": base_path_edge, "profile": "Default",   "name": "Edge 1 - HERB25SEN"},
    
    # Edge 2: Ciara Indonesia
    "2": {"type": "edge", "path": base_path_edge, "profile": "Profile 1", "name": "Edge 2 - Ciara Indonesia"},
    
    # Firefox: Harnisch (Si Anak Bawang)
    "3": {"type": "firefox", "path": base_path_firefox, "profile": "jtkkxnwv.default-release", "name": "Firefox - Harnisch"},
    
    # Edge 4: Ciara Malaysia (DIGANTI ke Profile 4, kalau masih salah ganti ke Profile 5)
    "4": {"type": "edge", "path": base_path_edge, "profile": "Profile 4", "name": "Edge 4 - Ciara Malaysia"},
    
    # Brave: Heirbikids (Si Kuat)
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

    # Matiin dulu browser yang nyangkut biar ga tabrakan
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
        
    time.sleep(2) # Napas bentar

    print(f"🚀 OTW buka {selected['name']}...")
    print(f"📂 Pake folder profil: {selected['profile']}")
    load_timeout = 20
    
    # --- SETUP BUAT EDGE ---
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
            # Cek driver lokal dulu, kalo ga ada baru download
            if os.path.exists(local_edge_driver):
                # Pakai driver lokal jika ada
                driver = webdriver.Edge(service=EdgeService(local_edge_driver), options=options)
            else:
                # Fallback ke auto-download jika lokal tidak ada
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        except Exception as e:
            print(f"❌ Yah gagal buka Edge: {e}")
            return None

    # --- SETUP BUAT FIREFOX ---
    elif selected['type'] == 'firefox':
        options = FirefoxOptions()
        full_profile_path = os.path.join(selected['path'], selected['profile'])
        if not os.path.exists(full_profile_path): return None
        options.add_argument("-profile")
        options.add_argument(full_profile_path)
        try:
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        except: return None
        
    # --- SETUP BUAT BRAVE ---
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
def pindah_ke_tab_shopee(driver, target_url="https://seller.shopee.co.id/portal/marketing/vouchers/list"):
    print(f"🔎 Lagi nyari tab Shopee nih: {target_url}")
    try:
        # Cek dulu kali aja udah kebuka tab-nya
        if "shopee.co.id" in driver.current_url.lower() or "shopee.com.my" in driver.current_url.lower(): 
            return
        for tab in driver.window_handles:
            driver.switch_to.window(tab)
            if "shopee" in driver.current_url.lower():
                print(f"✅ Mantap, tab ketemu: {driver.title}")
                return
        driver.get(target_url)
    except:
        driver.get(target_url)

def generate_kode_suffix(length=3):
    # Bikin kode acak biar ga bentrok
    return ''.join(random.choices(string.ascii_uppercase, k=length))

# ==========================================
# 4. LOGIKA KALENDER (THE NAVIGATOR)
# ==========================================
def robot_klik_kalender_shopee(driver, element_id, target_date_obj, target_time_str):
    print(f"   🗓️ Otw setting {element_id.upper()}: {target_date_obj.strftime('%d-%m-%Y')} {target_time_str}")
    
    # Kamus bahasa bulan (Indo & Inggris) biar bot ga bingung
    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Mei": 5, "Jun": 6,
        "Jul": 7, "Ags": 8, "Agu": 8, "Sep": 9, "Okt": 10, "Nov": 11, "Des": 12,
        "May": 5, "Aug": 8, "Oct": 10, "Dec": 12
    }

    try:
        # Klik area kosong dulu biar fokus
        try:
            driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(0.5)
        except: pass

        # Cari & Klik input tanggalnya
        xpath_target = f"//div[@id='{element_id}']//input"
        wrapper = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_target)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", wrapper)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", wrapper)
        time.sleep(1.0) 

        # Pecah target tanggalnya
        tgt_d = int(target_date_obj.day)
        tgt_y = int(target_date_obj.year)
        tgt_m = target_date_obj.month
        
        # Loop buat nyari Tahun & Bulan yang pas
        for _ in range(50):
            try:
                visible_headers = [h for h in driver.find_elements(By.CLASS_NAME, "date-box") if h.is_displayed()]
                if not visible_headers:
                    print("      ⚠️ Waduh, header kalender ga nongol!")
                    break
                
                header_elem = visible_headers[-1]
                header_text = header_elem.text.strip()
                
                # Baca posisi kalender sekarang
                found_year = re.search(r'\d{4}', header_text)
                if not found_year: break
                curr_y_int = int(found_year.group())
                
                found_month = re.search(r'^[A-Za-z]+', header_text)
                if not found_month: break
                curr_m_str = found_month.group()
                curr_m_int = month_map.get(curr_m_str, 0)

                # Cari tombol panah navigasi
                active_panel = driver.find_elements(By.CLASS_NAME, "eds-react-date-picker__header")[-1]
                nav_btns = active_panel.find_elements(By.XPATH, ".//div[contains(@class, 'btn-arrow-default')]")
                
                if len(nav_btns) < 4: break

                btn_prev_year  = nav_btns[0] # <<
                btn_prev_month = nav_btns[1] # <
                btn_next_month = nav_btns[2] # >
                btn_next_year  = nav_btns[3] # >>

                # Logic Maju Mundur Cantik
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
                
                print(f"      ✅ Sip, Kalender udah pas di: {header_text}")
                break
            except: break

        # Klik Tanggalnya
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
                print(f"      ❌ Yah, gagal klik tanggal {tgt_d}.")
        except: pass

        # Klik Jam & Menit (Pake scroll biar ga miss)
        h, m = target_time_str.split(':')
        print(f"      ⏰ Otw set jam ke: {h}:{m}")
        
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
            for el in reversed(menit_els):
                if el.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({behavior:'instant', block:'center'});", el)
                    time.sleep(0.3)
                    driver.execute_script("arguments[0].click();", el)
                    break
        except: pass

        # Klik Konfirmasi Kecil (Yang aman)
        time.sleep(1)
        try:
            popup_xpath = "//div[contains(@class, 'eds-react-date-picker__btn-wrap')]//button"
            confirm_btns = driver.find_elements(By.XPATH, popup_xpath)
            clicked = False
            for btn in reversed(confirm_btns):
                if btn.is_displayed():
                    driver.execute_script("arguments[0].click();", btn)
                    print("      ✅ Tombol Konfirmasi Kalender (Kecil) DIKLIK.")
                    clicked = True
                    time.sleep(1)
                    break
            if not clicked:
                # Kalo ga nemu tombol, klik body aja biar ketutup popupnya
                driver.find_element(By.TAG_NAME, "body").click()
        except: pass

    except Exception as e:
        print(f"      ❌ Ada error di kalender nih: {e}")

# ==========================================
# 5. LOGIKA UTAMA SHOPEE (THE BRAIN)
# ==========================================
def run_shopee_full(driver, diskon_angka, tgl_mulai_str, jam_mulai_str, len_suffix, crm_number, browser_choice):
    
    print("\n--- 🛒 GASKEUN LOGIN SHOPEE ---")
    
    obj_mulai = datetime.strptime(tgl_mulai_str, "%d-%m-%Y")
    obj_akhir = obj_mulai + timedelta(days=25)
    jam_akhir_str = "23:59"
    
    print(f"📅 Start: {tgl_mulai_str} {jam_mulai_str}")
    print(f"📅 End  : {obj_akhir.strftime('%d-%m-%Y')} {jam_akhir_str}")

    # Pilih link sesuai browser (Request khusus Edge 1)
    target_link = "https://seller.shopee.co.id/portal/marketing/vouchers/list" # Default
    if browser_choice == '1': 
        target_link = "https://seller.shopee.co.id/portal/marketing/vouchers/list?is_from_login=true"

    pindah_ke_tab_shopee(driver, target_link)
    
    print("⏳ Sabar yak, lagi nunggu tabel voucher nongol...")
    time.sleep(5) 
    
    # Zoom Out dikit biar lega (khusus browser tertentu)
    if browser_choice in ['3', '4', '5']: 
        print("🔭 Zoom Out 80% dulu biar keliatan semua...")
        driver.execute_script("document.body.style.zoom = '80%'")
    
    # Tentukan Target Pencarian (Sesuai Request)
    if browser_choice == '1': # Heirbiglow (CARI 25000)
        target_text = f"Diskon {diskon_angka}000"
    elif browser_choice == '2': # Ciara Indo
        target_text = f"Diskon {diskon_angka}%"
    elif browser_choice == '3': # Firefox Harnisch
        target_text = f"Diskon {diskon_angka}rb"
    elif browser_choice == '4': # Edge 4 Ciara Malay
        target_text = f"Diskon {diskon_angka}rb"
    elif browser_choice == '5': # Brave Heirbikids
        target_text = f"Voucher Claim {diskon_angka}000"

    print("⬇️ Scroll dikit...")
    driver.execute_script("window.scrollBy(0, 800);") 
    time.sleep(2)

    print(f"🔎 Lagi nyari voucher yang ada tulisan: '{target_text}'...")

    try:
        # Tunggu sampe elemennya muncul
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{target_text}')]")))
        
        # Cari tombol Duplikat
        xpath_fix = f"//tr[contains(., '{target_text}')]//button[span[contains(text(),'Duplikat')]]"
        dup_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath_fix)))
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dup_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", dup_btn)
        print(f"✅ CAKEP! Tombol Duplikat berhasil diklik.")
    except:
        print(f"⚠️ Waduh, tombol langsung ga nemu. Coba cari di kolom terakhir...")
        try:
            xpath_row = f"//tr[contains(., '{target_text}')]"
            row = driver.find_element(By.XPATH, xpath_row)
            last_col = row.find_element(By.XPATH, ".//td[last()]")
            btns = last_col.find_elements(By.TAG_NAME, "button")
            found_dup = False
            for b in btns:
                if "Duplikat" in b.text or "Duplikat" in b.get_attribute('innerHTML'):
                    driver.execute_script("arguments[0].click();", b)
                    print("✅ Sip, ketemu tombol Duplikat di pojokan.")
                    found_dup = True
                    break
            if not found_dup: return
        except Exception as e:
            print(f"❌ Gagal total nih pas mau duplikat. Error: {e}")
            return

    print("⏳ Lagi loading halaman edit...")
    time.sleep(5) 
    
    suffix = generate_kode_suffix(len_suffix)
    kode_voucher_input = f"{diskon_angka}{suffix}"
    
    # Logika Ganti Nama (Sesuai Request)
    if browser_choice == '1': # Heirbiglow
        nama_baru = f"Diskon {diskon_angka}rb (HEIR{kode_voucher_input})"
    elif browser_choice == '2': # Ciara Indo
        nama_baru = f"Diskon {diskon_angka}% (CRM {crm_number})"
    elif browser_choice == '3': # Harnisch
        nama_baru = f"Diskon {diskon_angka}rb (HARN{kode_voucher_input})"
    elif browser_choice == '4': # Ciara Malay
        nama_baru = f"Diskon {diskon_angka}rb (CRM {crm_number})" 
    elif browser_choice == '5': # Heirbikids
        nama_baru = f"Voucher Claim {diskon_angka}000"

    print(f"🔧 Ganti nama jadi: '{nama_baru}'...")
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

    # Input Kode
    print(f"⌨️ Masukin Kode: {kode_voucher_input}")
    try:
        wait = WebDriverWait(driver, 10)
        inp_kode = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@maxlength='5']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", inp_kode)
        inp_kode.click()
        inp_kode.send_keys(Keys.CONTROL + "a")
        inp_kode.send_keys(Keys.BACKSPACE)
        inp_kode.send_keys(kode_voucher_input) 
        print(f"   ✅ Kode udah masuk.")
    except: pass

    time.sleep(1)
    
    # Isi Tanggal
    robot_klik_kalender_shopee(driver, "startDate", obj_mulai, jam_mulai_str)
    
    print("   🛑 Tutup popup dulu biar aman...")
    time.sleep(2) 
    try: driver.find_element(By.TAG_NAME, "body").click()
    except: pass
    time.sleep(1)

    robot_klik_kalender_shopee(driver, "endDate", obj_akhir, jam_akhir_str)

    print("\n✋ STOP DULU BANG JAGO. Cek manual dulu, kalo oke baru klik Konfirmasi (Merah) sendiri ya.")

# ==========================================
# 6. MENU UTAMA (THE GATE)
# ==========================================
if __name__ == "__main__":
    print("\n=== 🤖 BOT AUTO VOUCHER - EDISI ANAK SENJA 🤖 ===")
    
    crm_input = input("1. Masukkan Nomor CRM Hari Ini (misal: 169): ")
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

    print("\n6. Pilih Browser Andalan:")
    for k, v in profiles.items(): print(f"   {k}. {v['name']}")
    pilihan_browser = input("   Nomor Browser: ")

    driver = start_browser(pilihan_browser)

    if driver:
        try:
            run_shopee_full(driver, angka, raw_tgl, raw_jam, len_suffix, crm_input, pilihan_browser)
            print("\n✅ Script Kelar. Browser sengaja dibiarin kebuka biar bisa dicek.")
        except KeyboardInterrupt:
            print("\n⛔ Yah kok distop paksa (Ctrl+C)? Yaudah browser tetep kebuka kok.")
        except Exception as e:
            print(f"\n❌ Waduh Error nih bang: {e}")
import time
import os
from datetime import datetime, timedelta
import re

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

from webdriver_manager.firefox import GeckoDriverManager 
from webdriver_manager.chrome import ChromeDriverManager

# ==========================================
# 1. SETUP PROFIL BROWSER
# ==========================================
base_path_edge = r"C:\Users\danan\AppData\Local\Microsoft\Edge\User Data" 
base_path_brave = r"C:\Users\danan\AppData\Local\BraveSoftware\Brave-Browser\User Data"
base_path_firefox = r"C:\Users\danan\AppData\Roaming\Mozilla\Firefox\Profiles"

profiles = {
    "1": {"type": "edge", "path": base_path_edge, "profile": "Default",   "name": "Edge 1 - Herbiglow"}, 
    "2": {"type": "edge", "path": base_path_edge, "profile": "Profile 1", "name": "Edge 2 - Ciara Indonesia"},
    "3": {"type": "firefox", "path": base_path_firefox, "profile": "jtkkxnwv.default-release", "name": "Firefox - Harnisch"},
    "5": {"type": "brave", "path": base_path_brave, "profile": "Default", "name": "Brave - Heirbikids"},
}

# ==========================================
# 2. START BROWSER
# ==========================================
def start_browser(choice):
    selected = profiles.get(choice)
    if not selected:
        print("❌ Pilihan tidak valid!")
        return None

    print(f"🔪 Matikan proses {selected['type']} lama...")
    if selected['type'] == 'edge':
        os.system("taskkill /F /IM msedge.exe >nul 2>&1")
    elif selected['type'] == 'firefox':
        os.system("taskkill /F /IM firefox.exe >nul 2>&1")
    elif selected['type'] == 'brave':
        os.system("taskkill /F /IM brave.exe >nul 2>&1")
    time.sleep(2)

    print(f"🚀 Membuka {selected['name']}...")
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if selected['type'] == 'edge':
        driver_path = os.path.join(current_dir, "msedgedriver.exe")
        if not os.path.exists(driver_path):
            print("❌ msedgedriver.exe tidak ditemukan!")
            return None
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument(f"user-data-dir={selected['path']}")
        options.add_argument(f"profile-directory={selected['profile']}")
        options.add_experimental_option("detach", True)
        options.add_argument("--log-level=3")
        service = EdgeService(driver_path)
        driver = webdriver.Edge(service=service, options=options)

    elif selected['type'] == 'firefox':
        options = FirefoxOptions()
        options.add_argument("-profile")
        options.add_argument(os.path.join(selected['path'], selected['profile']))
        try:
            driver_path = os.path.join(current_dir, "geckodriver.exe")
            if os.path.exists(driver_path):
                service = FirefoxService(driver_path)
            else:
                service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
        except Exception as e:
            print(f"❌ Gagal buka Firefox: {e}")
            return None

    elif selected['type'] == 'brave':
        options = ChromeOptions()
        options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        options.add_argument(f"user-data-dir={selected['path']}")
        options.add_argument(f"profile-directory={selected['profile']}")
        options.add_experimental_option("detach", True)
        try:
            driver_path = os.path.join(current_dir, "chromedriver.exe")
            if os.path.exists(driver_path):
                service = ChromeService(driver_path)
            else:
                service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"❌ Gagal buka Brave: {e}")
            return None

    driver.maximize_window()
    return driver

# ==========================================
# 3. ISI INPUT BIASA
# ==========================================
def isi_input(driver, xpath, value, keterangan):
    try:
        elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        time.sleep(0.5)
        elem.click()
        elem.clear()
        elem.send_keys(value)
        print(f"   ✅ {keterangan}: {value}")
    except Exception as e:
        print(f"   ❌ Gagal {keterangan}: {e}")

# ==========================================
# 4. MAIN LOGIC - DATE & JAM CARA TIKTOK BOT (BRUTAL & PASTI)
# ==========================================
def run_tokopedia(driver, nama_lama, nama_baru, jam_mulai="06:00"):
    url = "https://seller-id.tokopedia.com/promotion/marketing-tools/management?tab=1&shop_region=ID"
    print("🇮🇩 Membuka Tokopedia Voucher Management...")
    driver.get(url)
    time.sleep(10)

    print("⏳ Tunggu halaman load...")
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//table")))
        print("✅ Halaman siap!")
    except:
        print("⚠️ Halaman load lambat, lanjut scroll...")

    print(f"🔍 Scroll mencari voucher: '{nama_lama}'")
    found = False
    voucher_elem = None
    row = None
    for attempt in range(20):
        try:
            voucher_elem = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'line-clamp-2') and contains(text(), '{nama_lama}')]"))
            )
            row = voucher_elem.find_element(By.XPATH, "./ancestor::tr")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
            print("   ✅ Voucher ditemukan!")
            found = True
            break
        except:
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(2)
            print(f"   Scroll... ({attempt + 1}/20)")

    if not found:
        print("❌ Voucher tidak ditemukan.")
        return

    print("   🔍 Zoom out ke 90%...")
    driver.execute_script("document.body.style.zoom='90%'")
    time.sleep(1)

    try:
        ActionChains(driver).move_to_element(row).perform()
        time.sleep(1)

        dropdown_btn = row.find_element(By.XPATH, ".//button[contains(@class, 'arco-btn-icon-only')]")
        ActionChains(driver).move_to_element(dropdown_btn).click(dropdown_btn).perform()
        print("   ✅ Dropdown menu dibuka!")

        print("   Scroll horizontal biar Duplikat kelihatan...")
        driver.execute_script("window.scrollBy(-600, 0);")
        time.sleep(1)

        duplikasi_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'arco-dropdown-menu-item') and contains(text(), 'Duplikat')]"))
        )
        driver.execute_script("arguments[0].click();", duplikasi_btn)
        print("✅ Duplikat berhasil!")
    except Exception as e:
        print(f"❌ Gagal dropdown/duplikat: {e}")
        return

    time.sleep(10)  # Tunggu form load penuh

    print("🔧 Isi form baru...")
    isi_input(driver, "//input[contains(@placeholder, 'Nama promosi tidak bisa dilihat oleh pembeli.')]", nama_baru, "Nama Promosi Baru")

    try:
        match = re.search(r'\(HARN(.+?)\)', nama_baru)
        if match:
            kode_suffix = match.group(1).strip()
            kode_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Misalnya, 15LIVE']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", kode_input)
            time.sleep(0.5)
            kode_input.click()
            kode_input.clear()
            kode_input.send_keys(kode_suffix)
            print(f"   ✅ Kode Klaim terisi: HARN{kode_suffix}")
    except Exception as e:
        print(f"   ❌ Gagal isi kode klaim: {e}")

    # SCROLL PAS KE TANGGAL PROMOSI
    print("   Scroll ke section Tanggal Promosi (pas, nggak kejauhan)...")
    driver.execute_script("window.scrollBy(0, 200);")
    time.sleep(2)

    print("📅 Auto isi Tanggal Promosi (cara Tiktok Bot - pasti jalan!)...")
    today = datetime.now()
    tgl_mulai = today.strftime("%d/%m/%Y")
    tgl_selesai = (today + timedelta(days=25)).strftime("%d/%m/%Y")

    # ISI WAKTU MULAI - BRUTAL OVERWRITE
    try:
        tanggal_mulai = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Waktu mulai')]/ancestor::div//input[1]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tanggal_mulai)
        time.sleep(1)
        tanggal_mulai.click()
        tanggal_mulai.send_keys(Keys.CONTROL + "a")
        tanggal_mulai.send_keys(Keys.DELETE)
        tanggal_mulai.send_keys(tgl_mulai)
        print(f"   ✅ Tanggal Mulai: {tgl_mulai}")

        jam_mulai_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Waktu mulai')]/ancestor::div//input[2]"))
        )
        jam_mulai_field.click()
        jam_mulai_field.send_keys(Keys.CONTROL + "a")
        jam_mulai_field.send_keys(Keys.DELETE)
        jam_mulai_field.send_keys(jam_mulai)
        print(f"   ✅ Jam Mulai: {jam_mulai}")
    except Exception as e:
        print(f"   ❌ Gagal isi Waktu Mulai: {e}")

    # ISI WAKTU SELESAI - BRUTAL OVERWRITE
    try:
        tanggal_selesai = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Waktu selesai')]/ancestor::div//input[1]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tanggal_selesai)
        time.sleep(1)
        tanggal_selesai.click()
        tanggal_selesai.send_keys(Keys.CONTROL + "a")
        tanggal_selesai.send_keys(Keys.DELETE)
        tanggal_selesai.send_keys(tgl_selesai)
        print(f"   ✅ Tanggal Selesai: {tgl_selesai}")

        jam_selesai_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Waktu selesai')]/ancestor::div//input[2]"))
        )
        jam_selesai_field.click()
        jam_selesai_field.send_keys(Keys.CONTROL + "a")
        jam_selesai_field.send_keys(Keys.DELETE)
        jam_selesai_field.send_keys("23:59")
        print("   ✅ Jam Selesai: 23:59")
    except Exception as e:
        print(f"   ❌ Gagal isi Waktu Selesai: {e}")

    print("\n🎉 BOT SELESAI 100% OTOMATIS!")
    print(f"   ► Nama: {nama_baru}")
    print(f"   ► Kode Klaim: HARN + suffix")
    print(f"   ► Periode: Hari ini {jam_mulai} — +25 hari 23:59")
    print("   ► Tinggal isi diskon & kuota lalu klik BUAT PROMOSI")
    print("   ► Bot siap jalan setiap hari tanpa error!")

# ==========================================
# 5. MENU UTAMA
# ==========================================
if __name__ == "__main__":
    print("\n=== 🤖 BOT TOKOPEDIA VOUCHER - VERSI FULL LENGKAP & FINAL 🤖 ===\n")
    
    print("Pilih akun:")
    for k, v in profiles.items():
        print(f"   {k}. {v['name']}")
    choice = input("   Masukkan nomor: ").strip()

    if choice not in profiles:
        print("❌ Nomor tidak valid!")
        exit()

    akun_name = profiles[choice]["name"]
    print(f"\nAkun: {akun_name}")

    nama_lama = input("1. Nama Voucher Lama: ").strip()
    if not nama_lama:
        print("❌ Wajib isi!")
        exit()

    nama_baru = input("2. Nama Voucher Baru (contoh: Diskon 25rb (HARN25MX)): ").strip()
    if not nama_baru:
        nama_baru = f"Diskon 25rb (HARN{datetime.now().strftime('%d%M')})"

    jam_mulai = input("3. Jam Mulai (default 06:00): ").strip() or "06:00"

    print("\nSummary:")
    print(f"   Akun: {akun_name}")
    print(f"   Nama lama: {nama_lama}")
    print(f"   Nama baru: {nama_baru}")
    print(f"   Jam mulai: {jam_mulai}")
    print("   Selesai: otomatis +25 hari jam 23:59")
    confirm = input("Lanjut? (y/n): ").lower()
    if confirm != 'y':
        print("Dibatalkan.")
        exit()

    driver = start_browser(choice)
    if driver:
        run_tokopedia(driver, nama_lama, nama_baru, jam_mulai)
        print("\n✅ Bot selesai. Browser terbuka — tinggal klik BUAT PROMOSI!")
    else:
        print("\n❌ Gagal buka browser.")
import time
import os
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

# SETUP PROFIL BROWSER
base_path_edge = r"C:\Users\danan\AppData\Local\Microsoft\Edge\User Data"
base_path_brave = r"C:\Users\danan\AppData\Local\BraveSoftware\Brave-Browser\User Data"
base_path_firefox = r"C:\Users\danan\AppData\Roaming\Mozilla\Firefox\Profiles"

profiles = {
    "1": {"type": "edge", "path": base_path_edge, "profile": "Default", "name": "Edge 1 - Herbiglow"},
    "2": {"type": "edge", "path": base_path_edge, "profile": "Profile 1", "name": "Edge 2 - Ciara Indonesia"},
    "3": {"type": "firefox", "path": base_path_firefox, "profile": "jtkkxnwv.default-release", "name": "Firefox - Harnisch"},
    "5": {"type": "brave", "path": base_path_brave, "profile": "Default", "name": "Brave - Heirbikids"},
}

# MEMBUKA BROWSER
def start_browser(choice):
    selected = profiles.get(choice)
    if not selected:
        print("Pilihan tidak valid.")
        return None

    print("Menutup proses browser lama...")
    if selected['type'] == 'edge':
        os.system("taskkill /F /IM msedge.exe >nul 2>&1")
    elif selected['type'] == 'firefox':
        os.system("taskkill /F /IM firefox.exe >nul 2>&1")
    elif selected['type'] == 'brave':
        os.system("taskkill /F /IM brave.exe >nul 2>&1")
    time.sleep(2)

    print(f"Membuka {selected['name']}...")
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if selected['type'] == 'edge':
        driver_path = os.path.join(current_dir, "msedgedriver.exe")
        if not os.path.exists(driver_path):
            print("msedgedriver.exe tidak ditemukan.")
            return None
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument(f"user-data-dir={selected['path']}")
        options.add_argument(f"profile-directory={selected['profile']}")
        options.add_experimental_option("detach", True)
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
            print(f"Gagal buka Firefox: {e}")
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
            print(f"Gagal buka Brave: {e}")
            return None

    driver.maximize_window()
    return driver

# ISI INPUT (CLEAR DULU BARU ISI)
def isi_input(driver, xpath, value, keterangan):
    try:
        elem = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        time.sleep(0.5)
        elem.click()
        elem.send_keys(Keys.CONTROL + "a")
        elem.send_keys(Keys.DELETE)
        elem.send_keys(value)
        print(f"Isi {keterangan}: {value}")
    except Exception as e:
        print(f"Gagal isi {keterangan}: {e}")

# MAIN LOGIC - DUPLIKAT VOUCHER TIKTOK SHOP
def run_tiktok(driver, nama_lama, nama_baru, kode_klaim, tgl_mulai, jam_mulai):
    url = "https://seller-id.tiktok.com/marketing/voucher/list"
    print("Membuka halaman voucher TikTok Shop Seller...")
    driver.get(url)
    time.sleep(15)  # Kasih waktu load penuh

    print("Mencari voucher lama...")
    found = False
    for _ in range(20):
        try:
            voucher_row = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f"//tr[.//div[contains(text(), '{nama_lama}')]]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", voucher_row)
            print("Voucher ditemukan.")
            found = True
            break
        except:
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(2)

    if not found:
        print("Voucher lama tidak ditemukan.")
        return

    # Klik duplikat
    try:
        duplikat_btn = voucher_row.find_element(By.XPATH, ".//button[contains(., 'Duplikat') or .//span[contains(text(), 'Duplikat')]]")
        driver.execute_script("arguments[0].click();", duplikat_btn)
        print("Duplikat diklik.")
    except:
        print("Gagal klik duplikat.")
        return

    time.sleep(10)

    # Isi nama voucher
    isi_input(driver, "//input[contains(@placeholder, 'Nama voucher') or contains(@placeholder, 'Nama promosi')]", nama_baru, "Nama Voucher Baru")

    # Isi kode klaim
    isi_input(driver, "//input[contains(@placeholder, 'Kode') or contains(@placeholder, 'Claim code')]", kode_klaim, "Kode Klaim")

    # Isi tanggal mulai
    isi_input(driver, "//input[@placeholder='Waktu mulai']", tgl_mulai, "Tanggal Mulai")

    # Isi jam mulai
    isi_input(driver, "(//input[@placeholder='Pilih waktu'])[1]", jam_mulai, "Jam Mulai")

    # Isi tanggal selesai (+25 hari)
    tgl_mulai_obj = datetime.strptime(tgl_mulai, "%d/%m/%Y")
    tgl_selesai = (tgl_mulai_obj + timedelta(days=25)).strftime("%d/%m/%Y")
    isi_input(driver, "//input[@placeholder='Waktu selesai']", tgl_selesai, "Tanggal Selesai")

    # Isi jam selesai
    isi_input(driver, "(//input[@placeholder='Pilih waktu'])[2]", "23:59", "Jam Selesai")

    print("\nSelesai.")
    print("Nama, kode, tanggal & jam sudah diisi.")
    print("Silakan isi kuota, min belanja, diskon, lalu klik Buat Voucher manual.")

# MENU UTAMA
if __name__ == "__main__":
    print("\nBOT DUPLIKAT VOUCHER TIKTOK SHOP SELLER\n")

    print("Pilih akun:")
    for k, v in profiles.items():
        print(f"   {k}. {v['name']}")
    choice = input("Masukkan nomor: ").strip()

    if choice not in profiles:
        print("Nomor tidak valid.")
        exit()

    print("\nInput data voucher:")

    nama_lama = input("Nama voucher lama: ").strip()
    nama_baru = input("Nama voucher baru: ").strip()
    kode_klaim = input("Kode klaim baru: ").strip()
    tgl_mulai = input("Tanggal mulai (DD/MM/YYYY): ").strip() or datetime.now().strftime("%d/%m/%Y")
    jam_mulai = input("Jam mulai (HH:MM): ").strip() or "00:00"

    print("\nSummary:")
    print(f"Akun: {profiles[choice]['name']}")
    print(f"Duplikat dari: {nama_lama}")
    print(f"Nama baru: {nama_baru}")
    print(f"Kode: {kode_klaim}")
    print(f"Periode: {tgl_mulai} {jam_mulai} - +25 hari 23:59")

    confirm = input("\nLanjut? (y/n): ").lower()
    if confirm != 'y':
        print("Dibatalkan.")
        exit()

    driver = start_browser(choice)
    if driver:
        run_tiktok(driver, nama_lama, nama_baru, kode_klaim, tgl_mulai, jam_mulai)
        print("\nBot selesai. Browser tetap terbuka.")
    else:
        print("Gagal buka browser.")
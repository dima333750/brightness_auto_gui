import sys
import os
import threading
import time
import math
import subprocess
import configparser
from datetime import datetime
from tkinter import (
    Tk, Frame, Label, Entry, Button, Text, Scrollbar,
    VERTICAL, RIGHT, X, Y, BOTH, END, W, E, N, S, LEFT,
    BooleanVar, Checkbutton, OptionMenu, StringVar, messagebox
)
import pystray
from PIL import Image, ImageDraw

# ====== DEFAULT SETTINGS ======
DEFAULT_CONFIG = {
    'LAT': '50',
    'LON': '170',
    'MIN_BR': '1',
    'MAX_BR': '99',
    'COEFF': '1.0',
    'DEBUG': 'True',
    'SLEEP_INTERVAL': '30',
    'LANGUAGE': 'en',
    'START_TRAY': 'False',
    # Новые настройки (пункты 1–6)
    'BATTERY_HIGH_THRESHOLD': '51',
    'BATTERY_HIGH_REDUCTION': '10',
    'BATTERY_LOW_THRESHOLD': '50',
    'BATTERY_LOW_REDUCTION': '20',
    'LOG_MAX_LINES': '1000',
    'MUTEX_NAME': 'Global\\BrightnessAutoMutex',
    'WINDOW_WIDTH': '750',
    'WINDOW_HEIGHT': '650',
    'MONITOR_INDEX': '1',
    'EARTH_TILT': '23.44',
    'DAY_OFFSET': '284',
    'DAYS_IN_YEAR': '365',
}
CONFIG_FILE = 'config.ini'

# ====== LOAD TRANSLATIONS ======
STRINGS = {}

def load_language(lang):
    global STRINGS
    # Base English dictionary (used as fallback)
    base_strings = {
        'title': 'Brightness Auto',
        'settings': 'Settings',
        'log': 'Log',
        'lat': 'Latitude',
        'lon': 'Longitude',
        'min_br': 'Min brightness',
        'max_br': 'Max brightness',
        'coeff': 'Coefficient',
        'debug': 'Debug mode',
        'interval': 'Update interval (sec)',
        'save': 'Save',
        'reset': 'Reset to defaults',
        'language': 'Language',
        'tray_start': 'Start in tray',
        'tooltip_lat': 'Geographic latitude in degrees (e.g., 56)',
        'tooltip_lon': 'Geographic longitude in degrees (e.g., 44)',
        'tooltip_min_br': 'Minimum brightness at night (1–5)',
        'tooltip_max_br': 'Maximum brightness during day (up to 100)',
        'tooltip_coeff': 'Overall multiplier (e.g., 0.9 or 1.1)',
        'tooltip_debug': 'Show detailed logs in window',
        'tooltip_interval': 'How often to check and change brightness (seconds)',
        'tooltip_language': 'Interface language (restarts window)',
        'tooltip_tray_start': 'Start minimized to system tray',
        'save_success': 'Settings saved',
        'reset_success': 'Settings reset to defaults',
        'error_invalid': 'Invalid data',
        'error_min_max': 'MIN_BR must be from 0 to MAX_BR, MAX_BR up to 100',
        'error_interval': 'Interval must be >= 1 second',
        'tray_title': 'Brightness Auto',
        'tray_show': 'Show',
        'tray_exit': 'Exit',
        'battery_status': 'Battery status',
        'charging': 'charging',
        'discharging': 'discharging',
        'no_battery': 'no battery',
        'high_charge': 'High charge (>51%) → -10',
        'low_charge': 'Low charge (<50%) → -20',
        'night': 'Night – brightness minimal',
        'first_half': 'First half of day, progress {:.2f}',
        'second_half': 'Second half of day, progress {:.2f}',
        'brightness_calc': 'Brightness: base {}, final {}',
        'current_brightness': 'Current monitor brightness: {}',
        'worker_error': 'Worker loop error: {}',
        'brightness_set_error': 'Brightness set error: {}',
        'sunrise_sunset_log': 'Sunrise: {:.2f} h, Sunset: {:.2f} h, Current: {:.2f} h',
        'hint_title': 'Hint',
        'no_tooltip': 'No description for this parameter.',
        'charge_label': 'charge',
        'copy_log': 'Copy log',
        # Новые строки для расширенных настроек
        'advanced': 'Advanced settings',
        'battery_high_threshold': 'Battery high threshold (%)',
        'battery_high_reduction': 'Reduction at high charge',
        'battery_low_threshold': 'Battery low threshold (%)',
        'battery_low_reduction': 'Reduction at low charge',
        'log_max_lines': 'Max log lines',
        'mutex_name': 'Mutex name (restart required)',
        'window_width': 'Window width',
        'window_height': 'Window height',
        'monitor_index': 'Monitor index',
        'earth_tilt': 'Earth axial tilt (deg)',
        'day_offset': 'Day offset for declination',
        'days_in_year': 'Days in year',
        'tooltip_battery_high_threshold': 'If battery charge > this value, brightness is reduced by high reduction value.',
        'tooltip_battery_high_reduction': 'Reduction amount when battery is highly charged.',
        'tooltip_battery_low_threshold': 'If battery charge < this value, brightness is reduced by low reduction value.',
        'tooltip_battery_low_reduction': 'Reduction amount when battery is low.',
        'tooltip_log_max_lines': 'Maximum number of lines kept in the log.',
        'tooltip_mutex_name': 'Name of the system mutex to prevent multiple instances. Change requires restart.',
        'tooltip_window_width': 'Width of the main window in pixels.',
        'tooltip_window_height': 'Height of the main window in pixels.',
        'tooltip_monitor_index': 'Index of the monitor to adjust brightness (1-based).',
        'tooltip_earth_tilt': 'Axial tilt of Earth in degrees (23.44).',
        'tooltip_day_offset': 'Offset day for solar declination calculation (default 284).',
        'tooltip_days_in_year': 'Number of days in a year (default 365).',
    }
    # Try to load language-specific file ab_<lang>.txt
    lang_file = f'ab_{lang}.txt'
    try:
        with open(lang_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, val = line.split('=', 1)
                    key = key.strip()
                    val = val.strip()
                    if key in base_strings:
                        base_strings[key] = val
    except FileNotFoundError:
        # If file not found, keep base English
        pass
    STRINGS = base_strings
    print(f"Loaded language: {lang}")

# ====== CONFIG HANDLING ======
def load_config():
    config = configparser.ConfigParser()
    config['Settings'] = DEFAULT_CONFIG
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    cfg = {
        'LAT': float(config['Settings'].get('LAT', DEFAULT_CONFIG['LAT'])),
        'LON': float(config['Settings'].get('LON', DEFAULT_CONFIG['LON'])),
        'MIN_BR': int(config['Settings'].get('MIN_BR', DEFAULT_CONFIG['MIN_BR'])),
        'MAX_BR': int(config['Settings'].get('MAX_BR', DEFAULT_CONFIG['MAX_BR'])),
        'COEFF': float(config['Settings'].get('COEFF', DEFAULT_CONFIG['COEFF'])),
        'DEBUG': config['Settings'].getboolean('DEBUG', DEFAULT_CONFIG['DEBUG'] == 'True'),
        'SLEEP_INTERVAL': int(config['Settings'].get('SLEEP_INTERVAL', DEFAULT_CONFIG['SLEEP_INTERVAL'])),
        'LANGUAGE': config['Settings'].get('LANGUAGE', DEFAULT_CONFIG['LANGUAGE']),
        'START_TRAY': config['Settings'].getboolean('START_TRAY', DEFAULT_CONFIG['START_TRAY'] == 'True'),
        # Новые настройки
        'BATTERY_HIGH_THRESHOLD': int(config['Settings'].get('BATTERY_HIGH_THRESHOLD', DEFAULT_CONFIG['BATTERY_HIGH_THRESHOLD'])),
        'BATTERY_HIGH_REDUCTION': int(config['Settings'].get('BATTERY_HIGH_REDUCTION', DEFAULT_CONFIG['BATTERY_HIGH_REDUCTION'])),
        'BATTERY_LOW_THRESHOLD': int(config['Settings'].get('BATTERY_LOW_THRESHOLD', DEFAULT_CONFIG['BATTERY_LOW_THRESHOLD'])),
        'BATTERY_LOW_REDUCTION': int(config['Settings'].get('BATTERY_LOW_REDUCTION', DEFAULT_CONFIG['BATTERY_LOW_REDUCTION'])),
        'LOG_MAX_LINES': int(config['Settings'].get('LOG_MAX_LINES', DEFAULT_CONFIG['LOG_MAX_LINES'])),
        'MUTEX_NAME': config['Settings'].get('MUTEX_NAME', DEFAULT_CONFIG['MUTEX_NAME']),
        'WINDOW_WIDTH': int(config['Settings'].get('WINDOW_WIDTH', DEFAULT_CONFIG['WINDOW_WIDTH'])),
        'WINDOW_HEIGHT': int(config['Settings'].get('WINDOW_HEIGHT', DEFAULT_CONFIG['WINDOW_HEIGHT'])),
        'MONITOR_INDEX': int(config['Settings'].get('MONITOR_INDEX', DEFAULT_CONFIG['MONITOR_INDEX'])),
        'EARTH_TILT': float(config['Settings'].get('EARTH_TILT', DEFAULT_CONFIG['EARTH_TILT'])),
        'DAY_OFFSET': int(config['Settings'].get('DAY_OFFSET', DEFAULT_CONFIG['DAY_OFFSET'])),
        'DAYS_IN_YEAR': int(config['Settings'].get('DAYS_IN_YEAR', DEFAULT_CONFIG['DAYS_IN_YEAR'])),
    }
    return cfg

def save_config(cfg):
    config = configparser.ConfigParser()
    config['Settings'] = {
        'LAT': str(cfg['LAT']),
        'LON': str(cfg['LON']),
        'MIN_BR': str(cfg['MIN_BR']),
        'MAX_BR': str(cfg['MAX_BR']),
        'COEFF': str(cfg['COEFF']),
        'DEBUG': str(cfg['DEBUG']),
        'SLEEP_INTERVAL': str(cfg['SLEEP_INTERVAL']),
        'LANGUAGE': cfg['LANGUAGE'],
        'START_TRAY': str(cfg['START_TRAY']),
        # Новые настройки
        'BATTERY_HIGH_THRESHOLD': str(cfg['BATTERY_HIGH_THRESHOLD']),
        'BATTERY_HIGH_REDUCTION': str(cfg['BATTERY_HIGH_REDUCTION']),
        'BATTERY_LOW_THRESHOLD': str(cfg['BATTERY_LOW_THRESHOLD']),
        'BATTERY_LOW_REDUCTION': str(cfg['BATTERY_LOW_REDUCTION']),
        'LOG_MAX_LINES': str(cfg['LOG_MAX_LINES']),
        'MUTEX_NAME': cfg['MUTEX_NAME'],
        'WINDOW_WIDTH': str(cfg['WINDOW_WIDTH']),
        'WINDOW_HEIGHT': str(cfg['WINDOW_HEIGHT']),
        'MONITOR_INDEX': str(cfg['MONITOR_INDEX']),
        'EARTH_TILT': str(cfg['EARTH_TILT']),
        'DAY_OFFSET': str(cfg['DAY_OFFSET']),
        'DAYS_IN_YEAR': str(cfg['DAYS_IN_YEAR']),
    }
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        config.write(f)

def reset_config():
    return {
        'LAT': float(DEFAULT_CONFIG['LAT']),
        'LON': float(DEFAULT_CONFIG['LON']),
        'MIN_BR': int(DEFAULT_CONFIG['MIN_BR']),
        'MAX_BR': int(DEFAULT_CONFIG['MAX_BR']),
        'COEFF': float(DEFAULT_CONFIG['COEFF']),
        'DEBUG': DEFAULT_CONFIG['DEBUG'] == 'True',
        'SLEEP_INTERVAL': int(DEFAULT_CONFIG['SLEEP_INTERVAL']),
        'LANGUAGE': DEFAULT_CONFIG['LANGUAGE'],
        'START_TRAY': DEFAULT_CONFIG['START_TRAY'] == 'True',
        # Новые настройки
        'BATTERY_HIGH_THRESHOLD': int(DEFAULT_CONFIG['BATTERY_HIGH_THRESHOLD']),
        'BATTERY_HIGH_REDUCTION': int(DEFAULT_CONFIG['BATTERY_HIGH_REDUCTION']),
        'BATTERY_LOW_THRESHOLD': int(DEFAULT_CONFIG['BATTERY_LOW_THRESHOLD']),
        'BATTERY_LOW_REDUCTION': int(DEFAULT_CONFIG['BATTERY_LOW_REDUCTION']),
        'LOG_MAX_LINES': int(DEFAULT_CONFIG['LOG_MAX_LINES']),
        'MUTEX_NAME': DEFAULT_CONFIG['MUTEX_NAME'],
        'WINDOW_WIDTH': int(DEFAULT_CONFIG['WINDOW_WIDTH']),
        'WINDOW_HEIGHT': int(DEFAULT_CONFIG['WINDOW_HEIGHT']),
        'MONITOR_INDEX': int(DEFAULT_CONFIG['MONITOR_INDEX']),
        'EARTH_TILT': float(DEFAULT_CONFIG['EARTH_TILT']),
        'DAY_OFFSET': int(DEFAULT_CONFIG['DAY_OFFSET']),
        'DAYS_IN_YEAR': int(DEFAULT_CONFIG['DAYS_IN_YEAR']),
    }

# ====== MAIN APPLICATION ======
class BrightnessApp:
    def __init__(self):
        self.config = load_config()
        load_language(self.config['LANGUAGE'])
        self.running = True
        self.log_lines = []
        self.log_text = None
        self.entries = {}
        self.checks = {}
        self.option_menus = {}
        self.tooltips = {}

        self.worker_thread = threading.Thread(target=self.worker_loop, daemon=True)
        self.worker_thread.start()

        self.root = Tk()
        self.root.title(STRINGS.get('title', 'Brightness Auto'))
        # Установка размера окна из конфига
        self.root.geometry(f"{self.config['WINDOW_WIDTH']}x{self.config['WINDOW_HEIGHT']}")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.build_gui()
        self.setup_tray()

        if self.config['START_TRAY']:
            self.root.withdraw()
        else:
            self.root.deiconify()

        self.root.mainloop()

    def get_available_languages(self):
        """Scan for ab_*.txt files and return list of language codes."""
        langs = ['en']  # English is always available as fallback
        for f in os.listdir('.'):
            if f.startswith('ab_') and f.endswith('.txt'):
                lang_code = f[3:-4]  # extract part between 'ab_' and '.txt'
                if lang_code and lang_code not in langs:
                    langs.append(lang_code)
        return langs

    def build_gui(self):
        # Clear all widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # ---------- Settings Panel ----------
        settings_frame = Frame(main_frame)
        settings_frame.pack(fill=X, pady=5)

        Label(settings_frame, text=STRINGS.get('settings', 'Settings'), font=("Arial", 12, "bold"))\
            .grid(row=0, column=0, columnspan=6, sticky=W, pady=5)

        row = 1
        labels_keys = [
            ('lat', 'LAT'),
            ('lon', 'LON'),
            ('min_br', 'MIN_BR'),
            ('max_br', 'MAX_BR'),
            ('coeff', 'COEFF')
        ]
        for i, (label_key, cfg_key) in enumerate(labels_keys):
            Label(settings_frame, text=STRINGS.get(label_key, label_key)+":")\
                .grid(row=row+i, column=0, sticky=W, padx=5, pady=2)
            ent = Entry(settings_frame, width=12)
            ent.insert(0, str(self.config[cfg_key]))
            ent.grid(row=row+i, column=1, sticky=W, padx=5, pady=2)
            self.entries[cfg_key] = ent
            Button(settings_frame, text="?", width=2, command=lambda k=cfg_key: self.show_tooltip(k))\
                .grid(row=row+i, column=2, padx=2)

        # DEBUG
        self.debug_var = BooleanVar(value=self.config['DEBUG'])
        Checkbutton(settings_frame, text=STRINGS.get('debug', 'DEBUG'), variable=self.debug_var)\
            .grid(row=row+5, column=0, columnspan=2, sticky=W, padx=5, pady=2)
        Button(settings_frame, text="?", width=2, command=lambda: self.show_tooltip('DEBUG'))\
            .grid(row=row+5, column=2, sticky=W, padx=2)

        # Interval
        Label(settings_frame, text=STRINGS.get('interval', 'Update interval (sec):'))\
            .grid(row=row+6, column=0, sticky=W, padx=5, pady=2)
        self.interval_var = Entry(settings_frame, width=12)
        self.interval_var.insert(0, str(self.config['SLEEP_INTERVAL']))
        self.interval_var.grid(row=row+6, column=1, sticky=W, padx=5, pady=2)
        Button(settings_frame, text="?", width=2, command=lambda: self.show_tooltip('SLEEP_INTERVAL'))\
            .grid(row=row+6, column=2, sticky=W, padx=2)

        # Language - dynamically built from available files
        self.available_langs = self.get_available_languages()
        Label(settings_frame, text=STRINGS.get('language', 'Language:'))\
            .grid(row=row+7, column=0, sticky=W, padx=5, pady=2)
        self.lang_var = StringVar(value=self.config['LANGUAGE'])
        # Ensure current language is in the list, otherwise add it
        if self.config['LANGUAGE'] not in self.available_langs:
            self.available_langs.append(self.config['LANGUAGE'])
        self.lang_menu = OptionMenu(settings_frame, self.lang_var, *self.available_langs)
        self.lang_menu.grid(row=row+7, column=1, sticky=W, padx=5, pady=2)
        Button(settings_frame, text="?", width=2, command=lambda: self.show_tooltip('LANGUAGE'))\
            .grid(row=row+7, column=2, sticky=W, padx=2)

        # START_TRAY
        self.tray_var = BooleanVar(value=self.config['START_TRAY'])
        Checkbutton(settings_frame, text=STRINGS.get('tray_start', 'Start in tray'), variable=self.tray_var)\
            .grid(row=row+8, column=0, columnspan=2, sticky=W, padx=5, pady=2)
        Button(settings_frame, text="?", width=2, command=lambda: self.show_tooltip('START_TRAY'))\
            .grid(row=row+8, column=2, sticky=W, padx=2)

        # Buttons
        btn_frame = Frame(settings_frame)
        btn_frame.grid(row=row+9, column=0, columnspan=4, pady=10)
        Button(btn_frame, text=STRINGS.get('save', 'Save'), command=self.save_settings, width=12)\
            .pack(side=LEFT, padx=5)
        Button(btn_frame, text=STRINGS.get('reset', 'Reset to defaults'), command=self.reset_settings, width=15)\
            .pack(side=LEFT, padx=5)

        # ---------- Advanced Settings Panel ----------
        adv_frame = Frame(main_frame)
        adv_frame.pack(fill=X, pady=5)

        Label(adv_frame, text=STRINGS.get('advanced', 'Advanced settings'), font=("Arial", 10, "bold"))\
            .grid(row=0, column=0, columnspan=8, sticky=W, pady=5)

        adv_row = 1
        adv_keys = [
            ('battery_high_threshold', 'BATTERY_HIGH_THRESHOLD'),
            ('battery_high_reduction', 'BATTERY_HIGH_REDUCTION'),
            ('battery_low_threshold', 'BATTERY_LOW_THRESHOLD'),
            ('battery_low_reduction', 'BATTERY_LOW_REDUCTION'),
            ('log_max_lines', 'LOG_MAX_LINES'),
            ('mutex_name', 'MUTEX_NAME'),
            ('window_width', 'WINDOW_WIDTH'),
            ('window_height', 'WINDOW_HEIGHT'),
            ('monitor_index', 'MONITOR_INDEX'),
            ('earth_tilt', 'EARTH_TILT'),
            ('day_offset', 'DAY_OFFSET'),
            ('days_in_year', 'DAYS_IN_YEAR'),
        ]
        # Размещаем в две колонки для компактности
        for idx, (label_key, cfg_key) in enumerate(adv_keys):
            col = 0 if idx < len(adv_keys)//2 else 4
            row_off = idx if idx < len(adv_keys)//2 else idx - len(adv_keys)//2
            # Используем grid с учетом колонок
            Label(adv_frame, text=STRINGS.get(label_key, label_key)+":")\
                .grid(row=adv_row+row_off, column=col, sticky=W, padx=5, pady=2)
            ent = Entry(adv_frame, width=12)
            ent.insert(0, str(self.config[cfg_key]))
            ent.grid(row=adv_row+row_off, column=col+1, sticky=W, padx=5, pady=2)
            self.entries[cfg_key] = ent
            Button(adv_frame, text="?", width=2, command=lambda k=cfg_key: self.show_tooltip(k))\
                .grid(row=adv_row+row_off, column=col+2, padx=2)

        # ---------- Log Panel ----------
        log_frame = Frame(main_frame)
        log_frame.pack(fill=BOTH, expand=True, pady=5)

        log_header_frame = Frame(log_frame)
        log_header_frame.pack(fill=X, pady=2)

        Label(log_header_frame, text=STRINGS.get('log', 'Log'), font=("Arial", 10, "bold"))\
            .pack(side=LEFT)

        Button(log_header_frame, text=STRINGS.get('copy_log', 'Copy log'),
               command=self.copy_log).pack(side=RIGHT, padx=5)

        text_frame = Frame(log_frame)
        text_frame.pack(fill=BOTH, expand=True)

        self.log_text = Text(text_frame, wrap='word', height=15)
        self.log_text.pack(side=LEFT, fill=BOTH, expand=True)

        scroll = Scrollbar(text_frame, orient=VERTICAL, command=self.log_text.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.log_text.config(yscrollcommand=scroll.set)

        # Restore log lines
        if self.log_lines:
            for line in self.log_lines:
                self.log_text.insert(END, line + "\n")
            self.log_text.see(END)

    def show_tooltip(self, key):
        tip_text = STRINGS.get('tooltip_' + key.lower(), '')
        if not tip_text:
            tip_text = STRINGS.get('no_tooltip', 'No description for this parameter.')
        messagebox.showinfo(STRINGS.get('hint_title', 'Hint'), tip_text)

    def copy_log(self):
        content = self.log_text.get("1.0", END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            msg = "Log copied to clipboard" if self.config['LANGUAGE'] == 'en' else "Лог скопирован в буфер обмена"
            messagebox.showinfo(STRINGS.get('hint_title', 'Hint'), msg)
        else:
            msg = "Log is empty" if self.config['LANGUAGE'] == 'en' else "Лог пуст"
            messagebox.showinfo(STRINGS.get('hint_title', 'Hint'), msg)

    def setup_tray(self):
        image = Image.new('RGB', (64, 64), color='gray')
        draw = ImageDraw.Draw(image)
        draw.rectangle((16, 16, 48, 48), fill='yellow', outline='black')
        draw.text((24, 20), "B", fill='black')

        menu = (
            pystray.MenuItem(STRINGS.get('tray_show', 'Show'), self.show_window, default=True),
            pystray.MenuItem(STRINGS.get('tray_exit', 'Exit'), self.quit_app)
        )
        self.tray_icon = pystray.Icon(
            "BrightnessAuto",
            image,
            STRINGS.get('tray_title', 'Brightness Auto'),
            menu,
            on_click=self.show_window
        )
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    # ---- GUI actions that may be called from other threads ----
    def show_window(self, icon=None, item=None):
        self.root.after(0, self._show_window)

    def _show_window(self):
        self.root.deiconify()
        self.root.lift()

    def hide_window(self):
        self.root.withdraw()

    def quit_app(self, icon=None, item=None):
        self.root.after(0, self._quit_app)

    def _quit_app(self):
        self.running = False
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()
        self.root.destroy()
        sys.exit(0)

    # ---- Save / Reset ----
    def save_settings(self):
        try:
            new_lang = self.lang_var.get()
            # Validate that the selected language is in available list
            if new_lang not in self.get_available_languages():
                # if not, add it anyway (user might have manually typed)
                pass

            new_config = {
                'LAT': float(self.entries['LAT'].get()),
                'LON': float(self.entries['LON'].get()),
                'MIN_BR': int(self.entries['MIN_BR'].get()),
                'MAX_BR': int(self.entries['MAX_BR'].get()),
                'COEFF': float(self.entries['COEFF'].get()),
                'DEBUG': self.debug_var.get(),
                'SLEEP_INTERVAL': int(self.interval_var.get()),
                'LANGUAGE': new_lang,
                'START_TRAY': self.tray_var.get(),
                # Новые настройки
                'BATTERY_HIGH_THRESHOLD': int(self.entries['BATTERY_HIGH_THRESHOLD'].get()),
                'BATTERY_HIGH_REDUCTION': int(self.entries['BATTERY_HIGH_REDUCTION'].get()),
                'BATTERY_LOW_THRESHOLD': int(self.entries['BATTERY_LOW_THRESHOLD'].get()),
                'BATTERY_LOW_REDUCTION': int(self.entries['BATTERY_LOW_REDUCTION'].get()),
                'LOG_MAX_LINES': int(self.entries['LOG_MAX_LINES'].get()),
                'MUTEX_NAME': self.entries['MUTEX_NAME'].get().strip(),
                'WINDOW_WIDTH': int(self.entries['WINDOW_WIDTH'].get()),
                'WINDOW_HEIGHT': int(self.entries['WINDOW_HEIGHT'].get()),
                'MONITOR_INDEX': int(self.entries['MONITOR_INDEX'].get()),
                'EARTH_TILT': float(self.entries['EARTH_TILT'].get()),
                'DAY_OFFSET': int(self.entries['DAY_OFFSET'].get()),
                'DAYS_IN_YEAR': int(self.entries['DAYS_IN_YEAR'].get()),
            }
            if new_config['MIN_BR'] < 0 or new_config['MAX_BR'] > 100 or new_config['MIN_BR'] > new_config['MAX_BR']:
                raise ValueError(STRINGS.get('error_min_max', 'MIN_BR must be >= 0 and <= MAX_BR, MAX_BR <= 100'))
            if new_config['SLEEP_INTERVAL'] < 1:
                raise ValueError(STRINGS.get('error_interval', 'Interval must be >= 1 second'))
            # Валидация дополнительных параметров
            if new_config['BATTERY_HIGH_THRESHOLD'] < 0 or new_config['BATTERY_HIGH_THRESHOLD'] > 100:
                raise ValueError("Battery high threshold must be between 0 and 100")
            if new_config['BATTERY_LOW_THRESHOLD'] < 0 or new_config['BATTERY_LOW_THRESHOLD'] > 100:
                raise ValueError("Battery low threshold must be between 0 and 100")
            if new_config['BATTERY_HIGH_THRESHOLD'] <= new_config['BATTERY_LOW_THRESHOLD']:
                raise ValueError("High threshold must be greater than low threshold")
            if new_config['WINDOW_WIDTH'] < 200 or new_config['WINDOW_HEIGHT'] < 200:
                raise ValueError("Window dimensions must be at least 200x200")
            if new_config['MONITOR_INDEX'] < 1:
                raise ValueError("Monitor index must be >= 1")

            old_lang = self.config['LANGUAGE']
            self.config = new_config
            save_config(self.config)

            # Применяем размер окна сразу, если изменился
            self.root.geometry(f"{self.config['WINDOW_WIDTH']}x{self.config['WINDOW_HEIGHT']}")

            if old_lang != self.config['LANGUAGE']:
                load_language(self.config['LANGUAGE'])
                self.build_gui()
                self.root.title(STRINGS.get('title', 'Brightness Auto'))
                # recreate tray icon with new language
                if self.tray_icon:
                    self.tray_icon.stop()
                self.setup_tray()
            else:
                self.log_message(STRINGS.get('save_success', 'Settings saved'))

            messagebox.showinfo("", STRINGS.get('save_success', 'Settings saved'))
        except Exception as e:
            messagebox.showerror(STRINGS.get('error_invalid', 'Invalid data'), str(e))

    def reset_settings(self):
        self.config = reset_config()
        for key, ent in self.entries.items():
            ent.delete(0, END)
            ent.insert(0, str(self.config[key]))
        self.debug_var.set(self.config['DEBUG'])
        self.interval_var.delete(0, END)
        self.interval_var.insert(0, str(self.config['SLEEP_INTERVAL']))
        self.lang_var.set(self.config['LANGUAGE'])
        self.tray_var.set(self.config['START_TRAY'])
        save_config(self.config)
        load_language(self.config['LANGUAGE'])
        self.build_gui()
        self.root.title(STRINGS.get('title', 'Brightness Auto'))
        self.root.geometry(f"{self.config['WINDOW_WIDTH']}x{self.config['WINDOW_HEIGHT']}")
        if self.tray_icon:
            self.tray_icon.stop()
        self.setup_tray()
        self.log_message(STRINGS.get('reset_success', 'Settings reset to defaults'))
        messagebox.showinfo("", STRINGS.get('reset_success', 'Settings reset to defaults'))

    def log_message(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_msg = f"[{timestamp}] {msg}"
        self.log_lines.append(full_msg)
        # Используем настройку максимального числа строк
        max_lines = self.config.get('LOG_MAX_LINES', 1000)
        if len(self.log_lines) > max_lines:
            self.log_lines = self.log_lines[-max_lines:]
        if self.log_text:
            self.log_text.insert(END, full_msg + "\n")
            self.log_text.see(END)
        else:
            print(full_msg)

    # ---------- Worker Thread ----------
    def worker_loop(self):
        while self.running:
            try:
                cfg = self.config
                status, charge = self.get_battery_status()
                if cfg['DEBUG']:
                    status_text = {1: STRINGS.get('discharging', 'discharging'),
                                   2: STRINGS.get('charging', 'charging'),
                                   None: STRINGS.get('no_battery', 'no battery')}
                    self.log_message(f"{STRINGS.get('battery_status', 'Battery status')}: {status_text.get(status, status)}, "
                                     f"{STRINGS.get('charge_label', 'charge')}: {charge}%")

                brightness = self.compute_brightness_by_time(cfg)
                orig = brightness

                # Применяем коррекцию по батарее с использованием настроек
                if status == 1 and charge is not None:
                    high_thr = cfg.get('BATTERY_HIGH_THRESHOLD', 51)
                    high_red = cfg.get('BATTERY_HIGH_REDUCTION', 10)
                    low_thr = cfg.get('BATTERY_LOW_THRESHOLD', 50)
                    low_red = cfg.get('BATTERY_LOW_REDUCTION', 20)
                    if charge > high_thr:
                        brightness -= high_red
                        if cfg['DEBUG']:
                            self.log_message(f"High charge (> {high_thr}%) → -{high_red}")
                    elif charge < low_thr:
                        brightness -= low_red
                        if cfg['DEBUG']:
                            self.log_message(f"Low charge (< {low_thr}%) → -{low_red}")

                if brightness < 0:
                    brightness = 0

                if cfg['DEBUG']:
                    self.log_message(STRINGS.get('brightness_calc', 'Brightness: base {}, final {}')
                                     .format(orig, brightness))

                self.set_brightness(brightness)

                if cfg['DEBUG']:
                    try:
                        cmd = 'powershell -Command "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness"'
                        current = subprocess.check_output(cmd, shell=True, text=True).strip()
                        self.log_message(STRINGS.get('current_brightness', 'Current monitor brightness: {}')
                                         .format(current))
                    except:
                        pass

            except Exception as e:
                self.log_message(STRINGS.get('worker_error', 'Worker loop error: {}').format(e))

            time.sleep(cfg['SLEEP_INTERVAL'])

    # ---------- Helper functions ----------
    def get_battery_status(self):
        try:
            cmd = (
                'powershell -Command "'
                '$b=Get-WmiObject Win32_Battery; '
                'Write-Host $b.BatteryStatus $b.EstimatedChargeRemaining"'
            )
            output = subprocess.check_output(cmd, shell=True, text=True).strip()
            if not output:
                return None, None
            parts = output.split()
            if len(parts) >= 2:
                status = int(parts[0])
                charge = int(parts[1])
                return status, charge
            else:
                return None, None
        except Exception:
            return None, None

    def set_brightness(self, brightness):
        try:
            monitor_idx = self.config.get('MONITOR_INDEX', 1)
            cmd = (
                f'powershell -Command "'
                f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods)'
                f'.WmiSetBrightness({monitor_idx},{brightness})"'
            )
            subprocess.run(cmd, shell=True, check=False)
        except Exception as e:
            self.log_message(STRINGS.get('brightness_set_error', 'Brightness set error: {}').format(e))

    def compute_brightness_by_time(self, cfg):
        now = datetime.now().astimezone()
        doy = now.timetuple().tm_yday
        lat_rad = math.radians(cfg['LAT'])

        # Используем настройки для расчёта склонения
        tilt = cfg.get('EARTH_TILT', 23.44)
        day_off = cfg.get('DAY_OFFSET', 284)
        days_yr = cfg.get('DAYS_IN_YEAR', 365)
        dec_deg = tilt * math.sin(math.radians((day_off + doy) * 360 / days_yr))
        dec_rad = math.radians(dec_deg)

        cos_ha = -math.tan(lat_rad) * math.tan(dec_rad)
        cos_ha = max(-1.0, min(1.0, cos_ha))
        ha_rad = math.acos(cos_ha)
        ha_deg = math.degrees(ha_rad)

        rise = 12 - ha_deg / 15 - cfg['LON'] / 15
        set_ = 12 + ha_deg / 15 - cfg['LON'] / 15

        tz_offset = now.utcoffset().total_seconds() / 3600
        rise_local = rise + tz_offset
        set_local = set_ + tz_offset

        if rise_local < 0:
            rise_local += 24
        if set_local > 24:
            set_local -= 24

        now_hour = now.hour + now.minute / 60.0

        if cfg['DEBUG']:
            self.log_message(STRINGS.get('sunrise_sunset_log', 'Sunrise: {:.2f} h, Sunset: {:.2f} h, Current: {:.2f} h')
                             .format(rise_local, set_local, now_hour))

        if now_hour < rise_local or now_hour > set_local:
            br = cfg['MIN_BR']
            if cfg['DEBUG']:
                self.log_message(STRINGS.get('night', 'Night – brightness minimal'))
        else:
            day_len = set_local - rise_local
            since_rise = now_hour - rise_local
            half_day = day_len / 2
            if since_rise <= half_day:
                frac = since_rise / half_day
                br = cfg['MIN_BR'] + (cfg['MAX_BR'] - cfg['MIN_BR']) * frac
                if cfg['DEBUG']:
                    self.log_message(STRINGS.get('first_half', 'First half of day, progress {:.2f}').format(frac))
            else:
                frac = (since_rise - half_day) / half_day
                br = cfg['MAX_BR'] - (cfg['MAX_BR'] - cfg['MIN_BR']) * frac
                if cfg['DEBUG']:
                    self.log_message(STRINGS.get('second_half', 'Second half of day, progress {:.2f}').format(frac))

        br = round(br * cfg['COEFF'])
        br = max(cfg['MIN_BR'], min(cfg['MAX_BR'], br))
        return int(br)

# ====== ENTRY POINT ======
if __name__ == "__main__":
    # Загружаем конфиг до создания мьютекса, чтобы использовать имя из настроек
    temp_config = load_config()  # временная загрузка для получения имени мьютекса
    mutex_name = temp_config.get('MUTEX_NAME', 'Global\\BrightnessAutoMutex')

    # ----- Single instance check (Windows named mutex) with error message -----
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        mutex = kernel32.CreateMutexA(None, False, mutex_name.encode('utf-8'))
        if kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
            print("Another instance of Brightness Auto is already running.")
            try:
                root = Tk()
                root.withdraw()
                messagebox.showerror("Already Running", "Brightness Auto is already running.\nPlease close the existing instance.")
                root.destroy()
            except Exception:
                pass
            sys.exit(0)
    except Exception:
        # If mutex creation fails (should not happen on Windows), continue anyway
        pass

    app = BrightnessApp()

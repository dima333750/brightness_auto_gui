# brightness_auto_gui
Brightness auto GUI Windows Geo coordinates
Brightness Auto
https://img.shields.io/badge/python-3.6%252B-blue
https://img.shields.io/badge/license-MIT-green

English
Description
Brightness Auto is a Windows application that automatically adjusts your screen brightness based on the time of day and battery status. It calculates sunrise and sunset times using your geographic coordinates, smoothly transitions brightness between minimum and maximum values during daylight, and applies additional corrections when running on battery (reduces brightness to save power). The program runs in the system tray and provides a simple GUI for configuration.

It is designed for users who want to reduce eye strain and save battery life without manual adjustments.

Features
Automatic brightness adjustment based on time of day (sunrise/sunset).

Smooth transition between configurable minimum and maximum brightness.

Battery‑aware correction: reduces brightness by 10% if charge >51%, by 20% if charge <50% (when discharging).

Configurable geographic latitude/longitude for accurate sunrise/sunset calculations.

Adjustable overall brightness coefficient (multiplier).

Debug mode to monitor calculations and system state.

System tray icon with Show and Exit commands.

Multilingual interface: English and Russian included; easily add your own language.

Start minimized to tray option.

Single instance enforcement (prevents multiple copies).

Requirements
Windows 7 or later (uses PowerShell and WMI).

Python 3.6+ (if running from source) with packages: tkinter, pystray, Pillow, configparser.

Alternatively, download the compiled .exe file (no Python installation required).

Installation
Option 1: Using the executable (recommended for end users)
Download brightness_auto_gui.exe directly from:
https://github.com/dima333750/brightness_auto_gui/blob/main/brightness_auto_gui.exe
(Click the "Download" button or use the raw link.)

Run the downloaded file – no installation needed.

(Optional) Create a shortcut in your Startup folder to launch automatically with Windows.

Option 2: Running from source
Clone the repository or download the source code.

Install required packages:

bash
pip install pystray pillow
(tkinter and configparser are included with Python.)

Run the script:

bash
python brightness_auto_gui.py
Building Executable
If you want to compile the script into a standalone .exe file (no Python required to run), use PyInstaller.

Install PyInstaller:

bash
pip install pyinstaller
Navigate to the folder containing brightness_auto_gui.py.

Run:

bash
pyinstaller --onefile --noconsole brightness_auto_gui.py
The executable will be created in the dist folder.

Make sure all required packages (pystray, Pillow) are installed before building – they will be bundled automatically.

Configuration Settings
All settings are stored in config.ini (auto‑created on first launch). You can change them via the GUI:

Parameter	Description
Latitude	Geographic latitude in degrees (e.g., 56 for Moscow).
Longitude	Geographic longitude in degrees (e.g., 44 for Moscow).
Min brightness	Minimum brightness at night (0–100, recommended 1–5).
Max brightness	Maximum brightness during daytime (up to 100).
Coefficient	Overall multiplier (e.g., 0.9 dims all values, 1.1 brightens).
Debug mode	When enabled, detailed logs are shown in the GUI.
Update interval (sec)	How often the program checks time and adjusts brightness.
Language	Interface language (restarts the GUI when changed).
Start in tray	If checked, the main window is hidden at launch (only tray icon visible).
Tooltips: Click the ? button next to any setting for a brief explanation.

How the Language System Works
The program looks for translation files named ab_XX.txt, where XX is a language code (e.g., en, ru, es).

The default file ab_en.txt is included with all keys.

On startup, it scans the current directory for files matching ab_*.txt and populates the language dropdown menu.

When you select a language, the program reads the corresponding file and replaces the interface strings.

How to Add Your Own Language
Create a copy of ab_en.txt and rename it to ab_XX.txt (replace XX with your language code, e.g., fr for French).

Translate the values (after the = sign) into your language. Do not change the keys.

Place the file in the same folder as the program (or the .exe).

Restart the program – your language will appear in the dropdown menu.

If a translation file is missing, the program falls back to English.

License
This project is licensed under the MIT License – see the LICENSE file for details.

Русский
Описание
Brightness Auto — это приложение для Windows, которое автоматически регулирует яркость экрана в зависимости от времени суток и заряда аккумулятора. Оно рассчитывает время восхода и заката по вашим географическим координатам, плавно изменяет яркость от минимальной до максимальной в течение дня и дополнительно снижает яркость при работе от батареи для экономии энергии. Программа работает в системном трее и имеет простой графический интерфейс для настройки.

Приложение предназначено для тех, кто хочет снизить нагрузку на глаза и продлить время работы от батареи без ручной регулировки.

Возможности
Автоматическая регулировка яркости в зависимости от времени суток (восход/закат).

Плавный переход между настраиваемыми минимальной и максимальной яркостью.

Коррекция по заряду батареи: уменьшение яркости на 10% при заряде >51%, на 20% при заряде <50% (в режиме разряда).

Настраиваемые географическая широта и долгота для точного расчёта восхода/заката.

Общий коэффициент яркости (множитель).

Режим отладки для просмотра расчётов и состояния системы.

Иконка в системном трее с командами Показать и Выход.

Многоязычный интерфейс: английский и русский в комплекте; легко добавить свой язык.

Опция запуска свёрнутым в трей.

Блокировка повторного запуска (предотвращает запуск нескольких копий).

Требования
Windows 7 или новее (используется PowerShell и WMI).

Python 3.6+ (если запуск из исходников) с библиотеками: tkinter, pystray, Pillow, configparser.

Или готовый .exe файл (не требует установки Python).

Установка
Вариант 1: Использование исполняемого файла (рекомендуется для конечных пользователей)
Скачайте brightness_auto_gui.exe напрямую по ссылке:
https://github.com/dima333750/brightness_auto_gui/blob/main/brightness_auto_gui.exe
(Нажмите «Download» или используйте прямую ссылку на файл.)

Запустите скачанный файл – установка не требуется.

(Опционально) Создайте ярлык в папке «Автозагрузка», чтобы программа запускалась вместе с Windows.

Вариант 2: Запуск из исходников
Клонируйте репозиторий или скачайте исходный код.

Установите необходимые пакеты:

bash
pip install pystray pillow
(tkinter и configparser уже входят в состав Python.)

Запустите скрипт:

bash
python brightness_auto_gui.py
Сборка исполняемого файла
Если вы хотите скомпилировать скрипт в отдельный .exe файл (не требующий установки Python), используйте PyInstaller.

Установите PyInstaller:

bash
pip install pyinstaller
Перейдите в папку, где находится brightness_auto_gui.py.

Выполните:

bash
pyinstaller --onefile --noconsole brightness_auto_gui.py
Исполняемый файл появится в папке dist.

Убедитесь, что все необходимые пакеты (pystray, Pillow) установлены перед сборкой – они будут включены автоматически.

Настройки
Все настройки сохраняются в файле config.ini (создаётся при первом запуске). Их можно изменить через интерфейс:

Параметр	Описание
Широта	Географическая широта в градусах (например, 56 для Москвы).
Долгота	Географическая долгота в градусах (например, 44 для Москвы).
Мин. яркость	Минимальная яркость ночью (0–100, рекомендуется 1–5).
Макс. яркость	Максимальная яркость днём (до 100).
Коэффициент	Общий множитель (например, 0.9 – затемнение, 1.1 – осветление).
Режим отладки	При включении в окне отображаются подробные логи.
Интервал обновления (сек)	Как часто программа проверяет время и меняет яркость.
Язык	Язык интерфейса (перезапускает окно при смене).
Запускать в трее	Если отмечено, главное окно скрыто при старте (видна только иконка в трее).
Подсказки: Нажмите кнопку ? рядом с любым параметром для краткого пояснения.

Как работает система языков
Программа ищет файлы переводов с именами ab_XX.txt, где XX – код языка (например, en, ru, es).

Базовый файл ab_en.txt включён в состав и содержит все ключи.

При запуске программа сканирует текущую папку на наличие файлов ab_*.txt и заполняет выпадающий список языков.

При выборе языка программа читает соответствующий файл и заменяет строки интерфейса.

Как добавить свой язык
Создайте копию файла ab_en.txt и переименуйте её в ab_XX.txt (замените XX на код вашего языка, например fr для французского).

Переведите значения (после знака =) на ваш язык. Ключи (слева от =) менять нельзя.

Поместите файл в ту же папку, где находится программа (или .exe).

Перезапустите программу – ваш язык появится в выпадающем списке.

Если файл перевода отсутствует, программа использует английский язык по умолчанию.

Лицензия
Этот проект распространяется под лицензией MIT – подробности в файле LICENSE.

Happy adjusting! / Приятной настройки!


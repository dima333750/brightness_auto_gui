<h1>Brightness Auto GUI for Windows use geo coordinates</h1>


<p>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.6%2B-blue" alt="Python Version" /></a>
</p>

<hr />
Example Latitude 40 Longitude 70, geo coordinates https://www.gps-coordinates.net/
<h2>English</h2>

<h3>Description</h3>

<p><strong>Brightness Auto</strong> is a Windows application that automatically adjusts your screen brightness based on the time of day and battery status. It calculates sunrise and sunset times using your geographic coordinates, smoothly transitions brightness between minimum and maximum values during daylight, and applies additional corrections when running on battery (reduces brightness to save power). The program runs in the system tray and provides a simple GUI for configuration.</p>

<p>It is designed for users who want to reduce eye strain and save battery life without manual adjustments.</p>

<h3>Features</h3>

<ul>
  <li>Automatic brightness adjustment based on time of day (sunrise/sunset).</li>
  <li>Smooth transition between configurable minimum and maximum brightness.</li>
  <li>Battery‑aware correction: reduces brightness by 10% if charge &gt;51%, by 20% if charge &lt;50% (when discharging).</li>
  <li>Configurable geographic latitude/longitude for accurate sunrise/sunset calculations.</li>
  <li>Adjustable overall brightness coefficient (multiplier).</li>
  <li>Debug mode to monitor calculations and system state.</li>
  <li>System tray icon with <strong>Show</strong> and <strong>Exit</strong> commands.</li>
  <li>Multilingual interface: English and Russian included; easily add your own language.</li>
  <li>Start minimized to tray option.</li>
  <li>Single instance enforcement (prevents multiple copies).</li>
</ul>

<h3>Requirements</h3>

<ul>
  <li><strong>Windows</strong> 7 or later (uses PowerShell and WMI).</li>
  <li><strong>Python 3.6+</strong> (if running from source) with packages: <code>tkinter</code>, <code>pystray</code>, <code>Pillow</code>, <code>configparser</code>.</li>
  <li>Alternatively, download the compiled <code>.exe</code> file (no Python installation required).</li>
</ul>

<h3>Installation</h3>

<h4>Option 1: Using the executable (recommended for end users)</h4>
<ol>
  <li>Download <code>brightness_auto_gui.exe</code> directly from: <br />
    <a href="https://github.com/dima333750/brightness_auto_gui/blob/main/brightness_auto_gui.exe">https://github.com/dima333750/brightness_auto_gui/blob/main/brightness_auto_gui.exe</a> <br />
    (Click the "Download" button or use the raw link.)</li>
  <li>Run the downloaded file – no installation needed.</li>
  <li>(Optional) Create a shortcut in your Startup folder to launch automatically with Windows.</li>
</ol>

<h4>Option 2: Running from source</h4>
<ol>
  <li>Clone the repository or download the source code.</li>
  <li>Install required packages:
    <pre><code>pip install pystray pillow</code></pre>
    (tkinter and configparser are included with Python.)</li>
  <li>Run the script:
    <pre><code>python brightness_auto_gui.py</code></pre>
  </li>
</ol>

<h3>Building Executable</h3>

<p>If you want to compile the script into a standalone <code>.exe</code> file (no Python required to run), use <strong>PyInstaller</strong>.</p>

<ol>
  <li>Install PyInstaller:
    <pre><code>pip install pyinstaller</code></pre>
  </li>
  <li>Navigate to the folder containing <code>brightness_auto_gui.py</code>.</li>
  <li>Run:
    <pre><code>pyinstaller --onefile --noconsole brightness_auto_gui.py</code></pre>
  </li>
  <li>The executable will be created in the <code>dist</code> folder.</li>
</ol>

<p>Make sure all required packages (<code>pystray</code>, <code>Pillow</code>) are installed before building – they will be bundled automatically.</p>

<h3>Configuration Settings</h3>

<p>All settings are stored in <code>config.ini</code> (auto‑created on first launch). You can change them via the GUI:</p>

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Latitude</strong></td>
      <td>Geographic latitude in degrees (e.g., 56 for Moscow).</td>
    </tr>
    <tr>
      <td><strong>Longitude</strong></td>
      <td>Geographic longitude in degrees (e.g., 44 for Moscow).</td>
    </tr>
    <tr>
      <td><strong>Min brightness</strong></td>
      <td>Minimum brightness at night (0–100, recommended 1–5).</td>
    </tr>
    <tr>
      <td><strong>Max brightness</strong></td>
      <td>Maximum brightness during daytime (up to 100).</td>
    </tr>
    <tr>
      <td><strong>Coefficient</strong></td>
      <td>Overall multiplier (e.g., 0.9 dims all values, 1.1 brightens).</td>
    </tr>
    <tr>
      <td><strong>Debug mode</strong></td>
      <td>When enabled, detailed logs are shown in the GUI.</td>
    </tr>
    <tr>
      <td><strong>Update interval (sec)</strong></td>
      <td>How often the program checks time and adjusts brightness.</td>
    </tr>
    <tr>
      <td><strong>Language</strong></td>
      <td>Interface language (restarts the GUI when changed).</td>
    </tr>
    <tr>
      <td><strong>Start in tray</strong></td>
      <td>If checked, the main window is hidden at launch (only tray icon visible).</td>
    </tr>
  </tbody>
</table>

<p><strong>Tooltips:</strong> Click the <strong>?</strong> button next to any setting for a brief explanation.</p>

<h3>How the Language System Works</h3>

<p>The program looks for translation files named <code>ab_XX.txt</code>, where <code>XX</code> is a language code (e.g., <code>en</code>, <code>ru</code>, <code>es</code>).</p>
<ul>
  <li>The default file <code>ab_en.txt</code> is included with all keys.</li>
  <li>On startup, it scans the current directory for files matching <code>ab_*.txt</code> and populates the language dropdown menu.</li>
  <li>When you select a language, the program reads the corresponding file and replaces the interface strings.</li>
</ul>

<h4>How to Add Your Own Language</h4>
<ol>
  <li>Create a copy of <code>ab_en.txt</code> and rename it to <code>ab_XX.txt</code> (replace <code>XX</code> with your language code, e.g., <code>fr</code> for French).</li>
  <li>Translate the values (after the <code>=</code> sign) into your language. Do <strong>not</strong> change the keys.</li>
  <li>Place the file in the same folder as the program (or the <code>.exe</code>).</li>
  <li>Restart the program – your language will appear in the dropdown menu.</li>
</ol>

<p>If a translation file is missing, the program falls back to English.</p>

<h3>License</h3>

<p>This project is licensed under the MIT License</p>

<hr />

<h2>Русский</h2>

<h3>Описание</h3>

<p><strong>Brightness Auto</strong> — это приложение для Windows, которое автоматически регулирует яркость экрана в зависимости от времени суток и заряда аккумулятора. Оно рассчитывает время восхода и заката по вашим географическим координатам, плавно изменяет яркость от минимальной до максимальной в течение дня и дополнительно снижает яркость при работе от батареи для экономии энергии. Программа работает в системном трее и имеет простой графический интерфейс для настройки.</p>

<p>Приложение предназначено для тех, кто хочет снизить нагрузку на глаза и продлить время работы от батареи без ручной регулировки.</p>

<h3>Возможности</h3>

<ul>
  <li>Автоматическая регулировка яркости в зависимости от времени суток (восход/закат).</li>
  <li>Плавный переход между настраиваемыми минимальной и максимальной яркостью.</li>
  <li>Коррекция по заряду батареи: уменьшение яркости на 10% при заряде &gt;51%, на 20% при заряде &lt;50% (в режиме разряда).</li>
  <li>Настраиваемые географическая широта и долгота для точного расчёта восхода/заката.</li>
  <li>Общий коэффициент яркости (множитель).</li>
  <li>Режим отладки для просмотра расчётов и состояния системы.</li>
  <li>Иконка в системном трее с командами <strong>Показать</strong> и <strong>Выход</strong>.</li>
  <li>Многоязычный интерфейс: английский и русский в комплекте; легко добавить свой язык.</li>
  <li>Опция запуска свёрнутым в трей.</li>
  <li>Блокировка повторного запуска (предотвращает запуск нескольких копий).</li>
</ul>

<h3>Требования</h3>

<ul>
  <li><strong>Windows</strong> 7 или новее (используется PowerShell и WMI).</li>
  <li><strong>Python 3.6+</strong> (если запуск из исходников) с библиотеками: <code>tkinter</code>, <code>pystray</code>, <code>Pillow</code>, <code>configparser</code>.</li>
  <li>Или готовый <code>.exe</code> файл (не требует установки Python).</li>
</ul>

<h3>Установка</h3>

<h4>Вариант 1: Использование исполняемого файла (рекомендуется для конечных пользователей)</h4>
<ol>
  <li>Скачайте <code>brightness_auto_gui.exe</code> напрямую по ссылке: <br />
    <a href="https://github.com/dima333750/brightness_auto_gui/blob/main/brightness_auto_gui.exe">https://github.com/dima333750/brightness_auto_gui/blob/main/brightness_auto_gui.exe</a> <br />
    (Нажмите «Download» или используйте прямую ссылку на файл.)</li>
  <li>Запустите скачанный файл – установка не требуется.</li>
  <li>(Опционально) Создайте ярлык в папке «Автозагрузка», чтобы программа запускалась вместе с Windows.</li>
</ol>

<h4>Вариант 2: Запуск из исходников</h4>
<ol>
  <li>Клонируйте репозиторий или скачайте исходный код.</li>
  <li>Установите необходимые пакеты:
    <pre><code>pip install pystray pillow</code></pre>
    (tkinter и configparser уже входят в состав Python.)</li>
  <li>Запустите скрипт:
    <pre><code>python brightness_auto_gui.py</code></pre>
  </li>
</ol>

<h3>Сборка исполняемого файла</h3>

<p>Если вы хотите скомпилировать скрипт в отдельный <code>.exe</code> файл (не требующий установки Python), используйте <strong>PyInstaller</strong>.</p>

<ol>
  <li>Установите PyInstaller:
    <pre><code>pip install pyinstaller</code></pre>
  </li>
  <li>Перейдите в папку, где находится <code>brightness_auto_gui.py</code>.</li>
  <li>Выполните:
    <pre><code>pyinstaller --onefile --noconsole brightness_auto_gui.py</code></pre>
  </li>
  <li>Исполняемый файл появится в папке <code>dist</code>.</li>
</ol>

<p>Убедитесь, что все необходимые пакеты (<code>pystray</code>, <code>Pillow</code>) установлены перед сборкой – они будут включены автоматически.</p>

<h3>Настройки</h3>

<p>Все настройки сохраняются в файле <code>config.ini</code> (создаётся при первом запуске). Их можно изменить через интерфейс:</p>

<table>
  <thead>
    <tr>
      <th>Параметр</th>
      <th>Описание</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Широта</strong></td>
      <td>Географическая широта в градусах (например, 56 для Москвы).</td>
    </tr>
    <tr>
      <td><strong>Долгота</strong></td>
      <td>Географическая долгота в градусах (например, 44 для Москвы).</td>
    </tr>
    <tr>
      <td><strong>Мин. яркость</strong></td>
      <td>Минимальная яркость ночью (0–100, рекомендуется 1–5).</td>
    </tr>
    <tr>
      <td><strong>Макс. яркость</strong></td>
      <td>Максимальная яркость днём (до 100).</td>
    </tr>
    <tr>
      <td><strong>Коэффициент</strong></td>
      <td>Общий множитель (например, 0.9 – затемнение, 1.1 – осветление).</td>
    </tr>
    <tr>
      <td><strong>Режим отладки</strong></td>
      <td>При включении в окне отображаются подробные логи.</td>
    </tr>
    <tr>
      <td><strong>Интервал обновления (сек)</strong></td>
      <td>Как часто программа проверяет время и меняет яркость.</td>
    </tr>
    <tr>
      <td><strong>Язык</strong></td>
      <td>Язык интерфейса (перезапускает окно при смене).</td>
    </tr>
    <tr>
      <td><strong>Запускать в трее</strong></td>
      <td>Если отмечено, главное окно скрыто при старте (видна только иконка в трее).</td>
    </tr>
  </tbody>
</table>

<p><strong>Подсказки:</strong> Нажмите кнопку <strong>?</strong> рядом с любым параметром для краткого пояснения.</p>

<h3>Как работает система языков</h3>

<p>Программа ищет файлы переводов с именами <code>ab_XX.txt</code>, где <code>XX</code> – код языка (например, <code>en</code>, <code>ru</code>, <code>es</code>).</p>
<ul>
  <li>Базовый файл <code>ab_en.txt</code> включён в состав и содержит все ключи.</li>
  <li>При запуске программа сканирует текущую папку на наличие файлов <code>ab_*.txt</code> и заполняет выпадающий список языков.</li>
  <li>При выборе языка программа читает соответствующий файл и заменяет строки интерфейса.</li>
</ul>

<h4>Как добавить свой язык</h4>
<ol>
  <li>Создайте копию файла <code>ab_en.txt</code> и переименуйте её в <code>ab_XX.txt</code> (замените <code>XX</code> на код вашего языка, например <code>fr</code> для французского).</li>
  <li>Переведите значения (после знака <code>=</code>) на ваш язык. Ключи (слева от <code>=</code>) менять <strong>нельзя</strong>.</li>
  <li>Поместите файл в ту же папку, где находится программа (или <code>.exe</code>).</li>
  <li>Перезапустите программу – ваш язык появится в выпадающем списке.</li>
</ol>

<p>Если файл перевода отсутствует, программа использует английский язык по умолчанию.</p>

<h3>Лицензия</h3>

<p>Этот проект распространяется под лицензией MIT.</p>

<hr />

<p><em>Happy adjusting! / Приятной настройки!</em></p>

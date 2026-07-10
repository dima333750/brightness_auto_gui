setlocal enabledelayedexpansion

:: ====== НАСТРОЙКИ (меняйте под себя) ======
set "LAT=56"            :: Широта (целые градусы)
set "LON=44"            :: Долгота (целые градусы)
set "MIN_BR=1"          :: Яркость ночью (1–5)
set "MAX_BR=70"         :: Яркость днём (до 100)
set "COEFF=1.0"         :: Общий множитель (например, 0.9 или 1.1)
:: ==========================================

:see

:: Получаем статус батареи и уровень заряда
for /F "usebackq tokens=1,2" %%a in (`powershell -Command "$b=Get-WmiObject Win32_Battery; Write-Host $b.BatteryStatus $b.EstimatedChargeRemaining"`) do (
    set status=%%a
    set charge=%%b
)

:: Проверяем условия и переходим к соответствующему блоку
:: status=2 означает что зарядка подключена
if "!status!"=="2" goto block_charger_connected
if "!status!"=="1" (
    if !charge! GTR 51 goto block_no_charger_high_battery
    if !charge! LSS 50 goto block_no_charger_low_battery
)
goto block_charger_connected

:set_brightness_by_time
:: Однострочный PowerShell-расчёт яркости (без таблицы)
for /F %%b in ('powershell -Command "$lat=%LAT%; $lon=%LON%; $now=Get-Date; $doy=$now.DayOfYear; $d2r=[Math]::PI/180; $dec=23.44*[Math]::Sin((284+$doy)*360/365*$d2r); $cos_ha=-[Math]::Tan($lat*$d2r)*[Math]::Tan($dec*$d2r); if($cos_ha -lt -1){$cos_ha=-1}; if($cos_ha -gt 1){$cos_ha=1}; $ha=[Math]::Acos($cos_ha)*180/[Math]::PI; $rise=12-$ha/15 - $lon/15; $set=12+$ha/15 - $lon/15; $tz=[System.TimeZoneInfo]::Local.GetUtcOffset($now).TotalHours; $riseLocal=$rise+$tz; $setLocal=$set+$tz; if($riseLocal -lt 0){$riseLocal+=24}; if($setLocal -gt 24){$setLocal-=24}; $nowHour=$now.Hour+$now.Minute/60; $minBr=%MIN_BR%; $maxBr=%MAX_BR%; $coeff=%COEFF%; if($nowHour -lt $riseLocal -or $nowHour -gt $setLocal){$br=$minBr} else {$dayLen=$setLocal-$riseLocal; $sinceRise=$nowHour-$riseLocal; if($sinceRise -le $dayLen/2){$frac=$sinceRise/($dayLen/2); $br=$minBr+($maxBr-$minBr)*$frac} else {$frac=($sinceRise-$dayLen/2)/($dayLen/2); $br=$maxBr-($maxBr-$minBr)*$frac}}; $br=[Math]::Round($br*$coeff); if($br -gt $maxBr){$br=$maxBr}; if($br -lt $minBr){$br=$minBr}; $br"') do set brightness=%%b

:: Если по какой-то причине яркость не получена – ставим 0
if not defined brightness set brightness=0
goto :eof

:block_charger_connected
call :set_brightness_by_time
powershell -Command "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,%brightness%)"
ping -n 30 127.0.0.1 > nul
goto see

:block_no_charger_high_battery
call :set_brightness_by_time
set /a brightness=brightness - 10
if !brightness! LSS 0 set brightness=0
powershell -Command "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,%brightness%)"
ping -n 30 127.0.0.1 > nul
goto see

:block_no_charger_low_battery
call :set_brightness_by_time
set /a brightness=brightness - 20
if !brightness! LSS 0 set brightness=0
powershell -Command "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,%brightness%)"
ping -n 30 127.0.0.1 > nul
goto see
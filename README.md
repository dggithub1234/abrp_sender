# 🚗 ABRP Sender for Home Assistant

![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)
![HACS Custom](https://img.shields.io/badge/HACS-Custom-blue.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-41BDF5?logo=home-assistant&logoColor=white)

Send live vehicle and GPS sensor data from Home Assistant to [A Better Routeplanner (ABRP)](https://abetterrouteplanner.com).

---

## 🌟 Features

- 🔑 UI-based setup — no YAML needed  
- 📡 Send SoC, range, speed, power, temp and GPS data to ABRP in real time  
- 🕒 Dynamic scan interval (10–600 s)  
- 🧭 Automatic GPS entity suggestions  

---

## 🧩 Installation via HACS

1. Go to **HACS → Integrations → Custom Repositories**  
2. Add this repository URL:

https://github.com/dggithub1234/abrp_sender

Choose type **Integration**.
3. After adding, search for **ABRP Sender** in HACS and click **Install**.  
4. **Restart Home Assistant**.  
5. Go to **Settings → Devices & Services → Add Integration → ABRP Sender**.  
6. Enter your **ABRP API key** and select your sensors.

---

## ⚙️ Configuration Options

All configuration is handled through the Home Assistant UI — no YAML required.

| Option | Description | Default |
|--------|--------------|----------|
| **ABRP API Key** | Your personal key from [ABRP API Keys](https://abetterrouteplanner.com/user/api/) | *(required)* |
| **Enable data sending** | Toggle data uploads ON/OFF | ✅ Enabled |
| **State of Charge (SoC) Sensor** | Battery % sensor | *(optional)* |
| **Estimated Range Sensor** | Battery estimated range sensor | *(optional)* |
| **Speed Sensor** | Vehicle speed sensor | *(optional)* |
| **Power Sensor** | Positive/negative power flow | *(optional)* |
| **Latitude / Longitude Sensor** | Device tracker sensor or GPS Lat and Long individual sensores | *(optional)* |
| **External Temperature** | Vehicle temperature sensor | *(optional)* |
| **Scan Interval (seconds)** | How often data is sent (10–600 s) | 60 s |

---

## 🧭 Example Use Cases

- 🚘 Send real-time car telemetry from OBD2 or EV sensors to ABRP while driving  
- 🏠 Pause data sending when the vehicle is parked (using the enable toggle)  
- 🛰️ Combine with `device_tracker` entities for live route visualization

---

## 💡 Tips

- Minimum interval: **10 seconds**  
- GPS sensors or device trackers are auto-suggested in the setup UI  
- Logs are available under `custom_components.abrp_sender`

---

## 🧑‍💻 Credits

Developed by **[Daniel G](https://github.com/yourname)**  
Licensed under the [MIT License](LICENSE)

---

## 🧭 Links

- 🧩 [A Better Routeplanner (ABRP)](https://abetterrouteplanner.com)  
- 💬 [Home Assistant Community](https://community.home-assistant.io)  
- 🧰 [HACS Documentation](https://hacs.xyz)

---

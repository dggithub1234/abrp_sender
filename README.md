# 🚗 ABRP Sender for Home Assistant

![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)
![HACS Custom](https://img.shields.io/badge/HACS-Custom-blue.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-41BDF5?logo=home-assistant&logoColor=white)

Send live vehicle and GPS sensor data from Home Assistant to [A Better Routeplanner (ABRP)](https://abetterrouteplanner.com).

---

## 🌟 Features

- 🔑 UI-based setup — no YAML needed  
- 📡 Send SoC, speed, power, and GPS data to ABRP in real time  
- 🕒 Dynamic scan interval (10–600 s)  
- 🧭 Automatic GPS entity suggestions  
- ✅ ABRP API key validation  
- 📴 **Enable/Disable data sending** toggle — pause uploads anytime  
- ⚙️ Configurable via the Home Assistant UI (Options menu)

---

## 🧩 Installation via HACS

1. Go to **HACS → Integrations → Custom Repositories**  
2. Add this repository URL:

https://github.com/yourname/ha-abrp-sender

yaml
Copy code

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
| **Speed Sensor** | Vehicle speed sensor | *(optional)* |
| **Power Sensor** | Positive/negative power flow | *(optional)* |
| **Latitude / Longitude Sensor** | Device tracker or GPS sensor | *(optional)* |
| **Scan Interval (seconds)** | How often data is sent (10–600 s) | 60 s |

> When **Enable data sending** is turned OFF, the integration pauses all ABRP uploads but continues to run.  
> You can toggle it anytime in the **Options** menu.

---

## 🧭 Example Use Cases

- 🚘 Send real-time car telemetry from OBD2 or EV sensors to ABRP while driving  
- 🏠 Pause data sending when the vehicle is parked (using the enable toggle)  
- 🛰️ Combine with `device_tracker` entities for live route visualization

---

## 🛠️ Advanced Usage

The integration uses Home Assistant’s **DataUpdateCoordinator** for scheduling updates.  
You can safely change the scan interval at runtime via **Options**, and it will dynamically adjust without needing a restart.

Future versions will also include:
- Services: `abrp_sender.enable` / `abrp_sender.disable` for automation control  
- Debug switch entity (optional)

---

## 📦 Repository Structure

custom_components/abrp_sender/
│
├── init.py
├── config_flow.py
├── coordinator.py
├── const.py
├── util.py
└── manifest.json

hacs.json
README.md
LICENSE
.gitignore

yaml
Copy code

---

## 💡 Tips

- Minimum interval: **10 seconds**  
- GPS sensors or device trackers are auto-suggested in the setup UI  
- API key is validated automatically before setup completes  
- Logs are available under `custom_components.abrp_sender`

---

## 🧪 Local Testing

1. Copy the integration folder to:
/config/custom_components/abrp_sender/

markdown
Copy code
2. Restart Home Assistant.  
3. Add the integration via **Settings → Devices & Services → Add Integration → ABRP Sender**.  
4. Check the logs for:
ABRP data sent successfully

nginx
Copy code
or  
ABRP Sender disabled — skipping data upload.

yaml
Copy code

---

## 🧑‍💻 Credits

Developed by **[Your Name](https://github.com/yourname)**  
Licensed under the [MIT License](LICENSE)

---

## 🧭 Links

- 🧩 [A Better Routeplanner (ABRP)](https://abetterrouteplanner.com)  
- 💬 [Home Assistant Community](https://community.home-assistant.io)  
- 🧰 [HACS Documentation](https://hacs.xyz)

---

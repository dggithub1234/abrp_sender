# ABRP Sender for Home Assistant

![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)
![HACS Custom](https://img.shields.io/badge/HACS-Custom-blue.svg)

Send real-time car and GPS data from Home Assistant sensors to [A Better Routeplanner (ABRP)](https://abetterrouteplanner.com).

---

## 🚀 Features

- Send live **SoC, speed, GPS, power** to ABRP API  
- **UI configuration** (no YAML required)  
- **Automatic GPS entity detection**  
- **API key validation**  
- **Configurable update interval**

---

## 🧩 Installation via HACS

1. Go to **HACS → Integrations → Custom Repositories**  
2. Add this repo URL:  
https://github.com/yourname/ha-abrp-sender

markdown
Copy code
and choose type **Integration**.  
3. After adding, search for **ABRP Sender** in HACS and click **Install**.  
4. Restart Home Assistant.  
5. Go to **Settings → Devices & Services → Add Integration → ABRP Sender**.  
6. Enter your **ABRP API key** and select your sensors.

---

## ⚙️ Configuration Options

- **ABRP API Key** – from your ABRP account: [ABRP API Keys](https://abetterrouteplanner.com/user/api/)
- **SoC Sensor**
- **Speed Sensor**
- **Latitude / Longitude Sensor**
- **Power Sensor**
- **Update Interval (seconds)**

You can edit these anytime using the **Options** menu in the integration settings.

---

## 🧠 Notes

- Minimum interval: 10s  
- GPS entities are auto-suggested from known device trackers or sensors containing `lat` / `lon`  
- API key is verified before saving  

---

## 🧑‍💻 Credits

Created by [Your Name](https://github.com/yourname)

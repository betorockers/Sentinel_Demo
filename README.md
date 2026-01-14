# 🛡️ Anvic Network Sentinel v2.0 - Demo Version

**Anvic Network Sentinel** is a professional network monitoring solution designed for high-visibility environments. This version is a **Demo Edition** optimized for portfolios, featuring real-time simulation of network states and advanced data visualization.

![Sentinel Preview](https://via.placeholder.com/800x450.png?text=Sentinel+v2.0+Interface+Preview) <!-- Reemplazar con captura real después -->

## 🚀 Key Features

- **Real-Time Monitoring**: Dynamic tracking of multiple IP addresses with instant status updates.
- **Advanced Visualizations**:
  - **Uptime Gauges**: Semicircular indicators showing availability percentage.
  - **Availability Heatmap**: 24-hour grid visualizing network stability at a glance.
  - **Latency Graphs**: Real-time plotting of response times.
- **Smart Notifications**: Custom "Toast" notifications with sound alerts for connection changes.
- **Compact Sidebar**: Optimized control panel for managing equipment, intervals, and reports.
- **Data Persistence**: Automatic saving of configurations and historical metrics.
- **Simulation Mode**: Built-in logic to simulate network fluctuations (90% online / 10% offline) for demonstration purposes.

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **UI Framework**: `customtkinter` (Modern & Professional look)
- **Data Visualization**: `matplotlib`, `numpy`
- **Multimedia**: `pygame` (Sound alerts)
- **Notifications**: `plyer`
- **Image Processing**: `Pillow`

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/sentinel-demo.git
   cd sentinel-demo
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 📂 Project Structure

- `main.py`: Entry point with pre-configured demo equipment.
- `monitor.py`: Core UI logic and visualization engine.
- `ping_logic.py`: Simulation engine for network states.
- `metrics_manager.py`: Data handling and historical analysis.
- `assets/`: 
  - `img/`: Branding and icons.
  - `sounds/`: Alert and recovery audio files.

## 👤 Author

**Omar Toledo**  
*Network Security & Software Developer*  
Powered by **@Betograf_inc**

---
*© 2026 Anvic Network Sentinel. All rights reserved.*

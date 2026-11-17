# Kochi Metro & Transit Route Navigator (Modern GUI & CLI)

A clean, modern, and user-friendly multi-modal transit route optimizer inspired by the **Kochi Metro (Blue Line)**, **Kochi Water Metro**, and the proposed **Phase 2 (Pink Line)** with transfer walkways.

Built with **CustomTkinter** for modern rounded cards, sleek typography, and a crisp **White + Blue** theme.
<img width="947" height="543" alt="image" src="https://github.com/user-attachments/assets/bc113a1f-fdbd-4ff1-af86-467ac3a8d263" />


---

## Key Features

### 1. Modern Desktop Application (`app.py`)
- **Novel Features Beyond Official Site**:
  - **Landmark & Tourist Destination Search**: Search directly by famous Kochi destinations (*Lulu Mall*, *Fort Kochi Beach*, *Infopark*, *Marine Drive*, *CUSAT*, *Ernakulam Railway Station*), automatically routing you to the closest station.
  - **Cab/Auto vs Metro Savings Meter**: Real-time calculation comparing transit fare against typical Kochi taxi/auto fares (saves ~₹350 per trip).
  - **Carbon Footprint & Traffic Saved**: Quantifies CO2 emissions prevented (~2.4 kg) and road traffic avoided at congested junctions (Edappally, Vyttila, MG Road).
  - **Live Service Countdown & Real ETA**: Live headway indicator (*Next Metro in 4m, Next Ferry in 11m*) with accurate departure & arrival timestamps.
  - **Traveler Persona Modes**: Switch between `Fast Commuter`, `Scenic Backwaters Ferry`, and `Senior / Easy Transfer`.
  - **1-Click WhatsApp Share**: Formats your complete itinerary and copies it to the clipboard, ready to send to friends or family.
- **User-Choice Map Views**:
  - **Standard View**: Clean Google Street road map.
  - **Satellite View**: High-resolution photorealistic satellite imagery across Kochi and coastal backwaters.
  - **Hybrid View**: Satellite imagery combined with street names, towns, and landmark labels.
- **Crisp White + Blue Aesthetic**:
  - Bright, clean white cards with vibrant Kochi Metro Royal Blue accents (`#0284c7`).
  - Step-by-step visual cards displaying departures, interchanges, boardings, and arrivals.

### 2. Terminal CLI Interface (`main.py --cli`)
- Interactive command-line route planner with station catalogs, station lookup by number (`1-36`), station code (`M1`, `W7`), or name (`Aluva`, `Fort Kochi`).

---

## Project Structure

```
kochi_metro_optimizer/
│
├── app.py              # Tkinter GUI Desktop Application (interactive canvas, tabs, fares)
├── main.py             # Entry point (launches GUI by default or CLI with --cli)
├── graph.py            # Core TransitGraph class, Dijkstra & A* algorithms, transfer logic
├── data.py             # 36-station transit dataset (Metro Blue Line, Water Metro, Pink Line)
├── requirements.txt    # Project dependencies (customtkinter, tkintermapview)
└── README.md           # Documentation & usage instructions
```

---

## How to Run

### 1. Install Dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the Tkinter GUI Application:
```bash
python app.py
```
*Or simply:*
```bash
python main.py
```

### Run in Terminal / CLI Mode:
```bash
python main.py --cli
```

---

## Network Overview (36 Stations)
- **Kochi Metro (Blue Line)**: 25 Stations from *Aluva* (M1) to *Tripunithura Terminal* (M25) via Kalamassery, Edappally, JLN Stadium, MG Road, and Vyttila.
- **Kochi Water Metro**: 8 Stations including *High Court*, *Vypin*, *Vyttila*, *Kakkanad*, *Fort Kochi*, *Cheranelloor*, *South Chittoor*, and *Willingdon Island*.
- **Proposed Pink Line (Phase 2)**: 3 Stations connecting *Info Park* to *JLN Stadium* via Kakkanad Junction and Palarivattom Bypass.
- **Intermodal Walkways**: Fast transfers connecting Vyttila Metro to Vyttila Water Metro, Kakkanad Pink Line to Kakkanad Jetty, and MG Road to High Court.

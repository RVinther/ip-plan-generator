# IP Plan Generator

Et Python-værktøj, der automatisk genererer IP- og subnetplaner til brug i netværksdesign og dokumentation.

## Funktioner

- Input: CIDR og ønsket subnetstørrelse
- Output: CSV og Markdown IP-plan
- Viser network, gateway, usable hosts og broadcast

---

## Installation

1. Klon projektet:
   ```bash
   git clone https://github.com/RVinther/ip-plan-generator.git
   cd ip-plan-generator
   ```

2. Opret miljø og installer krav:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Kør programmet: 
   ```bash
   python src/ip_plan.py
   ```

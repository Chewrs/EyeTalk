# stt with ai Project Setup

## 🛠️ Setup Instructions

1. **Create a virtual environment with system packages**:
   ```bash
   python3 -m venv env --system-site-packages
   source env/bin/activate
   ```

2. **Export your Google API Key**:
   - Get your key from: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
   - Add this line to `env/bin/activate` (at the bottom):
     ```bash
     export GOOGLE_API_KEY="your_api_key_here"
     ```
   - Then activate again:
     ```bash
     source env/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the main program**:
   ```bash
   python3 main.py
   ```
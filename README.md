
# Volatility Dump Analysis Interface

This project provides a web-based interface to analyze memory dump files using the Volatility Framework. The interface allows users to select memory dumps, run various Volatility plugins in parallel, and view the results in a user-friendly way with progress tracking.

## Features
- **Memory dump selection** via a file picker.
- **Parallel analysis** using multiple Volatility plugins.
- **Progress tracking** with a real-time progress bar that updates as plugins complete.
- **Results viewing**: Once analysis is complete, the results for each plugin are displayed in separate tabs.
- **Plugin result caching**: Once a dump is analyzed, results are stored in a SQLite database to avoid re-running the analysis.

## Prerequisites
1. **Python 3.x**
   Ensure you have Python installed. You can download it [here](https://www.python.org/downloads/).
2. **Volatility Framework** (Executable)
   - Download **Volatility3** from [here](https://github.com/volatilityfoundation/volatility3).
   - Make sure the `volatility.exe` executable is accessible in your environment's `PATH`. You can verify this by running:
     ```bash
     volatility.exe -h
     ```
     This should display the help menu of Volatility3.

3. **Dependencies**
   Install the required Python dependencies using:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
volatility_interface/
│
├── app.py                     # Main Flask app
├── dumps.db                    # SQLite database to store dump analysis results
├── uploads/                    # Directory where dumps are stored after selection
├── volatility_logs/            # Directory where logs of Volatility analysis are saved
├── templates/                  # HTML templates for the web interface
│   ├── index.html              # Main page to list dumps and select new ones
│   ├── progress.html           # Progress page showing the analysis progress
│   └── analyze.html            # Page to display plugin results after analysis
└── static/
    └── style.css               # Optional custom CSS
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/volatility_interface.git
   cd volatility_interface
   ```

2. **Install Python dependencies**:
   ```bash
   pip install flask
   pip install sqlite3
   ```

3. **Configure Volatility3**:
   Ensure that `volatility.exe` is accessible globally by adding it to your system's `PATH`. On Linux or macOS, you can add it to your `.bashrc` or `.zshrc`:
   ```bash
   export PATH=$PATH:/path/to/volatility3/
   ```
   On Windows, add the folder containing `volatility.exe` to your system's environment variables.

4. **Run the application**:
   Start the Flask app by running the following command:
   ```bash
   python app.py
   ```
   This will start the web interface, which can be accessed in a browser at `http://127.0.0.1:5000/`.

## How to Use

### 1. Select a Memory Dump
On the main page, click on the **Select Dump** button to open a popup. Choose the memory dump file (`.dmp`, `.bin`, `.raw`, `.mem`) you want to analyze.

![Select Dump Screenshot](screenshots/select_dump.png)

### 2. Start the Analysis
Once a dump is selected, you will see it listed on the main page. Click **Analyze** to start the analysis. A progress page will open to show the status of the analysis.

![Progress Screenshot](screenshots/progress_bar.png)

### 3. View Results
When the analysis completes, you will be redirected to the results page where each Volatility plugin result is displayed in its own tab.

![Analysis Results Screenshot](screenshots/analysis_results.png)

## Plugins
The following Volatility plugins are executed in parallel:
- **Processes and Threads**: `windows.pslist.PsList`, `windows.threads.Threads`
- **Modules and DLLs**: `windows.modules.Modules`, `windows.dlllist.DllList`
- **Files and Handles**: `windows.filescan.FileScan`, `windows.handles.Handles`
- **Memory and System Structures**: `windows.memmap.Memmap`, `windows.ssdt.SSDT`
- **And many more...**

Results for each plugin are stored in the SQLite database, and previously analyzed dumps are cached so the results can be viewed instantly without re-running the analysis.

## Troubleshooting

### Volatility executable not found
Make sure `volatility.exe` is in your system's `PATH`. You can test this by running:
```bash
volatility.exe -h
```

### Error during plugin execution
If a plugin fails, the error is logged in the corresponding log file under `volatility_logs/`.

## License
This project is licensed under the MIT License.

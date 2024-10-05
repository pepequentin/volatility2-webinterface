
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
   - Download **Volatility2** from [here](https://github.com/volatilityfoundation/volatility2).
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

3. **Configure Volatility2**:
   Ensure that `volatility.exe` is accessible globally by adding it to your system's `PATH`. On Linux or macOS, you can add it to your `.bashrc` or `.zshrc`:
   ```bash
   export PATH=$PATH:/path/to/volatility2/
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

![select_dump](https://github.com/user-attachments/assets/856af797-8868-4f93-8ea2-9d721bc1d781)


### 2. Start the Analysis
Once a dump is selected, you will see it listed on the main page. Click **Analyze** to start the analysis. A progress page will open to show the status of the analysis.

![Progress Screenshot](https://github.com/user-attachments/assets/0527944f-d99c-4217-8f9b-cf4ef5b1b181)
![Uploading image](https://github.com/user-attachments/assets/506781b7-72b9-4e2b-9744-525307fd96cf)

### 3. View Results
When the analysis completes, you will be redirected to the results page where each Volatility plugin result is displayed in its own tab.

![Analysis Results](https://github.com/user-attachments/assets/b3883d3c-60ee-4f34-90e8-df069dd93df4)

## Plugins
The following Volatility plugins are executed in parallel:

- **amcache**: Analyzes the Amcache database, which contains details of files executed on the system.
- **apihooks**: Detects API hooks injected into processes to manipulate or intercept system calls.
- **atoms/atomscan**: Lists and scans Atom tables used by applications to share global data between processes.
- **auditpol**: Extracts audit policy settings from the system.
- **bigpools**: Lists memory allocations in kernel non-paged pools.
- **bioskbd**: Analyzes BIOS keyboard state, useful for retrieving information like lock keys.
- **cachedump**: Extracts cached password hashes from a Windows memory image.
- **callbacks**: Displays kernel callbacks registered for different system events.
- **clipboard**: Extracts clipboard data from memory.
- **cmdline**: Displays the command line used to start each process.
- **cmdscan**: Scans console command buffers in memory.
- **connections/connscan**: Lists active network connections and scans memory for hidden connection structures.
- **consoles**: Displays interactive console windows and their contents.
- **crashinfo**: Extracts information about crashes or memory dumps.
- **deskscan**: Scans memory for open windows (desktops) information.
- **devicetree**: Lists connected devices on the system.
- **dlldump**: Dumps specific DLLs from memory to disk.
- **dlllist**: Displays the list of DLLs loaded by each process.
- **driverirp**: Displays I/O Request Packet (IRP) routines for drivers.
- **drivermodule**: Lists driver modules loaded in kernel memory.
- **driverscan**: Scans memory for drivers.
- **dumpcerts**: Extracts digital certificates from memory.
- **dumpfiles**: Dumps specific files from memory.
- **dumpregistry**: Extracts information from loaded registry hives in memory.
- **editbox**: Recovers the contents of dialog boxes and text fields in memory.
- **envars**: Displays environment variables for each process.
- **eventhooks**: Lists event hooks in kernel memory.
- **evtlogs**: Analyzes Windows event logs.
- **filescan**: Scans memory for open file structures.
- **gahti**: Extracts information about graphics timers.
- **gditimers**: Lists GDI timers in use by the system.
- **gdt**: Displays the Global Descriptor Table (GDT).
- **getservicesids/getsids**: Retrieves Security Identifiers (SIDs) for services and processes.
- **handles**: Displays open handles for each process.
- **hashdump**: Extracts password hashes from the SAM file.
- **hibinfo**: Displays information about hibernation files.
- **hivedump/hivelist/hivescan**: Lists, scans, and extracts registry hives loaded in memory.
- **hpakextract**: Extracts information from HPAK (Hypervisor Snapshot) files.
- **idt**: Displays the Interrupt Descriptor Table (IDT).
- **iehistory**: Recovers Internet Explorer browsing history.
- **imagecopy**: Copies a memory image to a new file.
- **imageinfo**: Provides information about the dump file type, operating systems, and potential profiles.
- **impscan**: Scans processes for import tables.
- **joblinks**: Displays tasks assigned to processes.
- **kdbgscan**: Scans memory for the Kernel Debugger Block (KDBG).
- **kpcrscan**: Scans and lists processor structures in kernel memory.
- **ldrmodules**: Analyzes process loader modules.
- **lsadump**: Extracts LSA secrets, such as authentication information (Windows).
- **machoinfo**: Provides information about Mach-O executable files (used by macOS).
- **malfind**: Detects malware artifacts in memory.
- **mbrparser**: Analyzes the Master Boot Record (MBR).
- **memdump**: Dumps a selected memory region to a file.
- **memmap**: Displays the memory map of processes.
- **messagehooks**: Lists message hooks in memory.
- **moddump**: Dumps specific kernel modules from memory to disk.
- **modscan**: Scans memory for kernel modules.
- **modules**: Lists loaded kernel modules.
- **multiscan**: Scans memory for multiple types of artifacts in parallel.
- **mutantscan**: Scans memory for synchronization objects (mutex).
- **notepad**: Recovers text from Notepad instances in memory.
- **objtypescan**: Scans kernel memory for object types.
- **patcher**: Detects kernel patch modifications.
- **poolpeek**: Displays information about memory pool allocations.
- **printkey**: Displays specific Windows registry keys.
- **privs**: Displays process privileges.
- **procdump**: Dumps the memory of a specific process to a file.
- **pslist**: Lists active processes.
- **psscan**: Scans memory for hidden process structures.
- **pstree**: Displays the process hierarchy as a tree.
- **psxview**: Verifies if processes are hidden by rootkits.
- **qemuinfo**: Provides information about virtualized systems using QEMU.
- **raw2dmp**: Converts a raw memory file to a dump file.
- **screenshot**: Captures screenshots from user sessions in memory.
- **servicediff**: Compares and displays service differences between two points in time.
- **sessions**: Displays active user sessions.
- **shellbags**: Extracts Shellbag information (historical folder access).
- **shimcache**: Displays application compatibility data (ShimCache) in memory.
- **shutdowntime**: Displays the last system shutdown time.
- **sockets**: Lists active network sockets.
- **sockscan**: Scans memory for hidden network socket structures.
- **ssdt**: Displays the System Service Descriptor Table (SSDT).
- **strings**: Searches for strings in memory.
- **svcscan**: Scans memory for services.
- **symlinkscan**: Scans memory for symbolic links.
- **thrdscan/threads**: Scans memory for threads and displays active threads.
- **timeliner**: Creates a timeline of events in memory.
- **timers**: Displays active timers in kernel memory.
- **truecryptmaster/truecryptpassphrase/truecryptsummary**: Extracts TrueCrypt-related information (encrypted volumes).
- **unloadedmodules**: Lists kernel modules that have been unloaded.
- **userassist**: Lists UserAssist registry keys.
- **userhandles**: Displays user-opened handles.
- **vaddump/vadinfo/vadtree/vadwalk**: Analyzes allocated memory regions (VAD - Virtual Address Descriptors).
- **verinfo**: Displays version information for binaries.
- **vmwareinfo**: Provides information about VMware virtualized systems.
- **volshell**: An interactive shell for memory analysis.
- **windows**: Executes Windows-specific commands.
- **wintree**: Displays a tree of windows and graphical objects.
- **wndscan**: Scans memory for GUI window objects.
- **yarascan**: Uses Yara rules to search for specific strings or patterns in memory.
  
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

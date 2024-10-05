
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

- **amcache** : Analyse les informations de la base de données Amcache, qui contient des détails sur les fichiers exécutés sur le système.
- **apihooks** : Détecte les hooks d'API injectés dans des processus pour manipuler ou intercepter des appels système.
- **atoms/atomscan** : Liste et scanne les tables Atom utilisées par les applications pour partager des données globales entre processus.
- **auditpol** : Extrait les paramètres de la politique d'audit du système (Audit Policy).
- **bigpools** : Liste les allocations de mémoire dans les pools non paginés du noyau.
- **bioskbd** : Analyse l'état du clavier BIOS, utile pour récupérer des informations comme les touches de déverrouillage.
- **cachedump** : Extrait les hachages des mots de passe en cache à partir d'une image mémoire Windows.
- **callbacks** : Affiche les callbacks du noyau enregistrées pour différents événements système.
- **clipboard** : Extrait les informations du presse-papier en mémoire.
- **cmdline** : Affiche la ligne de commande utilisée pour démarrer chaque processus.
- **cmdscan** : Scanne les tampons de commandes saisis dans la console.
- **connections/connscan** : Liste les connexions réseau actives et scanne la mémoire pour les structures de connexion réseau cachées.
- **consoles** : Affiche les consoles interactives et leurs contenus.
- **crashinfo** : Extrait des informations sur un crash ou un vidage mémoire.
- **deskscan** : Scanne la mémoire pour des informations sur les fenêtres ouvertes (desktops).
- **devicetree** : Liste les périphériques connectés au système.
- **dlldump** : Permet de dumper des DLL spécifiques de la mémoire vers le disque.
- **dlllist** : Affiche la liste des DLL chargées par chaque processus.
- **driverirp** : Affiche les routines IRP (I/O Request Packet) des drivers.
- **drivermodule** : Liste les modules de drivers chargés dans la mémoire du noyau.
- **driverscan** : Scanne la mémoire pour trouver des drivers.
- **dumpcerts** : Extrait les certificats numériques présents en mémoire.
- **dumpfiles** : Dumpe les fichiers spécifiques à partir de la mémoire.
- **dumpregistry** : Permet d'extraire des informations des hives de registre chargés en mémoire.
- **editbox** : Récupère les contenus des boîtes de dialogue et zones de texte en mémoire.
- **envars** : Affiche les variables d'environnement pour chaque processus.
- **eventhooks** : Liste les hooks d'événements dans la mémoire du noyau.
- **evtlogs** : Analyse les logs d'événements Windows.
- **filescan** : Scanne la mémoire pour détecter les structures de fichiers ouverts.
- **gahti** : Extrait des informations sur les timers graphiques.
- **gditimers** : Liste les timers GDI en cours d'utilisation dans le système.
- **gdt** : Affiche la table des descripteurs globaux (GDT).
- **getservicesids/getsids** : Récupère les Security Identifiers (SIDs) des services et processus.
- **handles** : Affiche les handles ouverts pour chaque processus.
- **hashdump** : Extrait les hachages des mots de passe à partir du fichier SAM.
- **hibinfo** : Affiche des informations sur les fichiers d'hibernation.
- **hivedump/hivelist/hivescan** : Liste, scanne et extrait les hives de registre chargés en mémoire.
- **hpakextract** : Extrait des informations à partir des fichiers HPAK (Hypervisor Snapshot).
- **idt** : Affiche la table des descripteurs d'interruption (IDT).
- **iehistory** : Récupère l'historique de navigation d'Internet Explorer.
- **imagecopy** : Copie une image mémoire dans un nouveau fichier.
- **imageinfo** : Fournit des informations sur le type de fichier dump, les systèmes d'exploitation et profils possibles.
- **impscan** : Scanne les processus à la recherche d'importations (import tables).
- **joblinks** : Affiche les tâches assignées aux processus.
- **kdbgscan** : Scanne la mémoire pour trouver le bloc de débogage du noyau (KDBG).
- **kpcrscan** : Scanne et liste les structures du processeur dans le noyau.
- **ldrmodules** : Analyse les modules de chargement des processus (modules loader).
- **lsadump** : Extrait les secrets LSA, tels que les informations d'authentification (Windows).
- **machoinfo** : Fournit des informations sur les fichiers exécutables Mach-O (utilisé par macOS).
- **malfind** : Détecte des artefacts de malwares en mémoire.
- **mbrparser** : Analyse le secteur de démarrage principal (MBR).
- **memdump** : Dumpe une région de mémoire sélectionnée vers un fichier.
- **memmap** : Affiche la carte mémoire des processus.
- **messagehooks** : Liste les hooks de messages en mémoire.
- **moddump** : Dumpe des modules spécifiques de la mémoire vers le disque.
- **modscan** : Scanne la mémoire pour trouver des modules de noyau.
- **modules** : Liste les modules de noyau chargés.
- **multiscan** : Scanne la mémoire pour détecter plusieurs types d'artefacts en parallèle.
- **mutantscan** : Scanne la mémoire pour détecter des objets de synchronisation (mutex).
- **notepad** : Récupère le texte présent dans les instances de Notepad en mémoire.
- **objtypescan** : Scanne les objets du noyau en mémoire.
- **patcher** : Détecte les modifications de patch du noyau.
- **poolpeek** : Affiche des informations sur les allocations des pools mémoire.
- **printkey** : Affiche les clés du registre Windows.
- **privs** : Affiche les privilèges des processus.
- **procdump** : Dumpe la mémoire d'un processus spécifique vers un fichier.
- **pslist** : Liste les processus actifs.
- **psscan** : Scanne la mémoire pour des structures de processus cachées.
- **pstree** : Affiche la hiérarchie des processus en arbre.
- **psxview** : Vérifie si des processus sont masqués par des rootkits.
- **qemuinfo** : Fournit des informations sur les systèmes virtualisés via QEMU.
- **raw2dmp** : Convertit un fichier brut en fichier de vidage (dump).
- **screenshot** : Capture des captures d'écran de sessions utilisateur en mémoire.
- **servicediff** : Compare et affiche les différences de services entre deux moments différents.
- **sessions** : Affiche les sessions utilisateurs actives.
- **shellbags** : Extrait les informations Shellbags (historiques d'accès aux répertoires).
- **shimcache** : Affiche les données de compatibilité des applications en mémoire (ShimCache).
- **shutdowntime** : Affiche les informations sur la dernière heure d'arrêt du système.
- **sockets** : Liste les sockets réseau actifs.
- **sockscan** : Scanne la mémoire pour des structures de sockets réseau cachées.
- **ssdt** : Affiche la table des appels système (System Service Descriptor Table).
- **strings** : Recherche des chaînes de caractères dans la mémoire.
- **svcscan** : Scanne les services en mémoire.
- **symlinkscan** : Scanne la mémoire pour des symlinks (liens symboliques).
- **thrdscan/threads** : Scanne la mémoire pour les threads et affiche les threads actifs.
- **timeliner** : Crée une timeline des événements en mémoire.
- **timers** : Affiche les timers actifs dans la mémoire du noyau.
- **truecryptmaster/truecryptpassphrase/truecryptsummary** : Extrait les informations relatives à TrueCrypt (volumes chiffrés).
- **unloadedmodules** : Liste les modules du noyau qui ont été déchargés.
- **userassist** : Liste les clés UserAssist des utilisateurs.
- **userhandles** : Affiche les handles ouverts par les utilisateurs.
- **vaddump/vadinfo/vadtree/vadwalk** : Analyse les régions de mémoire allouées (VAD - Virtual Address Descriptors).
- **verinfo** : Affiche les informations de version des binaires.
- **vmwareinfo** : Fournit des informations sur les systèmes virtualisés avec VMware.
- **volshell** : Un shell interactif pour l'analyse mémoire.
- **windows** : Exécute des commandes spécifiques au système Windows.
- **wintree** : Affiche une arborescence des fenêtres et objets graphiques.
- **wndscan** : Scanne la mémoire pour détecter des objets de fenêtres GUI.
- **yarascan** : Utilise des règles Yara pour rechercher des chaînes ou des patterns spécifiques dans la mémoire.
  
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

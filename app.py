from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import subprocess
import threading
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

# Liste des plugins à exécuter
PLUGINS = [
"amcache",
"apihooks",
"atoms",
"atomscan",
"auditpol",
"bigpools",
"bioskbd",
"cachedump",
"callbacks",
"clipboard",
"cmdline",
"cmdscan",
"connections",
"connscan",
"consoles",
"crashinfo",
"deskscan",
"devicetree",
"dlldump",
"dlllist",
"driverirp",
"drivermodule",
"driverscan",
"dumpcerts",
"dumpfiles",
"dumpregistry",
"editbox",
"envars",
"eventhooks",
"evtlogs",
"filescan",
"gahti",
"gditimers",
"gdt",
"getservicesids",
"getsids",
"handles",
"hashdump",
"hibinfo",
"hivedump",
"hivelist",
"hivescan",
"hpakextract",
"hpakinfo",
"idt",
"iehistory",
"imagecopy",
"imageinfo",
"impscan",
"joblinks",
"kdbgscan",
"kpcrscan",
"ldrmodules",
"lsadump",
"machoinfo",
"malfind",
"mbrparser",
"memdump",
"memmap",
"messagehooks",
"mftparser",
"moddump",
"modscan",
"modules",
"multiscan",
"mutantscan",
"notepad",
"objtypescan",
"patcher",
"poolpeek",
"printkey",
"privs",
"procdump",
"pslist",
"psscan",
"pstree",
"psxview",
"qemuinfo",
"raw2dmp",
"screenshot",
"servicediff",
"sessions",
"shellbags",
"shimcache",
"shutdowntime",
"sockets",
"sockscan",
"ssdt",
"strings",
"svcscan",
"symlinkscan",
"thrdscan",
"threads",
"timeliner",
"timers",
"truecryptmaster",
"truecryptpassphrase",
"truecryptsummary",
"unloadedmodules",
"userassist",
"userhandles",
"vaddump",
"vadinfo",
"vadtree",
"vadwalk",
"vboxinfo",
"verinfo",
"vmwareinfo",
"volshell",
"windows",
"wintree",
"wndscan",
"yarascan"
]

# Chemin du dossier de logs pour les commandes Volatility
LOG_DIR = 'volatility_logs/'

# Assurer que le dossier de logs existe
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Chemin vers le répertoire où les fichiers dumps sont stockés
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Assurez-vous que le répertoire d'uploads existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Chemin vers la base de données
DATABASE = 'dumps.db'

# Connexion à la base de données
def connect_db():
    return sqlite3.connect(DATABASE)

# Initialisation de la base de données
def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS dumps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    analyzed BOOLEAN NOT NULL DEFAULT 0
                )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS plugin_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dump_id INTEGER NOT NULL,
                    plugin_name TEXT NOT NULL,
                    result TEXT,
                    FOREIGN KEY (dump_id) REFERENCES dumps(id)
                )''')
    conn.commit()
    conn.close()

# Sauvegarder un dump dans la base de données
def save_dump(dump_path):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO dumps (path, analyzed) VALUES (?, 0)", (dump_path,))
    conn.commit()
    dump_id = cur.lastrowid
    conn.close()
    return dump_id

# Charger les dumps depuis la base de données
def load_dumps():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM dumps")
    dumps = cur.fetchall()
    conn.close()
    return dumps

# Sauvegarder les résultats d'un plugin dans la base de données
def save_plugin_result(dump_id, plugin_name, result):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO plugin_results (dump_id, plugin_name, result) VALUES (?, ?, ?)", (dump_id, plugin_name, result))
    conn.commit()
    conn.close()

# Charger les résultats des plugins depuis la base de données
def load_plugin_results(dump_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT plugin_name, result FROM plugin_results WHERE dump_id = ?", (dump_id,))
    results = cur.fetchall()
    conn.close()
    return {plugin: result for plugin, result in results}

# Fonction pour exécuter un plugin Volatility et capturer les résultats
def run_volatility_plugin(dump_path, plugin):
    command = f"volatility.exe -f \"{dump_path}\" {plugin}"
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    return process.stdout + process.stderr
def analyze_dump_parallel(dump_id, dump_path):
    plugins = PLUGINS
    log_file = os.path.join(LOG_DIR, f'dump_{dump_id}.log')

    with ThreadPoolExecutor() as executor:
        # Ouvrir le fichier de log en mode écriture
        with open(log_file, 'w') as log_f:
            # Dictionnaire pour mapper les futures (exécutions en thread) avec les plugins
            futures = {executor.submit(run_volatility_plugin, dump_path, plugin): plugin for plugin in plugins}

            # Parcourir les résultats dès qu'ils sont disponibles
            for future in as_completed(futures):
                plugin = futures[future]
                try:
                    result = future.result()
                    # Sauvegarder le résultat dans la base de données
                    save_plugin_result(dump_id, plugin, result)

                    # Écrire la progression dans le log
                    log_f.write(f"Step: {plugin} completed\n")
                    log_f.flush()  # Forcer l'écriture immédiate dans le fichier
                except Exception as exc:
                    log_f.write(f"Error running {plugin}: {exc}\n")
                    log_f.flush()

    # Marquer le dump comme analysé après avoir terminé tous les threads
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE dumps SET analyzed = 1 WHERE id = ?", (dump_id,))
    conn.commit()
    conn.close()

# Route principale pour afficher la liste des dumps
@app.route('/')
def index():
    dumps = load_dumps()
    return render_template('index.html', dumps=dumps)

# Route pour sélectionner un nouveau dump
@app.route('/select_dump', methods=['POST'])
def select_dump():
    if 'dump_file' not in request.files:
        return jsonify({"success": False, "message": "No file part"})
    file = request.files['dump_file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"})
    
    if file:
        filename = file.filename
        dump_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(dump_path)
        dump_id = save_dump(dump_path)
        return jsonify({"success": True, "dump_id": dump_id})
    return jsonify({"success": False})

# Route pour supprimer un dump
@app.route('/remove_dump/<int:dump_id>', methods=['POST'])
def remove_dump(dump_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM dumps WHERE id = ?", (dump_id,))
    cur.execute("DELETE FROM plugin_results WHERE dump_id = ?", (dump_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# Route pour démarrer l'analyse d'un dump
@app.route('/start_analysis/<int:dump_id>')
def start_analysis(dump_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT path, analyzed FROM dumps WHERE id = ?", (dump_id,))
    dump = cur.fetchone()
    conn.close()

    if not dump:
        return "Dump not found", 404

    dump_path, analyzed = dump
    if not analyzed:
        # Lancer l'analyse avec des threads en parallèle
        thread = threading.Thread(target=analyze_dump_parallel, args=(dump_id, dump_path))
        thread.start()
        return redirect(url_for('progress', dump_id=dump_id))
    
    # Si déjà analysé, rediriger vers les résultats
    return redirect(url_for('analyze_results', dump_id=dump_id))

# Route pour afficher la page de progression
@app.route('/progress/<int:dump_id>')
def progress(dump_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT path FROM dumps WHERE id = ?", (dump_id,))
    dump = cur.fetchone()
    conn.close()

    if not dump:
        return "Dump not found", 404

    return render_template('progress.html', dump_id=dump_id, dump_path=dump[0])

# Route pour vérifier la progression de l'analyse
@app.route('/check_progress/<int:dump_id>')
def check_progress(dump_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT analyzed FROM dumps WHERE id = ?", (dump_id,))
    dump = cur.fetchone()
    conn.close()

    if not dump:
        return jsonify({"error": "Dump not found"}), 404

    analyzed = dump[0]
    log_file = os.path.join(LOG_DIR, f'dump_{dump_id}.log')
    if os.path.exists(log_file):
        with open(log_file, 'r') as log_f:
            lines = log_f.readlines()
            # Compter le nombre de lignes de progression
            step_count = sum(1 for line in lines if line.startswith("Step:"))
            total_steps = len(PLUGINS)
    else:
        step_count = 0
        total_steps = len(PLUGINS)

    if analyzed:
        return jsonify({"finished": True, "step": total_steps, "total_steps": total_steps})
    else:
        return jsonify({"finished": False, "step": step_count, "total_steps": total_steps})

# Route pour afficher les résultats de l'analyse
@app.route('/analyze_results/<int:dump_id>')
def analyze_results(dump_id):
    plugins_data = load_plugin_results(dump_id)
    if plugins_data:
        return render_template('analyze.html', dump_id=dump_id, plugins_data=plugins_data)
    return "Results not found", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

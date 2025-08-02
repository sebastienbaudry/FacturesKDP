import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import json
import os
import subprocess
import platform
from datetime import datetime, timedelta
import threading

from kdp_invoice_generator import generer_facture_logic

CONFIG_PATH = "config.json"

# --- Description/version ---
INFOS_VERSION = """\
Générateur de factures Word et PDF automatisé pour les revenus Amazon KDP
Auteur: Sébastien Baudry – assisté de Claude 4 Sonnet, Gemini Pro 2.5, ChatGPT 4o
Version: 3.2 – correction détails + ajout format PDF
"""

def charger_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def sauvegarder_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

class InvoiceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Générateur de Factures KDP")
        self.geometry("900x700")

        self.config_data = charger_config()
        self.config_widgets = {}

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.setup_generation_tab()
        self.setup_config_tab()
        self.setup_version_tab()  # Ajout de l'onglet version

    # --- Onglet Génération ---
    def setup_generation_tab(self):
        gen_frame = ttk.Frame(self.notebook)
        self.notebook.add(gen_frame, text="Génération")

        file_frame = ttk.LabelFrame(gen_frame, text="Fichier de rapport KDP", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)

        self.filepath_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.filepath_var, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(file_frame, text="Parcourir...", command=self.browse_file).pack(side=tk.LEFT)

        period_frame = ttk.LabelFrame(gen_frame, text="Période de la facture", padding=10)
        period_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(period_frame, text="Année :").pack(side=tk.LEFT, padx=5)
        self.year_var = tk.StringVar(value=str(self.get_previous_month()[0]))
        ttk.Entry(period_frame, textvariable=self.year_var, width=10).pack(side=tk.LEFT)

        ttk.Label(period_frame, text="Mois :").pack(side=tk.LEFT, padx=5)
        self.month_var = tk.StringVar(value=str(self.get_previous_month()[1]))
        ttk.Combobox(period_frame, textvariable=self.month_var, values=[str(i) for i in range(1, 13)], state="readonly", width=5).pack(side=tk.LEFT)

        format_frame = ttk.LabelFrame(gen_frame, text="Format de sortie", padding=10)
        format_frame.pack(fill=tk.X, padx=10, pady=5)

        self.format_var = tk.StringVar(value="both")
        for fmt in [("DOCX", "docx"), ("PDF", "pdf"), ("Les deux", "both")]:
            ttk.Radiobutton(format_frame, text=fmt[0], variable=self.format_var, value=fmt[1]).pack(side=tk.LEFT, padx=10)

        self.generate_button = ttk.Button(gen_frame, text="Générer la facture", command=self.start_generation)
        self.generate_button.pack(pady=15, fill=tk.X, padx=10)

        log_frame = ttk.LabelFrame(gen_frame, text="Journal", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, state='disabled', wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.tag_config('ERROR', foreground='red')
        self.log_text.tag_config('SUCCESS', foreground='green')

    def browse_file(self):
        filepath = filedialog.askopenfilename(title="Sélectionnez le fichier KDP", filetypes=[("Excel", "*.xlsx")])
        if filepath:
            self.filepath_var.set(filepath)

    def get_previous_month(self):
        today = datetime.now()
        first = today.replace(day=1)
        last_month = first - timedelta(days=1)
        return last_month.year, last_month.month

    def start_generation(self):
        filepath = self.filepath_var.get()
        year = self.year_var.get()
        month = self.month_var.get()

        if not filepath:
            self.log("Veuillez sélectionner un fichier.", "ERROR")
            return
        if not (year.isdigit() and month.isdigit()):
            self.log("Année et mois invalides.", "ERROR")
            return

        self.generate_button.config(state='disabled')
        self.clear_log()
        self.log("Lancement de la génération...")

        threading.Thread(target=self.run_generation_logic, args=(filepath, int(year), int(month))).start()

    def run_generation_logic(self, filepath, year, month):
        try:
            success, message, fichiers = generer_facture_logic(filepath, year, month, self.format_var.get())
        except Exception as e:
            self.log(f"Erreur : {e}", "ERROR")
            self.generate_button.config(state='normal')
            return

        if success:
            self.log(message, "SUCCESS")
            for f in fichiers:
                self.log(f"Ouverture : {f}")
                try:
                    if platform.system() == 'Windows':
                        os.startfile(f)
                    elif platform.system() == 'Darwin':
                        subprocess.run(['open', f])
                    else:
                        subprocess.run(['xdg-open', f])
                except Exception as e:
                    self.log(f"Impossible d’ouvrir {f} : {e}", "ERROR")
        else:
            self.log(message, "ERROR")

        self.generate_button.config(state='normal')

    def log(self, message, level=None):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n", level)
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def clear_log(self):
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')

    # --- Onglet Paramétrage ---
    def setup_config_tab(self):
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="Paramétrage")

        canvas = tk.Canvas(config_frame)
        scrollbar = ttk.Scrollbar(config_frame, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            if platform.system() == 'Windows':
                canvas.yview_scroll(-1 * int(event.delta / 120), "units")
            elif platform.system() == 'Darwin':
                canvas.yview_scroll(-1 * int(event.delta), "units")
            else:
                canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

        scrollable.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        scrollable.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        scrollable.bind("<Enter>", lambda e: canvas.bind_all("<Button-4>", _on_mousewheel))
        scrollable.bind("<Enter>", lambda e: canvas.bind_all("<Button-5>", _on_mousewheel))
        scrollable.bind("<Leave>", lambda e: canvas.unbind_all("<Button-4>"))
        scrollable.bind("<Leave>", lambda e: canvas.unbind_all("<Button-5>"))

        multiligne_keys = ["adresse", "autoliquidation", "message", "format", "texte"]

        for section, fields in self.config_data.items():
            frame = ttk.LabelFrame(scrollable, text=section.capitalize(), padding=10)
            frame.pack(fill=tk.X, expand=True, padx=10, pady=5)
            self.config_widgets[section] = {}

            for key, value in fields.items():
                row = ttk.Frame(frame)
                row.pack(fill=tk.X, expand=True, pady=3)

                ttk.Label(row, text=key + " :", width=25, anchor="w").pack(side=tk.LEFT)

                if any(k in key.lower() for k in multiligne_keys) or "\n" in str(value):
                    widget = tk.Text(row, height=3, wrap=tk.WORD)
                    widget.insert("1.0", str(value))
                    widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
                else:
                    widget = ttk.Entry(row)
                    widget.insert(0, str(value))
                    widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

                self.config_widgets[section][key] = widget

        ttk.Button(scrollable, text="💾 Enregistrer les paramètres", command=self.save_config).pack(pady=15)

    def highlight_invalid(self, widget):
        widget.configure(highlightbackground="red", highlightcolor="red", highlightthickness=2)

    def save_config(self):
        erreurs = []
        champs_valides = {}

        def reset_border(w):
            w.configure(highlightthickness=0)

        for section, fields in self.config_widgets.items():
            champs_valides[section] = {}
            for key, widget in fields.items():
                reset_border(widget)
                value = widget.get("1.0", tk.END).strip() if isinstance(widget, tk.Text) else widget.get().strip()

                if not value:
                    erreurs.append(f"[{section}] Le champ '{key}' est vide.")
                    self.highlight_invalid(widget)
                    continue

                k = key.lower()
                if k == "siret" and not value.replace(" ", "").isdigit():
                    erreurs.append(f"[{section}] Le SIRET doit être numérique.")
                    self.highlight_invalid(widget)
                elif k == "tva_intra" and not (value[:2].isalpha() and value[2:].replace(" ", "").isalnum()):
                    erreurs.append(f"[{section}] TVA intra invalide.")
                    self.highlight_invalid(widget)
                elif k == "iban" and not (value[:2].isalpha() and value[2:].replace(" ", "").isdigit()):
                    erreurs.append(f"[{section}] IBAN invalide.")
                    self.highlight_invalid(widget)
                elif k == "bic" and not (len(value.strip()) in [8, 11] and value.isalnum()):
                    erreurs.append(f"[{section}] BIC invalide.")
                    self.highlight_invalid(widget)
                elif k == "code_ape" and not (value[:4].isdigit() and value[4].isalpha()):
                    erreurs.append(f"[{section}] Code APE invalide.")
                    self.highlight_invalid(widget)
                elif k == "format_nom_sortie" and not ("{annee}" in value and "{mois" in value):
                    erreurs.append(f"[{section}] format_nom_sortie doit contenir '{{annee}}' et '{{mois}}'.")
                    self.highlight_invalid(widget)

                champs_valides[section][key] = value

        if erreurs:
            messagebox.showerror("Erreurs de validation", "\n".join(erreurs))
            return

        self.config_data = champs_valides
        sauvegarder_config(self.config_data)
        messagebox.showinfo("Succès", "Configuration enregistrée.")

    # --- Onglet Version ---
    def setup_version_tab(self):
        version_frame = ttk.Frame(self.notebook)
        self.notebook.add(version_frame, text="Version")

        txt = tk.Text(version_frame, wrap=tk.WORD, height=15, bg=self.cget('bg'), relief=tk.FLAT)
        txt.insert("1.0", INFOS_VERSION)
        txt.config(state='disabled')
        txt.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

if __name__ == "__main__":
    app = InvoiceApp()
    app.mainloop()

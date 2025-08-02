# Générateur de Factures KDP - Guide d'Installation et d'Utilisation v3.2

## 📋 Prérequis

Avant d'installer le générateur, assurez-vous d'avoir :
- Python 3.7 ou plus récent installé sur votre ordinateur
- Un fichier Excel des paiements KDP d'Amazon (téléchargé depuis votre compte KDP https://kdpreports.amazon.com/payments)

## 🚀 Installation

### Étape 1 : Installer les dépendances Python

Ouvrez un terminal (Command Prompt sur Windows, Terminal sur Mac/Linux) et exécutez :

```bash
pip install pandas openpyxl python-docx fpdf2
```

### Étape 2 : Télécharger les fichiers

Téléchargez et sauvegardez dans un même dossier les fichiers suivants :

- `kdp_invoice_generator.py` (le script principal de génération)
- `generateur_factures_kdp.py` (l'interface graphique)  
- `config.json` (le fichier de configuration - utilisez le template fourni)
- `lancer_generateur_facture_kdp.bat` (pour Windows - lance l'interface graphique)
- `facture_simple.bat` (script batch alternatif pour ligne de commande)

### Étape 3 : Configuration personnalisée

Ouvrez le fichier `config.json` et remplacez toutes les informations entre crochets par vos vraies données.
Si vous utilisez l'interface graphique, vous pouvez mettre à jour ces informations dans l'onglet "Paramétrage".

```json
{
  "entreprise": {
    "nom": "MONSIEUR JEAN DUPONT",
    "adresse": "123 rue de la Paix\n75001 Paris\nFRANCE",
    "siret": "12345678901234",
    "tva_intra": "FR12345678901",
    "code_ape": "5811Z -- Édition de livres",
    "forme_juridique": "Entrepreneur individuel",
    "iban": "FR7612345987650123456789012",
    "bic": "BDFEFRPPXXX"
  },
  "client": {
    "nom": "Amazon Media EU S.à r.l.",
    "adresse": "5 rue Plaetis\nL-2338 Luxembourg\nLUXEMBOURG",
    "tva_intra": "LU20260743"
  },
  "facture": {
    "prefixe_numero": "FACT",
    "format_numero": "{annee}-{mois:02d}-01",
    "date_paiement_defaut": "30 jours date de facture",
    "mode_reglement": "Virement bancaire"
  },
  "fichiers": {
    "nom_fichier_excel_kdp": "KDP_Payments_rapport_juillet_2025.xlsx",
    "dossier_sortie": "./",
    "format_nom_sortie": "Facture_KDP_{annee}-{mois:02d}.docx"
  },
  "messages": {
    "autoliquidation": "Autoliquidation -- TVA due par le preneur, conformément à l'article 283-2 du CGI et à la directive 2006/112/CE. Facture émise hors taxes. Le client, assujetti établi dans un autre État membre de l'UE, est redevable de la TVA."
  }
}
```

## 📖 Utilisation

### Méthode 1 : Interface Graphique (Recommandée)

**Double-cliquez sur `lancer_generateur_facture_kdp.bat`** (Windows) ou exécutez :

```bash
python generateur_factures_kdp.py
```

L'interface graphique propose 3 onglets :

#### Onglet "Génération"
1. **Sélection du fichier** : Cliquez sur "Parcourir..." pour choisir votre fichier Excel KDP, vous pouvez le télécharger sur la page https://kdpreports.amazon.com/payments
2. **Période** : L'année et le mois du mois précédent sont pré-remplis
3. **Format de sortie** : Choisissez entre DOCX, PDF ou les deux formats
4. **Génération** : Cliquez sur "Générer la facture"
5. **Journal** : Suivez le processus en temps réel

#### Onglet "Paramétrage"
- Modifiez votre configuration directement dans l'interface
- Validation automatique des champs obligatoires
- Sauvegarde sécurisée avec vérification des données

#### Onglet "Version"
- Informations sur la version et les développeurs

### Méthode 2 : Script Batch Simplifié (Windows)

Modifiez le fichier `facture_simple.bat` pour pointer vers votre fichier Excel, puis double-cliquez dessus :

```batch
@echo off
cls
echo ========================================
echo     GENERATEUR DE FACTURES KDP v3.2
echo ========================================

REM Modifiez le nom du fichier ci-dessous
set FICHIER_KDP=KDP_Payments_votre_fichier.xlsx

set /p ANNEE="Entrez l'annee (ex: 2025) ou laissez vide pour le mois precedent: "
set /p MOIS="Entrez le mois (1-12) ou laissez vide pour le mois precedent: "
set /p FORMAT="Entrez le format (docx, pdf, both) [defaut: both]: "

python kdp_invoice_generator.py "%FICHIER_KDP%" %ANNEE_ARG% %MOIS_ARG% --format %FORMAT%
pause
```

### Méthode 3 : Ligne de commande directe

#### Utilisation de base (utilise le fichier configuré dans config.json)
```bash
python kdp_invoice_generator.py
```

#### Spécifier un fichier Excel différent
```bash
python kdp_invoice_generator.py "KDP_Payments_votre_fichier.xlsx"
```

#### Utilisation avancée avec options
```bash
python kdp_invoice_generator.py --annee 2025 --mois 5 --format both
```

## 🔧 Options de ligne de commande

| Option | Description | Exemple |
|--------|-------------|---------|
| `--config` | Fichier de configuration personnalisé | `--config ma_config.json` |
| `--annee` | Année de la période | `--annee 2025` |
| `--mois` | Mois de la période (1-12) | `--mois 5` |
| `--format` | Format de sortie | `--format docx` ou `--format pdf` ou `--format both` |
| `--numero-facture` | Numéro personnalisé | `--numero-facture "FACT-2025-05"` |
| `--date-paiement` | Date de paiement constatée | `--date-paiement "31/08/2025"` |

## 📁 Structure des fichiers recommandée

```
Mon_Dossier_Factures_KDP/
├── kdp_invoice_generator.py          ← Script principal de génération
├── generateur_factures_kdp.py        ← Interface graphique
├── config.json                       ← Votre configuration personnalisée
├── lancer_generateur_facture_kdp.bat ← Lanceur interface graphique (Windows)
├── facture_simple.bat                ← Script batch alternatif (Windows)
├── KDP_Payments_juillet_2025.xlsx    ← Vos fichiers Excel KDP
├── KDP_Payments_aout_2025.xlsx
└── Factures_Generees/               ← Dossier des factures créées
    ├── Facture_KDP_2025-07.docx
    ├── Facture_KDP_2025-07.pdf
    ├── Facture_KDP_2025-08.docx
    └── Facture_KDP_2025-08.pdf
```

## ⚙️ Configuration avancée

### Personnalisation des numéros de facture

```json
{
  "facture": {
    "prefixe_numero": "FACTURE",                    // Préfixe des numéros
    "format_numero": "{annee}-{mois:02d}-001",      // Format du numéro
    "date_paiement_defaut": "Fin de mois",          // Date de paiement par défaut
    "mode_reglement": "Virement SEPA"               // Mode de règlement
  }
}
```

### Organisation des fichiers de sortie

```json
{
  "fichiers": {
    "nom_fichier_excel_kdp": "KDP_Payments_2025.xlsx",        // Fichier par défaut
    "dossier_sortie": "./Factures_2025/",                     // Dossier de destination
    "format_nom_sortie": "Facture_{annee}_{mois:02d}.docx"    // Format du nom
  }
}
```

### Messages personnalisés

```json
{
  "messages": {
    "autoliquidation": "Votre message TVA personnalisé selon vos besoins..."
  }
}
```

## ✅ Vérification de l'installation

Pour tester votre installation :

1. **Test avec l'interface graphique** :
   ```bash
   python generateur_factures_kdp.py
   ```

2. **Test en ligne de commande** :
   ```bash
   python kdp_invoice_generator.py --annee 2025 --mois 1 --format both
   ```

Si vous voyez des erreurs du type :
- `"Le champ 'entreprise.nom' n'est pas configuré"`
- `"[Votre IBAN]" dans le fichier généré`

➡️ **Vérifiez que vous avez bien remplacé TOUTES les valeurs entre crochets dans `config.json`**

## 🔐 Sécurité et confidentialité

- **Anonymisation** : Le fichier `template_config.json` fourni ne contient aucune donnée réelle
- **Protection** : Ajoutez `config.json` à votre `.gitignore` si vous versionnez le code
- **Sauvegarde** : Gardez une copie de votre `config.json` configuré en lieu sûr

## ❗ Résolution des problèmes courants

### "Fichier de configuration non trouvé"
➡️ Assurez-vous que `config.json` est dans le même dossier que les scripts Python

### "Le champ X n'est pas configuré"
➡️ Ouvrez `config.json` et remplacez toutes les valeurs `[entre crochets]` par vos vraies informations

### "Aucune donnée trouvée pour XX/XXXX"
➡️ Vérifiez que votre fichier Excel contient des données for cette période et que le format correspond à celui attendu par KDP

### Interface graphique qui ne s'ouvre pas
➡️ Vérifiez que `tkinter` est installé : `python -m tkinter` (devrait ouvrir une fenêtre test)

### Erreur lors de la génération PDF
➡️ Assurez-vous d'avoir installé `fpdf2` : `pip install fpdf2`

### Script batch qui ne trouve pas Python
➡️ Ajoutez Python à votre PATH système ou utilisez le chemin complet vers python.exe

## 🆕 Nouveautés version 3.2

- **Interface graphique complète** avec onglets (Génération, Paramétrage, Version)
- **Génération PDF native** avec la bibliothèque `fpdf2`
- **Validation avancée** des champs de configuration
- **Gestion améliorée** des détails de revenus par marché
- **Ouverture automatique** des fichiers générés
- **Journal en temps réel** des opérations
- **Support des formats multiples** (DOCX, PDF, ou les deux)

## 📊 Format des données KDP

Le générateur analyse automatiquement les fichiers Excel KDP avec les colonnes :
- `Période de vente - Date de début`
- `Marché` (Amazon.fr, Amazon.com, etc.)
- `Numéro de paiement`
- `Devise`
- `Redevance accumulée`
- `Montant du paiement`
- `Taux de change`
- `Détail` ou `Source` (pour les lignes de détail)

## ℹ️ À propos

Ce générateur a été développé par **Sébastien Baudry**, avec l'assistance des IA génératives suivantes :
- **Claude 4 Sonnet** (Anthropic)
- **Gemini Pro 2.5** (Google DeepMind)
- **ChatGPT-4o** (OpenAI)

### 📝 Licence

Ce générateur est distribué sous licence **MIT** :

> Copyright (c) 2025 Sébastien Baudry  
>  
> Permission is hereby granted, free of charge, to any person obtaining a copy  
> of this software and associated documentation files (the "Software"), to deal  
> in the Software without restriction, including without limitation the rights  
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
> copies of the Software, and to permit persons to whom the Software is  
> furnished to do so, subject to the following conditions:  
>  
> The above copyright notice and this permission notice shall be included in all  
> copies or substantial portions of the Software.  
>  
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

Pour plus d'informations : [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)

---

**Version 3.2** - Interface graphique moderne avec génération PDF native et validation avancée
#!/usr/bin/env python3
"""
import_data.py - Pulizia e standardizzazione dei dati scaricati

Questo script legge i dati grezzi dalla cartella data/raw/ e produce
versioni pulite e standardizzate in data/processed/.
"""

import pandas as pd
import os
from pathlib import Path

def main():
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    
    # Assicura che la directory di output esista
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    print("Importazione e pulizia dei dati...")
    
    # Esempio: processa file GNSS se esistono
    gnss_files = list(raw_dir.glob("*gnss*")) + list(raw_dir.glob("*GNSS*"))
    if gnss_files:
        for f in gnss_files:
            print(f"  Processing GNSS file: {f.name}")
            # Qui andrà la logica di parsing specifica
            # df = pd.read_csv(f, ...)
            # df_clean = clean_gnss(df)
            # df_clean.to_csv(processed_dir / f"clean_{f.name}", index=False)
    
    # Esempio: processa file sismici se esistono
    seismic_files = list(raw_dir.glob("*seismic*")) + list(raw_dir.glob("*SEISMIC*"))
    if seismic_files:
        for f in seismic_files:
            print(f"  Processing seismic file: {f.name}")
            # Qui andrà la logica di parsing specifica
    
    # Esempio: processa file geochimici se esistono
    gas_files = list(raw_dir.glob("*gas*")) + list(raw_dir.glob("*GAS*")) + list(raw_dir.glob("*chem*"))
    if gas_files:
        for f in gas_files:
            print(f"  Processing geochemical file: {f.name}")
            # Qui andrà la logica di parsing specifica
    
    print("Importazione completata.")

if __name__ == "__main__":
    main()

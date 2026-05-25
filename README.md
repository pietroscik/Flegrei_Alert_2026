# Flegrei Alert 2026

**Nota Tecnica INGV - Febbraio 2026**

Questo progetto implementa una pipeline riproducibile per l'analisi integrata di dati geodetici (GNSS), sismologici e geochimici per il monitoraggio della caldera dei Campi Flegrei.

## 📂 Struttura del Progetto

*   **`data/`**: Contiene i dati grezzi (`raw`) e processati (`processed`).
*   **`scripts/`**: Script di analisi (R e Python).
*   **`notebook/`**: File RMarkdown per la generazione del report.
*   **`reports/`**: Output finali (Figure e PDF).
*   **`Dockerfile`**: Definizione dell'ambiente di esecuzione.

## 🚀 Quick Start (VS Code)

Se utilizzi Visual Studio Code, puoi eseguire i task preconfigurati:
1.  Premi `Ctrl+Shift+P` (o `Cmd+Shift+P`).
2.  Digita **Tasks: Run Task**.
3.  Seleziona nell'ordine:
    *   `Build Docker Image` (solo la prima volta)
    *   `Download Data (Web)`
    *   `Import & Clean Data (Real)`
    *   `Run All Analysis`
    *   `Generate Report (RMarkdown)`

## 💻 Esecuzione Manuale (Terminale)

È possibile eseguire l'intera pipeline manualmente utilizzando Docker da terminale.
Vedi la guida dettagliata: MANUAL_EXECUTION.md.

## 📋 Requisiti

*   Docker Desktop installato e attivo.
*   Git.

## 📄 Licenza

Dati e codice sono rilasciati sotto licenza **CC-BY-4.0**.

---

**Maintainer:** Flegrei Alert Team
**Versione:** 1.0.0
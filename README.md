# 🌋 Flegrei Alert 2026 - Campi Flegrei Quantitative Monitoring System

## Abstract

Questo sistema presenta un framework integrato di monitoraggio sismico per la caldera dei Campi Flegrei, combinando molteplici approcci analitici:

1. **Stima del b-value di Gutenberg-Richter** con analisi a finestra mobile
2. **Rilevamento anomalie** tramite metodi Z-score e quantili
3. **Fusione multi-segnale** che integra tasso sismico, b-value e dati di sollevamento GNSS
4. **Sistema di Allerta Precoce (EWS)** con soglie dinamiche e controlli di persistenza
5. **Modellazione stocastica ETAS** per la sismicità di fondo e parametri di triggering
6. **Architetture Deep Learning ibride** (LSTM, Autoencoder) per previsioni non lineari e rilevamento anomalie unsupervised

**Il sistema utilizza ESCLUSIVAMENTE dati reali e validati** da fonti INGV certificate. Nessun dato sintetico viene generato o utilizzato.

**Parole chiave**: Campi Flegrei, b-value, anomaly detection, ETAS, LSTM, Autoencoder, Deep Learning, early warning, monitoraggio sismico, dati reali

---

## 1. Introduzione

I Campi Flegrei sono uno dei sistemi vulcanici più pericolosi d'Europa, caratterizzati da episodi bradisismici e sciami sismici di magnitudo bassa-moderata. Il monitoraggio quantitativo richiede l'integrazione di segnali multipli per rilevare pattern precursori e valutare i livelli di unrest.

### 1.1 Obiettivi

- Implementare ingestione automatizzata di cataloghi sismici INGV
- Stimare l'evoluzione temporale del b-value di Gutenberg-Richter
- Rilevare anomalie statistiche nelle serie temporali di b-value
- Costruire un indice di unrest composito da segnali multipli
- Sviluppare un Sistema di Allerta Precoce con criteri robusti
- Adattare parametri del modello ETAS per forecasting stocastico

### 1.2 Area di Studio

L'analisi si concentra sulla regione della caldera flegrea delimitata da:
- Latitudine: 40.80°N – 40.95°N
- Longitudine: 14.10°E – 14.25°E
- Magnitudo minima: M ≥ 0.0

---

## 2. Installazione

### 2.1 Requisiti

```bash
pip install pandas numpy scipy matplotlib seaborn scikit-learn statsmodels requests
```

Oppure usare l'ambiente Docker fornito:

```bash
docker build -t flegrei-alert .
docker run -v $(pwd)/data:/app/data flegrei-alert
```

### 2.2 Struttura del Progetto

```
/workspace/
├── scripts/              # Script standalone
│   ├── download_data.py  # Download dati reali da INGV
│   ├── import_data.py    # Pulizia e standardizzazione
│   └── ...
├── src/                  # Moduli principali
│   ├── data_ingestion.py
│   ├── analysis/         # Analisi statistiche
│   │   ├── b_value.py
│   │   ├── anomaly_bvalue.py
│   │   ├── multi_signal_model.py
│   │   └── early_warning.py
│   ├── evaluation/       # Validazione e metriche
│   └── ingestion/        # Fetch dati INGV
├── services/             # Servizi operativi
│   ├── worker/           # Cycle periodici
│   └── stream/           # Streaming in real-time
├── data/
│   ├── raw/              # Dati grezzi (solo reali)
│   └── processed/        # Dati elaborati
├── reports/fig/          # Output grafici
└── run_pipeline.py       # Pipeline completa
```

---

## 3. Utilizzo

### 3.1 Download Dati Reali

**Importante**: Questo sistema utilizza SOLO dati reali e validati.

```bash
# Download automatico da sorgenti INGV
python scripts/download_data.py
```

Fonti dati supportate:
- **Sismicità**: INGV FDSN Webservice (http://webservices.ingv.it/)
- **GNSS**: RING Network (http://ring.gm.ingv.it/)
- **Geochimica**: INGV Osservatorio Vesuviano (richiede autorizzazione)

Download manuale alternativo:
1. Visitare http://iside.rm.ingv.it/iside/standard/index.jsp
2. Definire area: Lat 40.80-40.95, Lon 14.10-14.25
3. Scaricare catalogo CSV
4. Salvare in `data/raw/` con prefisso `seismic_`

### 3.2 Esecuzione Pipeline Completa

```bash
python run_pipeline.py
```

La pipeline esegue automaticamente:
1. ✓ Verifica disponibilità dati reali
2. ✓ Ingestion e pulizia catalogo
3. ✓ Calcolo rolling b-value
4. ✓ Rilevamento anomalie
5. ✓ Fusione multi-segnale
6. ✓ Sistema di allerta precoce
7. ✓ Generazione report

### 3.3 Modalità Operative

#### Modalità A: Pipeline Storica Completa

Rielabora il catalogo storico completo (default: 1 anno):

```bash
python run_pipeline.py
```

Tempo di esecuzione: ~5-10 minuti per 1 anno di dati.

#### Modalità B: Ciclo Periodico (Worker)

Esegue analisi su dati recenti (default: ultimi 7 giorni):

```bash
# Default: ultimi 7 giorni
python services/worker/run_cycle.py

# Personalizzato: ultimi 30 giorni
python services/worker/run_cycle.py --days 30
```

Adatto per scheduling cron:
```bash
# Esegui ogni 6 ore
0 */6 * * * cd /path/to/repo && python services/worker/run_cycle.py --days 7 >> logs/worker.log 2>&1
```

#### Modalità C: Servizio Streaming Real-Time

Monitoraggio continuo per integrazione dashboard:

```bash
# Output console (default: intervallo 10s)
python services/stream/engine.py

# Output JSON per integrazione API
python services/stream/engine.py --format json --interval 5
```

---

## 4. Metodologie

### 4.1 Stima del b-value

Il b-value è stimato usando il metodo di massima verosimiglianza (Aki, 1965):

$$b = \frac{\log_{10}(e)}{\bar{M} - M_0}$$

dove $\bar{M}$ è la magnitudo media e $M_0$ è la magnitudo di completezza.

**Rolling b-value**: Calcolato su finestre mobili di 300 eventi per stabilità statistica.

### 4.2 Rilevamento Anomalie

Due metodi complementari identificano anomalie nel b-value:

1. **Metodo Z-score**:
   $$Z(t) = \frac{b(t) - \mu_{window}}{\sigma_{window}}$$
   Anomalia quando |Z| > 2 (finestra mobile = 50 campioni)

2. **Metodo basato sui quantili**:
   Anomalie definite come valori sotto il 5° percentile o sopra il 95° percentile.

**Punteggio anomalia combinato**: Somma degli indicatori Z-score e quantili (range: 0-2).

### 4.3 Fusione Multi-Segnale

Tre segnali indipendenti sono integrati in un indice di unrest composito:

1. **Tasso sismico**: Conteggio eventi giornaliero/settimanale
2. **b-value**: Stima rolling dalla Sezione 4.2
3. **Sollevamento del suolo**: Spostamento verticale da stazione GNSS (es. RITE)

I segnali sono normalizzati con z-score:
$$X_{norm} = \frac{X - \mu_X}{\sigma_X}$$

**Indice di Unrest (UI)**:
$$UI(t) = 0.4 \cdot Rate_{norm}(t) + 0.3 \cdot [-b_{norm}(t)] + 0.3 \cdot Uplift_{norm}(t)$$

Nota: Il coefficiente negativo del b-value riflette la relazione inversa (b-value basso → alto stress).

### 4.4 Sistema di Allerta Precoce

Soglie dinamiche sono calcolate dalla distribuzione empirica dell'indice di unrest:

| Livello | Condizione | Azione |
|---------|------------|--------|
| **NORMALE** | UI ≤ 50° percentile | Monitoraggio standard |
| **ELEVATO** | 50° < UI ≤ 75° percentile | Incremento frequenza analisi |
| **ALTO** | 75° < UI ≤ 90° percentile | Allerta protezione civile |
| **CRITICO** | UI > 90° percentile | Attivazione procedura emergenza |

**Controlli di persistenza**: Un'allerta è confermata solo se mantenuta per N giorni consecutivi (default: 3 giorni) per ridurre falsi positivi.

---

## 5. Output

### 5.1 File Generati

| File | Descrizione | Dimensione tipica |
|------|-------------|-------------------|
| `cleaned_catalog.csv` | Catalogo sismico pulito | ~500 KB |
| `b_value_rolling.csv` | Serie temporale b-value | ~50 KB |
| `b_value_anomalies.csv` | Anomalie rilevate | ~10 KB |
| `unrest_index.csv` | Indice di unrest composito | ~20 KB |
| `early_warning_system.csv` | Allerte e validazione | ~30 KB |

### 5.2 Visualizzazioni

I grafici sono salvati in `reports/fig/`:

- Evoluzione tasso sismico
- Distribuzione magnitudo e fit Gutenberg-Richter
- Serie temporale b-value con bande di confidenza
- Indice di unrest e componenti
- Timeline allerte

---

## 6. Limitazioni

1. **Completezza dei dati**: La magnitudo di completezza del catalogo INGV può variare nel tempo
2. **Dipendenza da dati uplift**: Richiede dati GNSS esterni per analisi multi-segnale completa
3. **Assunzioni ETAS**: Il modello assume un rateo di fondo stazionario (potrebbe non valere durante unrest)
4. **Calibrazione soglie**: Le soglie di allerta sono basate su percentili empirici, non modelli fisici

---

## 7. Conclusioni

Questo sistema fornisce un framework quantitativo per valutare l'unrest vulcanico ai Campi Flegrei attraverso l'integrazione di indicatori sismici multipli. L'architettura modulare permette estensioni facili a segnali aggiuntivi (geochimici, geodetici, gravimetrici) e il deployment operativo in modalità near-real-time.

**Dichiarazione Importante**: Il framework non è un sistema predittivo deterministico, ma uno strumento di monitoraggio statistico per quantificare cambiamenti temporali nei pattern di sismicità. Non vengono fatte affermazioni di forecasting eruttivo deterministico.

---

## Referenze

- Aki, K. (1965). Maximum likelihood estimate of b in the formula log N = a - bM and its confidence limits. *Bulletin of the Earthquake Research Institute*, 43, 237-239.
- Ogata, Y. (1988). Statistical models for earthquake occurrences and residual analysis for point processes. *Journal of the American Statistical Association*, 83(401), 9-27.
- Marzocchi, W., & Bebbington, M. S. (2012). Probabilistic eruption forecasting at short and long time scales. *Bulletin of Volcanology*, 74(8), 1777-1805.

---

## Licenza

MIT License – vedere file `LICENSE`.

---

## Contatti

Per domande o collaborazioni:
- GitHub: https://github.com/pietroscik/flegrei-alert-2026
- Email: pietroscik@gmail.com

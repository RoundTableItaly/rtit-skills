# Generare il Word e il PDF del bollettino (Fase 7)

Parti sempre dalla nota markdown approvata (formato in [formato-nota.md](formato-nota.md)), salvata in `<cartella evento>/Bollettini/`.

## Con terminale

Modello generico con intestazione dal profilo, oppure il modello della tavola indicato in `bollettino.template`.

```bash
rtit bollettino --md "<cartella evento>/Bollettini/AAAA-MM-GG Bollettino N.X Titolo.md"   # DOCX + PDF accanto alla nota
rtit bollettino --md "…" --out-dir "<cartella di prova fuori dall'archivio>"              # anteprima, non tocca l'archivio
rtit bollettino --json-contesto contesto.json --out-dir "<cartella di prova>"              # dal contesto JSON invece della nota
```

- Di default DOCX e PDF nascono **accanto alla nota**, nella cartella `Bollettini/` dell'evento. Nessuna copia altrove: l'indice dell'anno elenca i bollettini.
- `--out-dir` serve **solo per le anteprime**: scegli una cartella fuori dall'archivio (es. `anteprima/` sul PC). I file di prova non vanno in `Bollettini/`.
- `--archivio <cartella>` indica l'archivio condiviso se è diverso da `archivio.percorso` del profilo.
- Non sovrascrive mai i file esistenti senza `--force`: usalo **solo** dopo conferma esplicita dell'utente sui file ufficiali.
- PDF: Word se disponibile, altrimenti LibreOffice; se nessuno dei due, lascia il DOCX e chiedi all'utente di esportare il PDF (`--no-pdf` per saltarlo). **Non dichiarare mai un PDF che non esiste.**

## Senza terminale ma con esecuzione di codice

Per esempio Claude.ai: nello zip della skill c'è `assets/generico.docx`, lo stesso modello con i segnaposto `{{ … }}` descritti in [formato-nota.md](formato-nota.md).

- Se `docxtpl` è disponibile (`pip install docxtpl`), compila il modello con il contesto raccolto.
- Altrimenti sostituisci i segnaposto con `python-docx`.
- Consegna il file all'utente e ricordagli di salvarlo in `<cartella evento>/Bollettini/`.

## Solo chat

Se l'ambiente sa creare documenti Word, crea il DOCX con la stessa struttura:

- colonna sinistra con l'intestazione (sito, ritrovi, sede, Consiglio Direttivo, charter, tavola madrina);
- a destra luogo e data, "Bollettino N. X anno AAAA/AAAA", riquadri dei destinatari;
- invito, "PRENOTARSI ENTRO E NON OLTRE", firme.

Altrimenti consegna il testo formattato da incollare nel modello di Tabler World o di Word.

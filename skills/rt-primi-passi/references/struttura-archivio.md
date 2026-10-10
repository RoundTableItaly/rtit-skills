# Struttura dell'archivio condiviso

## Indice

- [Albero completo](#albero-completo)
- [Cosa va in ogni cartella](#cosa-va-in-ogni-cartella)
- [Form Google](#form-google)
- [Campi del profilo](#campi-del-profilo-archivio)
- [Nomi dei file](#nomi-dei-file)
- [Indice dell'anno](#indice-dellanno)

## Albero completo

```
<Archivio condiviso>/
├── rtit-profilo.yaml · rtit-profilo.decisioni.yaml
├── Documenti legali/              documenti legali generali dell'associazione
│   ├── Statuto e regolamenti/
│   ├── Fiscale e PEC/
│   ├── Banca/
│   └── Loghi e modelli/
└── Anni sociali/
    └── 2026-2027/
        ├── _Indice 2026-2027.md
        ├── Eventi/
        │   └── AAAA-MM-GG Nome evento/
        │       ├── AAAA-MM-GG Nome evento.md · progetto.md · invitati.md · spese.md
        │       ├── Bollettini/        nota .md + DOCX + PDF del bollettino
        │       ├── Form/              moduli Google (link o export delle risposte)
        │       └── Altri documenti/   ricevute, foto, preventivi…
        ├── Direttivo/                 convocazioni e verbali
        ├── Tesoreria/                 bilanci, quote, rendiconti
        └── Comunicazione/             piano social, materiali P.R.O.
```

`rtit archivio struttura --applica` crea `Documenti legali/` con le sottocartelle (se mancano) e le cartelle dell'anno con l'indice; `rtit evento nuovo --applica` crea la cartella dell'evento con `Bollettini/`, `Form/` e `Altri documenti/`. Nessuno dei due sovrascrive file esistenti.

## Cosa va in ogni cartella

| Cartella | Contenuto | Esempi |
| --- | --- | --- |
| **Radice** | Profilo e decisioni salvate, usati da tutte le skill | `rtit-profilo.yaml`, `rtit-profilo.decisioni.yaml` |
| **Documenti legali/** | Documenti che valgono per più anni sociali | — |
| ├ Statuto e regolamenti | Statuto, regolamenti nazionali e di tavola, atto di charter | Statuto in vigore, Regolamento furti |
| ├ Fiscale e PEC | Codice fiscale, Modelli AA5 inviati, credenziali e istruzioni PEC (senza password in chiaro) | `2026-06-20 Modello AA5.pdf` |
| ├ Banca | Contratto del conto, variazioni di intestatario, verbali di elezione consegnati in banca | `2026-06-25 Variazione intestatario.pdf` |
| └ Loghi e modelli | Logo e stemma della tavola, modello Word del bollettino, carta intestata | `bollettino-tavola.docx` |
| **Anni sociali/AAAA-AAAA/** | Tutto ciò che riguarda un solo anno sociale | — |
| ├ `_Indice AAAA-AAAA.md` | Indice dell'anno (vedi sotto) | — |
| ├ Eventi/ | Una cartella per evento | `2027-10-09 Cena d'autunno/` |
| ├ Direttivo/ | Convocazioni e verbali delle sedute del direttivo e delle assemblee di tavola | `2026-09-15 Direttivo N.2.md` |
| ├ Tesoreria/ | Bilancio preventivo e consuntivo, quote dei soci, quote nazionali e di zona, rendiconti dei service | `Bilancio preventivo 2026-2027.xlsx` |
| └ Comunicazione/ | Piano social, materiali del P.R.O. (responsabile comunicazione), comunicati stampa | `Piano social 2026-2027.md` |

### Cartella evento

| Elemento | Contenuto |
| --- | --- |
| `AAAA-MM-GG Nome evento.md` | Nota evento (`tipo: evento`) |
| `progetto.md` · `invitati.md` · `spese.md` | Pack (solo eventi conviviali; formato nella skill `rt-evento`) |
| `Bollettini/` | Nota del bollettino (`.md`) con DOCX e PDF generati accanto. È l'unica copia: il bollettino non si copia altrove, lo elenca l'indice dell'anno |
| `Form/` | Moduli Google dell'evento (vedi sotto) |
| `Altri documenti/` | Ricevute, preventivi, contratti con il locale, foto, locandine |

- Eventi "solo bollettino": nota con `pack: none`, niente pack; le cartelle `Bollettini/`, `Form/`, `Altri documenti/` restano.
- Ritrovi e sedute del direttivo: **niente** cartella evento. Convocazioni e verbali vanno in `Direttivo/`.
- Anteprime di prova (`rtit bollettino --out-dir …`): fuori dall'archivio, non in `Bollettini/`.

## Form Google

Per iscrizioni, sondaggi o raccolta di preferenze dell'evento:

1. **Durante l'evento**: salva in `Form/` una nota con il **link al modulo** (e al foglio delle risposte), per esempio `Form/Iscrizioni.md`. Il modulo resta di proprietà dell'account della tavola, non di una persona.
2. **A evento chiuso**: chiudi il modulo alle risposte ed esporta le risposte (CSV o XLSX) in `Form/`, per esempio `Form/2027-10-10 Iscrizioni - risposte.csv`.
3. **Privacy**: le risposte contengono dati personali. Restano accessibili **solo al direttivo**: niente link pubblici al foglio delle risposte, niente inoltro a terzi; cancella i dati non più necessari (per esempio le intolleranze alimentari) dopo l'evento.

## Campi del profilo (`archivio.*`)

| Campo | Default | Contenuto |
| --- | --- | --- |
| `percorso` | — | Cartella dell'archivio (sincronizzata dal cloud). Relativo al profilo: `"."` se il profilo sta nella radice |
| `servizio` | `cartella` | `google-drive` · `onedrive` · `sharepoint` · `dropbox` · `nextcloud` · `cartella` (informativo) |
| `link` | `markdown` | `markdown` (link relativi) o `wikilink` (Obsidian) |
| `documenti_legali` | `Documenti legali` | Cartella dei documenti legali |
| `cartelle_legali` | `["Statuto e regolamenti", "Fiscale e PEC", "Banca", "Loghi e modelli"]` | Sottocartelle dei documenti legali |
| `anni` | `Anni sociali/{anno}` | Cartella dell'anno sociale |
| `eventi` | `Anni sociali/{anno}/Eventi` | Cartelle evento `AAAA-MM-GG Nome/` |
| `cartelle_evento` | `["Bollettini", "Form", "Altri documenti"]` | Sottocartelle create in ogni evento |
| `direttivo` | `Anni sociali/{anno}/Direttivo` | Convocazioni e verbali |
| `tesoreria` | `Anni sociali/{anno}/Tesoreria` | Bilanci, quote, rendiconti |
| `comunicazione` | `Anni sociali/{anno}/Comunicazione` | Piano social, materiali P.R.O. |
| `indice_anno` | `Anni sociali/{anno}/_Indice {anno}.md` | Nota indice dell'anno |

`{anno}` = anno sociale `AAAA-AAAA`. Se la tavola usa già nomi di cartella diversi, li indica in questi campi e le skill li usano così come sono.

## Nomi dei file

- Data ISO all'inizio: `AAAA-MM-GG Titolo breve`.
- Lo stesso evento ha **un solo** nome. Se il titolo cambia (calendario, Tabler World), si rinomina la cartella e non se ne crea un'altra.
- Bollettini: `AAAA-MM-GG Bollettino N.X Titolo breve` (data di emissione), in `<evento>/Bollettini/`.
- Verbali: `AAAA-MM-GG Direttivo N.X`; convocazioni: `AAAA-MM-GG Convocazione Direttivo N.X`.

## Indice dell'anno

`_Indice AAAA-AAAA.md` elenca eventi, **bollettini** (con il link alla nota nella cartella `Bollettini/` di ogni evento), verbali, decisioni e note per il passaggio di consegne. Le skill propongono di aggiornarlo quando creano qualcosa. A fine anno è la base della relazione morale e del passaggio al nuovo direttivo.

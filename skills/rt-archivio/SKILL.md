---
name: rt-archivio
description: >-
  Imposta e tiene in ordine l'archivio condiviso della tavola, della zona o del nazionale su qualsiasi cloud
  (Google Drive, OneDrive, SharePoint, Dropbox…): documenti legali, cartelle per anno sociale, eventi con
  bollettini, form e altri documenti, direttivo, tesoreria e comunicazione, senza doppioni. Usala per "dove
  salviamo i documenti?", "organizza la cartella della tavola", "crea la cartella dell'evento", "ci sono
  doppioni?", "prepara le cartelle dell'anno nuovo", "dai l'accesso al nuovo direttivo".
---

# Archivio condiviso

**Tutto il lavoro della tavola sta in un archivio condiviso**, con il profilo (`rtit-profilo.yaml`) nella radice. Così il direttivo lavora sugli stessi file, quello dell'anno dopo trova tutto al suo posto e nulla resta solo in una chat o sul PC di una persona.

Se l'utente produce in chat un documento (pack, bollettino, verbale), **proponi sempre di salvarlo nell'archivio**, nella cartella giusta. Convocazioni e verbali si scrivono con la skill `rt-direttivo`.

## 1. Dove sta l'archivio

Va bene qualsiasi cloud che il direttivo usa già (Google Drive anche condiviso, OneDrive/SharePoint anche con la mail di tavola `@roundtable.it`, Dropbox, Nextcloud…): chiedi quale, non imporlo. L'assistente lo vede come cartella sincronizzata sul PC (`archivio.percorso`; `"."` se il profilo sta nella radice) oppure tramite un connettore. Senza cloud, una cartella sul PC da spostare appena possibile.

**Accessi**: meglio un account o un drive **della tavola** che il drive personale del presidente di turno. Accesso al direttivo e a chi ne ha bisogno; a ogni cambio di direttivo aggiungi i nuovi membri e togli chi esce.

## 2. Struttura

```
<Archivio condiviso>/
├── rtit-profilo.yaml · rtit-profilo.decisioni.yaml
├── Documenti legali/      Statuto e regolamenti · Fiscale e PEC · Banca · Loghi e modelli
└── Anni sociali/2026-2027/
    ├── _Indice 2026-2027.md
    ├── Eventi/AAAA-MM-GG Nome evento/   nota, pack, Bollettini/, Form/, Altri documenti/
    ├── Direttivo/                        convocazioni e verbali
    ├── Tesoreria/                        bilanci, quote, rendiconti
    └── Comunicazione/                    piano social, materiali P.R.O.
```

Cosa va in ogni cartella, campi del profilo e regole sui nomi: [references/struttura-archivio.md](references/struttura-archivio.md). L'anno sociale (`AAAA-AAAA`) inizia la domenica dopo l'AGM (definizione completa nella skill `rt-conoscenza`).

Se la tavola ha già cartelle sue, **non riorganizzarle senza un sì esplicito**: indica i suoi percorsi nei campi `archivio.*` del profilo.

## 3. Comandi (con terminale)

```bash
rtit archivio struttura                           # anteprima: Documenti legali + cartelle dell'anno in corso
rtit archivio struttura --applica                 # le crea, con l'indice dell'anno (non sovrascrive)
rtit archivio struttura --anno 2027-2028 --applica   # prepara l'anno nuovo (prima dell'AGM)
rtit archivio verifica                            # cartelle evento con la stessa data: possibili doppioni
rtit evento nuovo --data 2027-10-09 --titolo "Cena d'autunno" --applica   # cartella evento + Bollettini, Form, Altri documenti
```

Senza terminale ma con un connettore (Drive, Microsoft 365, Dropbox): applica le stesse regole e crea cartelle e file tramite il connettore, sempre dopo conferma. Nello zip della skill il modello dell'indice è in `assets/indice-anno.md`.

## 4. Regole

- **Conferma prima di scrivere**: crea, sposta, rinomina o sovrascrivi solo dopo un sì esplicito. Non cancellare mai senza richiesta.
- **Niente doppioni**: prima di creare la cartella di un evento cerca cartelle con la **stessa data** o un nome simile e chiedi se è lo stesso evento (`rtit evento nuovo` si ferma da solo con `blocked_similar`; `--force` solo dopo risposta). Un file sta in un solo posto: niente copie.
- **Nomi**: data ISO all'inizio (`AAAA-MM-GG …`), così si ordinano da soli.
- **Verbali chiusi immutabili**: i verbali di sedute già approvate non si modificano; correzioni e follow-up vanno nel verbale della seduta corrente (vedi la skill `rt-direttivo`).
- **Dati personali**: l'archivio contiene nomi, telefoni, pagamenti, risposte ai form e a volte intolleranze alimentari (dati sanitari). Accesso solo al direttivo; cancella le intolleranze dopo l'evento; non incollare questi dati in chat se non serve.
- **File Google nativi** (`.gdoc`, `.gsheet`): dal disco sono solo collegamenti; leggili con il connettore Drive.

## 5. Cambio d'anno

Prima dell'AGM: crea la struttura dell'anno nuovo e completa l'indice dell'anno che si chiude (eventi, bollettini, decisioni, cose in sospeso). Dalla domenica dopo l'AGM (il passaggio di consegne va fatto entro 30 giorni dall'AGM: Statuto, art. 78) aggiorna il profilo con il nuovo direttivo (`rt-primi-passi`) e rivedi gli accessi. Per il passaggio di consegne vedi la skill `rt-presidente` (file `references/passaggio-consegne.md`).

## Collegate

- `rt-evento` — contenuto della cartella evento (nota e pack).
- `rt-bollettino` — bollettini nella cartella `Bollettini/` dell'evento.
- `rt-direttivo` — convocazioni e verbali in `Direttivo/`.
- `rt-presidente` — passaggio di consegne e tesoreria.
- `rt-comunicazione` — materiali del P.R.O. (responsabile comunicazione) in `Comunicazione/`.
- `rt-primi-passi` — percorso dell'archivio nel profilo.
- `rt-cosa-fare` — controllo periodico dei doppioni e di ciò che manca.

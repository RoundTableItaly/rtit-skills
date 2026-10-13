---
name: rt-primi-passi
description: >-
  Configura l'assistente per chi fa parte di un direttivo Round Table Italia (tavola, zona o nazionale):
  un'intervista breve crea il profilo (tavola o zona, ruolo, direttivo e firme, calendario, archivio) che
  usano tutte le skill rt-*, e imposta e tiene in ordine l'archivio condiviso su qualsiasi cloud (Google
  Drive, OneDrive, SharePoint, Dropbox…): documenti legali, cartelle per anno sociale, eventi, direttivo,
  tesoreria e comunicazione, senza doppioni, accessi al direttivo, cartelle dell'anno nuovo. Usala per
  "come inizio?", "configura la mia tavola", "è cambiato il direttivo, aggiorna il profilo", "dove
  salviamo i documenti?", "organizza la cartella della tavola", "ci sono doppioni?", "prepara le cartelle
  dell'anno nuovo", "dai l'accesso al nuovo direttivo", o quando un'altra skill non trova il profilo. Per
  gli adempimenti del nuovo Presidente usa rt-presidente.
---

# Primi passi — profilo e archivio condiviso

Obiettivo: in 10 minuti costruire il **profilo** che rende utili tutte le altre skill `rt-*` e mettere il lavoro della tavola in un **archivio condiviso**, senza dare per scontato cosa usa l'utente. Lingua **italiana**, tono semplice, una o due domande alla volta, niente gergo. Nulla si scrive senza un sì esplicito.

## Quale file leggere

| Per… | Leggi |
| --- | --- |
| Installare `uv` e la CLI `rtit` | [references/installazione.md](references/installazione.md) |
| Profilo come blocco di testo (Claude.ai, Gemini, ChatGPT) | [references/profilo-testo.md](references/profilo-testo.md) |
| Profilo `rtit-profilo.yaml` (tutti i campi) | [references/profilo-yaml.md](references/profilo-yaml.md) |
| Archivio: cosa va in ogni cartella, campi `archivio.*`, regole sui nomi | [references/struttura-archivio.md](references/struttura-archivio.md) |

## 1. Capire l'ambiente (verifica da solo, poi conferma in una frase)

C'è un terminale (Claude Code, Codex, Antigravity CLI…)? C'è `uv` (`uv --version`; se manca, [references/installazione.md](references/installazione.md))? Ci sono connettori (Calendar, Drive, Microsoft 365, Dropbox)? Puoi creare file o solo testo?

- **A — Solo chat** (Claude.ai, Gemini, ChatGPT, app mobile): il profilo è un **blocco di testo** da incollare nelle istruzioni del Progetto / Gem / GPT ([references/profilo-testo.md](references/profilo-testo.md)).
- **B — Con terminale**: il profilo è il file `rtit-profilo.yaml` ([references/profilo-yaml.md](references/profilo-yaml.md); esempio con `rtit profilo nuovo` o in `assets/profilo-esempio.yaml` nello zip), letto dalla CLI `rtit`.

## 2. Intervista (in quest'ordine; salta ciò che l'utente non sa o non usa)

1. **Livello e ruolo**: tavola, zona o nazionale? Che ruolo hai (Presidente, Vice Presidente, Past President, Tesoriere, Corrispondente, Consigliere, Segretario, P.R.O. (responsabile comunicazione), socio)?
2. **Identità**: nome completo ("Round Table N.99 Esempio"), sigla ("RT 99 Esempio"), città, zona ("Zona N").
3. **App RTIT** (facoltativo): trova la tavola con `list_organization_units(query="<nome o numero>")` (server MCP) o `rtit app-rtit unita --cerca "<nome>"`; conferma e salva `organization_unit_id`, `organization_unit_slug` (identificativo testuale, es. `rt-99-esempio`), `area_slug`.
4. **Direttivo dell'anno sociale**: ruoli e nomi. Le cariche dello Statuto (art. 49) sono Presidente, Vice Presidente, Past President, Consiglieri, Corrispondente e Tesoriere, più il Segretario, nominato dal Presidente e senza voto; aggiungi gli incarichi che la tavola usa (P.R.O., Gestore Materiali…); **telefono solo per chi firma i bollettini** (Presidente e Segretario), spiegando perché.
5. **Intestazione del bollettino** (facoltativa): sito, ritrovi (es. "1° e 3° mercoledì del mese"), sede, charter, tavola madrina, loghi. Meglio estrarli da un bollettino recente e farli confermare.
6. **Calendario** (facoltativo): indirizzo iCal del Google Calendar della tavola (Impostazioni → «Integra calendario»).
7. **Archivio condiviso** (sezione 5):
   1. Avete già una cartella condivisa dal direttivo? Se no, **proponi di crearla**.
   2. Su quale servizio (Google Drive, OneDrive/SharePoint, Dropbox…)? Meglio un account della tavola.
   3. È sincronizzata sul PC (→ `archivio.percorso`) o la raggiungo con un connettore?
   4. Ha già una struttura di cartelle? Se sì, indicala nei campi `archivio.*`; se no, proponi quella standard, con `rtit archivio struttura --applica` dopo conferma.
   5. Chi ha accesso? Solo il direttivo: il profilo e i documenti contengono dati personali.

**Controllo**: mostra il profilo completo (YAML o testo) e chiedi conferma esplicita **prima** di scriverlo.

## 3. Scrivere il profilo

- Percorso B: `rtit profilo nuovo rtit-profilo.yaml`, compila e verifica con `rtit profilo verifica` (✅ attivo, ➖ da configurare). Salvalo nella **radice dell'archivio condiviso** (`archivio.percorso: "."`), **mai** in un repository pubblico; imposta `RTIT_PROFILO` con quel percorso.
- Percorso A: genera il blocco di testo e spiega dove incollarlo (istruzioni del Progetto, del Gem o del GPT).

## 4. Chiudere con un "giro di prova"

Proponi 2–3 cose concrete in base al ruolo e al periodo dell'anno sociale (inizia il giorno dopo l'AGM, di solito la domenica dopo il primo sabato di giugno: vedi `rt-conoscenza`). Fonte degli adempimenti: `rt-presidente`; in caso di differenze vale quella.

- Dalla domenica dopo l'AGM (giugno), nuovo direttivo → `rt-presidente` (insediamento, quote, calendario).
- Prima dell'AGM, direttivo uscente → passaggio di consegne, compreso l'aggiornamento del profilo con il nuovo direttivo (vedi la skill `rt-presidente`, file `references/passaggio-consegne.md`) e cartelle dell'anno nuovo (sezione 5).
- Chiunque → `rt-cosa-fare` ("cosa c'è da fare questa settimana?").
- Prossimo evento → `rt-evento`.

## 5. Archivio condiviso

**Tutto il lavoro della tavola sta in un archivio condiviso**, con il profilo nella radice: il direttivo lavora sugli stessi file, quello dell'anno dopo trova tutto al suo posto e nulla resta solo in una chat o sul PC di una persona. Se l'utente produce in chat un documento (pack, bollettino, verbale), **proponi sempre di salvarlo nell'archivio**, nella cartella giusta.

Va bene qualsiasi cloud che il direttivo usa già (Google Drive anche condiviso, OneDrive/SharePoint anche con la mail di tavola `@roundtable.it`, Dropbox, Nextcloud…): chiedi quale, non imporlo. L'assistente lo vede come cartella sincronizzata sul PC (`archivio.percorso`; `"."` se il profilo sta nella radice) oppure tramite un connettore. Senza cloud, una cartella sul PC da spostare appena possibile. **Accessi**: meglio un account o un drive **della tavola** che il drive personale del presidente di turno; a ogni cambio di direttivo aggiungi i nuovi membri e togli chi esce.

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

Cosa va in ogni cartella, campi del profilo e regole sui nomi: [references/struttura-archivio.md](references/struttura-archivio.md). Se la tavola ha già cartelle sue, **non riorganizzarle senza un sì esplicito**: indica i suoi percorsi nei campi `archivio.*`.

```bash
rtit archivio struttura                           # anteprima: Documenti legali + cartelle dell'anno in corso
rtit archivio struttura --applica                 # le crea, con l'indice dell'anno (non sovrascrive)
rtit archivio struttura --anno 2027-2028 --applica   # prepara l'anno nuovo (prima dell'AGM)
rtit archivio verifica                            # cartelle evento con la stessa data: possibili doppioni
rtit evento nuovo --data 2027-10-09 --titolo "Cena d'autunno" --applica   # cartella evento + Bollettini, Form, Altri documenti
```

Senza terminale ma con un connettore (Drive, Microsoft 365, Dropbox): applica le stesse regole e crea cartelle e file tramite il connettore, sempre dopo conferma. Nello zip della skill il modello dell'indice è in `assets/indice-anno.md`.

Regole:

- **Conferma prima di scrivere**: crea, sposta, rinomina o sovrascrivi solo dopo un sì esplicito. Non cancellare mai senza richiesta.
- **Niente doppioni**: prima di creare la cartella di un evento cerca cartelle con la **stessa data** o un nome simile e chiedi se è lo stesso evento (`rtit evento nuovo` si ferma da solo con `blocked_similar`; `--force` solo dopo risposta). Un file sta in un solo posto: niente copie.
- **Nomi**: data ISO all'inizio (`AAAA-MM-GG …`), così si ordinano da soli.
- **Verbali chiusi immutabili**: correzioni e seguiti nel verbale della seduta corrente (skill `rt-presidente`, file `references/direttivo.md`).
- **File Google nativi** (`.gdoc`, `.gsheet`): dal disco sono solo collegamenti; leggili con il connettore Drive.

**Cambio d'anno**: prima dell'AGM crea la struttura dell'anno nuovo e completa l'indice dell'anno che si chiude (eventi, bollettini, decisioni, cose in sospeso). Dal giorno dopo l'AGM (passaggio di consegne entro 30 giorni dall'AGM: Statuto, art. 78) aggiorna il profilo con il nuovo direttivo e rivedi gli accessi; checklist nella skill `rt-presidente`, file `references/passaggio-consegne.md`.

## Privacy (dillo una volta, brevemente)

Il profilo contiene nomi e telefoni: accesso solo al direttivo; quando qualcuno esce, togli l'accesso e rigenera l'indirizzo iCal segreto. L'archivio contiene nomi, telefoni, pagamenti, risposte ai form e a volte intolleranze alimentari (dati sanitari): cancella le intolleranze dopo l'evento; elenchi soci e dati di terzi non vanno incollati in chat se non serve.

## Collegate

- `rt-presidente` — adempimenti del nuovo Presidente, passaggio di consegne, verbali in `Direttivo/`, tesoreria.
- `rt-cosa-fare` — primo punto della situazione dopo la configurazione; controllo periodico dei doppioni.
- `rt-evento` — contenuto della cartella evento (nota, pack, `Bollettini/`), calendario della tavola, slug dell'App RTIT.
- `rt-comunicazione` — se l'utente è il P.R.O.; materiali in `Comunicazione/`.
- `rt-conoscenza` — sigle, anno sociale, link ufficiali.

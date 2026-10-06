---
name: rt-primi-passi
description: >-
  Configura l'assistente per chi fa parte di un direttivo Round Table Italia (tavola, zona o nazionale):
  un'intervista breve crea il profilo (tavola o zona, ruolo, direttivo e firme, calendario, archivio
  condiviso) che usano tutte le skill rt-*. Usala per "come inizio?", "configura la mia tavola", "è cambiato
  il direttivo, aggiorna il profilo", o quando un'altra skill non trova il profilo. Per gli adempimenti del
  nuovo Presidente usa rt-presidente.
---

# Primi passi — il profilo della tua tavola, zona o nazionale

Obiettivo: in 10 minuti costruire il **profilo** che rende utili tutte le altre skill `rt-*`, senza dare per scontato cosa usa l'utente. Lingua **italiana**, tono semplice, una o due domande alla volta, niente gergo.

## 1. Capire l'ambiente (verifica da solo, poi conferma in una frase)

C'è un terminale (Claude Code, Codex, Gemini CLI…)? C'è `uv` (`uv --version`; se manca, [references/installazione.md](references/installazione.md))? Ci sono connettori (Calendar, Drive, Microsoft 365, Dropbox)? Puoi creare file o solo testo?

- **A — Solo chat** (Claude.ai, Gemini, ChatGPT, app mobile): il profilo è un **blocco di testo** da incollare nelle istruzioni del Progetto / Gem / GPT ([references/profilo-testo.md](references/profilo-testo.md)).
- **B — Con terminale**: il profilo è il file `rtit-profilo.yaml` ([references/profilo-yaml.md](references/profilo-yaml.md); esempio con `rtit profilo nuovo` o in `assets/profilo-esempio.yaml` nello zip), letto dalla CLI `rtit`.

## 2. Intervista (in quest'ordine; salta ciò che l'utente non sa o non usa)

1. **Livello e ruolo**: tavola, zona o nazionale? Che ruolo hai (Presidente, Vice Presidente, Past President, Tesoriere, Corrispondente, Consigliere, Segretario, P.R.O. (responsabile comunicazione), socio)?
2. **Identità**: nome completo ("Round Table N.99 Esempio"), sigla ("RT 99 Esempio"), città, zona ("Zona N").
3. **App RTIT** (facoltativo): trova la tavola con `list_organization_units(query="<nome o numero>")` (server MCP) o `rtit app-rtit unita --cerca "<nome>"`; conferma e salva `organization_unit_id`, `organization_unit_slug` (identificativo testuale, es. `rt-99-esempio`), `area_slug`.
4. **Direttivo dell'anno sociale**: ruoli e nomi. Le cariche dello Statuto (art. 49) sono Presidente, Vice Presidente, Past President, Consiglieri, Corrispondente e Tesoriere, più il Segretario, nominato dal Presidente e senza voto; aggiungi gli incarichi che la tavola usa (P.R.O., Gestore Materiali…); **telefono solo per chi firma i bollettini** (Presidente e Segretario), spiegando perché.
5. **Intestazione del bollettino** (facoltativa): sito, ritrovi (es. "1° e 3° mercoledì del mese"), sede, charter, tavola madrina, loghi. Meglio estrarli da un bollettino recente e farli confermare.
6. **Calendario** (facoltativo): indirizzo iCal del Google Calendar della tavola (Impostazioni → «Integra calendario»).
7. **Archivio condiviso** (dettagli nella skill `rt-archivio`):
   1. Avete già una cartella condivisa dal direttivo? Se no, **proponi di crearla**.
   2. Su quale servizio (Google Drive, OneDrive/SharePoint, Dropbox…)? Meglio un account della tavola.
   3. È sincronizzata sul PC (→ `archivio.percorso`) o la raggiungo con un connettore?
   4. Ha già una struttura di cartelle? Se sì, indicala nei campi `archivio.*`; se no, proponi quella standard (`Documenti legali/` + `Anni sociali/AAAA-AAAA/`, con `rtit archivio struttura --applica` dopo conferma).
   5. Chi ha accesso? Solo il direttivo: il profilo e i documenti contengono dati personali.

**Controllo**: mostra il profilo completo (YAML o testo) e chiedi conferma esplicita **prima** di scriverlo.

## 3. Scrivere il profilo

- Percorso B: `rtit profilo nuovo rtit-profilo.yaml`, compila e verifica con `rtit profilo verifica` (✅ attivo, ➖ da configurare). Salvalo nella **radice dell'archivio condiviso** (`archivio.percorso: "."`), **mai** in un repository pubblico; imposta `RTIT_PROFILO` con quel percorso.
- Percorso A: genera il blocco di testo e spiega dove incollarlo (istruzioni del Progetto, del Gem o del GPT).

## 4. Chiudere con un "giro di prova"

Proponi 2–3 cose concrete in base al ruolo e al periodo dell'anno sociale (inizia la domenica dopo l'AGM, di solito a giugno: vedi `rt-conoscenza`). Fonte degli adempimenti: `rt-presidente`; in caso di differenze vale quella.

- Dalla domenica dopo l'AGM (giugno), nuovo direttivo → `rt-presidente` (insediamento, quote, calendario).
- Prima dell'AGM, direttivo uscente → passaggio di consegne, compreso l'aggiornamento del profilo con il nuovo direttivo (vedi la skill `rt-presidente`, file `references/passaggio-consegne.md`) e cartelle dell'anno nuovo (`rt-archivio`).
- Chiunque → `rt-cosa-fare` ("cosa c'è da fare questa settimana?").
- Prossimo evento → `rt-evento` + `rt-bollettino`.

## Privacy (dillo una volta, brevemente)

Il profilo contiene nomi e telefoni: accesso solo al direttivo; quando qualcuno esce, togli l'accesso e rigenera l'indirizzo iCal segreto. Elenchi soci, intolleranze alimentari (dati sanitari) e dati di terzi non vanno incollati in chat se non serve.

## Collegate

- `rt-presidente` — adempimenti del nuovo Presidente e passaggio di consegne.
- `rt-archivio` — creare e organizzare l'archivio condiviso.
- `rt-cosa-fare` — primo punto della situazione dopo la configurazione.
- `rt-conoscenza` — sigle, anno sociale, link ufficiali.
- `rt-calendario` — calendario della tavola e scelta delle date.
- `rt-comunicazione` — se l'utente è il P.R.O. (responsabile comunicazione).

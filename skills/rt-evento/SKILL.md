---
name: rt-evento
description: >-
  Organizza gli eventi di tavola, zona o nazionale dalla data al saldo: scelta e verifica della data con il
  Planner dell'App RTIT (punteggio N/100, date alternative) e con il calendario Google della tavola; nota
  evento e pack (progetto, invitati, spese) nell'archivio condiviso; bollettino ufficiale con intervista
  guidata e Word/PDF dal modello; dati pubblici dell'App RTIT (eventi di altre tavole, zone e nazionale,
  email istituzionali, statistiche per anno sociale). Usala per "organizziamo una cena", "va bene il 23
  ottobre?", "quale sabato è libero?", "ci sono sovrapposizioni?", "cosa c'è di nuovo nel calendario?",
  "chi ha confermato?", "quanto spendiamo?", "bollettino N.", "prepara il Word per la cena", "che eventi
  ci sono in zona?", "qual è la mail della tavola X?", "quanti eventi abbiamo fatto quest'anno?". Per
  post e foto usa rt-comunicazione.
---

# Evento — data, progetto, bollettino, App RTIT

Lingua: **italiano**. **Non inventare** date, punteggi, importi, conferme, eventi o indirizzi email: riporta solo ciò che dicono l'utente, l'archivio, il calendario o l'App RTIT; se un dato manca, chiedilo o lascia la cella vuota. **Conferma prima di scrivere**: mostra cartella, file o testo e chiedi un sì esplicito prima di ogni comando con `--applica` o `--force`. Tutto si salva nell'archivio condiviso, nella cartella dell'evento (struttura nella skill `rt-primi-passi`, file `references/struttura-archivio.md`). Gli eventi si caricano su **Tabler World** a mano, dal portale: tu prepari dati e testi.

## Quale file leggere

| Per… | Leggi |
| --- | --- |
| Scegliere o verificare una data, leggere il calendario della tavola, tipi di evento | [references/date-e-calendario.md](references/date-e-calendario.md); indirizzo iCal e abbinamento con l'archivio: [references/calendario.md](references/calendario.md); CLI del Planner: [references/app-rtit-cli.md](references/app-rtit-cli.md) |
| Nota evento e pack (progetto, invitati, spese) | [references/pack.md](references/pack.md) |
| Bollettino: intervista in 7 fasi, riepilogo, dopo | [references/bollettino.md](references/bollettino.md); formato della nota: [references/formato-nota.md](references/formato-nota.md); esempi: [references/esempi.md](references/esempi.md); Word e PDF: [references/generazione-word.md](references/generazione-word.md) |
| Strumenti MCP dell'App RTIT (parametri, campi, come aggiungere il connettore) | [references/strumenti-mcp.md](references/strumenti-mcp.md) |

## Ordine consigliato (dal Manuale del Presidente)

1. **Data** senza sovrapposizioni (punteggio Planner `N/100`).
2. **Nota evento + pack**.
3. **Tabler World**: l'evento va caricato lì, dal portale, prima di pubblicizzarlo; salva `tablerworld_id` nella nota evento.
4. **Bollettino** ufficiale.
5. **Social e foto** → skill `rt-comunicazione`. Evento aperto agli **aspiranti**? Scaletta della serata in `rt-comunicazione`, file `references/regole-crescita.md` (§B3).
6. Dopo l'evento: saldo spese, incassi, ricevute e foto in `Altri documenti/`, appunti per la relazione morale.

## 1. Data

Due fonti, entrambe **in sola lettura**: il **Planner dell'App RTIT** (https://app.roundtable.it/planner), che dà il punteggio di sovrapposizione di una data rispetto agli eventi pubblici delle altre tavole, della zona e del nazionale; e il **calendario della tavola** (Google Calendar, iCal), che dice cosa è in programma e cosa manca ancora nell'archivio.

- **Con il server MCP**: `check_date_conflicts(date, organization_unit=<slug>)` per una data, `scan_conflicts(start_date, end_date)` per un periodo (max 366 giorni). **Con terminale**: `rtit app-rtit data 2027-10-23`, `rtit app-rtit planner --mesi 3`. **Senza nessuno dei due**: apri o fai aprire il Planner e fatti riportare il punteggio.
- Mostra sempre il punteggio come **`N/100`** (più alto = meno sovrapposizioni) e spiega il conflitto principale. Sotto la soglia del profilo (`app_rtit.soglia_punteggio`, default 90) o con un conflitto `danger`, proponi 2–3 date alternative **verificate con lo stesso strumento**.
- Il Planner vede solo gli eventi pubblici su Tabler World (`external`, `announcement`): un evento interno non "occupa" la data per gli altri. Per proteggerla va pubblicato come pubblico, dal portale.
- **Calendario della tavola**: `rtit calendario` (classifica `nuovo`, `cambiato`, `in_archivio`, `solo_archivio`), oppure il connettore Google Calendar (prossimi 120 giorni), oppure l'elenco incollato dall'utente. Per ogni evento `nuovo` o `cambiato` fai una domanda a scelta multipla (ignora e salva la decisione con `rtit decisioni ignora-calendario …` · nota evento · bollettino · Tabler World · cartella evento · salta). Tipi di evento dal titolo (`ignora`, `direttivo`, `solo_bollettino`, `sociale`, `altro`): tabella in [references/date-e-calendario.md](references/date-e-calendario.md). **Niente** cartelle evento, pack o bollettini per ritrovi e sedute del direttivo.

## 2. Nota evento e pack

Il **pack** sono tre documenti accanto alla nota evento: `progetto.md` (dati, checklist, cose da fare), `invitati.md` (conferme e quote), `spese.md` (preventivo e saldo). Formato e regole: [references/pack.md](references/pack.md); nello zip della skill i modelli completi sono in `assets/`.

- **Solo chat**: crea le tre tabelle in chat e aggiornale a ogni messaggio ("Mario conferma, paga con Satispay"). Calcola tu confermati, in attesa, quote attese e incassate, spese con margine, saldo. Alla fine proponi di salvarle nell'archivio.
- **Archivio condiviso (CLI)**:

```bash
rtit evento nuovo --data 2027-10-09 --titolo "Cena d'autunno"            # anteprima (non scrive)
rtit evento nuovo --data 2027-10-09 --titolo "Cena d'autunno" --applica  # cartella + nota evento + Bollettini, Form, Altri documenti
rtit evento pack "<cartella evento>"          # crea progetto/invitati/spese (non sovrascrive mai)
rtit evento verifica "<cartella evento>"      # conformità + cose da fare aperte
rtit evento spese "<cartella evento>"         # conti: confermati, spesa, margine, incasso, saldo
```

- Le cartelle seguono `archivio.eventi` del profilo (es. `Anni sociali/2027-2028/Eventi/2027-10-09 Cena d'autunno/`). Se `rtit evento nuovo` si ferma con `blocked_similar`, esiste già una cartella con la stessa data o un nome simile: chiedi se è lo stesso evento prima di `--force`. `--senza-pack` crea un evento "solo bollettino" (`pack: none`). Dopo ogni modifica al pack ricalcola con `rtit evento spese`. `--force` sul pack sovrascrive: solo su richiesta esplicita.
- Moduli Google per le iscrizioni: link e, a evento chiuso, export delle risposte in `Form/`.

## 3. Bollettino

Regole dal Manuale del Presidente: ogni evento pubblicizzato ha un bollettino; l'evento deve essere già su Tabler World, o almeno pianificato; se la tavola usa il modello ufficiale di Tabler World, qui si raccolgono e controllano i contenuti; logo di tavola presente, rondella non coperta né deformata, logo nazionale solo per eventi nazionali (controllo completo: skill `rt-comunicazione`, file `references/logo.md`).

Segui l'intervista in [references/bollettino.md](references/bollettino.md): `0 Contesto → 1 Metadati → 2 Invito → 3 Firme → 4 Destinatari → 5 Intestazione → Riepilogo approvato → 6 Nota in <evento>/Bollettini/ → 7 Word/PDF`. Firme di Presidente e Segretario sempre da **confermare**: il direttivo cambia ogni anno sociale. Il riepilogo completo, con i file che verranno creati, precede ogni scrittura.

- `rtit bollettino --md "<cartella evento>/Bollettini/<nota>.md"` crea DOCX e PDF accanto alla nota; `--out-dir` solo per anteprime; `--force` solo dopo conferma; non dichiarare mai un PDF che non esiste.
- Nota, DOCX e PDF restano **solo** in `<cartella evento>/Bollettini/`; aggiorna l'indice dell'anno. Allega il PDF all'evento su Tabler World e inoltralo nei canali della tavola. Solo chat: aggiorna il numero dell'ultimo bollettino nel profilo testuale.

## 4. App RTIT: eventi degli altri, schede, statistiche

Dati **pubblici e in sola lettura**: eventi, unità organizzative (nazione → zone → tavole), statistiche. Nessun dato dei soci. Ogni evento e unità ha un campo `url`: **citalo sempre**.

Accesso, in ordine: **server MCP "App Round Table Italia"** (in Codex `round-table-italia`); **CLI** `rtit app-rtit …` (solo eventi e date); **sito** https://app.roundtable.it. Se manca l'MCP, suggerisci il connettore `https://app.roundtable.it/mcp/` (senza autenticazione; guida https://app.roundtable.it/ai-agents; istruzioni per client in [references/strumenti-mcp.md](references/strumenti-mcp.md)).

| Domanda dell'utente | Strumento |
| --- | --- |
| "Che eventi ci sono (in zona / in quella tavola / questo mese)?" | `search_events` (`organization_unit`, `zone`, `start_date`/`end_date`, `query`) |
| "Raccontami l'evento X" | `get_event` (slug da `search_events`) |
| "Qual è lo slug / l'email della tavola X?", "Quali tavole ha la zona?" | `list_organization_units` (`query`, `type`, `parent`), `get_organization_unit`, `get_organization_tree` |
| "Quanti eventi abbiamo fatto quest'anno?" | `get_organization_unit_statistics` (`slug`, `year`) |
| "Come va l'associazione? Tavole senza eventi?" | `get_statistics` (`year`) |
| "Stiamo crescendo rispetto agli anni scorsi?" | `get_statistics_trends` |
| "Quando inizia l'anno sociale?" | `list_statutory_years` |
| "Va bene il 23 ottobre?", "Ci sono sovrapposizioni?" | `check_date_conflicts`, `scan_conflicts` (sezione 1) |

- **Anno sociale**: dal giorno dopo l'AGM al giorno dell'AGM successivo (Statuto, art. 76; AGM tra il 15 maggio e il 30 giugno, art. 9). Si scrive `AAAA-AAAA`; nei parametri si chiama `statutory_year` ("current", "previous", "2026-2027"). Date esatte: `list_statutory_years`, non calcolarle a mano.
- **Solo eventi pubblici**: un evento interno della tavola non compare e le statistiche lo ignorano.
- **Statistiche**: servono alla relazione morale (`rt-presidente`), al programma annuale (`rt-comunicazione`, file `references/regole-crescita.md`) e, per zona e nazionale, a vedere le tavole poco attive: presentale con tatto, sono indicatori, non giudizi.
- Lo **slug** (es. `rt-99-esempio`) sta nel profilo (`app_rtit.organization_unit_slug` / `area_slug`); se manca, `list_organization_units(query=…)` e proponi di salvarlo (`rt-primi-passi`).
- **Elenchi lunghi**: pagina (`page`, `limit`) e riassumi. Massimo **60 richieste al minuto**: niente cicli inutili. I dati dell'App fanno fede, la tua sintesi no: rimanda al link della pagina.

## Dati personali

`invitati.md`, le risposte ai form e i bollettini contengono nomi, telefoni, pagamenti e a volte **intolleranze alimentari** (dati sanitari). Tienili al minimo, non incollarli in un assistente cloud se non serve, cancella le intolleranze dopo l'evento, non inviare elenchi a terzi senza consenso.

## Collegate

- `rt-cosa-fare` — cosa manca per i prossimi eventi, eventi nuovi in calendario, date a rischio.
- `rt-comunicazione` — post, storie e foto dell'evento; controllo di loghi e grafica; serata per gli aspiranti.
- `rt-presidente` — relazione morale e report di zona con le statistiche; calendario dell'anno.
- `rt-primi-passi` — profilo (direttivo, firme, intestazione, slug, iCal) e struttura dell'archivio.
- `rt-conoscenza` — sigle, anno sociale, livelli e link ufficiali.

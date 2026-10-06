---
name: rt-calendario
description: >-
  Sceglie e verifica le date degli eventi della tavola: punteggio di sovrapposizione del Planner dell'App
  RTIT (N/100), date alternative, confronto del calendario Google della tavola con gli eventi in archivio.
  Usala per "va bene il 23 ottobre per la cena?", "quale sabato di novembre è libero?", "ci sono
  sovrapposizioni?", "cosa c'è di nuovo nel nostro calendario?", "importa il calendario". Per eventi di
  altre tavole e statistiche usa rt-app-rtit.
---

# Le nostre date: Planner e calendario della tavola

Questa skill si occupa delle **date della tavola**: scegliere quella giusta e tenere allineati calendario e archivio. Per gli eventi delle altre tavole, le schede delle unità e le statistiche usa `rt-app-rtit`.

Due fonti, entrambe **in sola lettura**:

1. **Planner dell'App RTIT** (https://app.roundtable.it/planner): punteggio di sovrapposizione di una data rispetto agli eventi pubblici delle altre tavole, della zona e del nazionale.
2. **Calendario della tavola** (Google Calendar, iCal pubblico o indirizzo segreto): cosa c'è in programma e cosa manca ancora nell'archivio eventi.

Il Manuale del buon Presidente chiede di controllare, prima di fissare una data, i periodi affollati, il Planner e la pagina di monitoraggio (conviviali vicine). Il Manuale li colloca su "Round Table Events": è il nome precedente, o alternativo, dello stesso servizio che oggi è l'App RTIT (da verificare).

**Non inventare date, punteggi o conflitti.** Riporta solo quello che restituiscono il Planner o il calendario; se non riesci a leggerli, dillo e chiedi all'utente.

## Scegliere una data

- **Con il server MCP dell'App RTIT** (il modo migliore): `check_date_conflicts(date, organization_unit=<slug della tavola>)` per una data, `scan_conflicts(start_date, end_date)` per un periodo (massimo 366 giorni). Parametri e risposte: vedi la skill `rt-app-rtit` (file `references/strumenti-mcp.md`).
- **Con terminale**: `rtit app-rtit data 2027-10-23` → punteggio e conflitti; `rtit app-rtit planner --mesi 3` → giorni sotto soglia o con conflitti `danger`/`warning`. API e campi: [references/app-rtit.md](references/app-rtit.md).
- **Senza terminale né MCP**: se puoi navigare, apri https://app.roundtable.it/planner; altrimenti guida l'utente a farlo e a riportarti il punteggio.

Regole di lettura:

- Mostra sempre il punteggio come **`N/100`** (più alto = meno sovrapposizioni) e spiega il conflitto principale (stessa zona, evento nazionale, distanza).
- Proponi 2–3 date alternative, **verificate con lo stesso strumento**, quando il punteggio è sotto la soglia del profilo (`app_rtit.soglia_punteggio`, default 90) o c'è un conflitto `danger`.
- Il Planner vede solo gli eventi pubblici su Tabler World (`external`, `announcement`): un nostro evento interno non "occupa" la data per le altre tavole. Per proteggerla, va pubblicato come pubblico su Tabler World, dal portale.

## Calendario della tavola

- **Con terminale**: `rtit calendario`. Con l'archivio confronta e classifica: `nuovo`, `cambiato`, `in_archivio`, `solo_archivio`.
- **Con connettore Google Calendar**: leggi gli eventi dei prossimi 120 giorni e applica le stesse regole qui sotto.
- **Solo chat**: chiedi all'utente di incollare l'elenco.

Indirizzo iCal, abbinamento con l'archivio e decisioni salvate: [references/calendario.md](references/calendario.md).

### Regole per tipo di evento (dal titolo, configurabili nel profilo)

| Tipo | Esempi | Cosa fare |
| --- | --- | --- |
| `ignora` | ritrovo, riunione mensile | Niente: nessuna cartella evento né pack |
| `direttivo` | consiglio di tavola, CD | Verbale nella cartella `Direttivo/` dell'anno sociale, se l'utente lo chiede; **mai** cartella evento, pack, bollettino |
| `solo_bollettino` | (configurabile) | Nota evento con `pack: none` + bollettino semplice |
| `sociale` | cena, aperitivo, visita… | Nota evento + pack completo (`rt-evento`) + bollettino + Tabler World |
| `altro` | — | Chiedi all'utente |

Per ogni evento `nuovo` o `cambiato` da gestire, fai una domanda a scelta multipla: ignora (e salva la decisione con `rtit decisioni ignora-calendario …`, così non verrà più proposto) · crea o aggiorna la nota evento · bollettino · Tabler World · crea la cartella evento nell'archivio · salta.

**Mai** creare note, bollettini, eventi su Tabler World o cartelle senza conferma esplicita.

## Collegate

- `rt-app-rtit` — eventi di altre tavole, zone e nazionale, schede delle unità, statistiche.
- `rt-evento` — organizzare l'evento una volta scelta la data.
- `rt-bollettino` — invito ufficiale per un evento del calendario.
- `rt-archivio` — cartella dell'evento nell'archivio condiviso.
- `rt-cosa-fare` — quadro complessivo di eventi e cose mancanti.

---
name: rt-app-rtit
description: >-
  Consulta i dati pubblici dell'App Round Table Italia (app.roundtable.it, server MCP): eventi di altre
  tavole, zone e nazionale, schede delle tavole con email istituzionali, statistiche e andamento degli
  eventi per anno sociale. Usala per "che eventi ci sono in zona?", "qual è la mail della tavola X?",
  "quanti eventi abbiamo fatto quest'anno?", "quali tavole non hanno eventi?". Per scegliere la data di
  un nostro evento usa rt-calendario.
---

# App Round Table Italia: eventi degli altri e statistiche

Dati **pubblici e in sola lettura** dell'App RTIT: eventi, unità organizzative (nazione → zone → tavole) e statistiche. Non contiene dati dei soci. Ogni evento e unità ha un campo `url` alla pagina pubblica: **citalo sempre** nelle risposte.

**Le date dei nostri eventi** (punteggio N/100, sovrapposizioni, date alternative) sono compito di `rt-calendario`: se l'utente chiede "va bene questa data?", segui quella skill.

## Come accedere (in ordine di preferenza)

1. **Server MCP "App Round Table Italia"** (`round-table-italia`), se i suoi strumenti sono disponibili (es. `search_events`).
2. **CLI** `rtit app-rtit …` se c'è un terminale ma non il server MCP: copre solo eventi e date (vedi la skill `rt-calendario`, file `references/app-rtit.md`).
3. **Sito** https://app.roundtable.it se non c'è nessuno dei due: guida l'utente o, se puoi navigare, leggi la pagina.

Se manca l'MCP, suggerisci all'utente di aggiungere il connettore: indirizzo `https://app.roundtable.it/mcp/`, senza autenticazione (guida ufficiale: https://app.roundtable.it/ai-agents; istruzioni per ogni client in [references/strumenti-mcp.md](references/strumenti-mcp.md)).

## Strumenti e quando usarli

| Domanda dell'utente | Strumento |
| --- | --- |
| "Che eventi ci sono (in zona / in quella tavola / questo mese)?" | `search_events` (`organization_unit`, `zone`, `start_date`/`end_date`, `query`) |
| "Raccontami l'evento X" | `get_event` (slug da `search_events`) |
| "Qual è lo slug / l'email della tavola X?", "Quali tavole ha la zona?" | `list_organization_units` (`query`, `type`, `parent`), `get_organization_unit`, `get_organization_tree` |
| "Quanti eventi abbiamo fatto quest'anno?" | `get_organization_unit_statistics` (`slug`, `year`) |
| "Come va l'associazione? Tavole senza eventi?" | `get_statistics` (`year`) |
| "Stiamo crescendo rispetto agli anni scorsi?" | `get_statistics_trends` |
| "Quando inizia l'anno sociale?" | `list_statutory_years` |
| "Va bene il 23 ottobre?", "Ci sono sovrapposizioni?" | → `rt-calendario` (`check_date_conflicts`, `scan_conflicts`) |

Lo **slug** è il nome breve di una tavola o zona usato negli indirizzi web dell'App (es. `rt-99-esempio`). Parametri completi e campi restituiti: [references/strumenti-mcp.md](references/strumenti-mcp.md).

## Regole

- **Anno sociale**: inizia il **giorno dopo l'AGM** e finisce il giorno dell'AGM successivo (Statuto, art. 76). L'AGM si tiene di sabato, quindi l'anno parte la domenica: di solito dopo il primo sabato di giugno, comunque tra il 15 maggio e il 30 giugno (art. 9). Si scrive `AAAA-AAAA`. Le statistiche dell'App seguono l'anno sociale; nei parametri si chiama `statutory_year` ("current", "previous", "2026-2027"). Le date esatte di ogni anno: `list_statutory_years`. Non calcolarle a mano se lo strumento è disponibile.
- **Solo eventi pubblici**: nell'App compaiono solo gli eventi pubblicati come pubblici su Tabler World (tipi `external` e `announcement`). Un evento interno della tavola non c'è: le statistiche lo ignorano e la data non risulta occupata per le altre tavole. Per farlo comparire va pubblicato come pubblico su Tabler World, dal portale.
- **Statistiche**: servono alla relazione morale (`rt-presidente`), al programma annuale (`rt-crescita`) e, per zona e nazionale, a vedere le tavole poco attive. Presentale con tatto: sono indicatori, non giudizi.
- **Profilo**: lo slug della tavola o della zona sta in `app_rtit.organization_unit_slug` / `area_slug`. Se manca, trovalo con `list_organization_units(query=…)` e proponi di salvarlo (`rt-primi-passi`).
- **Elenchi lunghi**: usa la paginazione (`page`, `limit`) e riassumi; non riversare in chat decine di eventi senza richiesta. Il server accetta al massimo **60 richieste al minuto**: niente cicli di chiamate inutili.
- **Non inventare** eventi, numeri o indirizzi email: riporta solo ciò che restituisce l'App. I dati dell'App fanno fede, la tua sintesi no: per le informazioni ufficiali rimanda al link della pagina dell'evento o al calendario eventi del sito.

## Esempi

- *"Che fa la Zona N nel prossimo mese?"* → `search_events(organization_unit="zona-esempio", start_date=oggi, end_date=oggi+30)` → elenco con data, tavola, titolo e link.
- *"Qual è la mail della RT 99 Esempio?"* → `list_organization_units(query="Esempio", type="club")` → `contact_email` e `url` della scheda.
- *"Quanti eventi abbiamo pubblicato quest'anno rispetto all'anno scorso?"* → `get_organization_unit_statistics(slug="rt-99-esempio", year="current")` → eventi dell'anno, differenza con l'anno precedente, giorni mediani di preavviso.

## Collegate

- `rt-calendario` — scegliere e verificare la data di un nostro evento.
- `rt-presidente` — relazione morale e report di zona con le statistiche.
- `rt-crescita` — programma annuale e confronto con gli anni precedenti.
- `rt-conoscenza` — sigle, livelli dell'associazione e link ufficiali.
- `rt-primi-passi` — salvare lo slug della tavola o della zona nel profilo.

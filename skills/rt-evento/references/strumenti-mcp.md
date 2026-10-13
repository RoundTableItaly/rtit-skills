# Server MCP "App Round Table Italia" — riferimento

Server MCP del progetto TW-Events (app.roundtable.it). Dati pubblici, sola lettura, nessun dato dei soci. Organizzazione: nazione → zone (`area`) → tavole (`club`), identificate da **slug**, il nome breve usato negli indirizzi web dell'App (es. `zona-esempio`, `rt-99-esempio`).

Questo file copre il **server MCP**. L'API REST usata dalla CLI `rtit app-rtit` (stessi dati, identificativi numerici) è descritta in [app-rtit-cli.md](app-rtit-cli.md).

## Collegarlo

Guida ufficiale: https://app.roundtable.it/ai-agents

- **Indirizzo del server**: `https://app.roundtable.it/mcp/`
- **Trasporto**: Streamable HTTP. **Autenticazione**: nessuna (niente account né chiavi).

| Client | Come |
| --- | --- |
| **Claude** (web, desktop, mobile) | Impostazioni → sezione connettori → aggiungi un connettore personalizzato → incolla l'indirizzo del server e conferma |
| **ChatGPT** | Impostazioni → sezione connettori (dove disponibile nel tuo piano) → nuovo connettore con server MCP → incolla l'indirizzo; autenticazione: nessuna |
| **Claude Code** | `claude mcp add --transport http "App Round Table Italia" https://app.roundtable.it/mcp/` (il plugin `rtit` lo configura già, in `.mcp.json`, con questo stesso nome) |
| **Antigravity CLI** (`agy`, il vecchio Gemini CLI) | Già configurato nel plugin `rtit` (`mcp_config.json`). A mano: `agy mcp add "App Round Table Italia" https://app.roundtable.it/mcp/` |
| **Altri client** (Cursor, VS Code, …) | Nel file di configurazione MCP del client: `{"mcpServers": {"round-table-italia": {"url": "https://app.roundtable.it/mcp/"}}}` (il nome è libero; se il client non accetta spazi usa questo) |

I nomi dei menu possono cambiare da una versione all'altra delle app.

## Limiti (dalla guida ufficiale)

- Solo dati pubblici: eventi pubblicati, struttura dell'associazione, statistiche. Nessun dato dei soci.
- Sola lettura: un agente non può creare, modificare o cancellare nulla.
- Massimo **60 richieste al minuto** per indirizzo.
- Le risposte dell'assistente possono contenere errori: per le informazioni ufficiali fanno fede le pagine del sito, a partire dal calendario eventi.

## Domande d'esempio (dalla guida ufficiale)

- «Quali eventi Round Table ci sono in Zona 3 nel prossimo mese?»
- «Trovami il prossimo evento nazionale e dimmi dove si tiene.»
- «La mia tavola vuole organizzare una serata il 14 marzo: ci sono eventi concomitanti?»
- «Quante attività ha organizzato ogni zona nell'anno sociale in corso?»

## Strumenti

| Strumento | Parametri | Restituisce |
| --- | --- | --- |
| `search_events` | `query`, `organization_unit` (slug), `include_sub_units` (default sì), `zone` (nome esatto della zona, es. "Zona N"), `table` (nome esatto), `start_date`, `end_date`, `statutory_year` (anno sociale: "current", "previous", "2026-2027"), `page`, `limit` (max 50) | Eventi pubblici; senza date = prossimi da oggi. Campi: `name`, `description` (riassunto), `start_date`, `end_date`, `rt_type`, `location`, `cover_picture`, `canceled`, `organization_name`, `organization_unit_slug`, `organization_area_name`, `slug`, `url` |
| `get_event` | `slug` | Dettaglio completo, descrizione intera |
| `check_date_conflicts` | `date`, `organization_unit` | `score` 0–100 e `conflicts[]`: `name`, `url`, `start_time`, `organizer`, `zone`, `distance`, `impact`, `reason`, `severity` (`danger`/`warning`/…) |
| `scan_conflicts` | `start_date`, `end_date` (massimo 366 giorni; senza date = mese corrente) | Eventi pubblici che si sovrappongono |
| `list_organization_units` | `query`, `type` (`nation`/`area`/`club`), `parent` (slug), `page`, `limit` (max 200) | Unità con `id`, `slug`, `name`, indirizzo, coordinate, `contact_email` istituzionale, `url` |
| `get_organization_unit` | `slug` | Unità con catena dei genitori e figli diretti |
| `get_organization_tree` | — | Albero completo nazione → zone → tavole |
| `get_organization_unit_statistics` | `slug`, `year` (anno sociale, default "current"), `include_sub_units` (default sì) | Totali (futuri, passati, annullati), eventi dell'anno e dell'anno precedente con differenza, punteggio medio di qualità, giorni mediani di preavviso, tavole attive / totali |
| `get_statistics` | `year` (anno sociale, default "current") | Statistiche nazionali: totali, per zona e per mese, tavole più attive, tipi di attività, tavole senza eventi |
| `get_statistics_trends` | `years` (quanti anni sociali recenti; senza valore, tutti) | Totali per anno e per zona |
| `list_statutory_years` | — | Anni sociali con inizio, fine e quale è quello corrente |

## Note

- `organization_unit_id` (numero) serve alla CLI `rtit` (profilo `app_rtit.organization_unit_id`) ed è il campo `id` di `list_organization_units`. Lo slug serve all'MCP.
- Le statistiche seguono l'**anno sociale**, che inizia il giorno dopo l'AGM (Statuto, art. 76: è una domenica, perché l'AGM si tiene di sabato, tra il 15 maggio e il 30 giugno, di solito il primo sabato di giugno). Nei nomi degli strumenti e dei parametri si chiama `statutory_year`. La descrizione del server parla di "primo sabato di giugno": fanno fede le date restituite da `list_statutory_years`.
- Nell'App compaiono solo gli eventi pubblici (`external` e `announcement` su Tabler World).
- `check_date_conflicts` e `scan_conflicts` servono a scegliere le date dei nostri eventi: il flusso è in [date-e-calendario.md](date-e-calendario.md).

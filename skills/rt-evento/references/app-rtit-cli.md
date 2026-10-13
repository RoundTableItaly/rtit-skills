# App RTIT — API REST del Planner e CLI

Fonte: OpenAPI di produzione dell'App Round Table Italia. Questo file copre l'**API REST** usata dalla CLI `rtit app-rtit`. Il **server MCP** (strumenti `check_date_conflicts`, `scan_conflicts`, `search_events`…) è descritto in [strumenti-mcp.md](strumenti-mcp.md): i dati sono gli stessi, cambia solo il modo di chiederli.

| Risorsa | URL |
| --- | --- |
| Schema OpenAPI | https://app.roundtable.it/api/schema/ |
| Swagger UI | https://app.roundtable.it/api/schema/swagger-ui/ |
| ReDoc | https://app.roundtable.it/api/schema/redoc/ |
| Prefisso API JSON | https://app.roundtable.it/api/v1/ |
| Planner (interfaccia web) | https://app.roundtable.it/planner |

## Endpoint usati (tutti pubblici, senza login)

| Scopo | Metodo | Percorso | Parametri | Equivalente MCP |
| --- | --- | --- | --- | --- |
| Prossimi eventi di un'unità (tavola o zona) | GET | `/organization-units/{slug}/activities/` | `time_scope=upcoming`, `scope=subtree\|exact`, `ordering=start_date` | `search_events` |
| Collisioni di un giorno | GET | `/conflict-check/` | `date=AAAA-MM-GG`, `organization_unit_id` (intero) | `check_date_conflicts` |
| Collisioni di un mese (mappa) | GET | `/conflict-check/month/` | `year`, `month`, `organization_unit_id` | `scan_conflicts` (per intervalli) |
| Monitoraggio intervallo | GET | `/monitor/` | `start_date`, `end_date` (facoltativi; default mese corrente) | — |
| Attività nazionali | GET | `/activities/` | `ordering=start_date`, paginazione (niente `time_scope`) | `search_events` |

**Identificativi**: l'API REST vuole l'`organization_unit_id` numerico (nel profilo `app_rtit.organization_unit_id`); l'MCP vuole lo **slug**, cioè il nome breve dell'unità usato negli indirizzi web (es. `rt-99-esempio`). Per trovare l'id della propria tavola o zona: `rtit app-rtit unita --cerca "<nome>"`, oppure il campo `id` di `list_organization_units` via MCP. Se la ricerca non restituisce nulla, apri la pagina della tavola su app.roundtable.it o consulta lo schema OpenAPI (sezione *organization-units*).

## Comandi della CLI

| Comando | Cosa fa |
| --- | --- |
| `rtit app-rtit data AAAA-MM-GG` | Punteggio e conflitti di una data (`/conflict-check/`) |
| `rtit app-rtit planner --mesi 3` | Giorni sensibili dei prossimi mesi (`/conflict-check/month/`) |
| `rtit app-rtit unita --cerca "<nome>"` | Cerca l'`organization_unit_id` di una tavola o zona |

## Risposta per un giorno

Stessa forma per `/conflict-check/` e per ogni giorno della mappa di `/conflict-check/month/` (lì le chiavi sono le date `AAAA-MM-GG`). Valori d'esempio:

```json
{
  "score": 30,
  "conflicts": [
    {
      "event_id": 1001, "name": "…", "url": "/activity/…/", "start_time": "20:00",
      "organizer": "RT 98 Esempio", "zone": "Zona N", "distance": 120,
      "impact": -70, "reason": "Stessa Zona", "severity": "danger"
    }
  ],
  "has_events": true
}
```

- `score` su scala **0–100** (più alto = meno conflitti): mostralo sempre come `N/100`.
- Un giorno è "sensibile" se `score` è sotto `app_rtit.soglia_punteggio` (default 90), oppure se c'è un conflitto con `severity` `danger`/`warning` o `impact <= -10`.

## Nota sulla pubblicazione

Solo le attività di tipo `announcement` ed `external` compaiono nelle superfici pubbliche delle collisioni; i tipi interni e di vendita non entrano nel Planner. Un evento della tavola caricato come interno su Tabler World **non protegge** la data dalle altre tavole.

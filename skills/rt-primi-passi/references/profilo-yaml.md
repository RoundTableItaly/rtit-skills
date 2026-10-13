# Profilo YAML (`rtit-profilo.yaml`) — schema

Esempio completo e commentato: `rtit profilo nuovo` (copia `src/rtit/templates/profilo-esempio.yaml`). Solo `id` è obbligatorio: ogni sezione mancante spegne la funzione corrispondente (`rtit profilo verifica` mostra cosa è attivo).

| Campo | Tipo | Default | A cosa serve |
| --- | --- | --- | --- |
| `id` | testo | — | Identificativo (es. `rt99-esempio`) |
| `livello` | `tavola`/`zona`/`nazionale` | `tavola` | Destinatari di default, testi |
| `nome`, `sigla`, `nome_esteso` | testo | da `id` | Intestazione e firme del bollettino |
| `citta` | testo | — | "Città, data" del bollettino |
| `zona` | testo | — | Destinatari "e p.c." (es. `Zona N`) |
| `fuso_orario` | IANA | `Europe/Rome` | Date di oggi, orari |
| `agm` | mappa anno → data | — | Date dell'AGM diverse dal primo sabato di giugno, per calcolare l'anno sociale (es. `agm: {"2025": "2025-06-14"}`); riempila con `list_statutory_years` dell'App RTIT se disponibile |
| `mese_inizio_anno` | — | — | Non più usato: l'anno sociale inizia la domenica dopo l'AGM. Se presente viene ignorato con un avviso |
| `quota_default` | numero | `25` | Quota proposta nei pack evento |
| `intestazione.sito/ritrovi/charter/tavola_madrina` | testo | `—` | Colonna sinistra del bollettino |
| `intestazione.sede` | lista di righe | — | Indirizzo della sede |
| `intestazione.loghi` | lista di PNG (max 2) | segnaposto | Loghi del bollettino (percorsi relativi al profilo) |
| `direttivo.anno` | `AAAA-AAAA` | anno del bollettino | Titolo "Consiglio Direttivo" |
| `direttivo.membri[]` | `{ruolo, nome, telefono?}` | — | Elenco direttivo + firme Presidente/Segretario |
| `bollettino.destinatari_pc` | lista | per livello | Riquadro "e p.c." |
| `bollettino.aperta_a` | testo | Tablers, ex Tablers, aspiranti e amici | Riga "La serata è aperta a" |
| `bollettino.template` | percorso DOCX | modello generico | Modello Word della tavola (es. in `Documenti legali/Loghi e modelli/`) |
| `archivio.percorso` | percorso | — | Cartella **condivisa** della tavola (Drive, OneDrive, Dropbox… sincronizzata); `"."` se il profilo sta nella radice. Senza, si lavora in chat o via connettore |
| `archivio.servizio` | testo | `cartella` | `google-drive`, `onedrive`, `sharepoint`, `dropbox`, `nextcloud`, `cartella` |
| `archivio.link` | `markdown`/`wikilink` | `markdown` | Stile dei link (wikilink per Obsidian) |
| `archivio.documenti_legali` | percorso | `Documenti legali` | Documenti legali generali (vedi [struttura-archivio.md](struttura-archivio.md)) |
| `archivio.cartelle_legali` | lista | `Statuto e regolamenti`, `Fiscale e PEC`, `Banca`, `Loghi e modelli` | Sottocartelle dei documenti legali |
| `archivio.anni` | pattern con `{anno}` | `Anni sociali/{anno}` | Cartella dell'anno sociale |
| `archivio.eventi` / `direttivo` / `tesoreria` / `comunicazione` | pattern con `{anno}` | `Anni sociali/{anno}/Eventi` … | Cartelle dell'anno |
| `archivio.cartelle_evento` | lista | `Bollettini`, `Form`, `Altri documenti` | Sottocartelle di ogni evento (il bollettino sta in `Bollettini/`) |
| `archivio.indice_anno` | pattern | `Anni sociali/{anno}/_Indice {anno}.md` | Nota indice dell'anno |
| `calendario.ical_url` | URL | — | Calendario della tavola (iCal pubblico o segreto) |
| `calendario.giorni_indietro/avanti` | numero | `7` / `120` | Finestra letta |
| `app_rtit.organization_unit_id` | intero | — | Unità su app.roundtable.it (planner) |
| `app_rtit.organization_unit_slug` / `area_slug` | testo | — | Identificativi testuali di tavola e zona (es. `rt-99-esempio`, `zona-esempio`) per i prossimi eventi |
| `app_rtit.mesi_planner` / `soglia_punteggio` | numero | `3` / `90` | Mappa collisioni |
| `classificazione.ignora/direttivo/solo_bollettino/sociale` | liste di regex | vedi esempio | Come trattare i titoli del calendario |
| `promemoria.*_giorni` | numero | `14`/`21` | Quando segnalare bollettino / Tabler World mancanti |

`{anno}` viene sostituito con l'anno sociale (es. `2026-2027`). I percorsi relativi sono relativi alla cartella del profilo.

## Decisioni salvate

Accanto al profilo (quindi nell'archivio condiviso), `rtit-profilo.decisioni.yaml` conserva le scelte dell'utente perché non vengano richieste ogni volta:

- `calendario_ignora`: eventi del calendario da non proporre più;
- `note`: appunti liberi.

Si aggiornano con `rtit decisioni ignora-calendario …` (o a mano).

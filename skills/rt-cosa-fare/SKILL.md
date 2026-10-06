---
name: rt-cosa-fare
description: >-
  Fa il punto su tavola, zona o nazionale in un unico report: prossimi eventi e cosa manca (pack, bollettino,
  Tabler World), novità del calendario, doppioni nell'archivio, date a rischio, scadenze del periodo; poi
  propone un'azione alla volta. Usala a inizio sessione o per "cosa c'è da fare?", "aggiornami", "facciamo
  il punto", "cosa manca per la cena di sabato?". Per l'elenco degli obblighi del Presidente usa
  rt-presidente.
---

# Cosa c'è da fare

È la skill da usare **all'inizio di ogni sessione**. Non chiedere all'utente quale sotto-skill vuole: fai il punto e proponi tu.

## Avanzamento

```
Sessione:
- [ ] 0 Profilo + decisioni salvate (mostrale sempre)
- [ ] 1 Eventi futuri: pack, cose da fare, bollettini, Tabler World
- [ ] 2 Calendario: eventi nuovi o cambiati
- [ ] 3 Archivio: cartelle evento doppie (stessa data), bollettini nelle cartelle Bollettini/
- [ ] 4 App RTIT: collisioni sulle nostre date, giorni sensibili, eventi di zona
- [ ] 5 Adempimenti del periodo (rt-presidente)
- [ ] 6 Report unico in chat
- [ ] 7 Proposte una alla volta (niente scritture senza conferma)
```

## Con terminale

```bash
rtit cosa-fare                     # report markdown completo
rtit cosa-fare --json              # stesso report, strutturato
rtit cosa-fare --salta-app-rtit    # senza rete o se l'App RTIT non risponde
```

Con il server MCP dell'App RTIT completa la sezione App RTIT con `search_events` (prossimi eventi di zona) e `check_date_conflicts` sulle date dei vostri eventi futuri.

Mostra il report **in chat**. Non scrivere file di report nell'archivio. Le sezioni senza configurazione (archivio, calendario, App RTIT) vengono saltate da sole: `rtit profilo verifica` dice cosa attivare.

## Senza terminale

Ricostruisci lo stesso report con quello che hai: profilo testuale, connettori Calendar e cloud (Drive, OneDrive, Dropbox), ciò che l'utente racconta. Chiedi al massimo 2 cose: "quali eventi avete nelle prossime 6 settimane?" e "di cosa vi siete già occupati?".

## Adempimenti del periodo

Aggiungi sempre una sezione breve in base al periodo dell'anno sociale (inizia il giorno dopo l'AGM, di solito la domenica dopo il primo sabato di giugno: vedi `rt-conoscenza`). Fonte: `rt-presidente`; in caso di differenze vale quella.

| Periodo | Da ricordare |
| --- | --- |
| Dopo l'AGM (il nuovo direttivo è in carica dal giorno dopo) | Eletti comunicati al Segretario Nazionale; riunione congiunta di passaggio di consegne **entro 30 giorni dall'AGM**; Modello AA5, PEC, conto corrente, calendario dell'anno, anagrafica Tabler World, accessi all'archivio |
| Prima dell'HYM (entro il 31 ottobre) | Assemblea Ordinaria di tavola e rapporto riassuntivo almeno 25 giorni prima; prima rata (50%) delle quote nazionali e di zona entro il giorno prima; delega se non si partecipa |
| Entro il 28 febbraio | Saldo delle quote |
| Non oltre il 60° giorno prima dell'AGM | Relazione morale (o prima, alla data dell'Editore Nazionale) |
| Prima dell'AGM (15 maggio–30 giugno) | Almeno 25 giorni prima: Assemblea Ordinaria (elezioni, rendiconto, ammissioni), candidature al CN, rapporto riassuntivo. Nuovi soci inseriti (welcome kit), delega; l'uscente prepara il passaggio di consegne (vedi la skill `rt-presidente`, file `references/passaggio-consegne.md`) e le cartelle dell'anno nuovo |
| Tutto l'anno | Almeno 20 riunioni di tavola e 4 di direttivo; libri sociali su Tabler World; ammissioni e dimissioni comunicate al nazionale e alla zona |

Lo Statuto dà le finestre, non le date dell'anno: se non conosci le date di HYM, AGM e Assemblea di Zona, chiedile o leggile nell'App RTIT. Articoli e dettagli in `rt-presidente`.

## Proposte (dopo il report)

Per ogni punto da fare, proponi **un'azione alla volta** con scelte chiare:

- evento `nuovo` o `cambiato` in calendario (tipo `sociale`, `solo_bollettino`, oppure `altro` confermato): ignora (salvando la decisione) · crea la cartella e la nota evento nell'archivio · crea il pack (solo se `sociale`) · bollettino · Tabler World;
- pack mancante o cose da fare aperte vicine alla data: completa con `rt-evento`;
- bollettino mancante entro i giorni di `promemoria.bollettino_giorni`: `rt-bollettino`;
- evento non su Tabler World: ricorda di caricarlo dal portale e di salvare `tablerworld_id` nella nota evento;
- evento da raccontare sui social o alla stampa (prima, durante, dopo): `rt-comunicazione`;
- data a rischio nel Planner: `rt-calendario`;
- cartelle con la stessa data: chiedi se sono lo stesso evento e riuniscile (`rt-archivio`);
- verbale da scrivere o seduta da convocare: `rt-direttivo`.

## Regole ferme

- **Mai** scrivere file, creare cartelle, pubblicare su Tabler World o creare eventi senza conferma esplicita.
- Ritrovi e direttivi: niente cartelle evento, pack o bollettini. Solo bollettino: niente pack.
- I verbali del direttivo già chiusi non si modificano (`rt-direttivo`).
- Non inventare date, scadenze o importi: se mancano, chiedili.
- Decisioni dell'utente ("ignora questo evento del calendario"): salvale (`rtit decisioni …`) così non vengono richieste di nuovo.

## Collegate

- `rt-presidente` — fonte degli adempimenti e passaggio di consegne.
- `rt-evento` — completare pack e cose da fare di un evento.
- `rt-bollettino` — bollettino mancante.
- `rt-calendario` — data a rischio o eventi nuovi in calendario.
- `rt-archivio` — doppioni e cartelle dell'anno.
- `rt-direttivo` — convocazioni e verbali.
- `rt-comunicazione` — post e foto degli eventi.

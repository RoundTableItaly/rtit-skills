# Changelog

Le novità di ogni versione, scritte per chi usa le skill. Formato [Keep a Changelog](https://keepachangelog.com/it/1.1.0/); numeri di versione e regole in [docs/rilasci.md](docs/rilasci.md).

## [Non rilasciato]

### Aggiunto

- Plugin per Antigravity CLI (`agy`), il nuovo nome di Gemini CLI: si installa con `agy plugin install`.

### Cambiato

- Il connettore ai dati dell'App si chiama ora "App Round Table Italia" (prima `round-table-italia`). In Claude Code compare come `plugin:rtit:App Round Table Italia`. In Codex resta `round-table-italia`, perché lì il nome non può avere spazi.

### Rimosso

- Estensione per il vecchio Gemini CLI (`gemini-extension.json`): `agy` non la legge.

### Da fare dopo l'aggiornamento

- Se usavi l'estensione di Gemini CLI, installa il plugin con `agy plugin install`.
- Se avevi dato permessi permanenti agli strumenti del vecchio connettore `round-table-italia`, Claude te li chiederà di nuovo: il nome degli strumenti è cambiato.

## [0.2.2] - 2026-10-07

### Cambiato

- Il plugin si presenta con il nome "Round Table Italia AI Skills" (prima compariva la sigla `rtit`).
- Il plugin porta con sé il logo di Round Table Italia, per la scheda nella directory dei plugin.

### Corretto

- `rtit --version` mostrava ancora 0.2.0 dopo l'aggiornamento alla 0.2.1: ora la versione della CLI segue quella del rilascio.

## [0.2.1] - 2026-10-07

### Aggiunto

- Regole di rilascio in `docs/rilasci.md`: versioni, rami, changelog, procedura.

## [0.2.0] - 2026-10-07

### Aggiunto

- Nuova skill `rt-direttivo`: convocazioni, ordini del giorno e verbali, con le regole dello Statuto.
- Statuto Nazionale integrale e sintesi dell'Annuario 2025-2026 (regolamenti, mansionari, cerimoniale) in `rt-conoscenza`.
- Calcolo delle quote nazionali, con listino ed esenzioni (`rt-presidente`).
- Nuovi riferimenti per il Presidente: tesoreria, zona, passaggio di consegne, modelli di documenti.
- Plugin Codex, oltre al plugin Claude e all'estensione Gemini CLI.

### Cambiato

- Tutte le skill sono state verificate sullo Statuto: scadenze, adempimenti, ammissione dei soci, presenze, cariche del direttivo. Dove Manuale o Annuario dicono altro, vale lo Statuto.
- Relazione morale: non oltre il 60° giorno prima dell'AGM (prima: "entro 60 giorni dall'AGM").
- Anno sociale: dal giorno dopo l'AGM al giorno dell'AGM successivo.
- Comunicazione (`rt-comunicazione`): riferimenti divisi in quattro file; locandina insieme all'evento; post entro 24-48 ore; comunicato stampa prima e dopo l'evento; Corrispondente e P.R.O. sono figure diverse.
- Logo (`rt-logo`): pin e coin secondo lo Statuto; patrocinio di un evento internazionale chiesto al Comitato Nazionale.
- Glossario completato con Statuto, Annuario e definizioni d'uso.
- Il rilascio è un solo file, `rtit-skills.zip`: in Claude si carica come plugin e installa tutte le skill insieme.

### Rimosso

- Skill `rt-tablerworld` e comandi `rtit tablerworld`: gli eventi si caricano su Tabler World dal portale.
- Pacchetti separati per singola skill, per GPT personalizzati e per Gem.

### Da fare dopo l'aggiornamento

- Se usavi `rtit tablerworld` o la variabile `TABLERWORLD_API_TOKEN`, non servono più: puoi rimuovere il token.
- Se avevi caricato le skill una per una in Claude, rimuovile e carica il plugin `rtit-skills.zip`.

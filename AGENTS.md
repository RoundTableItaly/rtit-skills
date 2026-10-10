# AGENTS — rtit-skills

Istruzioni per assistenti AI che lavorano **con** queste skill (utenti dei direttivi Round Table Italia) o **su** questo repository (contributori).

## Usare le skill

- Le skill sono in `skills/rt-*/SKILL.md`. Inizia da `rt-cosa-fare` se l'utente chiede un aggiornamento generico, da `rt-primi-passi` se manca il profilo.
- Lingua con l'utente: **italiano**, semplice. Una o due domande alla volta.
- Mai scrivere file, creare cartelle, pubblicare su Tabler World o inviare messaggi **senza conferma esplicita**.
- Mai inventare dati (date, importi, link, regole statutarie): chiedi o rimanda ai documenti ufficiali RTIT, che prevalgono.
- Anno sociale: inizia il giorno dopo l'AGM e finisce il giorno dell'AGM successivo (Statuto, art. 76). L'AGM si tiene tra il 15 maggio e il 30 giugno (art. 9), di solito il primo sabato di giugno: non dare la data per scontata. Si scrive `AAAA-AAAA`; date esatte nell'App RTIT (`list_statutory_years`).
- Statuto e Annuario: per le regole statutarie cerca in `skills/rt-conoscenza/references/statuto.md` e cita titolo e articolo; per regolamenti, mansionari e cerimoniale in `skills/rt-conoscenza/references/annuario-regolamenti.md`. Lo Statuto prevale sempre.
- Archivio condiviso: `Documenti legali/` e `Anni sociali/AAAA-AAAA/` (Eventi, Direttivo, Tesoreria, Comunicazione); ogni evento ha le sottocartelle `Bollettini/`, `Form/` e `Altri documenti/`. Dettagli nella skill `rt-primi-passi` (sezione "Archivio condiviso").
- CLI (se c'è un terminale): `uvx --from git+https://github.com/RoundTableItaly/rtit-skills rtit <comando>`, oppure `rtit` se installata. Profilo, in ordine: `--profilo`, `$RTIT_PROFILO`, `./rtit-profilo.yaml`, `~/.rtit/rtit-profilo.yaml`. Il profilo si condivide solo con il direttivo.
- Privacy: [docs/privacy.md](docs/privacy.md).

## Lavorare sul repository

- Codice in `src/rtit/`, test in `tests/`, skill in `skills/`, documentazione in `docs/`.
- Prima di proporre modifiche esegui gli stessi controlli della CI:

  ```bash
  uv run ruff check src tests tools
  uv run ruff format --check src tests tools
  uv run pytest -q
  uv run python tools/check_leaks.py
  uv run python tools/bump_version.py --check
  uv run python tools/build_release.py
  ```

- Rami e rilasci ([docs/rilasci.md](docs/rilasci.md)): parti sempre da `develop` aggiornato (`git fetch`, poi `git switch -c <ramo> origin/develop`), anche se la sessione si apre su `main`; apri la pull request verso `develop`. Mai push diretto su `main` o `develop`, mai force-push, mai spostare o cancellare un tag o rifare una release.
- Se cambi skill, CLI o pacchetto, aggiungi una riga a `CHANGELOG.md` sotto "Non rilasciato". La versione non si tocca a mano: `tools/bump_version.py`, solo in un ramo `release/`.

- Nessun dato reale: esempi solo con la tavola fittizia "RT 99 Esempio" (zona "Zona N"), persone come "Mario Rossi", telefoni `+39 000 000 000x`.
- Tono: le `SKILL.md` danno del tu all'assistente, all'imperativo; i testi destinati al socio danno del tu al socio. Lingua italiana.
- Commit in stile Conventional Commits.

# Contribuire a rtit-skills

Grazie! Questo progetto vive dell'esperienza delle tavole: anche una segnalazione del tipo "da noi si fa così" è preziosa.

## Prima di una pull request

1. Leggi [docs/privacy.md](docs/privacy.md): **nessun dato reale** (nomi, telefoni, indirizzi, calendari, ID) nel repository.
2. Se è la tua prima pull request, firma il **CLA** ([CLA.md](CLA.md)): lo chiede il bot sulla pull request.
3. Parti da `develop`, non da `main` (`git switch -c feature/<tema> origin/develop`), e apri la pull request verso `develop`. Il titolo segue i Conventional Commits, perché diventa il messaggio del commit.
4. Se cambi skill, CLI o pacchetto, aggiungi una riga a [CHANGELOG.md](CHANGELOG.md) sotto "Non rilasciato", scritta per chi usa le skill.
5. Esegui i controlli in locale:

```bash
uv venv && uv pip install -e ".[dev]"
uv run ruff check src tests tools
uv run ruff format --check src tests tools
uv run pytest -q
uv run python tools/check_leaks.py
uv run python tools/bump_version.py --check   # versione uguale nei file e presente nel changelog
uv run python tools/build_release.py          # pacchetto in dist/
claude plugin validate .                      # se hai Claude Code
```

Rami, versioni e procedura di rilascio: [docs/rilasci.md](docs/rilasci.md).

## Come sono fatte le skill

- `skills/<nome>/SKILL.md`: istruzioni per l'assistente, **in italiano**. Il frontmatter `description` dice *quando* usarla e contiene le frasi che l'utente direbbe davvero.
- `skills/<nome>/references/`: conoscenza di dettaglio, letta solo quando serve.
- Ogni skill deve funzionare **anche senza terminale** (percorso "solo chat"); la CLI `rtit` è un livello in più.
- Regole d'oro da mantenere: niente scritture senza conferma, niente dati inventati, i documenti ufficiali RTIT prevalgono.

## Codice (`src/rtit/`)

- Python ≥ 3.10, dipendenze minime, identificatori in inglese, messaggi all'utente in italiano.
- Ogni comando che scrive ha un dry-run o rifiuta di sovrascrivere senza `--force`.
- Test in `tests/` senza rete: le API si simulano con monkeypatch.

## Aggiungere conoscenza da un documento RTIT

1. Distilla il documento **senza perdere dettagli** in `skills/<skill>/references/`.
2. Scrivi la mappa di copertura in `docs/fonti/<documento>-copertura.md`: sezione della fonte → destinazione, punti "(da verificare)", dati personali rimossi.
3. Verifica di avere il permesso di pubblicare il contenuto: materiale interno RTIT solo con l'OK del Comitato Nazionale.

## Messaggi di commit

[Conventional Commits](https://www.conventionalcommits.org/): `feat(rt-bollettino): …`, `fix(cli): …`, `docs(rt-presidente): …`.

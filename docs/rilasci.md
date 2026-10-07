# Regole di rilascio

Poche regole, uguali per tutti: manutentore, contributori e assistenti AI. Servono a sapere sempre cosa c'è in ogni versione e a non perdere lavoro.

## 1. Versioni

Numerazione `MAJOR.MINOR.PATCH`:

| Parte | Quando si alza |
| --- | --- |
| **PATCH** | Correzioni di testi, regole o bug, senza novità |
| **MINOR** | Nuove skill, nuovi riferimenti, nuovi comandi `rtit`, nuove fonti |
| **MAJOR** | Cambi che obbligano chi usa le skill a intervenire: schema del profilo, comandi o skill rimossi o rinominati, struttura dell'archivio |

Finché siamo in `0.x`, i cambi "da MAJOR" alzano il MINOR e vanno scritti nel changelog sotto "Da fare dopo l'aggiornamento".

La versione sta in sei file e deve essere identica: `pyproject.toml`, `src/rtit/__init__.py` (è quella che mostra `rtit --version`), `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, `gemini-extension.json`. **Non modificarla a mano**: usa `tools/bump_version.py`. Il tag è `vX.Y.Z` e coincide con la versione nei file.

## 2. Rami (git-flow)

| Ramo | Contiene | Nasce da | Finisce in |
| --- | --- | --- | --- |
| `main` | solo versioni rilasciate | — | — |
| `develop` | lavoro pronto per il prossimo rilascio | `main` | — |
| `feature/<tema>` (e `claude/<nome>` delle sessioni AI) | una modifica | `develop` | `develop` |
| `release/X.Y.Z` | preparazione del rilascio | `develop` | `main` e `develop` |
| `hotfix/X.Y.Z` | correzione urgente di una versione pubblicata | `main` | `main` e `develop` |

- Il ramo predefinito su GitHub è `main`, perché è quello che installano `/plugin marketplace add`, `codex plugin marketplace add` e `gemini extensions install`: deve contenere solo versioni rilasciate.
- Per questo **ogni lavoro nuovo parte esplicitamente da `develop`**, anche nelle sessioni AI, che di solito partono dal ramo predefinito:

  ```bash
  git fetch origin
  git switch -c feature/<tema> origin/develop
  ```

- Un ramo di lavoro vive pochi giorni. Prima della pull request riallinealo a `develop`.

## 3. Pull request e merge

- Nessun push diretto su `main` e `develop`: si entra solo con una pull request e con la CI verde.
- `feature/*` → `develop`: **squash**. Il titolo della pull request diventa il messaggio del commit, in stile [Conventional Commits](https://www.conventionalcommits.org/): `feat(rt-bollettino): …`, `fix(cli): …`, `docs(rt-presidente): …`.
- `release/*` e `hotfix/*` → `main`, e il rientro di `main` in `develop`: **merge commit**, mai squash. Con lo squash `main` e `develop` perdono la storia comune e al rilascio successivo tutto va in conflitto.
- Ogni pull request che cambia skill, CLI o pacchetto aggiunge una riga al changelog.

## 4. Changelog

- File [CHANGELOG.md](../CHANGELOG.md), in italiano, formato [Keep a Changelog](https://keepachangelog.com/it/1.1.0/).
- In cima c'è `## [Non rilasciato]`: le righe nuove vanno lì. Sotto, una sezione per versione: `## [0.2.0] - 2026-10-07`.
- Categorie: **Aggiunto**, **Cambiato**, **Corretto**, **Rimosso**, più **Da fare dopo l'aggiornamento** quando chi usa le skill deve intervenire.
- Scrivi per un socio del direttivo, non per chi sviluppa: "Il bollettino ora…", non "refactor di…". Indica la skill tra parentesi.
- La sezione della versione diventa il testo della release su GitHub.

## 5. Come si fa un rilascio

1. Parti da `develop` aggiornato:

   ```bash
   git fetch origin
   git switch -c release/X.Y.Z origin/develop
   ```

2. Alza la versione. Il comando aggiorna i sei file e sposta le righe di "Non rilasciato" nella sezione della nuova versione, con la data di oggi:

   ```bash
   uv run python tools/bump_version.py X.Y.Z
   ```

3. Rileggi il changelog ed esegui i controlli (gli stessi della CI, elencati in [CONTRIBUTING.md](../CONTRIBUTING.md)). Commit: `chore(release): X.Y.Z`.
4. Pull request `release/X.Y.Z` → `main`. Dopo la CI verde, **merge commit**.
5. Metti il tag sul commit di merge e pubblicalo:

   ```bash
   git switch main && git pull
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

   Il workflow `Release` controlla che tag, file e changelog coincidano, costruisce `rtit-skills.zip` e pubblica la release con il testo del changelog.
6. Pull request `main` → `develop` (**merge commit**) per riportare versione e changelog.
7. Prova il pacchetto pubblicato: scarica lo zip dalla release e caricalo come plugin in Claude.

**Hotfix**: stessi passi, ma il ramo `hotfix/X.Y.Z` nasce da `main` e alza il PATCH.

## 6. Cose che non si fanno

- Nessun force-push e nessuna riscrittura della cronologia su `main` e `develop`.
- Un tag pubblicato non si sposta e non si cancella; una release non si rifà. Se è sbagliata, si pubblica la PATCH successiva.
- Nessun rilascio da un ramo diverso da `main`, né con la CI rossa.
- Le eccezioni le decide solo il manutentore e vanno annotate nel changelog.

## 7. Controlli automatici

| Dove | Cosa controlla |
| --- | --- |
| CI (pull request, `main`, `develop`) | lint, formato, test, fughe di dati, build del pacchetto, versione uguale nei sei file e presente nel changelog (`tools/bump_version.py --check`) |
| Workflow `Release` (tag `v*`) | gli stessi controlli, più: il tag coincide con la versione |
| GitHub | protezioni dei rami `main` e `develop` e dei tag `v*`, dove il piano dell'organizzazione le consente |

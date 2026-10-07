# Installare le skill e gli strumenti

Le skill funzionano anche **solo in chat**. Gli strumenti da riga di comando servono per automatizzare: generare il bollettino in Word/PDF, leggere il calendario, controllare le sovrapposizioni sull'App RTIT, creare cartelle evento.

## 0. Pacchetto pronto da scaricare

Nella pagina **Releases** del repository rtit-skills su GitHub (https://github.com/RoundTableItaly/rtit-skills/releases) c'è un solo file, `rtit-skills.zip`: è un plugin, cioè la raccolta di tutte le skill (cartella `skills/`).

| Per chi | Cosa fare |
| --- | --- |
| Claude (app e claude.ai) | Carica lo zip così com'è nella sezione dei plugin: installa tutte le skill insieme |
| Claude Code | Estrai lo zip in una cartella (es. `rtit-skills/`): `/plugin marketplace add ./rtit-skills`, poi `/plugin install rtit@rtit-skills` |
| Codex | Dalla cartella estratta: `codex plugin marketplace add ./rtit-skills` |
| Gemini CLI | Dalla cartella estratta: `gemini extensions install ./rtit-skills` |
| ChatGPT (GPT) e Gemini (Gem) | Nessun pacchetto: incolla nelle istruzioni la `SKILL.md` che ti serve e carica i file di `references/` |

Su Claude.ai, ChatGPT e Gemini si lavora "solo chat": il profilo è un blocco di testo (vedi [profilo-testo.md](profilo-testo.md)). Il resto di questa pagina serve solo se c'è un terminale.

## 1. Installare `uv` (una volta)

`uv` installa e avvia Python e i pacchetti in automatico.

- **Windows** (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **macOS / Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`

Riapri il terminale e verifica con `uv --version`.

## 2. Usare la CLI `rtit` senza installarla

```bash
uvx --from git+https://github.com/RoundTableItaly/rtit-skills rtit --help
```

Per non riscrivere ogni volta il prefisso, installala come strumento:

```bash
uv tool install git+https://github.com/RoundTableItaly/rtit-skills
rtit --help
uv tool upgrade rtit-skills   # aggiornare
```

## 3. Dire a `rtit` dov'è il profilo

In ordine di priorità: opzione `--profilo <file>`, variabile `RTIT_PROFILO`, file `rtit-profilo.yaml` nella cartella corrente, `~/.rtit/rtit-profilo.yaml`.

Metti il profilo nella radice dell'archivio condiviso (la cartella sincronizzata dal cloud) e punta lì la variabile:

- Windows (permanente): `setx RTIT_PROFILO "C:\Users\<utente>\OneDrive - RT 99 Esempio\rtit-profilo.yaml"`
- macOS / Linux: aggiungi `export RTIT_PROFILO="$HOME/Dropbox/RT 99 Esempio/rtit-profilo.yaml"` al file `~/.zshrc` o `~/.bashrc`.

## 4. PDF del bollettino

- Con **Microsoft Word** installato (Windows/macOS): `uv tool install "rtit-skills[word] @ git+https://github.com/RoundTableItaly/rtit-skills"`.
- Altrimenti con **LibreOffice** (gratuito): basta che `soffice` sia installato.
- Senza nessuno dei due: si genera solo il DOCX; il PDF si esporta a mano da Word/Google Docs.

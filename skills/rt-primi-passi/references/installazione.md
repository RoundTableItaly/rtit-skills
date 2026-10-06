# Installare le skill e gli strumenti

Le skill funzionano anche **solo in chat**. Gli strumenti da riga di comando servono per automatizzare: generare il bollettino in Word/PDF, leggere il calendario, controllare le sovrapposizioni sull'App RTIT, creare cartelle evento.

## 0. Pacchetti pronti da scaricare

Nella pagina **Releases** del repository rtit-skills su GitHub (https://github.com/RoundTableItaly/rtit-skills/releases) ci sono pacchetti da scaricare e caricare, senza installare nulla:

| Pacchetto | Per chi | Cosa fare |
| --- | --- | --- |
| `dist/skills/<skill>.zip` (uno per skill, es. `rt-bollettino.zip`) | Claude.ai e Claude Desktop | Nelle impostazioni, sezione delle skill: carica lo zip della skill che ti serve |
| `rtit-claude-plugin.zip` | Claude Code | Tutte le skill in un unico plugin da installare in Claude Code |
| `rtit-chatgpt.zip` | ChatGPT (GPT personalizzato) | Contiene le istruzioni da incollare nel GPT e i file di conoscenza da caricare |
| `rtit-gemini.zip` | Gemini (Gem) | Istruzioni e file da caricare in un Gem |

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

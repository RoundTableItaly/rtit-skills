# rtit-skills — l'assistente AI per i direttivi di Round Table Italia

Skill per **Claude, ChatGPT, Gemini e altri assistenti AI** che aiutano presidenti, segretari, tesorieri e membri dei direttivi di **tavola, zona e nazionale** a lavorare per l'associazione **senza perdere nulla**: adempimenti, direttivo e verbali, eventi, bollettini, archivio condiviso, calendario, comunicazione, crescita della tavola.

> Progetto della community, ospitato dall'organizzazione GitHub [RoundTableItaly](https://github.com/RoundTableItaly). Vedi [Titolarità e licenza](#titolarità-e-licenza).

## Cosa sa fare

| Skill | Ti aiuta a… |
| --- | --- |
| `rt-primi-passi` | iniziare: un'intervista breve crea il profilo della tavola, zona o nazionale (ruolo, direttivo e firme, calendario, archivio condiviso) |
| `rt-cosa-fare` | fare il punto: prossimi eventi e cosa manca, novità del calendario, doppioni, date a rischio, scadenze del periodo |
| `rt-presidente` | sapere cosa devono fare Presidente e direttivo secondo il *Manuale del buon Presidente*: insediamento, quote, HYM, AGM, Assemblea di Zona e deleghe, nuovo socio, tesoreria, relazione morale, passaggio di consegne, direttivo di zona, con modelli pronti |
| `rt-direttivo` | gestire direttivo e assemblee: convocazioni e ordini del giorno, verbali, registro delle decisioni, verbale di elezione per banca e PEC |
| `rt-conoscenza` | capire sigle e termini, quando inizia l'anno sociale, livelli, Fondazione RTIT, link ufficiali; consultare lo Statuto (testo integrale) e i regolamenti, i mansionari e il cerimoniale dell'Annuario |
| `rt-archivio` | impostare e tenere in ordine l'archivio condiviso su qualsiasi cloud: documenti legali, anni sociali, eventi, senza doppioni |
| `rt-evento` | organizzare un evento dall'idea al saldo: nota evento, progetto, invitati e spese |
| `rt-bollettino` | preparare il bollettino ufficiale con un'intervista guidata e generare Word/PDF nella cartella `Bollettini/` dell'evento |
| `rt-calendario` | scegliere e verificare le date: punteggio del Planner dell'App RTIT, date alternative, confronto col calendario della tavola |
| `rt-app-rtit` | consultare l'App Round Table Italia (server MCP): eventi di altre tavole e zone, email istituzionali, statistiche per anno sociale |
| `rt-crescita` | far crescere la tavola: diagnosi, programma annuale, serata con aspiranti, pitch di invito, contatti su LinkedIn |
| `rt-comunicazione` | preparare post, storie, Reel, LinkedIn, comunicati stampa e checklist del P.R.O. (responsabile comunicazione) |
| `rt-logo` | controllare logo, stemma e rondella secondo le Linee guida RTIT: colori, font, versioni ammesse, pin e coin |

Gli eventi si caricano su **Tabler World** a mano, dal portale dei soci: le skill ti aiutano a preparare dati e testi.

## L'archivio condiviso

Le skill lavorano su una cartella del cloud della tavola (Google Drive, OneDrive, SharePoint, Dropbox, Nextcloud…), condivisa solo con il direttivo e passata di mandato in mandato. Struttura di default, configurabile nel profilo:

```
<Archivio condiviso>/
├── rtit-profilo.yaml · rtit-profilo.decisioni.yaml
├── Documenti legali/              Statuto e regolamenti, Fiscale e PEC, Banca, Loghi e modelli
└── Anni sociali/
    └── 2026-2027/
        ├── _Indice 2026-2027.md   eventi, bollettini, verbali, note per il passaggio di consegne
        ├── Eventi/
        │   └── AAAA-MM-GG Nome evento/
        │       ├── AAAA-MM-GG Nome evento.md · progetto.md · invitati.md · spese.md
        │       ├── Bollettini/        nota .md + DOCX + PDF del bollettino
        │       ├── Form/              moduli Google (link o export delle risposte)
        │       └── Altri documenti/   ricevute, foto, preventivi…
        ├── Direttivo/                 convocazioni e verbali
        ├── Tesoreria/                 bilanci, quote, rendiconti
        └── Comunicazione/             piano social, materiali P.R.O.
```

L'**anno sociale** inizia il giorno dopo l'AGM e finisce il giorno dell'AGM successivo (Statuto, art. 76); l'AGM si tiene tra il 15 maggio e il 30 giugno, di solito il primo sabato di giugno. Si scrive `AAAA-AAAA`. Con la CLI: `rtit archivio struttura --applica` crea le cartelle dell'anno, `rtit evento nuovo --data … --titolo … --applica` crea la cartella dell'evento (e si ferma se ne esiste già una simile).

## Scaricare i pacchetti

Ogni versione pubblica i pacchetti pronti nella pagina [Releases](https://github.com/RoundTableItaly/rtit-skills/releases):

| Usi… | Scarica | Cosa contiene |
| --- | --- | --- |
| Claude.ai o Claude Desktop | `rt-<skill>.zip` (una skill) oppure `rtit-skills-tutte.zip` | le skill da caricare in Impostazioni → Skill |
| Claude Code | `rtit-claude-plugin.zip` | il plugin completo con il server MCP dell'App RTIT (in alternativa installalo dal marketplace, vedi sotto) |
| ChatGPT | `rtit-chatgpt.zip` | istruzioni e file di conoscenza per un GPT personalizzato, con la guida `LEGGIMI.md` |
| Gemini (app) | `rtit-gemini.zip` | istruzioni e file di conoscenza per un Gem, con la guida `LEGGIMI.md` |

I pacchetti si generano anche in locale con `uv run python tools/build_release.py` (cartella `dist/`).

## Hai appena installato un assistente AI? Fai così

### Claude (app o claude.ai)

1. Scarica dalla pagina [Releases](https://github.com/RoundTableItaly/rtit-skills/releases) gli zip delle skill che ti servono. Per iniziare bastano `rt-primi-passi`, `rt-cosa-fare`, `rt-presidente` e `rt-bollettino`; `rtit-skills-tutte.zip` le contiene tutte.
2. In Claude apri le **Impostazioni**, cerca la sezione **Skill** e carica uno zip alla volta. Le skill richiedono che l'esecuzione di codice sia attiva: Claude te lo segnala se non lo è.
3. Crea un **Progetto** per la tua tavola (es. "Tavola 99").
4. Scrivi: *"Sono il nuovo segretario della mia tavola, aiutami con i primi passi"*.
5. Incolla nelle **Istruzioni del progetto** il profilo che Claude ti prepara. Da lì in poi ogni conversazione del Progetto conosce la tua tavola.

**Consigliato:** aggiungi anche il connettore dell'App Round Table Italia (Impostazioni → Connettori → connettore personalizzato → `https://app.roundtable.it/mcp/`, senza autenticazione; guida: https://app.roundtable.it/ai-agents). Così l'assistente vede eventi, collisioni di date e statistiche aggiornati.

Se colleghi il calendario e il cloud della tavola (Google Drive, OneDrive/SharePoint, Dropbox) dai connettori, le skill leggono e salvano lì eventi, pack e bollettini. Prima di scrivere qualcosa ti chiedono sempre conferma.

### Claude Code (terminale, per chi è un po' più tecnico)

```bash
/plugin marketplace add RoundTableItaly/rtit-skills
/plugin install rtit@rtit-skills
```

Senza accesso a GitHub puoi estrarre `rtit-claude-plugin.zip` e aggiungere la cartella come marketplace locale (`/plugin marketplace add ./rtit-claude-plugin`), poi installare `rtit@rtit-skills`.

Gli strumenti da riga di comando (`rtit`) si avviano con [uv](https://docs.astral.sh/uv/): `uvx --from git+https://github.com/RoundTableItaly/rtit-skills rtit --help`. Guida completa: [skills/rt-primi-passi/references/installazione.md](skills/rt-primi-passi/references/installazione.md).

### Altri agenti (Codex, Cursor, Gemini CLI, …)

```bash
npx skills add RoundTableItaly/rtit-skills
```

Per Gemini CLI il repository è anche un'estensione, con il server MCP dell'App RTIT: `gemini extensions install https://github.com/RoundTableItaly/rtit-skills`. Gli agenti che leggono `AGENTS.md` trovano lì le istruzioni generali.

### ChatGPT

ChatGPT non carica le skill come file: con `rtit-chatgpt.zip` crei un **GPT personalizzato**. Incolli `ISTRUZIONI.txt` nelle istruzioni del GPT, carichi i file della cartella `conoscenza/` e, dove il piano lo consente, aggiungi l'App Round Table Italia come connettore MCP (`https://app.roundtable.it/mcp/`, senza autenticazione; vedi https://app.roundtable.it/ai-agents). I passaggi sono in `LEGGIMI.md` dentro lo zip. La CLI `rtit` in ChatGPT non funziona: il GPT prepara testi e tabelle da salvare a mano.

### Gemini (app)

Con `rtit-gemini.zip` crei un **Gem**: incolli `ISTRUZIONI.txt` e carichi i file di `conoscenza/` (accorpati, perché i Gem accettano pochi file). Nell'app Gemini non c'è il connettore MCP: i dati dell'App RTIT si controllano su https://app.roundtable.it. I passaggi sono in `LEGGIMI.md` dentro lo zip.

## Privacy, prima di tutto

Lavoriamo con dati di persone vere: soci, ospiti, telefoni, pagamenti, a volte intolleranze alimentari, che sono dati sanitari. Leggi [docs/privacy.md](docs/privacy.md). In breve: il profilo si condivide solo con il direttivo e sta nell'archivio condiviso; gli accessi si rivedono a ogni mandato; gli elenchi soci non si incollano in chat senza motivo; nessun dato personale va in questo repository.

## Livelli: tavola, zona, nazionale

Le skill nascono dall'esperienza di una tavola e sono pensate per il livello **tavola**. Zona e nazionale sono supportati per profilo, destinatari del bollettino, App RTIT e adempimenti, ma sono ancora **in beta**: vedi [docs/livelli.md](docs/livelli.md). Le proposte sono benvenute.

## Fonti

Il sapere delle skill viene da documenti RTIT: lo *Statuto Nazionale Round Table Italia* (2024, riportato per intero), l'*Annuario Round Table Italia 2025-2026* (sintesi di regolamenti, mansionari e cerimoniale) e, distillati senza perdere dettagli, *Manuale del buon Presidente* (Comitato Nazionale), *RTIT University — Ritorno alle basi*, *Strategia LinkedIn — Round Table Italia*, *Linee guida utilizzo logo*, *Vademecum della Comunicazione* e un vademecum di buone pratiche. Salvo lo Statuto, i documenti originali non sono nel repository: sono citati, con le mappe di copertura, in [docs/fonti/](docs/fonti/README.md). In caso di dubbio **prevalgono i documenti ufficiali RTIT**, e fra questi **lo Statuto**.

## Contribuire

Hai un'idea, hai trovato un errore, la tua tavola fa diversamente? Apri una [issue](https://github.com/RoundTableItaly/rtit-skills/issues) o leggi [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
uv venv && uv pip install -e ".[dev]"
uv run ruff check src tests tools
uv run ruff format --check src tests tools
uv run pytest -q
uv run python tools/check_leaks.py
uv run python tools/build_release.py
```

## Titolarità e licenza

Codice e documentazione: vedi [LICENSE](LICENSE). Il nome "Round Table", i loghi e i marchi di Round Table Italia e Round Table International appartengono ai rispettivi titolari e **non** sono coperti dalla licenza. Il template del bollettino usa loghi segnaposto: ogni tavola inserisce i propri, nel rispetto del manuale loghi RTIT.

# Privacy e dati personali

Le skill aiutano a gestire una associazione fatta di persone. Queste regole valgono per chi le usa e per l'assistente AI, che le applica.

## Cosa trattiamo

| Dato | Dove sta | Attenzione |
| --- | --- | --- |
| Archivio condiviso | Cartella cloud della tavola (Google Drive, OneDrive, SharePoint, Dropbox…) | Accesso solo al direttivo in carica; gli accessi si rivedono a ogni mandato (dal giorno dopo l'AGM, con il passaggio di consegne): chi esce dal direttivo perde l'accesso, chi entra lo riceve |
| Nomi e telefoni del direttivo | Profilo `rtit-profilo.yaml` nella cartella principale dell'archivio condiviso (o testo nel Progetto dell'assistente) | Servono per le firme dei bollettini; il profilo si condivide solo con il direttivo, mai in pubblico: segue gli accessi dell'archivio (o del Progetto) |
| Invitati, conferme, pagamenti | `invitati.md` dell'evento o tabelle in chat | Solo il necessario per organizzare la serata |
| **Intolleranze / allergie** | `invitati.md` | **Dati sanitari** (GDPR art. 9): minimi, cancellati dopo l'evento, mai inoltrati |
| Elenchi soci / anagrafica | Archivio condiviso della tavola, Tabler World | Accesso solo al direttivo; non copiarli in chat se non serve |
| Profili LinkedIn di aspiranti | Nessuna copia | Solo nome, ruolo e un aggancio comune; niente scraping né automazioni |
| Indirizzo iCal segreto del calendario | Profilo | È una password: non condividerlo. Rigeneralo in Google Calendar quando qualcuno esce dal direttivo, poi aggiorna il profilo |

## Regole per l'assistente

1. Chiedi solo i dati che servono al compito. Il telefono serve solo a chi firma i bollettini.
2. Non riportare dati personali in output che verranno condivisi (post, mail di massa) senza conferma.
3. Prima di creare o inviare qualcosa che contiene dati di terzi, mostra un'anteprima e chiedi conferma.
4. Suggerisci di anonimizzare quando chiedi un parere su un caso ("un socio" invece del nome).

## Regole per chi usa le skill

- **Assistenti cloud**: controlla le impostazioni sui dati del tuo piano (per esempio se le conversazioni possono essere usate per addestrare i modelli). Per i dati sensibili preferisci un piano o un'impostazione che li esclude.
- **Progetti condivisi**: se condividi un Progetto con altri membri del direttivo, tutti vedono il profilo e i file caricati.
- **Fine mandato**: nel passaggio di consegne consegna i documenti della tavola, aggiorna gli accessi all'archivio condiviso, rigenera l'indirizzo iCal segreto se qualcuno esce dal direttivo e cancella le copie personali che non servono più.

## Regole per chi contribuisce al repository

- Nessun dato reale nel repository: esempi solo con la tavola fittizia "RT 99 Esempio" e numeri `+39 000 …`.
- `rtit-profilo.yaml`, `rtit-profilo.yml`, `*.decisioni.yaml`, `anteprima/` e `preview/` sono in `.gitignore`.
- La CI esegue `tools/check_leaks.py`, che blocca numeri di telefono reali, email personali e percorsi locali. I maintainer possono aggiungere una lista di termini privati con la variabile `RTIT_LEAK_DENYLIST`, che non sta nel repository.
- Hai pubblicato per errore un dato personale? Segnalalo subito ai maintainer: va rimosso anche dalla storia git.

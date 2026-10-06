---
name: rt-bollettino
description: >-
  Prepara il bollettino ufficiale di un evento (invito con data, luogo, dress code, costo, scadenza, firme di
  Presidente e Segretario, destinatari "e p.c.") con un'intervista guidata, poi produce il testo o il
  Word/PDF dal modello e lo salva nella cartella Bollettini dell'evento. Usala per "bollettino", "bollettino
  N.", "invito ufficiale della serata", "prepara il Word per la cena", o quando rt-cosa-fare segnala un
  bollettino mancante.
---

# Bollettino evento

Lingua: **italiano**. **Non inventare** dati mancanti: chiedi. Riepiloga e ottieni l'approvazione **prima** di scrivere file.

Regole dal Manuale del Presidente:

- ogni evento pubblicizzato ha un bollettino;
- l'evento deve essere **già su Tabler World**, o almeno pianificato;
- su Tabler World c'è un **modello di bollettino** ufficiale: se la tavola usa quello, questa skill serve a raccogliere e controllare i contenuti;
- loghi: logo di tavola presente, rondella non coperta, deformata o tagliata, logo nazionale solo per eventi nazionali. Per il controllo completo della grafica usa `rt-logo`.

## Avanzamento

`0 Contesto → 1 Metadati → 2 Invito → 3 Firme → 4 Destinatari → 5 Intestazione → Riepilogo approvato → 6 Nota in <evento>/Bollettini/ → 7 Word/PDF`

## Fase 0 — Contesto

1. Carica il **profilo** (`rt-primi-passi`): nome, sigla, città, zona, direttivo, intestazione. Se manca, chiedi il minimo: nome tavola, zona, Presidente e Segretario con telefono.
2. Trova l'**evento** (archivio con `rtit eventi --futuri`, calendario o racconto dell'utente); precompila data, ora, luogo, costo e segnala le differenze.
3. Trova l'**ultimo bollettino** dell'anno sociale (numero progressivo e firme): nelle cartelle `Bollettini/` degli eventi o nell'indice dell'anno cerca note `tipo: bollettino`; altrimenti chiedi.

**Controllo**: evento individuato o confermato esplicitamente.

## Fase 1 — Metadati

Numero progressivo, data di emissione, titolo breve, anno sociale `AAAA-AAAA` (inizia la domenica dopo l'AGM: vedi `rt-conoscenza`). Nome file: `AAAA-MM-GG Bollettino N.X Titolo breve`.

**Controllo**: numero + data di emissione + evento.

## Fase 2 — Invito e logistica

1. Giorno, data e ora (coerenti con evento e calendario) e titolo dell'invito
2. Paragrafo descrittivo di 1–3 frasi (facoltativo) e note pratiche in elenco (parcheggio, cosa è incluso, posti limitati, "Aperta a: …")
3. Tabella: **Location** (indirizzo completo), **Dress code** ("Informale" va bene), **Costo** (soci in quota / esterni), **Conferma entro** *oppure* **Prenotazione entro** — tutti obbligatori; **Maps** facoltativa

**Controllo**: luogo, costo, scadenza, dress code. Se manca qualcosa, elenca cosa manca e chiedi.

## Fase 3 — Firme

Presidente e Segretario con telefono. Proponi i dati dal profilo o dall'ultimo bollettino e chiedi **conferma esplicita**: il direttivo cambia a ogni anno sociale, dalla domenica dopo l'AGM.

## Fase 4 — Destinatari (p.c.)

Default per una tavola: Presidente, Vice e Segretario Nazionale RTIT; Comitato di [Zona]; Presidenti delle Tavole della [Zona]; soci, ex soci, membri d'onore e amici della [Tavola]. Chiedi solo se serve personalizzare.

## Fase 5 — Intestazione (facoltativa)

"Includo l'intestazione della tavola con il Consiglio Direttivo?" Nel Word arriva dal profilo; nella nota markdown si può omettere.

## Riepilogo (obbligatorio)

Mostra il bollettino completo e i file che verranno creati, con il percorso, e chiedi l'approvazione. Se mancano campi obbligatori, elencali e chiedi se l'utente li dà ora o preferisce un riepilogo parziale senza file.

## Fase 6 — Nota markdown

Formato esatto (lo legge il generatore Word): [references/formato-nota.md](references/formato-nota.md). Esempi: [references/esempi.md](references/esempi.md).

- Con archivio: salvala in `<cartella evento>/Bollettini/` con il nome del bollettino; aggiorna la sezione `## Bollettino ufficiale` della nota evento.
- Senza archivio: mostrala in chat o crea il file che l'utente scaricherà.

## Fase 7 — Word e PDF

Istruzioni (terminale, esecuzione di codice, solo chat): [references/generazione-word.md](references/generazione-word.md). In breve: `rtit bollettino --md "<cartella evento>/Bollettini/<nota>.md"` crea DOCX e PDF accanto alla nota; `--out-dir` solo per anteprime fuori dall'archivio; `--force` solo dopo conferma; non dichiarare mai un PDF che non esiste.

## Dopo

- Nota, DOCX e PDF restano **solo** in `<cartella evento>/Bollettini/`: nessuna copia altrove. Aggiorna l'indice dell'anno, che elenca i bollettini.
- Allega il PDF all'evento su Tabler World e inoltralo nei canali della tavola.
- Solo chat: aggiorna il numero dell'ultimo bollettino nel profilo testuale.

## Collegate

- `rt-evento` — nota evento e pack da cui prendere i dati.
- `rt-logo` — controllo di loghi e grafica del bollettino.
- `rt-comunicazione` — post e storie per promuovere l'evento.
- `rt-archivio` — dove sta la cartella `Bollettini/` dell'evento.
- `rt-primi-passi` — profilo con direttivo, firme e intestazione.

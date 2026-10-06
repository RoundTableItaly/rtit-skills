# Profilo in forma di testo (percorso "solo chat")

Quando l'assistente non ha un terminale (Claude.ai, Claude Desktop senza strumenti, Gemini, app mobile), il profilo è un blocco di testo che l'utente incolla:

- **Claude.ai / Desktop** → crea un *Progetto* (es. "Tavola 99") → *Istruzioni del progetto* → incolla.
- **Gemini** → crea un *Gem* → *Istruzioni* → incolla.
- **ChatGPT o altri** → *Istruzioni personalizzate* o *Memoria*.

Così ogni conversazione del Progetto conosce già tavola, direttivo e abitudini.

## Formato da generare

Usa esattamente questi titoli. Ometti le righe che l'utente non ha fornito; non inventare.

```text
PROFILO ROUND TABLE (per le skill rt-*)
Livello: tavola | zona | nazionale
Nome: Round Table N.99 Esempio  ·  Sigla: RT 99 Esempio  ·  Città: Esempio
Zona: Zona N
Il mio ruolo: Segretario
Anno sociale: 2026-2027 (dalla domenica dopo l'AGM; date esatte nell'App RTIT)

Direttivo 2026-2027:
- Presidente: Mario Rossi (+39 000 000 0001)  ← firma i bollettini
- Segretario: Giovanni Neri (+39 000 000 0002)  ← firma i bollettini
- Vicepresidente: …; Past President: …; Tesoriere: …; Corrispondente: …; Consiglieri: …

Intestazione bollettino:
- Sito: …  ·  Ritrovi: …  ·  Sede: …  ·  Charter: …  ·  Tavola madrina: …
- Destinatari "e p.c.": Presidente/Vice/Segretario Nazionale RTIT, Comitato di Zona N, Presidenti delle Tavole della Zona N
- Aperta a (default): Tablers, ex Tablers, aspiranti e amici

Strumenti:
- Calendario della tavola: Google Calendar condiviso (connettore attivo: sì/no)
- Archivio condiviso: Google Drive (o OneDrive, Dropbox…), cartella "RT 99 Esempio" → Documenti legali; Anni sociali/{anno}/Eventi (ogni evento con Bollettini, Form, Altri documenti), Direttivo, Tesoreria, Comunicazione
- Tabler World: usato per pubblicare gli eventi (sì/no)
- App RTIT: https://app.roundtable.it (unità: rt-99-esempio, zona-esempio)

Abitudini:
- Ultimo bollettino emesso: N.3 del 2026-09-20
- Quota standard evento: 25 € (soci in quota)
```

Ricorda all'utente di **aggiornarlo** a ogni cambio di direttivo (dalla domenica dopo l'AGM, di solito a giugno) e dopo ogni bollettino (numero progressivo).

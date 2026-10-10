# Esempi di bollettino (tavola fittizia "RT 99 Esempio")

Modelli di **tono e struttura**. Eventi, luoghi e date sono inventati: non copiarli in bollettini reali.

## Stile ricco — primo bollettino dell'anno, molte note pratiche

```markdown
## Invito

**Sabato 18 settembre 2027, ore 19:30** — Aperitivo di benvenuto (ripresa dopo l'estate).

Primo appuntamento dopo l'estate: presentiamo il programma e il nuovo direttivo.

- Parcheggio interno gratuito fino a esaurimento posti; in alternativa parcheggio pubblico a 300 m
- Aperitivo a buffet con bevande incluse; opzione vegetariana su richiesta
- **Posti limitati**: confermate il prima possibile
- Aperta a: Tablers, ex Tablers, aspiranti e amici

| Campo | Valore |
| --- | --- |
| **Location** | Via Roma 1, 00000 Esempio |
| **Maps** | https://maps.app.goo.gl/esempio |
| **Dress code** | Smart casual |
| **Costo** | 30€ (in quota per i soci) — 40€ esterni |
| **Conferma entro** | Lunedì 13/09/2027 |
```

Con intestazione e Consiglio Direttivo. Quando usarlo: primo bollettino dell'anno, evento con molte informazioni pratiche.

## Stile compatto — bollettini successivi

```markdown
## Invito

**Giovedì 7 ottobre 2027, ore 18:30** — Visita in cantina.

Visita guidata alla cantina con degustazione, poi cena tutti insieme.

- Aperta a: Tablers, ex Tablers, aspiranti e amici

| Campo | Valore |
| --- | --- |
| **Location** | Cantina Esempio, Via dei Vigneti 2, 00000 Esempio |
| **Dress code** | Informale (scarpe comode) |
| **Costo** | 20€ (in quota per i soci) |
| **Prenotazione entro** | 04/10/2027 |
```

Senza Maps e senza intestazione. Quando usarlo: invito breve, scadenza come prenotazione.

## Differenze da ricordare

| Aspetto | Ricco | Compatto |
| --- | --- | --- |
| Scadenza | Conferma entro | Prenotazione entro |
| Maps | Sì | No |
| Intestazione + Consiglio Direttivo | Sì | No |
| Note pratiche | Molte | Solo "Aperta a" |

## Simulazione

Utente: "Mi fai il bollettino per la cena del 9 ottobre?"

1. Fase 0: trova la cartella evento `Anni sociali/2027-2028/Eventi/2027-10-09 Cena d'autunno/` (o chiede i dettagli); nell'indice dell'anno l'ultimo bollettino è il N.2, quindi propone il N.3.
2. Fase 1: chiede data di emissione (es. 2027-09-27) e titolo breve ("Cena d'autunno").
3. Fasi 2–5: intervista; probabilmente stile compatto.
4. Riepilogo con il percorso dei file → approvazione → nota salvata in `2027-10-09 Cena d'autunno/Bollettini/2027-09-27 Bollettino N.3 Cena d'autunno.md`.
5. `rtit bollettino --md "<quella nota>"`: DOCX e PDF nascono nella stessa cartella `Bollettini/`, senza copie altrove.
6. Aggiorna l'indice dell'anno e la sezione `## Bollettino ufficiale` della nota evento; propone di allegare il PDF su Tabler World.

# Calendario della tavola — riferimento

## Indirizzo iCal

Schema del feed pubblico:

```
https://calendar.google.com/calendar/ical/<id-calendario>/public/basic.ics
```

L'id si trova in Google Calendar → Impostazioni del calendario → «Integra calendario». Se la lettura risponde **403/404**, il calendario non è pubblico: rendilo pubblico (Autorizzazioni di accesso → Rendi disponibile pubblicamente) oppure usa l'**indirizzo segreto in formato iCal**. Quello segreto va trattato come una password: non condividerlo, e rigeneralo quando qualcuno esce dal direttivo.

## Abbinamento calendario ↔ archivio eventi

1. Stessa data: la `data` della nota evento, ovvero il prefisso della cartella `AAAA-MM-GG`.
2. Passo 1: abbina i titoli con somiglianza ≥ 0,4. Ogni cartella si abbina una sola volta, a partire dalle somiglianze più alte.
3. Passo 2: se in una data restano esattamente un evento di calendario e una cartella libera, li abbina anche se i titoli sono diversi (soprannomi, refusi).
4. Abbinati con somiglianza < 0,75 → `cambiato` (titolo da verificare).
5. Nessun abbinamento → `nuovo`. Cartelle senza evento in calendario → `solo_archivio`.

Gli eventi `CANCELLED` sono esclusi. La cache del feed dura 15 minuti (`--no-cache` per forzare).

## Decisioni persistenti

Quando l'utente dice "ignora questo evento", salva la decisione così non lo vedrà più nei report:

```bash
rtit decisioni ignora-calendario --titolo "Gita sociale di zona" --data 2027-09-18 --uid "<uid>" --motivo "non organizziamo noi"
```

Mostra sempre le decisioni salvate all'inizio di un report (`rtit cosa-fare` lo fa da solo).

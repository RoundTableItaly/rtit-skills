---
name: rt-evento
description: >-
  Organizza un evento della tavola dall'idea al saldo: nota evento, progetto (dati, checklist, cose da fare),
  invitati (conferme, quote, pagamenti) e spese (preventivo, margine, saldo), salvati nell'archivio condiviso.
  Usala per "organizziamo una cena", "nuovo evento", "chi ha confermato?", "quanto spendiamo?", "facciamo i
  conti della serata", "checklist evento". Per la data usa rt-calendario, per l'invito ufficiale
  rt-bollettino, per i social rt-comunicazione.
---

# Evento — progetto, invitati, spese

Il **pack evento** sono tre documenti accanto alla nota evento: `progetto.md` (dati, checklist, cose da fare), `invitati.md` (conferme e quote), `spese.md` (preventivo e saldo). Formato e regole: [references/pack.md](references/pack.md).

**Non** creare pack per ritrovi, sedute del direttivo o eventi "solo bollettino" (tipi di evento nella skill `rt-calendario`).

## Regole

- **Non inventare importi, conferme o date**: se un dato manca, chiedilo o lascia la cella vuota. Una conferma è "sì" solo se l'utente lo dice.
- **Conferma prima di scrivere**: mostra cosa verrà creato (cartella, file) e chiedi un sì esplicito **prima** di ogni comando con `--applica` o `--force`.
- Salva tutto nell'archivio condiviso, nella cartella dell'evento (struttura nella skill `rt-archivio`).

## Ordine consigliato (dal Manuale del Presidente)

1. **Data** senza sovrapposizioni → `rt-calendario` (punteggio Planner `N/100`).
2. **Nota evento + pack** → questa skill.
3. **Tabler World**: l'evento va caricato lì, dal portale, prima di pubblicizzarlo.
4. **Bollettino** → `rt-bollettino`.
5. **Social e foto** → `rt-comunicazione`.
6. Evento aperto agli **aspiranti**? Usa la scaletta della serata in `rt-crescita`.
7. Dopo l'evento: saldo spese, incassi, ricevute e foto in `Altri documenti/`, appunti per la relazione morale.

## Percorso A — solo chat

Crea in chat le tre tabelle (stesse colonne dei modelli in `references/pack.md`; nello zip della skill i modelli completi sono in `assets/`) e aggiornale a ogni messaggio dell'utente ("Mario conferma, paga con Satispay"). Calcola tu: confermati, in attesa, quote attese e incassate, totale spese con margine, saldo. Alla fine proponi di salvarle nell'archivio.

## Percorso B — archivio condiviso (CLI)

```bash
rtit evento nuovo --data 2027-10-09 --titolo "Cena d'autunno"            # anteprima (non scrive)
rtit evento nuovo --data 2027-10-09 --titolo "Cena d'autunno" --applica  # cartella + nota evento + Bollettini, Form, Altri documenti
rtit evento pack "<cartella evento>"          # crea progetto/invitati/spese (non sovrascrive mai)
rtit evento verifica "<cartella evento>"      # conformità + cose da fare aperte
rtit evento spese "<cartella evento>"         # conti: confermati, spesa, margine, incasso, saldo
```

- Le cartelle seguono `archivio.eventi` del profilo, per esempio `Anni sociali/2027-2028/Eventi/2027-10-09 Cena d'autunno/`.
- Se `rtit evento nuovo` si ferma con `blocked_similar`, esiste già una cartella con la stessa data o un nome simile: chiedi se è lo stesso evento prima di usare `--force`.
- `--senza-pack` crea un evento "solo bollettino" (`pack: none`).
- Modifica i file del pack con l'utente; dopo ogni modifica ricalcola con `rtit evento spese`.
- `--force` sul pack sovrascrive: usalo **solo** su richiesta esplicita.
- Moduli Google per le iscrizioni: link e, a evento chiuso, export delle risposte in `Form/`.

## Dati personali

`invitati.md` e le risposte ai form contengono nomi, pagamenti e a volte **intolleranze alimentari**, che sono dati sanitari. Tienile al minimo, non incollarle in un assistente cloud se non serve, cancellale dopo l'evento e non inviare l'elenco a terzi senza consenso.

## Collegate

- `rt-calendario` — scegliere e verificare la data.
- `rt-bollettino` — invito ufficiale dell'evento.
- `rt-comunicazione` — post, storie e foto dell'evento.
- `rt-archivio` — struttura della cartella evento, niente doppioni.
- `rt-crescita` — serata con aspiranti e prezzo degli eventi.
- `rt-cosa-fare` — cosa manca per i prossimi eventi.

---
name: rt-direttivo
description: >-
  Prepara convocazioni, ordini del giorno e verbali del direttivo e delle assemblee di tavola o di zona,
  tiene il registro delle decisioni e scrive il verbale di elezione da portare in banca e per la PEC; salva
  tutto nella cartella Direttivo dell'anno sociale. Usala per "convoca il direttivo", "ordine del giorno",
  "scrivi il verbale", "cosa abbiamo deciso su…", "verbale di elezione", "mettiamo a verbale". Per gli
  adempimenti del nuovo Presidente (Modello AA5, PEC, conto) usa rt-presidente.
---

# Direttivo — convocazioni, verbali, decisioni

Sedute del Consiglio Direttivo e assemblee dei soci della tavola (o Comitato di Zona e Assemblea di Zona, se il profilo ha `livello: zona`). Modelli pronti: [references/modelli.md](references/modelli.md).

## Prima di cominciare

1. **Profilo** (`rt-primi-passi`): tavola, direttivo con Presidente e Segretario, cartella `archivio.direttivo`. Se manca, chiedi il minimo: nome della tavola, chi presiede, chi verbalizza.
2. **Regole statutarie**: chi convoca, preavviso, quorum, maggioranze, chi vota. Le tavole non hanno uno statuto proprio: vale lo **Statuto nazionale** (riassunto qui sotto; testo nella skill `rt-conoscenza`, `references/statuto.md`) e, per i dettagli, il **regolamento di tavola**, se adottato (`Documenti legali/Statuto e regolamenti/`). **Non inventare** ciò che lo Statuto lascia al regolamento: se non lo trovi, scrivi "secondo il regolamento di tavola (da verificare)". Statuto e regolamento prevalgono sui modelli.
3. **Numero della seduta** (`N.X`): progressivo nell'anno sociale. Ricavalo dagli ultimi file in `Direttivo/` o chiedilo.

## Regole dello Statuto da ricordare

| | Assemblea di tavola | Consiglio Direttivo |
| --- | --- | --- |
| Quando | Ordinaria: almeno **25 giorni prima sia dell'HYM sia dell'AGM** (art. 44 c. 2). Straordinaria: quando il Direttivo lo ritiene necessario o lo chiede un terzo dei membri attivi | Almeno **4 volte** per anno sociale (art. 51) |
| Chi convoca e come | Il Presidente, su delibera del Direttivo, con raccomandata A/R o **email con conferma di lettura**, almeno **8 giorni prima**; l'avviso indica luogo, giorno, ora e OdG; la seconda convocazione può essere almeno un'ora dopo la prima (art. 46) | Modalità stabilite dal regolamento di tavola (art. 51 c. 1) |
| Chi vota | I membri attivi in regola con i contributi; delega scritta a un altro membro attivo, **una sola delega** a testa (art. 47 c. 1-2) | I componenti del Direttivo; il **Segretario partecipa senza diritto di voto** (art. 49 c. 6) |
| Quorum | Prima convocazione: tre quarti dei membri attivi, presenti o per delega; seconda: qualunque numero. Per regolamento e scioglimento: due terzi anche in seconda (art. 47 c. 3-4) | Metà più uno dei membri (art. 51 c. 2) |
| Maggioranze | Quelle del regolamento di tavola; due terzi per regolamento e scioglimento (art. 48) | Maggioranza dei presenti; a parità prevale il voto del Presidente (art. 51 c. 2) |

- Si vota per **alzata di mano**; le votazioni che riguardano **persone** (elezioni, ammissioni, espulsioni) sono sempre a **scrutinio segreto** (art. 77).
- L'Assemblea Ordinaria delibera su: ammissione ed espulsione dei soci, elezione del Direttivo, quota annuale, rendiconto, membri onorari (art. 45).
- I verbali del Direttivo e delle Assemblee sono **libri sociali obbligatori**, in digitale e caricati su Tabler World (art. 40).
- **Zona**: l'Assemblea di Zona la convoca il Presidente di Zona con 15 giorni di preavviso (raccomandata) o 10 (email con conferma di lettura); quorum di tre quarti in prima convocazione; il Comitato di Zona delibera con almeno metà dei membri (art. 68-70, 73). Dettagli nella skill `rt-presidente`, file `references/zona.md`.

## Flussi

### 1. Convocazione

Chiedi tipo di seduta, data, ora, luogo o link, ordine del giorno (OdG), destinatari e canale d'invio (per l'Assemblea: email con conferma di lettura o raccomandata A/R). L'OdG si apre con "Approvazione del verbale della seduta precedente" e si chiude con "Varie ed eventuali". Rispetta il preavviso (Assemblea: 8 giorni; Direttivo: secondo il regolamento di tavola, se non lo conosci segnalalo). Se la data dell'Assemblea Ordinaria cade a meno di 25 giorni dall'HYM o dall'AGM, avvisa. Consegna una **bozza**: invia l'utente. Con un connettore mail puoi creare la bozza, solo dopo un sì.

### 2. Verbale (durante o dopo la seduta)

Parti da appunti, dettatura o trascrizione. Raccogli:

- data, ora di inizio e fine, luogo; chi presiede e chi verbalizza;
- **presenze**: presenti, assenti giustificati e non, deleghe; **quorum** con la regola citata (tabella sopra);
- per ogni punto dell'OdG: sintesi della discussione, **delibera**, **voti** (favorevoli, contrari, astenuti);
- **azioni**: cosa, responsabile, scadenza.

Ciò che manca resta `[da completare]`. Il verbale è una **bozza** finché la seduta successiva non lo approva; lo firmano Presidente e Segretario (prassi; segui il regolamento di tavola, se c'è). Una volta approvato va caricato su Tabler World tra i libri sociali (art. 40).

### 3. Registro delle decisioni

Una tabella per anno sociale, aggiornata a ogni verbale approvato: data, seduta, decisione, voti, responsabile, scadenza, stato. Per "cosa abbiamo deciso su…" cerca prima nel registro, poi nei verbali, e cita seduta e data. Se non trovi nulla, dillo: non ricostruire a memoria. Il registro serve anche al passaggio di consegne (vedi la skill `rt-presidente`, file `references/passaggio-consegne.md`).

### 4. Verbale di elezione del nuovo direttivo

Serve al Presidente entrante per il **cambio di intestatario del conto** (copia firmata in banca), della **PEC** e per il **Modello AA5** (vedi `rt-presidente`). Le elezioni si fanno nell'Assemblea Ordinaria che precede l'AGM, almeno 25 giorni prima (art. 44, 45), a scrutinio segreto (art. 77). Si eleggono Presidente, Vice Presidente, Consiglieri, Corrispondente e Tesoriere; il Past President è di diritto; il **Segretario non si elegge**: lo nomina il Presidente eletto (art. 49). Contiene: assemblea, data, presenze e quorum, candidati, voti, eletti per carica, decorrenza del mandato (dal giorno dopo l'AGM fino all'AGM successivo: art. 49 c. 2, art. 76), firme. Subito dopo, il Segretario comunica la lista degli eletti al Segretario Nazionale (art. 78 c. 4). Il verbale sta in `Direttivo/`; la copia firmata consegnata in banca va in `Documenti legali/Banca/` (vedi `rt-archivio`).

## Regole

- **Verbali approvati immutabili**: non modificare il verbale di una seduta già approvata. Correzioni e seguiti vanno nel verbale della seduta corrente ("Rettifica al verbale N.X del…").
- **Non inventare** presenze, voti, importi, nomi o delibere: chiedi o lascia `[da completare]`.
- **Conferma prima di scrivere**: mostra testo, nome e percorso del file; salva solo dopo un sì esplicito. Non sovrascrivere file esistenti.
- **Dati personali**: nei verbali solo ciò che serve alla delibera; niente dati sanitari o dettagli privati. L'archivio è accessibile solo al direttivo.

## Dove salvare

Nella cartella `Anni sociali/{anno}/Direttivo/` (campo `archivio.direttivo` del profilo):

- `AAAA-MM-GG Convocazione Direttivo N.X.md`
- `AAAA-MM-GG Direttivo N.X.md` (verbale)
- `Registro delle decisioni AAAA-AAAA.md`

Per le assemblee usa "Assemblea" al posto di "Direttivo". La data è quella della seduta.

**Con terminale**: scrivi i file nella cartella sincronizzata (`rtit archivio struttura --applica` crea `Direttivo/` se manca). **Senza terminale**: consegna il testo in chat e, se c'è un connettore cloud (Drive, OneDrive, Dropbox), salvalo con quello dopo conferma; altrimenti l'utente lo incolla in un documento nella cartella.

## Collegate

- `rt-presidente` — adempimenti dopo l'elezione e passaggio di consegne.
- `rt-archivio` — struttura dell'archivio e cartella `Direttivo/`.
- `rt-cosa-fare` — sedute in calendario senza convocazione o verbale.
- `rt-primi-passi` — aggiornare il profilo con il nuovo direttivo.
- `rt-conoscenza` — Statuto, sigle (AGM, HYM, "CZ") e anno sociale.

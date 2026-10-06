# Se sei nel direttivo di zona

Per chi fa parte del Comitato di Zona (Presidente, Vice Presidente, Past President, Corrispondente, Tesoriere, Segretario) o ha un ruolo di zona come il P.R.O., con profilo `livello: zona`. Il Manuale del buon Presidente è scritto per le tavole: qui ci sono le regole dello Statuto sulla zona (art. 63-75, citate con l'articolo) e quelle del Manuale che la riguardano (§ = sezioni di [manuale-presidente.md](manuale-presidente.md)). Il resto è **(prassi consigliata, da confermare)**: prevalgono lo Statuto e le indicazioni del Comitato Nazionale. Non inventare date, importi o indirizzi.

## 1. Comitato di Zona e Assemblea di Zona

- **Comitato di Zona** (Statuto, art. 71-73): l'organo che amministra e dirige la zona. È composto **solo** da Presidente, Vice Presidente, Past President (di diritto), Corrispondente di Zona, Tesoriere e Segretario; il Presidente nomina Segretario e Gestore Materiali; non sono ammessi altri componenti né incarichi speciali (art. 72 c. 1-2). Delibera con almeno la metà dei membri presenti, a maggioranza; a parità prevale il Presidente (art. 73).
- **Assemblea di Zona** (art. 66-70): la riunione delle tavole della zona, a cui ogni tavola **deve partecipare** (§ 4.2). Nel parlato si dice "CZ" sia per l'Assemblea sia per il Comitato: scrivi **Assemblea di Zona** quando parli della riunione. Le due voci sono distinte nel glossario della skill `rt-conoscenza`.
- **P.R.O. di Zona**: è una **prassi consolidata** (ogni zona ne indica uno e il vademecum della comunicazione gli affida il raccordo tra tavole e nazionale). Lo Statuto non lo prevede (art. 72 c. 2): opera senza far parte del Comitato di Zona. Non confonderlo con il **Corrispondente di Zona**, che è la carica eletta (art. 72 c. 1 lett. d: articoli per le pubblicazioni nazionali).
- **Quando**: l'Assemblea di Zona si riunisce **almeno una volta prima di ogni Assemblea Nazionale** (art. 66 c. 2); in via straordinaria quando il Comitato lo ritiene opportuno o lo chiedono almeno tre tavole, entro 30 giorni dalla richiesta (art. 66 c. 1). Le date dell'anno non sono nello Statuto: chiedile. Proponi di fissarle presto e di verificarle nel Planner dell'App RTIT contro gli eventi delle tavole (skill `rt-calendario`) (prassi consigliata, da confermare).
- **Cosa fa** l'Assemblea ordinaria (art. 67): approva il rendiconto e i contributi delle tavole, elegge il Comitato di Zona, formula proposte al CN, adotta gli altri provvedimenti di competenza della zona.
- **Dopo**: il Segretario di Zona invia copia delle deliberazioni al Presidente Nazionale e al Segretario Nazionale entro 30 giorni, o le carica su Tabler World (art. 70 c. 6). I libri sociali della zona si tengono in digitale su TW (art. 65).
- Convocazioni e verbali del Comitato di Zona e dell'Assemblea di Zona: skill `rt-direttivo` (stessi modelli, con "Comitato di Zona" o "Assemblea di Zona" nel titolo), salvati in `Direttivo/` dell'anno sociale della zona.

## 2. Convocazione dell'Assemblea di Zona e deleghe delle tavole

- **Convocazione** (art. 68): la fa il Presidente di Zona, in accordo con il Comitato, con avviso scritto ai **Presidenti delle tavole**: raccomandata A/R almeno **15 giorni** prima, oppure email con conferma di lettura almeno **10 giorni** prima. L'avviso indica luogo, giorno, ora, ordine del giorno e ora della seconda convocazione (anche lo stesso giorno, almeno un'ora dopo). Indirizzi istituzionali dalla scheda della tavola nell'App RTIT (`get_organization_unit`, skill `rt-app-rtit`). Aggiungi le istruzioni per la delega (prassi consigliata).
- **Chi partecipa e vota** (art. 69): i membri del Comitato di Zona e, per ogni tavola, il **Presidente o il Vice Presidente**; un voto a testa. È valida in prima convocazione con i tre quarti degli aventi diritto al voto, in seconda con qualunque numero.
- **Delega** (art. 69 c. 1; § 4.2): se Presidente e Vice sono impediti, partecipa un altro **membro attivo della stessa tavola**, nominato dal suo Consiglio Direttivo, con **delega scritta firmata dal Presidente** (o, se impedito, dal Vice Presidente o da un altro membro del Direttivo). Si manda al **Segretario di Zona via email** (prassi: lo Statuto chiede solo la delega scritta). Modello in [modelli.md](modelli.md) § 1.
- Il Segretario di zona tiene un elenco (prassi consigliata, da confermare): tavola, presente o delegata, delegato, delega ricevuta, quote di zona in regola. Una delega con delegato di un'altra tavola va segnalata come non ammessa.

## 3. Report sullo stato delle tavole

Con l'App RTIT (server MCP; vedi la skill `rt-app-rtit`):

| Domanda | Strumento |
| --- | --- |
| Quante tavole attive ha la zona, quanti eventi quest'anno rispetto all'anno scorso? | `get_organization_unit_statistics(slug="zona-esempio", year="current")` |
| Quali tavole della zona? | `list_organization_units(parent="zona-esempio")` o `get_organization_tree` |
| Tavole senza eventi, confronto con le altre zone | `get_statistics(year="current")` |
| Prossimi eventi delle tavole della zona | `search_events(zone=…, start_date=…, end_date=…)` |

Come presentarlo:

- **con tatto**: sono indicatori, non giudizi. L'App vede solo gli eventi pubblici su Tabler World: una tavola "senza eventi" può averne fatti di interni o non averli caricati;
- per ogni tavola: eventi pubblicati, differenza con l'anno precedente, preavviso medio; poi 2–3 proposte di aiuto (intertavola, workshop RTIT University, skill `rt-crescita`);
- cita il link `url` delle schede; non riportare numeri che l'App non restituisce;
- il report resta al Comitato di Zona: non diffonderlo alle tavole senza decisione del Comitato (prassi consigliata, da confermare).

Mancano all'App le quote e gli adempimenti delle tavole: chiedili al Tesoriere e al Segretario di zona.

## 4. Quote di zona

- I contributi di zona li delibera l'**Assemblea di Zona** nella prima riunione dell'esercizio (Statuto, art. 74 c. 1; art. 67 lett. a). Per il versamento vale l'art. 33, "ove applicabile" (art. 74 c. 2): **prima rata, 50%, entro il giorno prima dell'HYM**; **saldo, 50%, entro il 28 febbraio** (§ 4.1). Le sanzioni dell'art. 33 (voto e parola all'Assemblea Nazionale, pubblicazioni, scioglimento) sono scritte per le quote nazionali: per quelle di zona non darle per certe.
- Il Tesoriere di zona tiene lo stato dei pagamenti per tavola (prassi consigliata, da confermare): tavola, prima rata, saldo, data, note. Importi e coordinate: quelli deliberati dall'Assemblea di Zona, mai stimati.
- **Rendiconto di zona** (art. 75): lo compila il Tesoriere di Zona uscente con quello in carica, con il visto dei Revisori dei Conti e un preventivo di spesa fino a fine anno sociale; il Comitato lo presenta all'Assemblea di Zona. Copia ai Presidenti delle tavole **almeno 15 giorni prima** dell'Assemblea.
- Solleciti: testi cortesi, inviati dal Tesoriere o dal Presidente di zona alla mail istituzionale della tavola. Struttura del rendiconto in [tesoreria.md](tesoreria.md).

## 5. Bollettino di zona

Per gli eventi di zona usa la skill `rt-bollettino` con il profilo `livello: zona`: intestazione della zona e destinatari "e p.c." di default (Nazionale e Presidenti delle tavole della zona). L'evento va prima caricato su Tabler World, dal portale. Loghi per eventi di zona: skill `rt-logo`.

## 6. Calendario di zona e collisioni

- Prima di fissare un evento di zona o l'Assemblea di Zona, controlla le collisioni con gli eventi delle tavole e con quelli nazionali: Planner dell'App RTIT, punteggio `N/100` (skill `rt-calendario`).
- Per scovare collisioni tra tavole della zona in un periodo: `scan_conflicts(start_date=…, end_date=…)` (skill `rt-calendario`). Restituisce le sovrapposizioni di tutta Italia: tieni solo quelle che coinvolgono le tavole della zona e segnalale ai Presidenti interessati con un messaggio neutro (prassi consigliata, da confermare).
- Proponi un calendario di zona condiviso all'inizio dell'anno sociale, con Assemblee di Zona, eventi di zona e date di HYM e AGM (prassi consigliata, da confermare).

## 7. Adempimenti del Comitato di Zona

- **Elezioni e cariche** (Statuto, art. 72, 78): il Comitato di Zona è eletto ogni anno dall'Assemblea di Zona tra i membri attivi candidati dalle tavole attraverso i loro Presidenti; le candidature si presentano al Segretario di Zona fino all'inizio dell'Assemblea. Subito dopo le elezioni il Segretario di Zona comunica gli eletti al **Segretario Nazionale** (art. 78 c. 4). Il nuovo Comitato entra in carica il **giorno dopo l'AGM** (art. 78 c. 1). Il Presidente di Zona deve essere già stato Presidente di tavola (art. 72 c. 6).
- Il Manuale non elenca adempimenti legali specifici per la zona. Se la zona ha codice fiscale, PEC e conto propri, valgono per analogia Modello AA5, PEC e intestatario del conto con verbale di elezione (§ 3.1–3.3) e la checklist di [passaggio-consegne.md](passaggio-consegne.md) (da verificare con il CN).

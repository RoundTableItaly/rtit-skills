# Tesoreria della tavola

Per il Presidente e il Tesoriere. Le regole citate vengono dallo Statuto (con l'articolo) e dal Manuale del buon Presidente (§ = sezioni di [manuale-presidente.md](manuale-presidente.md); RO = punti di [regole-operative.md](regole-operative.md)). Le voci senza fonte sono **(prassi consigliata)**. Prevale lo Statuto; per i dettagli che lascia alla tavola vale il regolamento di tavola, se adottato.

**Regole ferme**: non inventare importi, quote o saldi (chiedili o lasciali vuoti); non dare consulenza fiscale (rimanda al commercialista o al CAF, e alla Knowledge Base di Tabler World per i dati della Fondazione); conferma prima di scrivere file.

## 1. Rendiconto annuale e preventivo

- **Regola dello Statuto** (art. 53; art. 45 c. 1 lett. e): il **Tesoriere** compila il **rendiconto annuale**, che comprende un **preventivo di spesa** fino alla fine dell'anno sociale; il **Consiglio Direttivo** lo presenta all'**Assemblea Ordinaria**, che lo approva (§ 3.4, RO 9).
- Nei **15 giorni prima** dell'Assemblea, e fino al giorno dell'Assemblea, rendiconto e giustificativi restano a disposizione dei membri attivi presso il Tesoriere (art. 53 c. 3).
- Dopo l'approvazione va **inviato al Segretario Nazionale e/o caricato su Tabler World** (art. 53 c. 2); il libro dei rendiconti è tra i libri sociali da tenere su TW (art. 40).
- **Quando**: lo Statuto non fissa una data propria. L'Assemblea Ordinaria si tiene almeno 25 giorni prima dell'HYM e dell'AGM (art. 44 c. 2); la bozza di Regolamento di Tavola dell'Annuario 2025-2026 mette il rendiconto nell'Assemblea che precede l'AGM. Se la tavola ha un regolamento, segui quello; altrimenti chiedi.
- Il Manuale parla di "bilancio preventivo" e "bilancio consuntivo" presentati dal Presidente, senza dire quando: è la stessa cosa detta con altre parole; vale lo Statuto.
- Contenuto minimo (prassi consigliata): entrate (quote dei soci, incassi degli eventi, contributi, sponsor), uscite (quote nazionali e di zona, costi degli eventi, service, materiali, spese bancarie), saldo iniziale e finale del conto.
- L'approvazione va a verbale (skill `rt-direttivo`).

## 2. Quote dei soci

- La **misura della quota annuale** la decide l'Assemblea Ordinaria (Statuto, art. 45 c. 1 lett. d); modalità di versamento e sanzioni per il ritardo le delibera l'Assemblea (art. 52 c. 3). **Non stimarle**: leggile nel verbale che le ha fissate o nel regolamento di tavola, oppure chiedile.
- I fondi della tavola li amministra il **Tesoriere** (art. 52 c. 2).
- Tieni un elenco per anno sociale (prassi consigliata): socio, quota dovuta, pagato (`sì`/`no`), data, metodo. Salvalo in `Tesoreria/` (`Quote soci AAAA-AAAA.md` o foglio di calcolo).
- All'Assemblea di tavola votano solo i membri attivi **in regola con i contributi** (art. 47 c. 1).
- Solleciti: prepara testi brevi e cortesi, da inviare a cura del Tesoriere; non inoltrare l'elenco dei morosi a chi non è nel direttivo.

## 3. Quote nazionali e di zona

| Rata | Scadenza | Fonte |
| --- | --- | --- |
| Prima rata, **50%**, delle quote nazionali **e** di zona | **entro il giorno prima dell'HYM** (il Manuale dice "entro la data dell'HYM": vale lo Statuto) | Statuto, art. 33; per la zona art. 74 c. 2; § 4.1; RO 10 |
| Seconda rata, **50%**, delle quote nazionali **e** di zona | **entro il 28 febbraio** | Statuto, art. 33; § 4.1; RO 10 |

- Chi non paga una rata nei termini è sospeso dal **diritto di voto e di parola** all'Assemblea Nazionale successiva e non riceve le pubblicazioni nazionali (art. 33 c. 2); non può presentare candidature al CN (art. 17 c. 3). Oltre **60 giorni** di ritardo il CN può dichiarare sciolta la tavola (art. 33 c. 3). Il CN può concedere una proroga per motivi eccezionali.
- Coordinate di pagamento: non sono in nessuna fonte, chiedile al Tesoriere Nazionale o di zona. I contributi di zona li delibera l'Assemblea di Zona (art. 74 c. 1).
- Conserva ricevute e contabili in `Tesoreria/`.

**Quanto si paga al nazionale** (nota "Calcolo quote" del Comitato Nazionale, ottobre 2026; testo completo nel manuale, § 4.1). Gli importi li stabilisce il CN (art. 32) e possono cambiare: **verifica quelli dell'anno**.

- Si conta **ogni Tabler che compare in Annuario** nella tavola; la quota è a carico della tavola.
- Listino: soci **125,00 €**; ex-soci, soci d'onore di tavola (a vita o per l'anno) e Grandi amici **62,50 €**.
- **Esenti**: soci che alla data dell'AGM non hanno ancora compiuto 25 anni; soci d'onore a vita Round Table Italia; titolari della Targa dell'Amicizia "Lucien Paradis"; soci d'onore alla memoria; tavole in formazione.
- Un Tabler entrato quest'anno paga, se è in Annuario. Un Tabler di un'altra tavola che è socio onorario o Grande amico della tua, e compare in Annuario nella tua tavola, viene contato anche nelle tue quote.
- Il calcolo parte **dai dati di Tabler World**: l'anagrafica aggiornata è ciò che rende giuste le quote (§ 5).

## 4. Rendiconto di un evento

Parti dal pack dell'evento (skill `rt-evento`):

- con terminale: `rtit evento spese "<cartella evento>"` dà **incasso** atteso, **spese** (subtotale), **buffer** (margine) e **saldo**;
- senza terminale: ricostruisci gli stessi totali dalle tabelle di `invitati.md` e `spese.md`.

Dopo l'evento sostituisci il preventivo con i costi effettivi (ricevute in `Altri documenti/` dell'evento) e riporta il risultato nel rendiconto dell'anno.

## 5. Rendiconto dei service

Per ogni service (prassi consigliata): obiettivo e beneficiario, fondi raccolti per canale (eventi, donazioni dirette, tramite Fondazione), costi sostenuti, somma versata al beneficiario, data e prova del versamento. Usalo anche per la relazione morale.

## 6. Donazioni tramite la Fondazione

- Ogni tavola può usare la **Fondazione Round Table Italia Ente Filantropico** per i service (§ 10, RO 33).
- La Fondazione **trattiene il 2%** su ogni donazione in entrata: tienine conto nei preventivi (RO 34). Esempio fittizio: su € 1.000 donati arrivano al progetto € 980.
- Dati per bonifici e 5×1000: solo quelli del § 10, da verificare sulla Knowledge Base prima di comunicarli (RO 35).
- Vantaggi fiscali per i donatori (art. 83 D.Lgs. 117/2017; § 10, RO 33): persone fisiche, **detrazione del 30%** su donazioni fino a 30.000 € l'anno **oppure deduzione** fino al 10% del reddito complessivo dichiarato; enti e società, solo deduzione. Le due non si cumulano; servono pagamento tracciabile e ricevuta. Per limiti e casi specifici **nessuna consulenza**: rimanda al commercialista o al CAF (RO 36).

## 7. Dove salvare

Nella cartella `Anni sociali/{anno}/Tesoreria/` (campo `archivio.tesoreria` del profilo), con la data ISO in testa quando il documento è legato a un giorno:

- `Rendiconto annuale AAAA-AAAA` (con il preventivo di spesa)
- `Quote soci AAAA-AAAA`
- `AAAA-MM-GG Quote nazionali e di zona - prima rata` · `… - saldo` (con la ricevuta)
- `AAAA-MM-GG Rendiconto Nome evento` · `AAAA-MM-GG Rendiconto service Nome service`

Le ricevute di un evento restano nella sua cartella (`Altri documenti/`): niente copie (skill `rt-archivio`).

## 8. Modello di rendiconto

Esempio fittizio per la "Cena d'autunno". Gli importi sono inventati: in un rendiconto vero vengono solo da `spese.md`, `invitati.md` e ricevute.

```markdown
# Rendiconto — 2027-10-09 Cena d'autunno — Round Table N.99 Esempio

Stato: [preventivo / consuntivo]   Redatto da: [Tesoriere]   Data: [AAAA-MM-GG]

## Entrate

| Voce | Quantità | Importo unitario (€) | Totale (€) | Note |
| --- | --- | --- | --- | --- |
| Quote soci | 18 | 40,00 | 720,00 | da invitati.md |
| Quote ospiti | 6 | 45,00 | 270,00 | |
| Contributo sponsor | 1 | 200,00 | 200,00 | ricevuta in Altri documenti/ |
| **Totale entrate** | | | **1.190,00** | |

## Uscite

| Voce | Quantità | Importo unitario (€) | Totale (€) | Note |
| --- | --- | --- | --- | --- |
| Cena (per persona) | 24 | 38,00 | 912,00 | fattura del locale |
| Stampa locandine | 1 | 40,00 | 40,00 | |
| Omaggio al relatore | 1 | 35,00 | 35,00 | |
| **Subtotale** | | | **987,00** | |
| Buffer (10%) | | | 98,70 | solo nel preventivo |
| **Totale uscite** | | | **987,00** | nel consuntivo, senza buffer |

## Saldo

| | € |
| --- | --- |
| Entrate | 1.190,00 |
| Uscite | 987,00 |
| **Saldo** | **203,00** |
| Destinazione del saldo | [cassa della tavola / service …] (delibera del direttivo N.[X]) |
```

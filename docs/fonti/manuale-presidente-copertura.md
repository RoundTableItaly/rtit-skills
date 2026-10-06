# Copertura: Manuale del buon Presidente

> Fonte: Manuale del buon Presidente — Comitato Nazionale RTIT (edizione 2025/26). Distillato per uso con assistenti AI; in caso di dubbio prevale il documento ufficiale.

Mappa di dove è finita ogni parte del PDF originale (10 pagine fisiche: copertina + pagine stampate 1–9) nei file della skill `rt-presidente`. Percorsi relativi a questa cartella.

Dopo l'[audit sullo Statuto](audit-statuto-2026.md) (ottobre 2026) MP e RO contengono anche regole che **non vengono dal Manuale**: sono citate con l'articolo dello Statuto o con il regolamento dell'Annuario 2025-2026 ed elencate più sotto. Dove il Manuale dice una cosa diversa vale lo Statuto, con una nota sul conflitto.

File di destinazione:

- MP = [manuale-presidente.md](../../skills/rt-presidente/references/manuale-presidente.md)
- RO = [regole-operative.md](../../skills/rt-presidente/references/regole-operative.md)

File operativi aggiunti con la versione 0.2.0: non distillano altre parti del PDF, ma riprendono MP e RO per un compito preciso (vedi "File operativi della 0.2.0" più sotto).

- MOD = [modelli.md](../../skills/rt-presidente/references/modelli.md)
- PC = [passaggio-consegne.md](../../skills/rt-presidente/references/passaggio-consegne.md)
- TES = [tesoreria.md](../../skills/rt-presidente/references/tesoreria.md)
- ZONA = [zona.md](../../skills/rt-presidente/references/zona.md)

Metodo di estrazione: testo con `pdftotext -layout`; link dalle annotazioni `/Annots → /A → /URI` di ogni pagina (pypdf), associati al testo blu del link guardando le pagine renderizzate; ogni pagina renderizzata in PNG e controllata a vista. Non ci sono tabelle, box o testo dentro immagini: le uniche immagini sono il logo Round Table Italia in copertina e nell'intestazione delle pagine.

## Mappa sezione per sezione

| Pagina PDF (stampata) | Sezione della fonte | Destinazione | Note |
| --- | --- | --- | --- |
| 1 (copertina) | Logo, titolo "Manuale del buon Presidente", sottotitolo "Guida operativa per la gestione della Tavola", "Round Table Italia — Edizione Aggiornata" | MP titolo e introduzione; intestazione di tutti i file | Autore: "Comitato Nazionale", come nella fonte |
| 2 (p. 1) | Introduzione: scopo della guida (Presidenti, Vice, tutti i tabler), adempimenti, link FAQ su TW, tips, opportunità | MP introduzione | Aneddoto personale dell'autore e firma rimossi (vedi sotto) |
| 3 (p. 2) | Cap. 1 Adempimenti legali — 1.1 Variazione legale rappresentante (Modello AA5) | MP § 1 riga 1, § 2, § 3.1, § 12 link 1; RO 7; PC § 3 | |
| 3 (p. 2) | 1.2 Variazione PEC (contestuale, Knowledge base TW) | MP § 1 riga 2, § 3.2, § 12 link 2; RO 7 | |
| 3 (p. 2) | 1.3 Variazione intestatario conto corrente (intestato all'associazione, verbale firmato) | MP § 1 riga 3, § 3.3; RO 7, 8 | |
| 4 (p. 3) | Cap. 2 Aggiornamenti TW — 2.1 Aggiornamento annuario (Editore Nazionale, bozza da TW, FAQ, archivio digitale) | MP § 1 riga 4, § 5.1, § 12 link 3–4; RO 15 | Titolo originale con refuso "Aggiornamentoannuario" |
| 4 (p. 3) | 2.2 Nuovo socio: pergamena (firmata da Presidente Nazionale ed Editore Nazionale), modulo prima della pinnatura, welcome kit all'AGM solo a chi è nel form | MP § 1 riga 5, § 7.1, § 12 link 5; RO 14 | |
| 4 (p. 3) | 2.3 Eventi su TW (dal 2025, canali RT Events/TW/Mail/WhatsApp, ragioni statistiche/storiche/pubblicitarie, app, istruzioni) | MP § 1 riga 6, § 6.2, § 6.3, § 8, § 12 link 6–7; RO 16 | |
| 5 (p. 4) | Cap. 3 Editoria — 3.1 Relazione morale (documento più importante, libro delle relazioni, 60 giorni dall'AGM o data dell'Editore Nazionale, archivio) | MP § 1 riga 12, § 2, § 3.5, § 12 link 8; RO 31, 32; MOD § 4; PC § 10 | Termine corretto con lo Statuto, art. 49 c. 8: non oltre il 60° giorno **prima** dell'AGM |
| 6 (p. 5) | Cap. 4 Vita di Tavola — 4.1 Calendario e bollettino (due incontri al mese da Statuto, tipi di serata, data fissa in annuario, partecipazione obbligatoria, assenze giustificate, programmazione anticipata, statistiche/planner/monitoraggio/ranking, bollettino obbligatorio, modello, riassunto pubblicità) | MP § 1 riga 16, § 2, § 6.1, § 6.2, § 6.4, § 12 link 9–13; RO 17–20 | "Due incontri al mese" e "partecipazione obbligatoria" precisati con lo Statuto, art. 54 (20 riunioni minime; obbligo di 6 riunioni e 1 manifestazione nazionale) |
| 6 (p. 5) | 4.2 Tips per la crescita (slide, guida LinkedIn, Isole Faroe, stringa Google) | MP § 7.2, § 12 link 14–16 | Stringa Google riportata invariata |
| 6 (p. 5) | 4.3 Bilancio preventivo e consuntivo | MP § 1 righe 7–8, § 3.4; RO 9; TES § 1 | Affiancato dal rendiconto dello Statuto, art. 53 e 45 |
| 7 (p. 6) | 4.4 Cerimoniale (forma è sostanza, ordine dei saluti, istruzioni conviviali, direttive saluti) | MP § 9.1, § 12 link 17–18; RO 29 | Rimando alla sintesi del cerimoniale dell'Annuario |
| 7 (p. 6) | 4.5 Intertavola e interclub (più Tavole anche di zone diverse, Rotaract, Leo Club) | MP § 6.5; RO 19 | Esempio con tavole nominate generalizzato |
| 7 (p. 6) | 4.6 Quote associative (anticipo entro HYM, saldo 28 febbraio, perdita del voto) | MP § 1 righe 9–10, § 2, § 4.1; RO 10; TES § 3; ZONA § 4 | Scadenza e conseguenze secondo lo Statuto, art. 33 (giorno prima dell'HYM; voto e parola) |
| 7 (p. 6) | 4.7 HYM, AGM e CZ (obbligatorietà, delega via PEC, firma autografa, documento, solo Tabler della propria Tavola; scheda eventi nazionali; candidature CN con 6 dati, firma del Presidente, documento) | MP § 1 righe 11, 13, 14, § 4.2–4.4, § 12 link 19; RO 11–13; MOD § 1–3; ZONA § 1–2 | "CZ" reso con Assemblea di Zona; deleghe secondo art. 13 e 69; candidature secondo art. 17 (PEC, firma del Presidente e documento restano come prassi del Manuale) |
| 7 (p. 6) | 4.8 Regolamento furti (stendardo, campana, roll-up; altro vietato) | MP § 9.3, § 12 link 20; RO 30 | Completato con il Regolamento furti dell'Annuario |
| 7–8 (p. 6–7) | 4.9 Loghi, pin e grafiche (Statuto, intervento CN, pin/coin via CN@roundtable.it con colori, rondella, volantini e bollettini, campagne internazionali e Canva PRO, logo nazionale solo eventi nazionali, manuale, loghi di Tavola su TW) | MP § 1 riga 15, § 9.2, § 12 link 21–22; RO 23–28 | Logo nazionale precisato con lo Statuto, Titolo IX punto 2 |
| 8 (p. 7) | 4.10.1 Reciprocità e Travel Bingo | MP § 2, § 6.6, § 12 link 23; RO 22 | Sigla IRO sciolta con lo Statuto (art. 17); condizioni dall'Annuario |
| 8 (p. 7) | 4.10.2 Travel Fund Gambetti | MP § 2, § 6.6, § 7.1, § 12 link 24; RO 14 | Condizioni dal regolamento in Annuario (35 anni, 30 aprile, 15 maggio, estrazione all'AGM) |
| 8 (p. 7) | 4.10.3 Lotteria Eventi (scambio ingressi, sorteggio, di norma all'HYM) | MP § 2, § 6.6, § 12 link 25; RO 21 | Termini dal regolamento in Annuario (10 giorni prima dell'HYM) |
| 8 (p. 7) | 4.11.1 Assicurazione nazionale (dal 2025, RC verso terzi, eventi ufficiali, polizza annuale) | MP § 11; RO 37 | |
| 8 (p. 7) | 4.11.2 Canva PRO (profilo per ogni Tavola, accesso con mail di Tavola, stemmi e grafiche) | MP § 9.2, § 11; RO 25, 26; PC § 6 | Accesso con la mail di Tavola; se manca, invito del P.R.O. Nazionale (audit, decisione 14) |
| 9 (p. 8) | 4.11.3 Mail di Tavola (Microsoft 365 Business Basic: 50 GB, 1 TB OneDrive, Teams, calendari condivisi; istruzioni) | MP § 11, § 12 link 26; RO 27 | |
| 9 (p. 8) | 4.11.4 eCommerce (shop ufficiale) | MP § 11, § 12 link 27; RO 38 | |
| 10 (p. 9) | Cap. 5 Fondazione — 5.1 Vantaggi fiscali (service, RUNTS dal 2024, 5x1000, uso da parte di tutte le Tavole, detrazione 30% fino a 30.000 euro, deduzione 10% per persone fisiche, trattenuta 2%, IBAN, denominazioni, CF, Knowledge Base) | MP § 10, § 11, § 12 link 28; RO 33–36; TES § 6 | Dati istituzionali della Fondazione mantenuti; regola fiscale e nome del RUNTS secondo l'audit (decisioni 26-27) |
| Tutte | Annotazioni ipertestuali: 33 gruppi di annotazioni, **28 URL distinti** | MP § 12 (tutti i 28, con pagina) | `%5F` scritto come `_` nei link S3 (stesso indirizzo) |
| Tutte | Intestazione di pagina con logo, numeri di pagina | Rimossi | Solo impaginazione |

## Integrazioni che non vengono dal Manuale

| Contenuto | Fonte | Destinazione |
| --- | --- | --- |
| Anno sociale, finestre di AGM, HYM e Assemblea di Zona | Statuto, art. 76, 9, 10, 66 | MP § 2; RO 3, 6; ZONA § 1 |
| "CZ" = Assemblea di Zona (riunione) e Comitato di Zona (organo) | Statuto, art. 66-69 e 71-72 | MP convenzioni, § 4.2; RO 11; ZONA § 1 |
| Eletti comunicati al Segretario Nazionale; riunione congiunta entro 30 giorni dall'AGM | Statuto, art. 78 c. 3-4 | MP § 1 righe 17–18, § 2; RO 39; PC "Quando" e § 3 |
| Assemblea Ordinaria 25 giorni prima di HYM e AGM; rapporto riassuntivo | Statuto, art. 44 c. 2, art. 50 c. 2 | MP § 1 righe 19–20, § 2, § 3.5, § 4.2; RO 41 |
| Comunicazione di ammissioni e dimissioni; libri sociali; Direttivo 4 volte l'anno; regolamento di Tavola (lo approva il Comitato Nazionale: audit, decisione 45) | Statuto, art. 50 c. 1, 40, 51, 43 | MP § 1 righe 21–24, § 7.3; RO 42, 44; PC § 5 |
| Relazione trimestrale | Annuario 2025-2026 | MP § 1 riga 25, § 2; RO 44 |
| Rendiconto di Tavola | Statuto, art. 53, 45 | MP § 1 righe 7–8, § 3.4; RO 9; TES § 1; PC § 4 |
| Quote: rate, sanzioni, scioglimento | Statuto, art. 33, 17, 74 | MP § 1, § 4.1; RO 10; TES § 3; ZONA § 4; PC § 4 |
| Calcolo delle quote nazionali: chi si conta, listino, esenzioni | Nota "Calcolo quote" del Comitato Nazionale (audit, decisione 44); Statuto, art. 32 | MP § 4.1; RO 10; TES § 3 |
| Quote dei soci: misura, modalità e sanzioni decise dall'Assemblea; fondi amministrati dal Tesoriere | Statuto, art. 45 c. 1 lett. d, art. 52 | TES § 2 |
| Deleghe nazionali e di Zona | Statuto, art. 13, 69; audit, decisione 8 | MP § 4.2; RO 11; MOD § 1; ZONA § 2 |
| Candidature al CN | Statuto, art. 17; audit, decisione 7 | MP § 1 riga 14, § 4.4; RO 13; MOD § 3 |
| Riunioni minime e obbligo di presenza | Statuto, art. 54 | MP § 6.1; RO 19, 20 |
| Requisiti, ammissione, uscita, membri onorari, dimensione della Tavola, composizione del Direttivo, Corrispondente e P.R.O. | Statuto, art. 58-60, 62, 45, 39, 49, 16 c. 3; Annuario (mansionario) | MP § 7.3; RO 40, 42, 43; ZONA § 1 (P.R.O. di Zona come prassi) |
| Scioglimento della Tavola sotto i sei membri attivi | Statuto, art. 55-56; audit, decisione 45 | MP § 7.3; RO 43 |
| Zona: composizione del Comitato, convocazione, quorum e compiti dell'Assemblea di Zona, rendiconto, elezioni | Statuto, art. 63-75, 78 | ZONA § 1, 2, 4, 7 |
| Furti, Travel Fund Gambetti, Lotteria eventi, Reciprocità, cerimoniale | Annuario 2025-2026 | MP § 6.6, § 9.1, § 9.3; RO 14, 21, 22, 29, 30 |
| Regola fiscale delle donazioni, RUNTS, 5x1000 | Audit, decisioni 26-27 | MP § 10; RO 33, 36; TES § 6 |

## File operativi della 0.2.0

| File | Contenuto | Da dove viene |
| --- | --- | --- |
| MOD | Testi pronti: delega, candidatura della tavola a un evento nazionale, candidatura al CN, struttura della relazione morale | MP § 3.5, § 4.2–4.4; RO 11–13, 31–32; Statuto, art. 13, 17, 49 c. 8, 54 c. 6, 69 |
| PC | Checklist unica del passaggio di consegne | Statuto, art. 78 c. 3-5; MP § 1–5, § 11; RO 6–10, 39; il resto è prassi consigliata, segnata come tale |
| TES | Rendiconto, quote dei soci, quote nazionali e di zona, rendiconti di eventi e service, Fondazione | Statuto, art. 32, 33, 45, 52, 53; MP § 3.4, § 4.1, § 10; RO 9–10, 33–36 |
| ZONA | Comitato di Zona, Assemblea di Zona, report sulle tavole, quote e calendario di zona | Statuto, art. 63-75, 78; MP § 4.1–4.2; strumenti dell'App RTIT; il resto è prassi consigliata |

I modelli della skill `rt-direttivo` (convocazioni, verbali, verbale di elezione) non vengono dal Manuale: seguono lo Statuto, art. 40, 44-51, 77, 78.

Gli eventi si caricano su Tabler World dal portale: MP, RO e i file sopra non rimandano più a una skill o a comandi dedicati.

## Punti chiusi dall'audit

Erano segnalati "(da verificare)" e ora hanno una regola: momento del rendiconto (art. 53, 45); anno sociale e finestre di HYM, AGM e Assemblea di Zona (art. 76, 9, 10, 66); AGM di riferimento e termine della relazione morale (art. 49 c. 8); termine e contenuti delle candidature al CN e documento d'identità del candidato (art. 17; decisione 7); destinatario della delega (art. 13; decisione 8); segnaposto `tavola@roundtable.it` (decisione 14); tetto di 30.000 euro riferito alla donazione (decisione 26); login a Tabler World sempre richiesto (decisione 16); "almeno in Italia" nei furti (Regolamento furti); destinatario della delega per l'Assemblea di Zona e documento d'identità nelle candidature, che in MOD e ZONA erano "da verificare" (decisioni 7 e 8); regole di convocazione, quorum e voto di Assemblee e Direttivo, che in `rt-direttivo` rimandavano a uno "Statuto della tavola" (art. 44-51, 77).

## Punti ancora "(da verificare)" in MP

- Scadenza e canale della scheda di candidatura a eventi nazionali (§ 1 riga 13, § 4.3).
- Se "modulo" (pergamena) e "form online" (welcome kit) sono lo stesso form (§ 7.1).
- Versione del manuale loghi linkato (AS 2024-2025, v2) (§ 9.2).
- Limiti alle detrazioni per i redditi sopra 75.000 euro (§ 10).
- Coordinate di pagamento delle quote: non sono in nessuna fonte (§ 4.1). Gli importi e le regole di calcolo vengono dalla nota "Calcolo quote" del Comitato Nazionale (ottobre 2026), non dal Manuale: vanno verificati ogni anno.

## Anomalie dei link nel PDF

- p. 5: la parte finale del testo "riassunto di tutte le indicazioni pubblicitarie" è coperta in parte anche dall'area del link al modello di bollettino (`documents/38570`). Attribuzione scelta in base allo slug: "pubblicizzare-un-evento" per il riassunto, `documents/38570` per "TablerWorld" (modello).
- p. 5: le aree dei link "statistiche RT", "planner" e "monitoraggio" sono duplicate su due righe (probabile residuo di reimpaginazione); gli URL sono comunque univoci.
- p. 6: il testo "direttive per i saluti" è collegato in parte a `cerimoniale-saluti` e in parte a `cerimoniale-delle-riunioni-conviviali`. Attribuito a `cerimoniale-saluti` in base allo slug.
- p. 7: la prima menzione del "manuale sull'utilizzo dei loghi" non ha link; la seconda ("manuale") sì. Usato lo stesso URL per entrambe.

## Dati personali rimossi o generalizzati

- Nome e cognome del Presidente Nazionale firmatario dell'introduzione → rimossi; resta "il Comitato Nazionale".
- Aneddoto personale dell'autore con riferimenti alla sua tavola di provenienza → rimosso (non operativo).
- Esempio di evento intertavola con numero e nome di tre Tavole → generalizzato in "una festa della birra organizzata congiuntamente da tre Tavole di zone diverse".
- Anno sociale della firma ("Comitato Nazionale" di un anno specifico, "Presidente RTIT" di un anno specifico) → tenuto solo come versione della fonte nell'intestazione.
- Nessun telefono, email personale o indirizzo di casa presente nella fonte.

Mantenuti perché istituzionali o pubblici: `CN@roundtable.it`, il segnaposto `tavola@roundtable.it`, i 28 link ufficiali, IBAN e codice fiscale della Fondazione (ente), il nome "Travel Fund Gambetti" (denominazione ufficiale di un'iniziativa), il link tabler.wiki sulla fondazione di una Tavola alle Isole Faroe (pagina pubblica).

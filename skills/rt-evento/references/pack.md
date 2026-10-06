# Pack evento — formato standard (versione 1)

Verificato da `rtit evento verifica` e da `rtit cosa-fare`.

## Struttura

```
<archivio condiviso>/<archivio.eventi>/AAAA-MM-GG Nome/
├── AAAA-MM-GG Nome.md   tipo: evento
├── progetto.md          tipo: progetto-evento, standard_version: 1
├── invitati.md          tipo: invitati
├── spese.md             tipo: spese
├── Bollettini/          nota del bollettino (.md) + DOCX + PDF
├── Form/                link ai moduli Google; a evento chiuso, export delle risposte
└── Altri documenti/     ricevute, preventivi, foto, locandine
```

Con il default del profilo `<archivio.eventi>` è `Anni sociali/{anno}/Eventi` (anno sociale `AAAA-AAAA`). Le tre sottocartelle (`archivio.cartelle_evento`) le crea `rtit evento nuovo --applica`.

Se la nota evento ha `pack: none` oppure `modalita: bollettino_semplice`, il pack **non** è richiesto: serve solo il bollettino.

Il bollettino sta **solo** in `Bollettini/` dell'evento: non si copia in altre cartelle; l'indice dell'anno (`archivio.indice_anno`) lo elenca.

## Sezioni obbligatorie

- `progetto.md`: `## Dati evento` · `## Descrizione` · `## Checklist operativa` · `## TODO` · `## Link`
- `spese.md`: `## Parametri` · `## Voci di spesa` · `## Riepilogo`

## Checklist operativa (standard)

- [ ] Nota evento
- [ ] Pack completo (progetto + invitati + spese)
- [ ] Bollettino (nota + DOCX + PDF in `Bollettini/`)
- [ ] Evento su Tabler World + tipo evento impostato nel portale
- [ ] Copertina
- [ ] Dopo l'evento: ricevute e foto in `Altri documenti/`, saldo in spese.md

Se l'evento usa un modulo Google, aggiungi alla checklist: link in `Form/` e, a evento chiuso, export delle risposte.

Le caselle non spuntate (`- [ ]`) sotto `## TODO` e `## Checklist operativa` compaiono nel report come cose da fare aperte.

## invitati.md

| Nome | Ruolo | Conferma | Intolleranze / note cibo | Quota (€) | Pagato | Metodo | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |

- **Ruolo**: socio · esterno · ospite (o altri ruoli della tavola)
- **Conferma**: `sì` / `no` / `tbd`. In attesa = `tbd`, `?` o vuoto.
- **Pagato**: `sì` / `no`
- **Metodo**: satispay · contanti · bonifico · —
- Formato nome consigliato: «Nome Cognome»
- Intolleranze: dati sanitari, da tenere al minimo e cancellare dopo l'evento

## spese.md — come si calcola

- **N** = confermati in `invitati.md`; se sono 0, si usa `N_stimati`, poi `N_confermati` dei parametri.
- Voci `per_persona` (o quantità `=N`) = importo × N; voci `fisso` = importo × quantità (default 1).
- **Margine** (parametro `Buffer_%`) = subtotale × `Buffer_%` (default 10%).
- **Incasso atteso** = somma delle quote dei confermati (se 0: N × `Quota_persona`).
- **Saldo** = incasso atteso − (subtotale + margine).

Il calcolo non modifica il file. Se l'utente lo chiede, l'assistente può riportare i totali nella sezione `## Riepilogo`.

## Link

- `archivio.link: markdown` (default): link relativi, `[testo](<file.md>)`, leggibili ovunque.
- `archivio.link: wikilink`: link Obsidian dalla radice dell'archivio, `[[percorso|testo]]`.
- `## Link` include anche la nota indice dell'anno (`archivio.indice_anno`), utile per la relazione morale e il passaggio di consegne.

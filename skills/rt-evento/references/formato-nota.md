# Formato della nota bollettino

La CLI `rtit bollettino` legge **questo** formato. Rispetta titoli di sezione, grassetti e righe della tabella. La nota si salva in `<cartella evento>/Bollettini/` con il nome `AAAA-MM-GG Bollettino N.X Titolo breve.md`.

```markdown
---
tipo: bollettino
anno_sociale: 2027-2028
numero: 3
data_emissione: 2027-09-20
evento: "<riferimento alla nota evento, se c'è>"
---

# Bollettino N. 3 — Titolo lungo

## Invito

**Sabato 9 ottobre 2027, ore 20:00** — Titolo dell'invito (dettaglio).

Paragrafo descrittivo facoltativo (1–3 frasi).

- Nota pratica (parcheggio, cosa è incluso, posti limitati…)
- Aperta a: Tablers, ex Tablers, aspiranti e amici

| Campo | Valore |
| --- | --- |
| **Location** | Via Roma 1, 00000 Esempio |
| **Maps** | https://maps.app.goo.gl/… |
| **Dress code** | Informale |
| **Costo** | 25€ (in quota per i soci) — 35€ esterni |
| **Prenotazione entro** | 04/10/2027 |

## Firme

- **Presidente**: Mario Rossi — +39 000 000 0001
- **Segretario**: Giovanni Neri — +39 000 000 0002

## Destinatari (p.c.)

Presidente/Vice/Segretario Nazionale RTIT, Comitato di [Zona], Presidenti delle Tavole della [Zona], soci/ex soci/membri d'onore/amici della [Tavola].

## Intestazione bollettino

(facoltativa: sito, ritrovi, sede, Consiglio Direttivo)

## File

- DOCX · PDF (link locali quando generati, nella stessa cartella `Bollettini/`)
```

## Regole di lettura

| Elemento | Regola |
| --- | --- |
| Riga invito | `**<Giorno data>, ore <HH:MM>** — <Titolo>`; il titolo va in maiuscolo nel Word |
| Corpo | Ogni paragrafo e ogni voce di elenco diventa una riga; la riga "Aperta a:" va nel campo dedicato |
| Tabella | Chiavi in grassetto; usare **Conferma entro** *oppure* **Prenotazione entro** |
| Maps | Facoltativa: nel Word diventa "Link prenotazione" (o "—") |
| Firme | Se una firma manca nella nota, si usa il direttivo del profilo; se manca anche lì, errore (non si inventa) |
| Destinatari / intestazione | Nel Word arrivano dal **profilo**; nella nota servono come documentazione |

## Segnaposto del modello Word generico

Per personalizzare un modello della tavola (`bollettino.template` nel profilo), mantieni questi segnaposto Jinja:

`{{ nome_tavola_maiuscolo }}` · `{{ sito }}` · `{{ ritrovi }}` · ciclo `{%p for r in sede_righe %}{{ r }}{%p endfor %}` · `{{ anno_direttivo }}` · ciclo `{%p for m in direttivo %}{{ m.ruolo }} {{ m.nome }}{%p endfor %}` · `{{ charter }}` · `{{ tavola_madrina }}` · `{{ citta }}` · `{{ data_emissione_it }}` · `{{ numero }}` · `{{ anno_slash }}` · ciclo `destinatari_pc` · `{{ nome_esteso }}` · `{{ data_evento_it }}` · `{{ ora }}` · `{{ titolo }}` · ciclo `corpo_righe` · `{{ aperta_a }}` · `{{ location }}` · `{{ dress_code }}` · `{{ costo }}` · `{{ link_prenotazione }}` · `{{ scadenza }}` · `{{ presidente }}` · `{{ tel_presidente }}` · `{{ segretario }}` · `{{ tel_segretario }}` · `{{ sigla }}`.

I loghi del modello generico sono segnaposto grigi: si sostituiscono con `intestazione.loghi` nel profilo (due PNG, sinistra e destra). Prima di usare loghi RT, rispetta le Linee guida del logo (vedi la skill `rt-comunicazione`, file `references/logo.md`).

---
tipo: spese
data_evento: {{data}}
evento: "{{evento_ref}}"
valuta: EUR
created: {{oggi}}
last_modified: {{oggi}}
---

# Spese — {{titolo}}

## Parametri

| Parametro | Valore | Note |
| --- | --- | --- |
| N_confermati | 0 | da invitati.md (Conferma=sì) |
| N_stimati | 0 | se prenotazione aperta |
| Buffer_% | 10 | scarto spesa |
| Quota_persona | {{quota_persona}} | allineata a costo evento |

## Voci di spesa

| Voce | €/persona o fisso | Tipo | Quantità | Totale € |
| --- | --- | --- | --- | --- |
| Cibo | 12 | per_persona | =N | 0 |
| Bevande | 5 | per_persona | =N | 0 |
| Affitto / location | 0 | fisso | 1 | 0 |
| Altro | 0 | fisso | 1 | 0 |

## Riepilogo

| Voce | € |
| --- | --- |
| Subtotale voci | 0 |
| Buffer | 0 |
| **Totale spesa prevista** | 0 |
| Incasso atteso (quote) | 0 |
| **Saldo previsto (incasso − spesa)** | 0 |

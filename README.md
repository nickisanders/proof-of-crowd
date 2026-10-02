# Proof of Crowd

Evidence-based attention audits for tokens: is the community real?

**Site:** [nickisanders.github.io/proof-of-crowd](https://nickisanders.github.io/proof-of-crowd/)

An audit answers one question with evidence: who is actually talking about a token, how much of that conversation is manufactured, and whether its attention compounds or round-trips. Verdicts describe measurable conversation patterns (spam waves vs the token's own baseline, creator concentration, decay and residue signatures); they never claim to identify who is behind amplification.

## Setting up the intake form

`index.html` posts to a `FORM_ENDPOINT` placeholder. Any endpoint that accepts
a plain POST works and none of them need JavaScript or a backend:

- **Formspree** — create a form, copy the `https://formspree.io/f/XXXXXXX` URL.
- **Tally** — create a form, use its POST endpoint.

Replace the one occurrence and push:

```bash
sed -i '' 's|FORM_ENDPOINT|https://formspree.io/f/XXXXXXX|' index.html
```

The form carries a hidden `_gotcha` honeypot field, which Formspree reads as a
spam trap, and a `_subject` line so requests arrive labelled.

Do not put a personal email address in this repo; it is public. The point of
using a form service is that the address stays with the service.

## How it works

The methodology is developed and stress-tested in public through daily published verdicts and research findings. This repo holds the service: the site and the [report template](report-template.md) every engagement follows.

## Integrity policy

- The fee buys the audit, not the answer. Conclusions follow the data, including for paying clients.
- I don't audit tokens I hold.
- Social data comes from LunarCrush (affiliate relationship, disclosed on every report). Analysis and conclusions are my own.

## Engagements

| Tier | Price | Turnaround |
|---|---|---|
| Pulse Check | $500 | 48 hours |
| Full Audit | $2,500 | one week |
| Monitoring | $750/mo | ongoing |

Independent analysis. Not financial advice.

# Proof of Crowd

Evidence-based attention audits for tokens: is the community real?

**Site:** [proofofcrowd.com](https://proofofcrowd.com)

An audit answers one question with evidence: who is actually talking about a token, how much of that conversation is manufactured, and whether its attention compounds or round-trips. Verdicts describe measurable conversation patterns (spam waves vs the token's own baseline, creator concentration, decay and residue signatures); they never claim to identify who is behind amplification.

## Setting up the intake form

`index.html` posts to Formspree. Submissions arrive at the address registered
with that form, so no email address appears in this public repo.

To point it somewhere else, replace the one `action` URL in `index.html` with
any endpoint that accepts a plain POST; none of them need JavaScript or a
backend.

The form carries a hidden `_gotcha` honeypot field, which Formspree reads as a
spam trap, and a `_subject` line so requests arrive labelled.

Do not put a personal email address in this repo; it is public. The point of
using a form service is that the address stays with the service.

## How it works

The methodology is developed and stress-tested in public through daily published verdicts and research findings. This repo holds the service: the site and the [report template](report-template.md) every engagement follows.

## Brand

The mark is a ring of evenly spaced dots around a solid centre, which reads
both as a crowd and as a stamp. Even spacing is the whole idea: a real crowd is
many voices carrying roughly equal weight, and that is the shape the ring
draws.

`python3 assets/make_logo.py` rebuilds every variant from one definition, so
the favicon, the nav icon and the social card can't drift apart.

| File | Use |
|---|---|
| `assets/logo-wordmark.png` | horizontal lockup, dark ground |
| `assets/logo-wordmark-light.png` | the same on white |
| `assets/logo-wordmark-mono.png` | single colour, for documents |
| `assets/logo-mark.png` | square mark, avatars and app icons |
| `assets/logo-mark-bare.png` | mark with no ground, for arbitrary backgrounds |
| `assets/favicon-{16,32,180}.png` | browser and Apple touch icons |

Palette: `#0d1117` ground, `#3fb950` accent, `#e6edf3` text. Bold text stays at
weight 700, since librsvg fakes anything heavier by double-striking the glyphs.

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

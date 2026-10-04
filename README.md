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

The mark is a fingerprint whose ridges are made of separate dots. Proof drawn
as the oldest proof there is, and built out of a population, because what this
product verifies is how many distinct people are really there.

The palette is paper and ink, so an audit reads as a document rather than a
dashboard screenshot. The brand is deliberately not green: when the brand
colour and the "organic" verdict colour are the same, the logo casts a vote
just by sitting on the page. Cool ink carries the brand, warm hues and green
carry judgement, and nothing crosses over.

| Token | | |
|---|---|---|
| ground | `#f6f3ec` | panel `#ffffff`, rules `#ded8cd` |
| text | `#15171c` | secondary `#6e6a60` |
| brand | `#1b3a6b` | `#7da7e0` on dark grounds, where the navy goes unreadable |
| verdicts | `#236440` organic | `#7d560c` mixed, `#a33228` manufactured |

Every pair clears WCAG AA at its size. The verdict colours were darkened from
their first draft, where amber came in at 3.5:1 on paper and failed the
body-text threshold.

`python3 assets/make_logo.py` rebuilds every logo variant from one definition,
and `assets/make_og.py` and `assets/make_report_charts.py` import the mark from
it, so the favicon, the nav icon, the social card and the report figures cannot
drift apart.

| File | Use |
|---|---|
| `assets/logo-wordmark.png` | horizontal lockup, paper |
| `assets/logo-wordmark-dark.png` | the same on ink |
| `assets/logo-wordmark-mono.png` | single colour, for documents |
| `assets/logo-mark.png` | square mark, avatars and app icons |
| `assets/logo-mark-bare.png` | mark with no ground, for arbitrary backgrounds |
| `assets/favicon-{16,32,180}.png` | browser and Apple touch icons |
| `assets/x-avatar-{400,1000}.png` | X profile picture, built for a circular crop |
| `assets/x-header.png` | X header, 1500x500 |

`python3 assets/make_social.py` rebuilds the X pair. The header leaves its
lower left empty on purpose, since that is where X lays the profile picture
over the top.

A fingerprint doesn't survive 16px at full detail, so the favicon runs a
three-ridge version with much fatter dots at the same silhouette.

## Type

Charter for everything, figures in a monospace. Charter is a reading serif
drawn for small sizes, so it holds up in a table, and it makes a report look
like a document instead of a webpage. Figures go mono because an audit's
numbers should read as measured rather than asserted, and an aligned column
stops a wider glyph passing for a bigger value.

Two notes for anyone regenerating the imagery:

- `fc-list` listing a family proves nothing. librsvg goes through pango, which
  cannot load several macOS `.ttc` collections and then falls back to Helvetica
  without saying so. Verify by rendering against a deliberately fake family
  name and comparing. Iowan Old Style, Superclarendon, Seravek, Hoefler Text,
  Marion and Athelas all fail this way here.
- Bold weights need no hand-set word spacing. That workaround existed because
  librsvg faked a bold Helvetica by double-striking glyphs, which swallowed the
  spaces. Charter ships a real bold, so real spaces work.

The site stack is `Charter, "Bitstream Charter", "Charis SIL", Georgia, serif`,
which resolves natively on Apple platforms and falls back to Georgia elsewhere.
Self-hosting an open Charter would close that gap.

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

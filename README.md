<div align="center">

# masry-skills

**AI writes Arabic like a translated press release. This makes it write like an Egyptian.**

خلّي الـ AI يكتب مصري بجد، مش فصحى مترجمة ولا عامية مزيفة.

[![License: MIT](https://img.shields.io/badge/license-MIT-black.svg)](LICENSE)
[![Eval](https://img.shields.io/badge/eval-30%2F33%20vs%2022%2F33%20baseline-black.svg)](#proven-not-claimed)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-black.svg)](#install)
[![Agent Skills](https://img.shields.io/badge/agentskills.io-compatible-black.svg)](https://agentskills.io)

</div>

---

## Before / After

Same model (Claude Sonnet), same request, one run each. Copied from
[the eval results](skills/masry-writing/evals/results/20261118-054202.json), not edited.

> **Request:** اكتبلي بوست فيسبوك لكافيه بيعلن عن مشروب جديد: سبانش لاتيه بالبندق، سعره 95 جنيه.

<table>
<tr><th width="50%">Without the skill</th><th width="50%">With masry-skills</th></tr>
<tr>
<td dir="rtl">

☕ خبر لذيذ في طريقه ليك!

جديدنا في الكافيه: سبانش لاتيه بالبندق 🌰❤️

مزيج ساخن من الإسبريسو الغني، مع لمسة البندق المحمّص، وطبقة كريمة ناعمة فوقه... تجربة لازم تجربها!

بسعر 95 جنيه بس 😍

تعال جرّبه وقولنا رأيك 👇

📍 [مكان الفرع]
🕐 [مواعيد العمل]

#قهوة #سبانش_لاتيه #كافيه

</td>
<td dir="rtl">

جديد عندنا ☕

سبانش لاتيه بالبندق، بـ 95 جنيه.

جرّبوه وقولولنا رأيكم 🤎

</td>
</tr>
<tr>
<td>Invents espresso, cream and "roasted" hazelnut. Template hook, emoji on every line, <code>تجربة لازم تجربها</code>.</td>
<td>Every fact is one the user gave. Reads like the cafe owner wrote it.</td>
</tr>
</table>

> **Request (Franco):** `7awel el kalam da l 3araby: ana msh 3aref a5ales el project 3ashan el server w2e3 mn embare7`

| Without the skill | With masry-skills |
|---|---|
| Misreads it as a bug report and asks three troubleshooting questions. No conversion. | <div dir="rtl">مش عارف أخلّص الـ project علشان الـ server واقع من إمبارح.</div> |

## Proven, not claimed

Every change to the skill is measured on [10 real requests](skills/masry-writing/evals/evals.json):
Facebook posts, Instagram captions, WhatsApp to a parent, a reply to a 1-star review,
app UI text, a letter to the tax authority, Franco conversion. Each request runs with
and without the skill; a stronger model grades both answers **blind** (shuffled as A/B).

| | Without | **With masry-skills** |
|---|---:|---:|
| Expectations met (graded blind) | 22 / 33 | **30 / 33** |
| MSA words in Egyptian text (`هذا`، `سوف`، `الذي`…) | 3 | **0** |
| AI tells (`في عالمنا المتسارع`، `تجربة فريدة`…) | 2 | **0** |
| Em dashes | 1 | **0** |
| Picked as more natural by the grader | 2 / 10 | **8 / 10** |

<sub>masry-writing v0.3, Claude Sonnet writing, Claude Opus grading, one run per request, 2026-11-18.
Counts are regex, not opinion. Run it yourself: <code>python3 skills/masry-writing/evals/run.py</code></sub>

## Install

### Claude Code

```text
/plugin marketplace add Tayel-Ai-Labs/masry-skills
/plugin install masry-skills@masry-skills
```

### Codex, Cursor, Gemini CLI and other agents

```bash
npx skills add Tayel-Ai-Labs/masry-skills --global --agent '*'
```

### Claude.ai and Claude Desktop

Download [`skills/masry-writing`](skills/masry-writing) as a ZIP and upload it as a skill in
Settings.

### By hand

Copy the `skills/masry-writing` folder into your agent's skills folder
(`~/.claude/skills/` for Claude Code).

## What it does

It works on its own whenever you ask for Arabic aimed at Egyptians. No command needed.

**1. Picks the register before writing a word.**

| You're writing | It writes |
|---|---|
| Posts, captions, ads, menus, WhatsApp, app UI, explaining to a student | Egyptian Arabic |
| Contracts, official letters, government forms | Short, plain MSA |
| Email to a company you don't know | Polite Egyptian, MSA-leaning words |

**2. Writes Egyptian grammar, not MSA with slang on top.**
`مش` not `لا/لم/لن`, `ده` not `هذا`, `هـ` not `سوف`, `اللي` not `الذي`, `إزاي` not `كيف`.

**3. Strips the tells.** The five that give AI Arabic away fastest:

| Tell | Instead |
|---|---|
| `في عالمنا المتسارع` / `في ظل التطور` | Start with the point |
| `يلعب دوراً محورياً` | Say what it actually does |
| `تجربة فريدة لا مثيل لها` | A fact about it, or nothing |
| `بالإضافة إلى ذلك` / `حيث إن` | `وكمان`, or a new sentence |
| `لا تتردد في التواصل معنا` | `كلمنا على [رقم]` |

[The full list, with fixes →](skills/masry-writing/references/tells.md)

**4. Never invents.** No made-up prices, ingredients, discounts, urgency
(`قبل ما تخلص`) or promises (`هنعوضك`). Missing facts become `[ ... ]`.

**5. Reads Franco.** `3`→ع, `7`→ح, `2`→ء, `5`→خ, and keeps `project`, `server`,
`deadline` as Egyptians say them.

## Known limits

We publish where it still loses, so you know what to check:

- **Rewrites can still add small claims** that weren't in the original
  (1 of 10 evals).
- **Short product copy can come out too bare** once invention is forbidden.
- Graded by a model, not a panel of native speakers. One run per request.
  Found a bad output? [Open an issue](../../issues) with the request and the text.

## Roadmap

| Skill | Status |
|---|---|
| `masry-writing` | ✅ v0.3 |
| `masry-edu`: Thanaweya / Baccalaureate explanations in Egyptian, exam terms kept | Next |
| `masry-business`: quotes, proposals, client follow-ups | Planned |
| `masry-review`: list every tell and register slip without rewriting | Planned |

## Contributing

The most useful contribution is a **tell we missed** or **a request where the skill
writes badly**. Open an issue with the text. Every accepted fix gets an eval case,
so it can't come back.

---

<div align="center">

Built in Egypt by **[Tayel AI Labs](https://github.com/Tayel-Ai-Labs)**.
MIT licensed. Use it, fork it, ship it.

</div>

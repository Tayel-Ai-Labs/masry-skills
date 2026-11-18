---
name: masry-writing
description: >-
  Write or rewrite text in natural Egyptian Arabic (مصري) that does not read
  like AI or like translated English. Use when the user asks for Arabic copy,
  posts, messages, captions, product text, explanations or replies aimed at
  Egyptians, when they write in Franco/Arabizi and want Arabic script, or when
  they ask to make Arabic text sound more natural or less like AI.
version: 0.3.0
license: MIT
compatibility: Any agentskills.io SKILL.md client (Claude Code, Codex, Cursor). No tools or APIs required.
metadata:
  author: Tayel AI Labs
  tags: writing arabic egyptian masry localization de-ai franco
---

# Egyptian Arabic writing

You write Arabic the way a sharp Egyptian writer would for this exact reader:
natural, specific, and impossible to mistake for a model translating English.

## 1. Pick the register first

Decide before writing a word. If the request names the audience, follow it.
If it doesn't:

| Context | Register |
|---|---|
| Chat, WhatsApp, social posts, captions, ads, menus, product copy, app UI, explaining something to a student | **Egyptian (عامية مصرية)** |
| Contracts, official letters, government forms, legal notices, academic papers | **Simple modern MSA (فصحى بسيطة)**: short sentences, no ornament |
| Business email to a company you don't know | Polite Egyptian with MSA-leaning vocabulary; never stiff MSA |

Never mix registers inside one sentence by accident. A deliberate MSA term
inside Egyptian text is fine when it's the term people use (e.g. exam terms:
"المعادلة", "التفاضل").

## 2. Egyptian grammar, not MSA with slang on top

When writing Egyptian:

- **Negation:** `مش` for nouns, adjectives and future (`مش عارف`, `مش هييجي`);
  `ما...ش` for verbs (`ماعرفتش`, `مابيحبش`). Never `لا/لم/لن/ليس`.
- **Demonstratives:** `ده`, `دي`, `دول`. Never `هذا/هذه/هؤلاء`.
- **Questions:** `إيه`, `ليه`, `إزاي`, `فين`, `إمتى`, `مين`, `كام`, placed
  where Egyptians put them (`اسمك إيه؟`, not `ما اسمك؟`).
- **Tense markers:** `بـ` for present habitual (`بنشتغل`), `هـ` for future
  (`هنبعتلك`). Never `سوف` or `سـ`.
- **Relative:** `اللي`. Never `الذي/التي/الذين`.
- **Possession:** `بتاع/بتاعة/بتوع` where natural (`الأوردر بتاعك`).

## 3. Spelling: pick one form and keep it

- `ده` / `دي` (not `دا` / `دة`); `إزاي`; `علشان` or `عشان` (pick one per text);
  `كده`; `برضه`; `خلاص`; `دلوقتي`; `إمبارح`; `بكرة`.
- Hamza on `إ/أ` at word start where standard (`إنت`, `أنا`).
- Keep **English brand names, product names and technical terms in Latin
  script** (`Vercel`, `iPhone 15`, `API`) unless an Arabic form is what people
  actually say (`الواي فاي`, `الموبايل`).
- Numbers: Western digits (`150 جنيه`) in casual and product text unless the
  user's existing text uses Arabic-Indic digits.
- No em dashes or en dashes. Use a comma, a period, or `،`.

## 4. Strip the tells

These mark text as AI or as translated English. Remove them on sight. Read
[references/tells.md](references/tells.md) for the full list with fixes. The
worst offenders:

- Openers about the world: `في عالمنا المتسارع`, `في ظل التطور التكنولوجي`,
  `في عصر`. Start with the point.
- Calques: `يلعب دوراً مهماً`, `على صعيد`, `في هذا السياق`, `من ناحية أخرى`,
  `تجدر الإشارة إلى أن`, `لا شك أن`, `بالإضافة إلى ذلك`.
- Grand words for small things: `رحلة`, `استكشاف`, `عالم الـ`, `تجربة فريدة`,
  `لا مثيل لها`, `الأفضل على الإطلاق`.
- Closers: `في الختام`, `وفي النهاية`, `نتمنى لكم`, `لا تتردد في التواصل`.
- Triplets by reflex (three adjectives, three bullet points every time).
- `حيث` as glue between clauses.
- Emoji at the end of every line.

## 5. Be specific

A real writer names the thing. Replace empty adjectives with the facts **the
user gave you**: if they said the latte has hazelnut and costs 95, say that,
not `مشروب مميز`. If they gave no fact, don't invent one to fill the gap:
write the line without it, or leave a short `[ ... ]` placeholder and say so
after the text. Short and true beats rich and made up.

Keep every name exactly as the user spelled it (`كافيه النخلة` stays `كافيه النخلة`).

Never invent prices, numbers, addresses, testimonials or claims. That
includes the quiet ones:

- **Scarcity or urgency** the user didn't state: `قبل ما تخلص`, `الكمية
  محدودة`, `لفترة محدودة`.
- **Promises** on the user's behalf: `هنعوضك`, `هنرجعلك فلوسك`, `خصم`. Offer
  to talk (`ابعتلنا رقم الأوردر ونشوف حصل إيه`) unless they said what they'll
  give.
- **Attributes** of a product beyond the brief: if they said black cotton
  hoodie, don't add `سادة`, `تقيل`, `مريح`.
- **Names** the user didn't give (the business name, the sender's name).
- **Dates** that contradict theirs: if they said it drops Friday, don't write
  `نزل النهاردة`.

## 6. Franco (Arabizi) input

If the user writes in Franco and wants Arabic, convert to Arabic script:
`2`→ء/أ, `3`→ع, `7`→ح, `5`→خ. `3'`→غ, `7'`→خ. `8`, `9`, `6` vary between
writers (commonly `8`→غ or ق, `9`→ق or ص, `6`→ط): resolve from the word,
and if a word is still ambiguous, pick the reading that makes sense and
mention it.

Franco text is full of English words (`project`, `server`, `meeting`,
`deadline`). **Never translate them into MSA** (`المشروع`, `الخادم`). Keep
them in Latin script, or write the loanword the way Egyptians say it
(`البروجكت`, `السيرفر`, `الميتنج`, `الديدلاين`). Pick one approach per text.

When the user writes *to you* in Franco, reply in Arabic script unless they
ask for Franco.

## 7. Rewriting someone's text

- Keep their meaning, facts and order unless asked to restructure.
- Keep their voice: if they're funny, stay funny.
- Fix register, tells and spelling. Don't add new claims.
- After the rewrite, list the main changes in one or two short lines, unless
  the user only wants the text.

## 8. Output

Give the text ready to paste. No preamble like "إليك النص", no markdown
(bold, headings) inside text meant for WhatsApp, Instagram, reviews or SMS.

The user will copy everything above your note, so keep the note out of the
text:

- Put any note **after a line containing only `---`**.
- At most one or two short lines, in the language the user wrote to you in.
- Only when needed: you used a placeholder, picked a register they didn't
  specify, or resolved an ambiguity. Otherwise write no note at all.
- Never explain the skill's rules or comment on your own emoji.

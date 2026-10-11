# Reel review: @elibrandow, "Opus 5.5 did this in one prompt"

Source: https://www.instagram.com/reel/DeUyEboAW-F/ (reviewed from a 53 s screen recording, since Instagram is blocked from the build environment).

Caption: *"Opus 5.5 did this in one prompt. Want it …"*
At recording time: 302 likes, **370 comments**, 5 reposts, 119 shares.

## The "comment PROMPT" prompt

The reel shows it in full twice: as the `prompt.md` card at ~0:10 and typed into a Claude Code input at ~0:15.

```
Make a one-minute ad: what if you could make ads without an editor?
Inside it, an ad for local business websites. Phoenix at golden hour,
navy and green.
```

The card is subtitled "one prompt for Claude Code". The DM people receive is probably this same text, or a longer version of it.

## How the reel works as a funnel

- **There are more comments (370) than likes (302).** That's what comment-to-DM gating looks like. Commenting "PROMPT" is the conversion event.
- The author pinned *"IF YOUR ACCOUNT IS PRIVATE CHECK YOUR HIDDEN REQUESTS!"* and answers every "Prompt" comment with "Just DMed you", "In your DMs now" or "Sent it, check your DMs 🙌". It's either a ManyChat-style auto-DM or done by hand.
- The bio in the CTA mock-up reads *"I build websites for local businesses with Claude."* So the prompt is the giveaway, and the DM conversation is where the creator can pitch web design.

## Scene by scene

Times are reel time, roughly 4.5 s behind the recording. "Sticker" means the Instagram text overlay on top of the video.

| Time | Visual | On-screen copy |
|---|---|---|
| 0:00–0:03 | Phone footage of a real laptop. A hand taps play. Pink/violet silk sky. | "What if you could make" (word-by-word blur-in) · Sticker: **"Opus 5.5 is SOO good 😮‍💨"** |
| 0:03–0:04.5 | Sonoran desert at golden hour (buttes, saguaro, cholla) | **"ads like this"** large · Sticker: **"You can do it too"** |
| 0:04.5–0:07 | Pale lilac/peach gradient | "without ever touching an" small, then giant green **"Editor?"** with a blur-in |
| 0:07–0:10 | Vertical slot list. The active row has a green arrow; the rows above and below are faded. | "No studio. / → No designer. / → No camera. / → No timeline. / No crew." · Sticker: **"Just comment PROMPT"** (stays up until 0:41) |
| 0:10–0:12 | `prompt.md` card on a cloud tile, with a selection box like a design tool's | "Just *Claude*." (italic serif) / "and one **prompt**." (green) |
| 0:14–0:16 | 3D laptop floating in clouds. Its screen shows the desert with a Claude Code input holding the prompt. A model picker opens (Opus 5.5 / Sonnet 5 / Haiku 4.5), then a green halftone wipe. | — |
| 0:16–0:18 | Laptop in clouds. Its screen is a collage of ugly local-business sites. | "Here's what it built me." |
| 0:18–0:22 | Push into the collage: "Welcome to Desert Lawn Care!!", "AAA PLUMBING SERVICES – CALL NOW!!!", "Roofing Company" with broken images. Tags pop on: *Slow to load · Not secure · No mobile site · No reviews*. | "Most local businesses are losing **customers**" → "to a *bad website.*" (red italic serif) |
| 0:22.5–0:24.5 | Mocked chat UI with a cactus icon. `my-yard.jpg` is attached. Chips: *Build a website · Write the copy · Make it fast on phones*. | "*What should we build?*" · typed: "Build a website for Ironwood & Sage Landscaping in Mesa, Arizona. Warm, modern, a quote button up top." |
| 0:24.5 | Blank canvas | "✳ Claude is writing…" |
| 0:25–0:28 | Dark code panel next to the site as it assembles. Status chips: *Writing copy ✓ · Designing pages ✓ · Publishing*, then "● Live · ironwoodandsage.com". | — |
| 0:28.5–0:31 | Full-bleed hero montage with bracket labels: **Ironwood & Sage** (Landscapers), **Mesa Ridge Roofing** (Roofers), **Blue Basin Plumbing** (Plumbers) | "Desert yards that feel like a *resort.*" / "ROOFS BUILT FOR ARIZONA SUN" / "Fast, clean plumbing. Same day." |
| 0:31–0:32.5 | The three sites fanned out in 3D | "A real website, *in minutes.*" |
| 0:32.5–0:34.5 | Warm off-white end card | "✳ Built with *Claude.*" |
| 0:34.5–0:38.5 | Pull back to the laptop in clouds. Floating pills appear, and the `prompt.md` card drifts in. | "Every frame" · "came from" · "one prompt" · "from that one video" |
| 0:39–0:41 | Black, with a glowing green planet horizon | "I know." / "I didn't **believe** it either." (green highlight block) |
| 0:41.5–0:42 | Teal-to-green gradient with the `prompt.md` card | "Want it?" · Sticker: **"Make sure to like and follow!"** |
| 0:42.5–0:46 | The creator's Instagram profile card mocked up: Follow → Following ✓. Then "PROMPT" is typed into a comment box, then a DM mock: "PROMPT" → "Here's the exact prompt ✳ prompt.md". | "Make sure you're following me" / "and comment "PROMPT"" / "I'll send it to your [DMs]" (last word partly hidden) |

There's also a voiceover (the spectrogram shows speech over music). I couldn't transcribe it in this environment because the speech-to-text model download is blocked. The kinetic captions seem to track it word for word.

## What's working

1. **The phone-filming-a-laptop frame.** It reads as a real person showing a real thing, not an ad. The hand pressing play is the first thing you see.
2. **Ad inside an ad.** The reel is the proof of its own claim, and then it keeps nesting (laptop in clouds → screen → site). Each zoom works as a scene change.
3. **A clean story arc.** Hook (what if) → enemy (editors, designers, crews) → mechanism (one prompt) → problem (bad local sites) → build → proof in three industries → disbelief beat → CTA.
4. **The proof montage uses three trades in three palettes.** That answers "does it only make one look?" in under three seconds.
5. **The CTA shows the steps instead of describing them.** Viewers watch someone follow, comment PROMPT and get the DM, so they know exactly what to do.
6. **Restrained type system.** Grotesk sans for statements, italic serif for the emotional word (*Claude*, *resort*, *bad website*), green for the key nouns. This is the same move as the CoffeeSpot reel's `.accent` treatment.

## What's weak, or worth being skeptical about

1. **"One prompt" stretches it.** The prompt names no businesses, copy, scenes or photos, yet the output has specific brand names, a three-act script and photographic images (desert landscapes, a plumber, a patio). Claude Code can write and render the HTML/CSS animation, the same way `coffeespot-reel/render.cjs` does. It doesn't produce photos, so those came from stock, image generation or the author's library. That means more setup, or more prompts, than the reel shows. Treat "one prompt" as marketing shorthand.
2. **The gated prompt is on screen twice.** Anyone who pauses has it, which shows the DM is really about capturing the lead.
3. **It targets two audiences.** The hook is for creators ("make ads without an editor"), while the bio and the ad inside the ad pitch local businesses. The comments come from creators who want the prompt, not plumbers who need a site.
4. **Readability.** Copy shot off a laptop screen gets moiré and loses contrast, and the "Just comment PROMPT" sticker sits over the top of the frame for 33 s. Small text, like the prompt card and the code panel, is unreadable at feed speed.
5. **The payoff comes late.** The real websites don't appear until about 0:28 of roughly 46 s, well over halfway through. Everything before that is promise.

## What to reuse in our reels

These all fit the existing `coffeespot-reel` setup (HTML scenes → headless Chromium → ffmpeg):

- **Slot-list negation** ("No studio. / No designer. / No camera."): one stack of words, `translateY` stepping one row at a time, and opacity/blur falling off away from the active row.
- **Device-in-sky mock-up**: a CSS 3D laptop (or a PNG with the screen as a transformed `<div>`) over a cloud plate, using a zoom-through as the scene transition. Our `.cam` zoom already does this.
- **Before/after collage**: generate deliberately bad sites in HTML (Comic-ish fonts, "CALL NOW!!!", broken-image boxes) and pop on red issue tags.
- **The fake build**: a typed prompt, then "✳ Claude is writing…", then status chips ticking ✓, then a "● Live · domain" pill. It's cheap to build and makes the process feel real.
- **Bracket labels** over a hero shot ("[ Landscapers ]") to name each example during a fast montage.
- **CTA as UI**: animate the follow → comment → DM flow instead of saying it.

Things to do differently: keep key text large and rendered natively (skip filming the laptop, or film it only for the hook), put the proof before 0:10, and make the hook and the CTA speak to the same audience.

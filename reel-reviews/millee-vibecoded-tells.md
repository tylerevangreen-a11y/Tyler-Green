# Reel review: @millee.md, "20 reasons why your app looks vibecoded"

Source: https://www.instagram.com/reel/DcrqbqZRVvC/ (reviewed from a 34 s screen recording; Instagram is blocked from the build environment).

Caption: *"Does your website or app have any of these …"* · on-screen: *"20 reasons why your app looks vibecoded (Give this to Claude/chatGPT)"*.
At recording time: 7,302 likes and 6,752 shares.

## Format

The creator reads the list to camera at speed. A numbered two-column checklist sits over the top half of the frame and fills in one item at a time, with a small example clip of each tell beside their face and word-by-word captions underneath. The pinned author comment holds the full list "to copy and paste".

Why it spreads: it's a checklist people save and send ("give this to Claude"), so shares run almost level with likes. The list stays on screen the whole time, so a screenshot captures all of it.

## The 20 tells

1. Purple-to-blue gradient
2. Gradient hero text
3. Emojis in your headings
4. Inter font everywhere
5. Colored left-border cards
6. Glassmorphism cards
7. Low-contrast dark mode
8. Three icon boxes in a row
9. A badge above the headline
10. Lucide icons everywhere
11. Untouched shadcn components
12. Sections fading in as you scroll
13. A beam that follows your cursor
14. Hover effects that make buttons fade
15. Inconsistent spacing
16. Em dashes everywhere
17. Generic buzzword copy
18. Serif italics for accent words
19. Space Grotesk plus Instrument Serif
20. Grain texture over a gradient

## Audit of `coffeespot-fit-reel`

Several of these are web-UI tells, but the reel had its own versions of the visual ones.

| # | Tell | In the reel? | Change |
|---|---|---|---|
| 2 | Gradient text | Yes: every accent word was gradient-filled | Solid colour: rust on light, amber on dark |
| 18 | Serif italic accent words | Yes: "why?", "fit.", "you.", "today.", "focus?", "night?", "rush?", "4.7 stars…", "there." were EB Garamond italic inside Plex Sans lines | Accent words now stay in the line's own face and weight; emphasis is colour only. Garamond is kept for the wordmark, café names and app headings, where it's the brand face. |
| 19 | Grotesk + display-serif pairing | Same pattern as 18 (Plex Sans + Garamond italic) | Resolved by 18 |
| 20 | Grain/gradient backgrounds | Close: the light scenes used drifting soft gradient blobs | Flat paper background (`#f3eadc`). The golden-hour bokeh behind the phone stays, since it's a deliberate café-light scene. |
| 6 | Glassmorphism cards | Slight: montage cards had a translucent white inner hairline | Hairline removed |
| 12 | Fade-in on scroll | Video version of it: every word faded and un-blurred into place | Words now cut in on the beat (appear at once, short drop, settle) and exits are quick cuts. Scene transitions still carry the motion. |
| 15 | Inconsistent spacing | About 11 different headline sizes and drifting caption positions | One scale: 148 / 112 / 96 / 72 / 46 px; top captions all sit at y = 250 |
| 7 | Low-contrast text | Borderline: secondary grey `#8a7d72` on cream | Darkened to `#766a5f` |
| 1, 3, 4, 5, 8, 9, 10, 11, 13, 14, 16, 17 | | No | |

**Not changed yet:** the first reel (`coffeespot-reel/`) has the same two big tells. Its `.accent` words are gradient-filled italic serif, and its background is gradient silk ribbons. The same pass would apply there.

## Using the list

Paste it into the prompt as a "don't" list whenever asking Claude for a page, a reel or a deck. It's specific enough to steer the output, and most items name the default an AI reaches for when nothing else is specified.

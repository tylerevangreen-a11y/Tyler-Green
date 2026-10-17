# Phone-native reels

Three short videos built to look like something a person made on their phone, not an ad. Every one opens on its hook, stays under 16 s, and ends on a reason to comment or share.

| File | Format | Ends on | Length |
|---|---|---|---|
| `out/imessage.mp4` | iMessage story: a friend refuses "the usual place" and sends coffeespotfinder.com | "send this to your study buddy 📚" (shares) | 15.6 s |
| `out/notes.mp4` | Notes app, typed live: "coffee shop red flags 🚩" | "what did i miss? 👇" (comments) | 14.7 s |
| `out/orders.mp4` | Text post: "what your coffee order says about you ☕" | "comment yours 👇 i'll tell you your café" (comments) | 10.6 s |

The only audio is quiet sound effects (keyboard ticks, message sounds, pops).

## Posting

1. Upload the MP4 as a Reel. Tap the music icon and pick a **trending sound**: in the audio browser, look for the ↗ arrow next to a track. Set the original audio low (about 10–20%) so the clicks still come through, or mute it.
2. Set the cover to the first frame, since it carries the hook.
3. Paste a caption:
   - **imessage:** `she has a point though 😭 #studytok #studyspot #coffeeshop #cafe #collegelife`
   - **notes:** `#3 should be illegal 🚩 #coffeeshop #redflags #coffee #cafe #relatable`
   - **orders:** `be honest, which one are you 👇 #coffee #coffeeorder #coffeetok #matcha #coldbrew`
4. Reply to every comment in the first hour. On **orders**, answer each comment with an actual café pick for that order. That reply is where coffeespotfinder.com (link in bio) gets clicked.
5. Post the same files to TikTok as well. They have no watermark.

Post one a day rather than all three at once, so each gets its own push.

## What to film next (the formats that earn follows)

Faceless text formats get views. A face and a series get followers. Each of these takes about ten minutes on a phone.

1. **"Rating every café in town for studying, day 1."** Walk in, show the drink, the table and whether there's an outlet, then put a score out of 10 on screen. End with "day 2 tomorrow". A numbered series is the most reliable follow driver.
2. **"POV: you finally found a café with outlets AND quiet."** Sit down, plug in, do a small happy dance. 5–7 s with a trending sound and one line of text.
3. **Reply videos.** For each good comment on `orders`, use "reply with video": show their comment on screen and say which café fits that order. Every reply is a new post and points back to the original.
4. **"I made a website that picks your café based on your mood."** Talk to camera in front of coffeespotfinder.com, using green screen or a screen recording. Founder stories get followed.
5. **"Asking strangers their coffee order and telling them what it says about them."** Uses the `orders` lines as material. It's the highest-effort format and has the highest ceiling.

Send the raw clips over and they can be cut here, with captions, zooms and sound effects in the same style.

## Rebuilding

```
NODE_PATH="$(npm root -g)" node viral-reels/render.cjs imessage   # or notes, orders → out/<name>-silent.mp4
python3 viral-reels/sfx.py imessage                                # → out/<name>.mp4 with sound effects
```

Copy, timing and messages live at the top of each `<name>/index.html` script.

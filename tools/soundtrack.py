#!/usr/bin/env python3
"""Original music + synced sound effects for the CoffeeSpot reels.

Everything is synthesised here from oscillators and noise (no samples, nothing licensed), so the
tracks are safe to post. Cue times mirror the T timelines in each reel's index.html.

  python3 tools/soundtrack.py          -> both reels
  python3 tools/soundtrack.py fit      -> coffeespot-fit-reel only
  python3 tools/soundtrack.py first    -> coffeespot-reel only

Each reel gets two files next to its silent master:
  <name>-music.mp4  music + sound effects, loudness-matched for Instagram (-14 LUFS)
  <name>-sfx.mp4    sound effects only, at the same level: pick a trending sound in Instagram on top
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import wave

import numpy as np

SR = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(7)


def T(d):
    return np.arange(int(d * SR)) / SR


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def noise(d):
    return rng.standard_normal(int(d * SR))


def band(x, lo=None, hi=None, order=2):
    """Zero-phase Butterworth-shaped band filter, applied in the frequency domain."""
    n = len(x)
    if n == 0:
        return x
    N = 1 << int(np.ceil(np.log2(n + 1)))
    f = np.fft.rfftfreq(N, 1 / SR)
    H = np.ones_like(f)
    if hi:
        H /= np.sqrt(1 + (f / hi) ** (2 * order))
    if lo:
        H /= np.sqrt(1 + (lo / np.maximum(f, 1e-3)) ** (2 * order))
    return np.fft.irfft(np.fft.rfft(x, N) * H, N)[:n]


def place(dst, src, t, gain=1.0):
    i = int(round(t * SR))
    if i < 0:
        src, i = src[-i:], 0
    n = min(len(src), len(dst) - i)
    if n > 0:
        dst[i:i + n] += gain * src[:n]


def saw(f, t):
    return 2 * ((f * t + rng.random()) % 1.0) - 1


def ramp(t, a, b):
    """0 before a, 1 after b, linear between."""
    return np.clip((t - a) / (b - a), 0, 1)


# ---------- instruments ----------

def kick(dec=0.2, f0=125, f1=45):
    t = T(0.5)
    f = f1 + (f0 - f1) * np.exp(-t / 0.03)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / dec)
    y += band(noise(0.5), lo=2000, hi=7000) * np.exp(-t / 0.003) * 0.3
    return np.tanh(1.8 * y) * 0.8


def clap():
    t = T(0.35)
    e = np.zeros_like(t)
    for o, tau in ((0, 0.005), (0.012, 0.005), (0.024, 0.11)):
        e += (t >= o) * np.exp(-np.maximum(t - o, 0) / tau)
    return band(noise(0.35) * e, lo=1000, hi=7000) * 0.5


def snare():
    t = T(0.3)
    y = band(noise(0.3), lo=900, hi=6000) * np.exp(-t / 0.09) * 0.45
    y += np.sin(2 * np.pi * 185 * t) * np.exp(-t / 0.05) * 0.4
    return y


def rim():
    t = T(0.05)
    return band(noise(0.05), lo=1500, hi=4500) * np.exp(-t / 0.004) * 0.4 + np.sin(2 * np.pi * 820 * t) * np.exp(-t / 0.015) * 0.25


def hat(open_=False):
    d, tau = (0.3, 0.09) if open_ else (0.07, 0.014)
    return band(noise(d), lo=7000) * np.exp(-T(d) / tau) * 0.25


def crash(d=1.6):
    return band(noise(d), lo=4500, hi=14000) * np.exp(-T(d) / 0.45) * 0.22


def pad(notes, dur, att=0.08, rel=0.6):
    t = T(dur + rel)
    y = np.zeros_like(t)
    for m in notes:
        for c in (-9, 0, 9):
            y += saw(hz(m) * 2 ** (c / 1200), t)
    env = np.minimum(1, t / att) * np.clip((dur + rel - t) / rel, 0, 1)
    return y * env / (len(notes) * 3)


def bass(m, dur):
    t = T(dur + 0.03)
    f = hz(m)
    y = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t)
    env = np.minimum(1, t / 0.006) * (0.65 + 0.35 * np.exp(-t / 0.08)) * np.clip((dur + 0.03 - t) / 0.03, 0, 1)
    return np.tanh(1.5 * y * env) * 0.6


def pluck(m, d=0.45):
    t = T(d)
    f = hz(m)
    y = 0.5 * (saw(f, t) + saw(f * 1.006, t))
    return band(y * np.exp(-t / 0.11), hi=3000) * np.minimum(1, t / 0.002) * 0.5


def epiano(m, d=1.8):
    t = T(d)
    f = hz(m)
    y = np.sin(2 * np.pi * f * t + 1.5 * np.exp(-t / 0.3) * np.sin(2 * np.pi * f * t))
    y += 0.2 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t / 0.12)
    trem = 1 + 0.1 * np.sin(2 * np.pi * 4.5 * t)
    return y * np.exp(-t / 1.1) * np.minimum(1, t / 0.003) * trem * 0.22


def crackle(dur):
    n = int(dur * SR)
    y = np.zeros(n)
    idx = rng.integers(0, n, int(dur * 7))
    y[idx] = rng.uniform(-1, 1, len(idx))
    return band(y, lo=800, hi=5000) * 0.5 + band(noise(dur), lo=1000, hi=6000) * 0.004


def riser(d):
    n = noise(d)
    p = T(d) / d
    return (band(n, lo=300, hi=1500) * (1 - p) + band(n, lo=3000, hi=10000) * p) * p ** 2 * 0.25


# ---------- sound effects ----------

def sfx_key():
    t = T(0.04)
    y = band(noise(0.04), lo=1800, hi=7500) * np.exp(-t / 0.005) * 0.55
    y += np.sin(2 * np.pi * rng.uniform(160, 240) * t) * np.exp(-t / 0.01) * 0.35
    return y * rng.uniform(0.7, 1.0)


def sfx_tap():
    t = T(0.08)
    return (np.sin(2 * np.pi * 1150 * t) * np.exp(-t / 0.012) * 0.35 + np.sin(2 * np.pi * 150 * t) * np.exp(-t / 0.02) * 0.5
            + band(noise(0.08), lo=2000, hi=6000) * np.exp(-t / 0.003) * 0.2)


def sfx_stamp():
    t = T(0.3)
    f = 55 + 95 * np.exp(-t / 0.03)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)
    y += band(noise(0.3), hi=2500) * np.exp(-t / 0.025) * 0.6
    return np.tanh(2 * y) * 0.7


def sfx_tick(f=2300):
    t = T(0.06)
    return (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.012) + 0.5 * np.sin(2 * np.pi * f / 2 * t) * np.exp(-t / 0.02)) * 0.25


def sfx_pop(f0=700, f1=260):
    t = T(0.09)
    f = f1 + (f0 - f1) * np.exp(-t / 0.015)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.03) * 0.4


def sfx_bell(ms=(88, 95), d=1.4, g=0.22):
    t = T(d)
    y = np.zeros_like(t)
    for k, m in enumerate(ms):
        f, o = hz(m), k * 0.07
        u = np.maximum(t - o, 0)
        y += (t >= o) * (np.sin(2 * np.pi * f * u) * np.exp(-u / 0.6) + 0.25 * np.sin(2 * np.pi * 2.76 * f * u) * np.exp(-u / 0.2)
                         + 0.1 * np.sin(2 * np.pi * 5.4 * f * u) * np.exp(-u / 0.08))
    return y * g


def sfx_whoosh(d=0.7, peak=0.5, g=0.35):
    """Noise swell whose brightness follows its loudness. Place it so `peak` lands on the cut."""
    n = noise(d)
    p = T(d) / d
    env = np.where(p < peak, (p / peak) ** 2, ((1 - p) / (1 - peak)) ** 1.5)
    w = np.where(p < peak, p / peak, 1 - (p - peak) / (1 - peak))
    return (band(n, lo=200, hi=1200) * (1 - w) + band(n, lo=2500, hi=9000) * w * 0.8) * env * g


def sfx_swish(d=0.25):
    p = T(d) / d
    return band(noise(d), lo=3000, hi=11000) * np.minimum(1, p / 0.1) * (1 - p) ** 2 * 0.3


# ---------- mixing ----------

def duck(n, kicks, depth, tau=0.13):
    env = np.zeros(n)
    for k in kicks:
        place(env, np.exp(-T(0.5) / tau), k)
    return 1 - depth * np.clip(env, 0, 1)


def automate(x, dark, bright, amt):
    """Crossfade a bus between a dark and a bright filtering by amt(t) in 0..1."""
    return band(x, hi=dark) * (1 - amt) + band(x, hi=bright) * amt


# ---------- coffeespot-fit-reel (31.5 s) ----------
# 120 bpm, bars start at 1.95 + 2k. Muted next-room groove under the problem, builds through
# "what if it asked why?" and the slot list, drops on "Just coffeespot", breaks down for the tagline.

def build_fit():
    D = 31.5
    n = int(D * SR)
    tt = np.arange(n) / SR
    beat = lambda b: 1.95 + 0.5 * b
    CH = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]  # Fmaj7 Em7 Dm7 Cmaj7
    RT = [41, 40, 38, 36]
    chord_at = lambda bar: 0 if bar >= 14 else bar % 4
    full = lambda t: 9.95 <= t < 23.95 or 26.95 <= t < 29.95

    drums, muffled, bas, pads, plk, fx = (np.zeros(n) for _ in range(6))
    kicks = []
    for bar in range(-1, 15):
        t0 = beat(bar * 4)
        c = chord_at(bar)
        place(pads, pad(CH[c], 1.6 if bar == 14 else 2.0, att=0.9 if bar < 0 else 0.08, rel=1.2 if bar == 14 else 0.6), max(t0, 0))
        for b in range(4):
            tb = t0 + 0.5 * b
            if tb < 0 or tb > 29.96:
                continue
            if 1.95 <= tb < 5.95:
                place(muffled, kick(), tb)
            elif 5.95 <= tb < 23.95 or 26.95 <= tb <= 29.96:
                place(drums, kick(), tb)
                kicks.append(tb)
            if tb >= 29.95:
                continue
            if (full(tb) or 7.95 <= tb < 9.95) and b in (1, 3):
                place(drums, clap(), tb, 0.8)
            if full(tb) or 5.95 <= tb < 9.95:
                place(drums, hat(open_=(b == 3 and full(tb))), tb + 0.25, 0.9)
            if full(tb):
                place(drums, hat(), tb + 0.125, 0.35)
                place(drums, hat(), tb + 0.375, 0.35)
            if 7.95 <= tb < 23.95 or 26.95 <= tb < 29.95:
                place(bas, bass(RT[c] + (12 if b == 2 else 0), 0.2), tb + 0.25)
            if full(tb):
                tones = [m + 12 for m in CH[c]]
                for h, j in enumerate(((0, 2), (1, 3), (2, 0), (3, 1))[b]):  # 8th-note arp over the chord
                    place(plk, pluck(tones[j]), tb + 0.25 * h, 0.9 if h == 0 else 0.6)
    # breakdown: held sub under the tagline
    place(bas, bass(RT[3], 2.0) * 0.8, 23.95)
    place(bas, bass(RT[0], 1.0) * 0.8, 25.95)
    # build: riser and a snare roll into the drop
    place(fx, riser(2.0), 7.95, 0.9)
    for k in range(8):
        place(drums, snare(), 8.95 + k * 0.125, 0.15 + 0.06 * k)
    place(fx, riser(1.0) * 0.6, 25.95)
    for tc, g in ((9.95, 1.0), (26.95, 0.6), (29.95, 0.8)):
        place(drums, crash(), tc, g)
    # final hit: pluck strum on Fmaj7
    for k, m in enumerate(CH[0]):
        place(plk, pluck(m + 12, 1.2), 29.95 + 0.03 * k, 0.8)

    bright = np.clip(ramp(tt, 5.95, 9.95) - ramp(tt, 23.95, 24.4) + ramp(tt, 26.45, 26.95), 0, 1)
    g = duck(n, kicks, 0.55)
    music = (drums * 0.8 + band(muffled, hi=260) * 1.2 + bas * 0.55 * g + automate(pads, 500, 2400, bright) * 0.38 * g
             + plk * 0.32 * g + fx)
    music *= 0.5 + 0.5 * ramp(tt, 5.95, 9.95)  # half level under the problem, swelling into the drop
    music *= np.clip((D - tt) / 1.4, 0, 1) * np.minimum(1, tt / 0.3)

    sfx = np.zeros(n)
    for k in range(1, 15):
        place(sfx, sfx_key(), 0.3 + 0.07 * k, 0.6)
    place(sfx, sfx_key() * 1.4, 1.40)
    for i in range(4):
        place(sfx, sfx_pop(520, 240), 1.7 + 0.11 * i, 0.45)
        place(sfx, sfx_stamp(), 3.0 + 0.2 * i, 0.6)
    for tc in (5.0, 11.2, 16.5, 22.0):
        place(sfx, sfx_whoosh(0.7, 0.45), tc - 0.05)
    for tc in (18.45, 20.25):
        place(sfx, sfx_whoosh(0.6, 0.5, 0.3), tc - 0.3)
    for tc in (7.95, 8.45, 8.95):
        place(sfx, sfx_tick(), tc, 0.8)
    place(sfx, sfx_bell((84, 91)), 10.55, 0.6)
    for tc in (12.3, 12.65, 13.05, 13.4, 13.75, 13.93, 14.11, 14.45):
        place(sfx, sfx_tap(), tc, 0.8)
    for tc in (14.87, 15.09):
        place(sfx, sfx_tick(3000), tc, 0.6)
    place(sfx, sfx_bell((88, 95)), 15.4, 0.8)
    for tc in (22.15, 22.23, 22.31):
        place(sfx, sfx_pop(), tc, 0.6)
    place(sfx, sfx_swish(), 25.62, 0.9)
    place(sfx, sfx_bell((84, 91)), 27.05, 0.5)
    place(sfx, sfx_tap(), 29.1, 0.9)
    place(sfx, sfx_bell((91, 96), g=0.18), 29.2, 0.7)
    return music, sfx


# ---------- coffeespot-reel (25.6 s) ----------
# 100 bpm lo-fi: Rhodes, swung hats, boom-bap. Bars start at 1.4 + 2.4k; the beat drops as the
# ring logo draws at 3.8 and resolves to Cmaj9 under the end card.

def build_first():
    D = 25.6
    n = int(D * SR)
    tt = np.arange(n) / SR
    bt = 0.6
    beat = lambda b: 1.4 + bt * b
    CH = [[50, 53, 57, 60, 64], [53, 57, 59, 64], [52, 55, 59, 62], [52, 55, 57, 60]]  # Dm9 G13 Cmaj9 Am7
    RT = [38, 43, 36, 45]
    full = lambda t: 3.8 <= t < 23.0

    drums, bas, keys, fx = (np.zeros(n) for _ in range(4))
    kicks = []
    for bar in range(-1, 10):
        t0 = beat(bar * 4)
        c = 2 if bar == 9 else bar % 4

        def strum(t1, g, d=1.8):
            for k, m in enumerate(CH[c]):
                place(keys, epiano(m, d), t1 + 0.012 * k, g)

        if t0 >= 0:
            strum(t0, 1.0, 2.6 if bar == 9 else 1.8)
        elif bar == -1:
            strum(0.0, 0.8)
        if bar == 9:
            place(drums, kick(0.25), t0)
            place(bas, bass(RT[c], 2.0) * 0.8, t0)
            place(drums, crash(2.2), t0, 0.5)
            continue
        if full(t0):
            strum(t0 + 2.5 * bt, 0.45, 1.5)
        for b in range(4):
            tb = t0 + bt * b
            if tb < 0:
                continue
            swing = 0.08 * bt
            if full(tb) or 1.4 <= tb < 3.8:
                place(drums, hat(), tb, 0.7)
                place(drums, hat(), tb + 0.5 * bt + swing, 0.4)
            if 1.4 <= tb < 3.8 and b in (1, 3):
                place(drums, rim(), tb, 0.8)
            if full(tb):
                if b in (1, 3):
                    place(drums, snare(), tb, 0.9)
                for kb in {0: (0,), 1: (0.5,), 2: (0, 0.25), 3: (0.5,)}[b]:
                    place(drums, kick(0.22, 110, 42), tb + kb * bt)
                    kicks.append(tb + kb * bt)
                note = {0: (RT[c], 1.4), 1: (RT[c], 0.4), 2: (RT[c] + 7, 0.5), 3: (RT[c] + 12, 0.9)}[b]
                place(bas, bass(note[0], note[1] * bt), tb + (0.5 * bt if b == 1 else 0))
    place(fx, riser(1.2) * 0.7, 2.6)
    place(drums, crash(), 3.8, 0.7)

    g = duck(n, kicks, 0.25)
    warm = band(keys, hi=3200)
    music = drums * 0.7 + bas * 0.6 * g + warm * 0.75 * g + fx + crackle(D) * 0.35
    music = band(music, hi=9000)  # lo-fi top end
    music *= np.clip((D - tt) / 1.6, 0, 1) * np.minimum(1, tt / 0.2)

    sfx = np.zeros(n)
    place(sfx, sfx_swish(0.45), 1.42, 1.0)
    place(sfx, sfx_whoosh(0.5, 0.5, 0.2), 1.85)
    place(sfx, sfx_bell((86, 93)), 4.45, 0.6)
    for tc in (5.7, 11.95, 18.55):
        place(sfx, sfx_whoosh(0.7, 0.45), tc - 0.1)
    for tc in (7.55, 8.4, 9.3, 10.05, 16.0, 17.25, 23.5):
        place(sfx, sfx_tap(), tc, 0.8)
    for i in range(6):
        place(sfx, sfx_tick(2000 + 120 * i), 10.65 + 0.11 * i, 0.5)
    place(sfx, sfx_whoosh(0.5, 0.6, 0.2), 13.9)
    for i in range(3):
        place(sfx, sfx_pop(560 + 80 * i, 240), 18.9 + 0.34 * i, 0.6)
    place(sfx, sfx_bell((86, 93)), 21.9, 0.5)
    place(sfx, sfx_bell((93, 98), g=0.18), 23.6, 0.7)
    return music, sfx


# ---------- output ----------

def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def loudness(path):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'loudnorm=I=-14:TP=-1.5:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True, check=True)
    return float(json.loads(re.search(r'\{[^{}]*\}', r.stderr).group(0))['input_i'])


def mux(video, wav, gain_db, out):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', f'volume={gain_db:.2f}dB,alimiter=limit=0.79:level=false', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', out], check=True)


REELS = {
    'fit': ('coffeespot-fit-reel', 'coffeespot-fit-reel', build_fit),
    'first': ('coffeespot-reel', 'coffeespot-reel', build_first),
}

if __name__ == '__main__':
    for key in sys.argv[1:] or list(REELS):
        folder, name, build = REELS[key]
        music, sfx = build()
        mix = np.tanh(1.1 * (music * 0.85 + sfx * 0.75)) / np.tanh(1.1)
        fx_only = np.tanh(1.1 * sfx * 0.75) / np.tanh(1.1)
        out = os.path.join(ROOT, folder, 'out')
        video = os.path.join(out, name + '.mp4')
        with tempfile.TemporaryDirectory() as tmp:
            wm, ws = os.path.join(tmp, 'mix.wav'), os.path.join(tmp, 'sfx.wav')
            write_wav(wm, mix)
            write_wav(ws, fx_only)
            gain = -14 - loudness(wm)  # same gain for both, so the effects sit at the same level under a trending sound
            mux(video, wm, gain, os.path.join(out, name + '-music.mp4'))
            mux(video, ws, gain, os.path.join(out, name + '-sfx.mp4'))
        print(f'{name}: wrote -music.mp4 and -sfx.mp4 (gain {gain:+.1f} dB)')

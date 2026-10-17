#!/usr/bin/env python3
"""Lays sound effects onto a phone-native reel from the cues its page exports (render.cjs writes <name>.cues.json).

  python3 viral-reels/sfx.py imessage     -> viral-reels/out/imessage.mp4

The effects are synthesised (no Apple or other recorded sounds) and kept quiet, around -20 LUFS, so a trending
sound picked inside Instagram or TikTok sits on top of them. A reel with no cues is copied through silent.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'tools'))
import soundtrack as st  # noqa: E402  (reuses its synth helpers)


def key():
    t = st.T(0.03)
    return (st.band(st.noise(0.03), lo=2500, hi=9000) * np.exp(-t / 0.0035) * 0.5
            + np.sin(2 * np.pi * st.rng.uniform(380, 460) * t) * np.exp(-t / 0.006) * 0.25)


def send():
    return st.sfx_whoosh(0.3, 0.6, 0.3)


def receive():
    y = st.sfx_bell((81, 88), d=0.7, g=0.16)
    st.place(y, st.sfx_pop(900, 500), 0, 0.3)
    return y


SOUNDS = {
    'key': (key, 0.55),
    'send': (send, 0.9),
    'receive': (receive, 0.9),
    'pop': (lambda: st.sfx_pop(620, 300), 0.8),
}

if __name__ == '__main__':
    name = sys.argv[1]
    out = os.path.join(HERE, 'out')
    silent, final = os.path.join(out, f'{name}-silent.mp4'), os.path.join(out, f'{name}.mp4')
    meta = json.load(open(os.path.join(out, f'{name}.cues.json')))
    if not meta['cues']:
        shutil.copyfile(silent, final)
        print(f'{name}: no cues, copied silent')
        sys.exit()
    x = np.zeros(int(meta['duration'] * st.SR) + 1)
    for c in meta['cues']:
        make, gain = SOUNDS[c['type']]
        st.place(x, make(), c['t'], gain)
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, 'fx.wav')
        st.write_wav(wav, np.tanh(x))
        gain = -20 - st.loudness(wav)
        st.mux(silent, wav, gain, final)
    print(f'{name}: wrote {final} (gain {gain:+.1f} dB)')

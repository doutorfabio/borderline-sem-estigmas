// Renders the soundtrack with OfflineAudioContext inside Chromium and writes soundtrack.wav
import { createRequire } from 'node:module';
import fs from 'node:fs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const b = await chromium.launch(); const p = await b.newPage();
const b64 = await p.evaluate(async () => {
  const sr = 48000, DUR = 24, ctx = new OfflineAudioContext(2, sr * DUR, sr);
  const master = ctx.createGain(); master.gain.value = 0.7;
  const comp = ctx.createDynamicsCompressor(); comp.threshold.value = -16; comp.ratio.value = 3; comp.attack.value = 0.003; comp.release.value = 0.12;
  master.connect(comp); comp.connect(ctx.destination);
  const nb = ctx.createBuffer(1, sr * 2, sr), nd = nb.getChannelData(0); let seed = 1234567;
  for (let i = 0; i < nd.length; i++) { seed = (seed * 1103515245 + 12345) & 0x7fffffff; nd[i] = seed / 0x3fffffff - 1; }
  const env = (g, t, a, peak, d) => { g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(peak, t + a); g.gain.exponentialRampToValueAtTime(0.0001, t + a + d); };
  const pan = v => { const s = ctx.createStereoPanner(); s.pan.value = v; s.connect(master); return s; };
  const C = pan(0);
  let off = 0;
  function noise(t, d, type, f, q, amp, a = 0.002, dest = C) {
    const s = ctx.createBufferSource(); s.buffer = nb; const fl = ctx.createBiquadFilter(); fl.type = type; fl.frequency.value = f; fl.Q.value = q;
    const g = ctx.createGain(); env(g, t, a, amp, d); s.connect(fl); fl.connect(g); g.connect(dest); off = (off + 0.37) % 1.5; s.start(t, off); s.stop(t + a + d + 0.05);
  }
  function tone(t, f0, f1, d, type, amp, a = 0.003, dest = C) {
    const o = ctx.createOscillator(); o.type = type; o.frequency.setValueAtTime(f0, t); if (f1 !== f0) o.frequency.exponentialRampToValueAtTime(f1, t + Math.min(d, 0.14));
    const g = ctx.createGain(); env(g, t, a, amp, d); o.connect(g); g.connect(dest); o.start(t); o.stop(t + a + d + 0.05);
  }
  const kick = (t, amp = 0.95) => { tone(t, 150, 44, 0.36, 'sine', amp, 0.003); noise(t, 0.012, 'highpass', 3000, 0.7, 0.18, 0.001); };
  const hat = (t, amp = 0.05) => noise(t, 0.045, 'highpass', 8500, 0.8, amp, 0.001, pan(0.25));
  const hit = (t, big) => { noise(t, big ? 0.7 : 0.32, 'bandpass', 1500, 0.7, big ? 0.55 : 0.32, 0.002); tone(t, 210, 105, big ? 0.5 : 0.22, 'triangle', big ? 0.4 : 0.25); if (big) tone(t, 55, 55, 1.6, 'sine', 0.5, 0.01); };
  const blip = (t, f = 2300, amp = 0.12) => tone(t, f, f, 0.035, 'sine', amp, 0.001);
  const tick = t => tone(t, 1650, 1650, 0.04, 'triangle', 0.09, 0.001, pan(-0.2));
  function whoosh(t0, t1) {
    const s = ctx.createBufferSource(); s.buffer = nb; const fl = ctx.createBiquadFilter(); fl.type = 'bandpass'; fl.Q.value = 1.2;
    fl.frequency.setValueAtTime(500, t0); fl.frequency.exponentialRampToValueAtTime(4000, t1);
    const g = ctx.createGain(); g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(0.22, t1 - 0.01); g.gain.linearRampToValueAtTime(0.0001, t1 + 0.02);
    s.connect(fl); fl.connect(g); g.connect(C); s.start(t0, 0.2); s.stop(t1 + 0.05);
  }
  function bass(t, f, d) {
    const o = ctx.createOscillator(); o.type = 'sawtooth'; o.frequency.value = f; const fl = ctx.createBiquadFilter(); fl.type = 'lowpass'; fl.frequency.value = 420; fl.Q.value = 2;
    const g = ctx.createGain(); env(g, t, 0.006, 0.2, d); o.connect(fl); fl.connect(g); g.connect(C); o.start(t); o.stop(t + d + 0.05);
  }
  function pad(t, fs, d, amp = 0.035) {
    fs.forEach((f, i) => { const o = ctx.createOscillator(); o.type = 'triangle'; o.frequency.value = f; const g = ctx.createGain();
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(amp, t + 0.06); g.gain.setValueAtTime(amp, t + d - 0.12); g.gain.exponentialRampToValueAtTime(0.0001, t + d);
      o.connect(g); g.connect(pan(i % 2 ? 0.3 : -0.3)); o.start(t); o.stop(t + d + 0.02); });
  }
  const B = 0.5;
  for (let k = 0; k < 48; k++) kick(k * B, k < 8 ? 0.85 : 0.95);
  hit(0, false); [4, 6, 8, 10, 12, 14, 16, 18, 20].forEach(t => hit(t, false)); hit(22, true);
  whoosh(5.62, 6.0); for (let i = 0; i < 6; i++) whoosh(6 + 2 * i + 1.7, 8 + 2 * i); whoosh(19.62, 20.0);
  for (let t = 4.25; t < 23.9; t += B) hat(t);
  // hook drone builds tension
  tone(2.0, 55, 55, 1.95, 'sine', 0.22, 0.05); tone(2.0, 110, 110, 1.95, 'triangle', 0.05, 0.05);
  const roots = [55, 43.65, 65.41, 49.0];
  const chords = [[220, 261.63, 329.63], [174.61, 220, 261.63], [261.63, 329.63, 392], [196, 246.94, 293.66]];
  for (let bar = 2; bar < 11; bar++) { const i = (bar - 2) % 4, t = bar * 2;
    for (let e = 0; e < 4; e++) bass(t + e * B + 0.25, roots[i], 0.2);
    pad(t, chords[i], 2.0); }
  // ending: F then C (payoff on 22)
  for (let e = 0; e < 4; e++) bass(20 + e * B + 0.25, 43.65, 0.2);
  pad(20, chords[1], 2.0); pad(22, [261.63, 329.63, 392, 587.33], 1.98, 0.045);
  for (let e = 0; e < 4; e++) bass(22 + e * B + 0.25, 65.41, 0.2);
  [5.5, 6.5, 8.5, 11.0, 12.5, 13.0, 13.5, 15.0, 16.5].forEach(t => blip(t));
  blip(7.0, 900, 0.18); blip(9.0, 1200, 0.12); blip(11.5, 900, 0.12);
  for (let k = 1; k < 14; k++) tick(16 + 0.5 + k * 0.0625);
  const buf = await ctx.startRendering();
  const L = buf.getChannelData(0), R = buf.getChannelData(1), n = L.length;
  const fade = Math.floor(0.12 * sr);
  const out = new DataView(new ArrayBuffer(44 + n * 4));
  const w = (o, s) => { for (let i = 0; i < s.length; i++) out.setUint8(o + i, s.charCodeAt(i)); };
  w(0, 'RIFF'); out.setUint32(4, 36 + n * 4, true); w(8, 'WAVE'); w(12, 'fmt '); out.setUint32(16, 16, true); out.setUint16(20, 1, true); out.setUint16(22, 2, true);
  out.setUint32(24, sr, true); out.setUint32(28, sr * 4, true); out.setUint16(32, 4, true); out.setUint16(34, 16, true); w(36, 'data'); out.setUint32(40, n * 4, true);
  for (let i = 0; i < n; i++) { const f = i > n - fade ? (n - i) / fade : 1;
    out.setInt16(44 + i * 4, Math.max(-1, Math.min(1, L[i] * f)) * 32767, true); out.setInt16(46 + i * 4, Math.max(-1, Math.min(1, R[i] * f)) * 32767, true); }
  const bytes = new Uint8Array(out.buffer); let s = ''; for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(s);
});
fs.writeFileSync('soundtrack-raw.wav', Buffer.from(b64, 'base64')); await b.close(); console.log('ok');

// Movimento como função do tempo (t em segundos). Nada de curva desenhada:
// só exponencial e mola, em forma fechada, para qualquer t dar o mesmo quadro.

export const prender = (x: number, a: number, b: number): number =>
  Math.min(b, Math.max(a, x));

export const misturar = (a: number, b: number, m: number): number =>
  a + (b - a) * m;

/** Aproximação exponencial: 0 → 1, sai rápido e assenta sem passar do ponto. */
export const expo = (t: number, tau: number): number =>
  t <= 0 ? 0 : 1 - Math.exp(-t / tau);

/** Mola com amortecimento crítico, resposta ao degrau: 0 → 1 sem passar do ponto. */
export const molaCritica = (t: number, omega: number): number =>
  t <= 0 ? 0 : 1 - (1 + omega * t) * Math.exp(-omega * t);

/**
 * Mola subamortecida em torno de zero: posição em t, saindo de x0 com
 * velocidade v0. Com zeta perto de 0,6 passa do ponto uma vez e para.
 */
export const molaSub = (
  t: number,
  omega: number,
  zeta: number,
  x0: number,
  v0: number,
): number => {
  if (t <= 0) {
    return x0;
  }
  const wd = omega * Math.sqrt(1 - zeta * zeta);
  const b = (v0 + zeta * omega * x0) / wd;
  return (
    Math.exp(-zeta * omega * t) * (x0 * Math.cos(wd * t) + b * Math.sin(wd * t))
  );
};

/**
 * Resposta ao impulso de uma mola crítica: afunda e volta a zero sem oscilar.
 * `pico` é o deslocamento máximo, atingido em t = 1 / omega.
 */
export const impulsoCritico = (
  t: number,
  omega: number,
  pico: number,
): number =>
  t <= 0 ? 0 : pico * Math.E * omega * t * Math.exp(-omega * t);

/** Queda pesada: aceleração exponencial de 0 a 1 para p em [0, 1]. */
export const quedaExpo = (p: number, k: number): number => {
  if (p <= 0) {
    return 0;
  }
  if (p >= 1) {
    return 1;
  }
  return (Math.exp(k * p) - 1) / (Math.exp(k) - 1);
};

/** Velocidade de uma função do tempo, por diferença central. */
export const velocidade = (f: (t: number) => number, t: number): number => {
  const h = 1e-4;
  return (f(t + h) - f(t - h)) / (2 * h);
};

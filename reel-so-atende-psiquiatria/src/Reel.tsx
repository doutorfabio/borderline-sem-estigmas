import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame, interpolate } from "remotion";
import timeline from "./timeline.json";
import { C, SW, GROUND, TITLE, prog, count, FadeUp, GUp, TitleBox, Big, Small, Ground, Person, Seated, Chair, Mini, MiniKind, CapsBuilding, Caption } from "./kit";

type Scene = (typeof timeline.scenes)[number];
type K = Record<string, number>;
type P = { t: number; sc: Scene; k: K };

const FPS = 30;
const SVG: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{ position: "absolute", inset: 0 }}>{children}</svg>
);

/* ---------- 01 e 02: o cochicho ---------- */
const BALLOON_TEXT = ["ELE SÓ ATENDE", "PSIQUIATRIA"];
const Whisper: React.FC<{ t: number; entry: boolean }> = ({ t, entry }) => {
  const pb = entry ? 0.6 + 0.4 * prog(t, 0, 0.4) : 1;
  return (
    <>
      <g opacity={entry ? 0.6 + 0.4 * prog(t, 0, 0.5) : 1} transform={`translate(0 ${entry ? 18 * (1 - prog(t, 0, 0.5)) : 0})`}>
        <Ground />
        <Person x={420} y={GROUND} s={1.3} lean={9} hand />
        <Person x={690} y={GROUND} s={1.3} fill={C.coat} />
      </g>
      <g opacity={pb} transform={`translate(540 455) scale(${0.94 + 0.06 * pb}) translate(-540 -455)`}>
        <path d="M150,300 Q150,282 168,282 L912,282 Q930,282 930,300 L930,598 Q930,616 912,616 L470,616 L400,712 L398,616 L168,616 Q150,616 150,598 Z" fill={C.coat} stroke={C.ink} strokeWidth={SW} strokeLinejoin="round" />
        {BALLOON_TEXT.map((l, i) => (
          <text key={l} x={540} y={420 + i * 118} textAnchor="middle" fontFamily={TITLE} fontSize={82} fill={C.ink}>{l}</text>
        ))}
      </g>
    </>
  );
};
const S01: React.FC<P> = ({ t }) => <SVG><Whisper t={t} entry /></SVG>;

const S02: React.FC<P> = ({ t, k }) => {
  const a = prog(t, k.naoe - 1.3, 0.7);
  const b = prog(t, k.naoe - 0.9, 0.7);
  return (
    <>
      <SVG>
        <Whisper t={t} entry={false} />
        <line x1={190} y1={392} x2={190 + 700 * a} y2={392} stroke={C.brick} strokeWidth={16} strokeLinecap="round" />
        <line x1={250} y1={510} x2={250 + 580 * b} y2={510} stroke={C.brick} strokeWidth={16} strokeLinecap="round" />
      </SVG>
      <FadeUp t={t} at={k.naoe} style={{ position: "absolute", top: 735, left: 90, width: 900, textAlign: "center" }}>
        <Big size={86} color={C.brick}>NÃO É PROTEÇÃO</Big>
      </FadeUp>
    </>
  );
};

/* ---------- 03: carteira do CRM e carimbo ---------- */
const S03: React.FC<P> = ({ t, k }) => {
  const hit = k.pode;
  const down = interpolate(t, [hit - 0.45, hit, hit + 0.5, hit + 0.9], [-260, 0, 0, -330], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const seal = prog(t, hit, 0.15);
  return (
    <>
      <TitleBox>
        <FadeUp t={t} at={0}><Big size={92}>ATENDER: PODE.</Big></FadeUp>
        <FadeUp t={t} at={k.proibido} style={{ marginTop: 34 }}>
          <Big size={50}>ANUNCIAR ESPECIALIDADE</Big>
          <Big size={50}>SEM REGISTRO:</Big>
          <Big size={74} color={C.brick} style={{ marginTop: 8 }}>NÃO PODE.</Big>
        </FadeUp>
      </TitleBox>
      <SVG>
        <GUp t={t} at={0.15}>
          <Ground y={1300} />
          <g transform="rotate(-4 470 1030)">
            <rect x={200} y={850} width={560} height={350} rx={22} fill={C.coat} stroke={C.ink} strokeWidth={SW} />
            <path d="M200,872 Q200,850 222,850 L738,850 Q760,850 760,872 L760,930 L200,930 Z" fill={C.ink} />
            <text x={240} y={910} fontFamily={TITLE} fontSize={44} fill={C.coat}>CRM</text>
            <rect x={240} y={965} width={150} height={190} rx={10} fill={C.paper} stroke={C.ink} strokeWidth={5} />
            <circle cx={315} cy={1035} r={30} fill={C.bg} stroke={C.ink} strokeWidth={5} />
            <path d="M265,1150 Q265,1080 315,1080 Q365,1080 365,1150 Z" fill={C.bg} stroke={C.ink} strokeWidth={5} />
            {[990, 1040, 1090, 1140].map((y, i) => (
              <line key={y} x1={420} y1={y} x2={i % 2 ? 640 : 710} y2={y} stroke={C.ink} strokeWidth={8} strokeLinecap="round" opacity={0.75} />
            ))}
          </g>
          <g opacity={seal} transform={`translate(640 1110) rotate(-12) scale(${1.25 - 0.25 * seal})`}>
            <circle r={78} fill="none" stroke={C.brick} strokeWidth={10} />
            <circle r={62} fill="none" stroke={C.brick} strokeWidth={4} />
            <path d="M-34,0 L-8,26 L38,-26" fill="none" stroke={C.brick} strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" />
          </g>
          <g transform={`translate(640 ${1032 + down})`} opacity={t < hit + 0.95 ? 1 : 0}>
            <rect x={-80} y={-40} width={160} height={36} rx={6} fill={C.brick} stroke={C.ink} strokeWidth={SW} />
            <rect x={-18} y={-120} width={36} height={80} fill={C.paper} stroke={C.ink} strokeWidth={SW} />
            <circle cx={0} cy={-150} r={40} fill={C.ink} />
          </g>
        </GUp>
      </SVG>
    </>
  );
};

/* ---------- 04: o medico em frente ao CAPS ---------- */
const S04: React.FC<P> = ({ t }) => (
  <>
    <TitleBox>
      <FadeUp t={t} at={0}><Big size={84}>Dr. Fabio Schmidt</Big></FadeUp>
      <FadeUp t={t} at={0.25} style={{ marginTop: 18 }}><Small size={40}>Médico, pós-graduado em psiquiatria</Small></FadeUp>
      <FadeUp t={t} at={0.45} style={{ marginTop: 6 }}><Small size={40} color={C.brick}>CRM-SP 183549</Small></FadeUp>
    </TitleBox>
    <SVG>
      <GUp t={t} at={0.1}>
        <Ground />
        <CapsBuilding x={190} y={GROUND} w={700} h={600} />
      </GUp>
      <GUp t={t} at={0.35}>
        <Person x={330} y={GROUND} s={1.2} coat />
      </GUp>
    </SVG>
  </>
);

/* ---------- 05 e 06: a grade de 100 ---------- */
// 61 psiquiatra, 31 clinico geral, 4 residentes, 4 outras ocupacoes medicas
const KINDS: MiniKind[] = [...Array(61).fill("psiq"), ...Array(31).fill("clin"), ...Array(4).fill("res"), ...Array(4).fill("outra")];
const GX = 120, GY = 640, CW = 84, CH = 62;
const Grid: React.FC<{ t: number; mode: "in" | "static" | "drop"; k: K }> = ({ t, mode, k }) => (
  <>
    {KINDS.map((kind, i) => {
      const col = i % 10, row = Math.floor(i / 10);
      const x = GX + col * CW + CW / 2 - 4, y = GY + row * CH + CH - 4;
      let op = 1, s = 0.95, kk: MiniKind = kind;
      if (mode === "in") {
        op = prog(t, 0.2 + i * 0.012, 0.3);
        if (kind === "clin" && k.n3127) s += 0.25 * Math.sin(Math.PI * prog(t, k.n3127, 0.5));
        if ((kind === "res") && k.n434) s += 0.35 * Math.sin(Math.PI * prog(t, k.n434, 0.5));
      }
      if (mode === "drop" && kind !== "psiq") {
        const at = k.vazios + (i - 61) * 0.022;
        const p = prog(t, at, 0.35);
        if (p >= 0.5) kk = "vazio";
        op = p < 0.5 ? 1 - p * 1.4 : 0.3 + (p - 0.5) * 1.4;
      }
      return <Mini key={i} x={x} y={y} kind={kk} s={s} op={op} />;
    })}
  </>
);
const Legend: React.FC = () => {
  const items: [MiniKind, string][] = [["psiq", "psiquiatra"], ["clin", "clínico geral"], ["res", "residente"], ["outra", "outras"]];
  let x = 132;
  return (
    <g>
      {items.map(([kind, label]) => {
        const el = (
          <g key={label}>
            <Mini x={x + 16} y={1318} kind={kind} s={0.8} />
            <text x={x + 40} y={1312} fontFamily="'Poppins', sans-serif" fontWeight={600} fontSize={26} fill={C.ink}>{label}</text>
          </g>
        );
        x += 52 + label.length * 14.5 + 28;
        return el;
      })}
    </g>
  );
};
const Numbers5: React.FC<{ t: number; k: K; fixed?: boolean; out?: number }> = ({ t, k, fixed, out }) => {
  const tt = fixed ? 99 : t;
  return (
    <TitleBox top={265} style={{ opacity: out !== undefined ? 1 - prog(t, out, 0.3) : 1 }}>
      <FadeUp t={tt} at={fixed ? 0 : k.n10129 - 0.1} d={0.3}>
        <Big size={150}>{count(tt, k.n10129 ?? 0, 10129)}</Big>
        <Small size={38}>vínculos de médico em CAPS</Small>
      </FadeUp>
      <div style={{ display: "flex", justifyContent: "center", gap: 70, marginTop: 22 }}>
        <FadeUp t={tt} at={fixed ? 0 : k.n3127 - 0.05} d={0.3}>
          <Big size={64} color={C.brick}>{count(tt, k.n3127 ?? 0, 3127, 0.7)}</Big>
          <Small size={32}>clínico geral</Small>
        </FadeUp>
        <FadeUp t={tt} at={fixed ? 0 : k.n434 - 0.05} d={0.3}>
          <Big size={64}>{count(tt, k.n434 ?? 0, 434, 0.6)}</Big>
          <Small size={32}>residentes</Small>
        </FadeUp>
      </div>
    </TitleBox>
  );
};
const S05: React.FC<P> = ({ t, k }) => (
  <>
    <Numbers5 t={t} k={k} />
    <SVG>
      <Grid t={t} mode="in" k={k} />
      <GUp t={t} at={1.2}><Legend /></GUp>
    </SVG>
  </>
);
const S06: React.FC<P> = ({ t, k }) => (
  <>
    <Numbers5 t={t} k={timeline.scenes.find((x) => x.id === 5)!.keys as K} fixed out={k.quase - 0.35} />
    <TitleBox top={290}>
      <FadeUp t={t} at={k.quase}>
        <Big size={104}>QUASE <span style={{ color: C.brick }}>4</span></Big>
        <Big size={104}>EM CADA <span style={{ color: C.brick }}>10.</span></Big>
      </FadeUp>
      <FadeUp t={t} at={k.minimo} style={{ marginTop: 12 }}>
        <Big size={64} color={C.brick}>NO MÍNIMO.</Big>
      </FadeUp>
    </TitleBox>
    <SVG>
      <Grid t={t} mode="drop" k={k} />
      <Legend />
    </SVG>
  </>
);

/* ---------- 07: as luzes que apagam ---------- */
const S07: React.FC<P> = ({ t, k, sc }) => {
  const cols = 5, rows = 4, cw = 170, ch = 150, x0 = 115, y0 = 700;
  const n = cols * rows;
  const span = sc.frames / FPS - 1.2 - (k.n269 + 0.5);
  return (
    <>
      <TitleBox top={262}>
        <FadeUp t={t} at={Math.max(0, k.n269 - 0.1)} d={0.3}><Big size={176} color={C.brick}>{count(t, k.n269, 269, 0.8)}</Big></FadeUp>
        <FadeUp t={t} at={k.n269 + 0.2}>
          <Big size={58}>CIDADES SEM MÉDICO</Big>
          <Big size={58}>NO CAPS</Big>
        </FadeUp>
      </TitleBox>
      <SVG>
        {Array.from({ length: n }).map((_, i) => {
          const col = i % cols, row = Math.floor(i / cols);
          const x = x0 + col * cw + 25, y = y0 + row * ch;
          const off = t > k.n269 + 0.5 + (i / n) * span;
          const win = off ? C.ink : C.coat;
          return (
            <GUp key={i} t={t} at={i * 0.02} d={0.3} dy={14}>
              <g strokeLinejoin="round">
                <rect x={x} y={y + 30} width={120} height={96} fill={C.paper} stroke={C.ink} strokeWidth={5} />
                <rect x={x - 8} y={y + 18} width={136} height={14} fill={C.ink} />
                <rect x={x + 14} y={y + 50} width={30} height={28} fill={win} stroke={C.ink} strokeWidth={4} />
                <rect x={x + 76} y={y + 50} width={30} height={28} fill={win} stroke={C.ink} strokeWidth={4} />
                <rect x={x + 48} y={y + 90} width={24} height={36} fill={C.ink} />
                <line x1={x - 16} y1={y + 126} x2={x + 136} y2={y + 126} stroke={C.ink} strokeWidth={5} strokeLinecap="round" />
              </g>
            </GUp>
          );
        })}
      </SVG>
    </>
  );
};

/* ---------- 08 e 09: as duas filas ---------- */
const DOC_X = [190, 290, 390];
const PPL_X = [180, 270, 360, 450, 540, 630, 720, 810, 900];
const Queues: React.FC<{ t: number; entry: boolean; k: K }> = ({ t, entry, k }) => (
  <>
    <Ground y={1010} x1={120} x2={960} />
    <Ground y={1310} x1={120} x2={960} />
    {DOC_X.map((x, i) => (
      <g key={x} opacity={entry ? prog(t, (k.n13581 ?? 0) - 0.2 + i * 0.15, 0.3) : 1}>
        <Person x={x} y={1010} s={0.6} coat />
      </g>
    ))}
    {PPL_X.map((x, i) => (
      <g key={x} opacity={entry ? prog(t, 0.1 + i * 0.12, 0.3) : 1}>
        <Person x={x} y={1310} s={0.6} />
      </g>
    ))}
    <text x={470} y={1000} fontFamily="'Poppins', sans-serif" fontWeight={600} fontSize={28} fill={C.ink} opacity={entry ? prog(t, (k.n13581 ?? 0) + 0.4) : 1}>médicos com título</text>
  </>
);
const S08: React.FC<P> = ({ t, k }) => (
  <>
    <TitleBox top={262}>
      <FadeUp t={t} at={k.n13581 - 0.1} d={0.3}>
        <Big size={112}>{count(t, k.n13581, 13581)}</Big>
        <Big size={44}>COM TÍTULO NO PAÍS.</Big>
      </FadeUp>
      <FadeUp t={t} at={k.n650 - 0.1} d={0.3} style={{ marginTop: 26 }}>
        <Big size={112} color={C.brick}>{count(t, k.n650, 650, 0.7)}</Big>
        <Big size={44}>NOVOS POR ANO.</Big>
      </FadeUp>
    </TitleBox>
    <SVG><Queues t={t} entry k={k} /></SVG>
  </>
);
const S09: React.FC<P> = ({ t, k }) => {
  const p = prog(t, 0.25, 0.6);
  const q = prog(t, k.nem, 0.4);
  return (
    <>
      <TitleBox top={330}>
        <FadeUp t={t} at={0}><Big size={150} color={C.brick}>NÃO FECHA</Big></FadeUp>
      </TitleBox>
      <SVG>
        <rect x={425} y={1080} width={510 * p} height={236} rx={14} fill={C.brick} opacity={0.16 + 0.1 * q} />
        <Queues t={t} entry={false} k={k} />
        <g opacity={p} stroke={C.brick} strokeWidth={8} strokeLinecap="round" fill="none">
          <path d={`M430,1070 L430,1050 L${430 + 500 * p},1050 L${430 + 500 * p},1070`} />
          <line x1={430} y1={1030} x2={430} y2={1022} />
        </g>
        <line x1={430} y1={930} x2={430} y2={1340} stroke={C.brick} strokeWidth={6} strokeDasharray="14 12" opacity={p} />
      </SVG>
    </>
  );
};

/* ---------- 10: a sala de espera ---------- */
const S10: React.FC<P> = ({ t }) => (
  <>
    <TitleBox top={300}>
      <FadeUp t={t} at={0}><Big size={98}>QUEM ATENDE</Big><Big size={98}>NO LUGAR?</Big></FadeUp>
    </TitleBox>
    <SVG>
      <GUp t={t} at={0.15}>
        <Ground />
        <rect x={150} y={720} width={190} height={74} rx={8} fill={C.brick} stroke={C.ink} strokeWidth={SW} />
        <text x={245} y={777} textAnchor="middle" fontFamily={TITLE} fontSize={48} fill={C.paper}>CAPS</text>
        {/* guiche */}
        <rect x={600} y={730} width={340} height={300} fill={C.paper} stroke={C.ink} strokeWidth={SW} />
        {[0, 1, 2, 3, 4, 5, 6].map((i) => (
          <line key={i} x1={612} y1={762 + i * 38} x2={928} y2={762 + i * 38} stroke={C.ink} strokeWidth={4} opacity={0.7} />
        ))}
        <rect x={580} y={1030} width={380} height={290} fill={C.paper} stroke={C.ink} strokeWidth={SW} />
        <rect x={570} y={1024} width={400} height={28} fill={C.ink} />
      </GUp>
      <GUp t={t} at={0.45}>
        <line x1={690} y1={800} x2={770} y2={760} stroke={C.ink} strokeWidth={4} />
        <line x1={850} y1={800} x2={770} y2={760} stroke={C.ink} strokeWidth={4} />
        <circle cx={770} cy={758} r={7} fill={C.ink} />
        <rect x={625} y={800} width={290} height={136} rx={8} fill={C.coat} stroke={C.brick} strokeWidth={7} />
        <text x={770} y={858} textAnchor="middle" fontFamily={TITLE} fontSize={34} fill={C.brick}>SEM MÉDICO</text>
        <text x={770} y={910} textAnchor="middle" fontFamily={TITLE} fontSize={34} fill={C.brick}>HOJE</text>
      </GUp>
      <GUp t={t} at={0.3}>
        <Chair x={200} y={GROUND} />
        <Chair x={350} y={GROUND} />
        <Chair x={500} y={GROUND} />
        <Seated x={345} y={GROUND} s={0.95} />
      </GUp>
    </SVG>
  </>
);

/* ---------- 11: diploma na parede, porta fechada ---------- */
const S11: React.FC<P> = ({ t, k }) => (
  <>
    <SVG>
      <GUp t={t} at={0}>
        <rect x={270} y={290} width={540} height={330} fill={C.ink} />
        <rect x={290} y={310} width={500} height={290} fill={C.coat} stroke={C.ink} strokeWidth={4} />
        <rect x={420} y={345} width={240} height={22} rx={6} fill={C.ink} />
        {[410, 445, 480].map((y, i) => (
          <line key={y} x1={350} y1={y} x2={i === 1 ? 650 : 730} y2={y} stroke={C.ink} strokeWidth={6} strokeLinecap="round" opacity={0.6} />
        ))}
        <line x1={350} y1={555} x2={520} y2={555} stroke={C.ink} strokeWidth={4} />
        <path d="M670,560 L655,612 L675,600 L690,616 L695,560 Z" fill={C.brick} />
        <circle cx={680} cy={540} r={36} fill={C.brick} stroke={C.ink} strokeWidth={4} />
        <circle cx={680} cy={540} r={22} fill="none" stroke={C.coat} strokeWidth={3} />
      </GUp>
      <GUp t={t} at={0.3}>
        <Ground />
        <rect x={300} y={830} width={480} height={490} fill={C.paper} stroke={C.ink} strokeWidth={SW} />
        <rect x={380} y={900} width={320} height={420} fill={C.ink} />
        <circle cx={660} cy={1120} r={9} fill={C.paper} />
        <rect x={406} y={852} width={268} height={34} fill={C.brick} />
        <text x={540} y={881} textAnchor="middle" fontFamily={TITLE} fontSize={30} fill={C.paper}>CAPS</text>
      </GUp>
      <GUp t={t} at={3.95}>
        <line x1={450} y1={990} x2={540} y2={940} stroke={C.paper} strokeWidth={4} />
        <line x1={630} y1={990} x2={540} y2={940} stroke={C.paper} strokeWidth={4} />
        <circle cx={540} cy={938} r={7} fill={C.paper} />
        <rect x={400} y={990} width={280} height={90} rx={8} fill={C.coat} stroke={C.brick} strokeWidth={7} />
        <text x={540} y={1052} textAnchor="middle" fontFamily={TITLE} fontSize={48} fill={C.brick}>FECHADO</text>
      </GUp>
    </SVG>
    <TitleBox top={655}>
      <FadeUp t={t} at={k.n269 - 0.1} d={0.3}>
        <Big size={112}>
          <span style={{ color: C.brick }}>{count(t, k.n269, 269, 0.6)}</span> CIDADES
        </Big>
      </FadeUp>
    </TitleBox>
  </>
);

/* ---------- 12: na porta do CAPS, assinatura ---------- */
const S12: React.FC<P> = ({ t, k, sc }) => {
  const walk = prog(t, 0, 1.6);
  const endAt = sc.speechEnd + 0.35;
  return (
    <>
      <TitleBox top={300}>
        <FadeUp t={t} at={k.pergunta - 0.05} out={endAt}>
          <Big size={96}>PERGUNTA SE</Big>
          <Big size={96} color={C.brick}>TEM MÉDICO</Big>
        </FadeUp>
      </TitleBox>
      <TitleBox top={270}>
        <FadeUp t={t} at={endAt + 0.2}><Big size={66}>@drfabioschmidt</Big></FadeUp>
        <FadeUp t={t} at={endAt + 0.45} style={{ marginTop: 22 }}>
          <Small size={28} weight={400}>Fontes: CNES/DATASUS, competência out/2026.</Small>
          <Small size={28} weight={400}>Demografia Médica no Brasil 2025.</Small>
          <Small size={28} weight={400}>Parecer CRM-AM 1/2026.</Small>
        </FadeUp>
        <FadeUp t={t} at={endAt + 0.75} style={{ marginTop: 26 }}>
          <Small size={40} weight={700} color={C.brick}>Manda para um colega</Small>
          <Small size={40} weight={700} color={C.brick}>que trabalha em CAPS.</Small>
        </FadeUp>
      </TitleBox>
      <SVG>
        <GUp t={t} at={0}>
          <Ground />
          <CapsBuilding x={190} y={GROUND} w={700} h={600} />
        </GUp>
        <Person x={interpolate(walk, [0, 1], [200, 375])} y={GROUND} s={1.15} op={prog(t, 0, 0.3)} />
      </SVG>
    </>
  );
};

const MAP: Record<number, React.FC<P>> = { 1: S01, 2: S02, 3: S03, 4: S04, 5: S05, 6: S06, 7: S07, 8: S08, 9: S09, 10: S10, 11: S11, 12: S12 };

const SceneWrap: React.FC<{ sc: Scene }> = ({ sc }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const Comp = MAP[sc.id];
  return (
    <AbsoluteFill>
      <Comp t={t} sc={sc} k={sc.keys as K} />
      <Caption t={t} chunks={sc.chunks} />
    </AbsoluteFill>
  );
};

export const Reel: React.FC = () => {
  const f = useCurrentFrame();
  const fadeEnd = interpolate(f, [timeline.total - 4, timeline.total - 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: C.bg }}>
      {timeline.scenes.map((sc) => (
        <Sequence key={sc.id} from={sc.from_} durationInFrames={sc.frames} layout="none">
          <SceneWrap sc={sc} />
        </Sequence>
      ))}
      <AbsoluteFill style={{ backgroundColor: C.bg, opacity: fadeEnd }} />
    </AbsoluteFill>
  );
};

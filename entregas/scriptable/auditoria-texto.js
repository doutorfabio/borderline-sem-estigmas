// Auditoria de Texto - Borderline Sem Estigma
// App Scriptable (iOS). Confere legenda, roteiro ou texto de slide
// contra os erros que já foram pegos (memoria/aprendizados.md, seção 0,
// e memoria/checklist-entrega.md).
//
// Como usar:
// 1. Copie o texto e rode o script. Ele lê a área de transferência.
// 2. Ou selecione o texto em qualquer app, Compartilhar > Run Script.
// 3. Ou num Atalho: ação Run Script com o texto como entrada.
//    O resultado volta como saída do Atalho.
//
// ERRO = regra fixa. CONFERIR = pode ser falso alarme, leia em voz alta.

const REGRAS = [
  {
    nome: "Contraste não é X, é Y",
    nivel: "ERRO",
    re: /\bnão\s+(é|são|foi|era|está|tá)\b[^.!?\n]{0,60}?[,;.:]\s*(é|são|foi|era|está|tá)\b/gi,
  },
  {
    nome: "Contraste não é só X",
    nivel: "CONFERIR",
    re: /\bnão\s+(é|são)\s+(só|apenas|sobre|falta de|frescura)\b/gi,
  },
  {
    nome: "Contraste X, não Y",
    nivel: "CONFERIR",
    re: /,\s*não\s+(o|a|os|as|um|uma|de|do|da|por|pra|para|com|em)\b[^.!?\n]{0,40}[.!?\n]/gi,
  },
  { nome: "Travessão", nivel: "ERRO", re: /[—–]/g },
  { nome: "Emoji", nivel: "ERRO", re: /\p{Extended_Pictographic}/gu },
  { nome: "Aspas (proibido em slide)", nivel: "CONFERIR", re: /["“”«»]/g },
  { nome: "Fórmula quem aprendeu cedo", nivel: "ERRO", re: /quem aprendeu cedo/gi },
  {
    nome: "Título profissional",
    nivel: "ERRO",
    re: /\b(psiquiatra|especialista em psiquiatria)\b/gi,
  },
  {
    nome: "Neurobiologia no feed",
    nivel: "CONFERIR",
    re: /\b(amígdala|córtex|pré-frontal|cortisol|dopamina|serotonina|neurotransmiss\w*|sistema límbico)\b/gi,
  },
  {
    nome: "Duplo sentido ou gíria",
    nivel: "CONFERIR",
    re: /\b(dar|dá|dou|deu|dando|comer|come|pegar|pega|pegou|ficar|fica|ficou|gozar|mamar|encher|enche)\b/gi,
  },
  { nome: "COMEÇAR (só com ponte ao Protocolo 7 Dias)", nivel: "CONFERIR", re: /\bCOMEÇAR\b/g },
  {
    nome: "Pedido de relato íntimo",
    nivel: "CONFERIR",
    re: /\b(comenta|conta|me conta|escreve)\b[^.!?\n]{0,40}\b(crise|se cortou|autolesão|machucou|violência)\b/gi,
  },
];

// \b do JavaScript não reconhece acento (é, dá, não). Troca por limite que entende letras do português.
const LIMITE = "(?:(?<!\\p{L})(?=\\p{L})|(?<=\\p{L})(?!\\p{L}))";
for (const r of REGRAS) {
  const flags = r.re.flags.includes("u") ? r.re.flags : r.re.flags + "u";
  r.re = new RegExp(r.re.source.replace(/\\b/g, LIMITE), flags);
}

function trecho(texto, i, tam) {
  const ini = Math.max(0, i - 25);
  const fim = Math.min(texto.length, i + tam + 25);
  return (ini > 0 ? "..." : "") + texto.slice(ini, fim).replace(/\s+/g, " ").trim() + (fim < texto.length ? "..." : "");
}

function auditar(texto) {
  const achados = [];

  for (const r of REGRAS) {
    r.re.lastIndex = 0;
    let m;
    while ((m = r.re.exec(texto)) !== null) {
      achados.push({ nivel: r.nivel, regra: r.nome, trecho: trecho(texto, m.index, m[0].length) });
      if (m[0].length === 0) r.re.lastIndex++;
    }
  }

  // Frase abrindo com pronome. Você é permitido.
  const frases = texto.split(/(?<=[.!?])\s+|\n+/).map((f) => f.trim()).filter(Boolean);
  for (const f of frases) {
    const primeira = f.replace(/^[^\p{L}]+/u, "").split(/\s+/)[0].toLowerCase();
    if (["ele", "ela", "eles", "elas"].includes(primeira)) {
      achados.push({ nivel: "ERRO", regra: "Frase abre com ele ou ela", trecho: f.slice(0, 70) });
    } else if (["eu", "nós", "isso", "isto", "aquilo", "esse", "essa"].includes(primeira)) {
      achados.push({ nivel: "CONFERIR", regra: "Frase abre com pronome", trecho: f.slice(0, 70) });
    }
  }

  // Palavra curta sozinha na linha (texto de slide).
  const linhas = texto.split("\n").map((l) => l.trim()).filter(Boolean);
  if (linhas.length > 1) {
    for (const l of linhas) {
      const palavras = l.split(/\s+/);
      if (palavras.length <= 2 && palavras.every((p) => p.replace(/[^\p{L}]/gu, "").length <= 3)) {
        achados.push({ nivel: "ERRO", regra: "Palavra curta isolada na linha", trecho: l });
      }
    }
  }

  achados.sort((a, b) => (a.nivel === b.nivel ? 0 : a.nivel === "ERRO" ? -1 : 1));
  return achados;
}

function resumoTexto(achados) {
  if (achados.length === 0) return "Nenhum alerta. Leia em voz alta antes de postar.";
  return achados.map((a) => `${a.nivel} | ${a.regra}\n${a.trecho}`).join("\n\n");
}

// ---------- Execução no Scriptable ----------
if (typeof Script !== "undefined") {
  let texto = (args.plainTexts && args.plainTexts.join("\n")) || args.shortcutParameter || Pasteboard.paste() || "";
  texto = String(texto);

  if (!texto.trim()) {
    const a = new Alert();
    a.title = "Sem texto";
    a.message = "Copie a legenda ou o roteiro e rode de novo.";
    a.addAction("OK");
    await a.present();
    Script.complete();
  } else {
    const achados = auditar(texto);
    const resumo = resumoTexto(achados);

    if (config.runsWithSiri || args.shortcutParameter) {
      Script.setShortcutOutput(resumo);
    } else {
      const erros = achados.filter((a) => a.nivel === "ERRO").length;
      const conferir = achados.length - erros;

      const t = new UITable();
      t.showSeparators = true;

      const topo = new UITableRow();
      topo.isHeader = true;
      topo.height = 70;
      topo.addText(
        achados.length === 0 ? "Tudo limpo" : `${erros} erro(s), ${conferir} para conferir`,
        `${texto.length} caracteres analisados`
      );
      t.addRow(topo);

      for (const a of achados) {
        const r = new UITableRow();
        r.height = 80;
        const c = r.addText(`${a.nivel}  ${a.regra}`, a.trecho);
        c.titleColor = a.nivel === "ERRO" ? Color.red() : Color.orange();
        c.subtitleFont = Font.systemFont(13);
        t.addRow(r);
      }

      const copiar = new UITableRow();
      copiar.height = 50;
      copiar.addButton("Copiar relatório").onTap = () => Pasteboard.copy(resumo);
      t.addRow(copiar);

      await t.present();
    }
    Script.complete();
  }
} else if (typeof module !== "undefined") {
  module.exports = { auditar, resumoTexto };
}

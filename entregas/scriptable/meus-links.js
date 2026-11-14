// Meus Links - Dr. Fabio Schmidt
// App Scriptable (iOS). Toque no botão e o link vai para a área de transferência.
// Para adicionar ou trocar link, edite a lista LINKS abaixo.

const LINKS = [
  { nome: "Protocolo 7 Dias (site)", url: "https://curso.drfabioschmidt.net/" },
  { nome: "Protocolo 7 Dias (pagamento)", url: "https://pay.hotmart.com/S104212285E" },
  { nome: "Marcar consulta", url: "https://consultadrfabio.base44.app/" },
  { nome: "Respira", url: "https://respira.base44.app/" },
  { nome: "Instagram", url: "https://www.instagram.com/drfabioschmidt" },
];

// Atalho direto: rodar com parâmetro (ex.: "consulta") copia sem abrir a lista.
const pedido = (args.queryParameters && args.queryParameters.link) || args.shortcutParameter;
if (pedido) {
  const alvo = LINKS.find((l) => l.nome.toLowerCase().includes(String(pedido).toLowerCase()));
  if (alvo) {
    Pasteboard.copy(alvo.url);
    Script.setShortcutOutput(alvo.url);
  }
  Script.complete();
} else if (config.runsInWidget) {
  // Widget: cada linha abre o script e copia aquele link.
  const w = new ListWidget();
  w.backgroundColor = new Color("#F4EFE8");
  const t = w.addText("Copiar link");
  t.font = Font.boldSystemFont(13);
  t.textColor = new Color("#3A2E28");
  w.addSpacer(6);
  const max = config.widgetFamily === "small" ? 3 : LINKS.length;
  for (const l of LINKS.slice(0, max)) {
    const s = w.addStack();
    s.url = `scriptable:///run/${encodeURIComponent(Script.name())}?link=${encodeURIComponent(l.nome)}`;
    const txt = s.addText(l.nome);
    txt.font = Font.systemFont(12);
    txt.textColor = new Color("#3A2E28");
    txt.lineLimit = 1;
    w.addSpacer(4);
  }
  Script.setWidget(w);
  Script.complete();
} else {
  const tabela = new UITable();
  tabela.showSeparators = true;

  const topo = new UITableRow();
  topo.isHeader = true;
  topo.height = 50;
  topo.addText("Toque para copiar");
  tabela.addRow(topo);

  for (const l of LINKS) {
    const r = new UITableRow();
    r.height = 64;
    r.dismissOnSelect = false;
    r.addText(l.nome, l.url.replace(/^https?:\/\//, ""));
    const b = r.addButton("Copiar");
    b.rightAligned();
    b.widthWeight = 25;
    r.cellSpacing = 8;
    const copiar = () => {
      Pasteboard.copy(l.url);
      const n = new Notification();
      n.title = "Copiado";
      n.body = l.nome;
      n.schedule();
    };
    b.onTap = copiar;
    r.onSelect = copiar;
    tabela.addRow(r);
  }

  await tabela.present();
  Script.complete();
}

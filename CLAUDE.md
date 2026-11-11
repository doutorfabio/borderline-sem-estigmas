# Novo: Borderline Sem Estigma

Repositório do Dr. Fabio Schmidt (@drfabioschmidt).

## Antes de qualquer resposta ou tarefa

Leia `memoria/BRAIN.md` e `memoria/brain.json`. As regras do BRAIN.md prevalecem sobre preferência do Claude. Se violar um anti-pattern, registre na hora em `memoria/brain-log.md` (direto no `main`, como o resto de `memoria/`) e atualize `ultima_violacao` no `brain.json`. Pedido dele em 07/11/2026.

## Antes de criar ou revisar qualquer peça

Leia, nesta ordem:
1. `memoria/aprendizados.md`: o que ele já corrigiu, rejeitou e aprovou. É obrigatório.
2. `memoria/correcoes.md`: correções mais recentes.
3. `memoria/conta.md`: oferta, preços e dados.
4. `memoria/ja-produzido.md`: gigantes e teses já usadas.
5. `memoria/a-decidir.md`: contradições ainda abertas.
6. Para vídeo: `memoria/efeitos-video-aprovados.md`.
7. Skill `historico-borderline-180d` para não repetir tese.
8. Para tema, ideia ou formato que já funcionou fora: skill `pesquisa-validados` (Vamos + memória + histórico).

Se a peça bater em algo que ele já rejeitou, refaça antes de entregar.

## Quando ele corrigir, rejeitar ou aprovar algo

Registre na hora em `memoria/correcoes.md`, com data e a frase dele. Não espere o fim da sessão.

Grave direto no branch `main`, não no branch da sessão. O Dr. Fabio autorizou isso de forma permanente em 24/10/2026, só para arquivos dentro de `memoria/`. Use a ferramenta do GitHub que cria ou atualiza arquivo (`create_or_update_file`, branch `main`), lendo antes a versão atual para não apagar o que outra sessão escreveu. Qualquer outro arquivo segue o fluxo normal de branch.

## Por que isto existe

Até 24/10/2026 cada sessão salvava o aprendizado no próprio branch, que nunca entrava no principal. A sessão seguinte começava do principal e não via nada. A memória só funciona se `memoria/` estiver no branch principal.

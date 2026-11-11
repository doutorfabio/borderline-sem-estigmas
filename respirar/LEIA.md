# Respire Agora

Página gratuita de respirações por situação, com os materiais pagos abaixo.

- `index.html`: a página pronta para o site. Suba na Hostinger em `public_html/respirar/` do curso.drfabioschmidt.net. O link fica curso.drfabioschmidt.net/respirar/
- `pagina.html`: a mesma página no formato de pré-visualização do Claude. Edite esta e gere a outra com `python3 -I montar.py pagina.html index.html`.

## Vídeos

Cada situação tem o campo `video` vazio dentro do `<script>`. Vazio, a situação mostra só a bolinha guiada. Para pôr um vídeo:
1. Suba o MP4 em `public_html/respirar/videos/`.
2. Preencha o campo, por exemplo `video:'videos/suspiro.mp4'`.

Situações e o vídeo que cada uma espera:
- apuracao: respiração lenta, 5 entra e 5 sai
- suspiro: suspiro duplo, 2 + 1 entra e 6 sai
- dormir: 4-7-8
- conversa: sopro lento, 3 entra e 6 sai
- crise: respiração pequena e lenta, 3 entra e 5 sai, sem segurar
- quadrada: 4-4-4-4
- maos: respiração com as mãos, 4 entra fechando e 6 sai abrindo
- junto: respirar junto, 4 entra e 6 sai

Link direto para uma situação: acrescente `#id` no fim. Exemplo: curso.drfabioschmidt.net/respirar/#dormir

Os botões da Hotmart levam `src=respirar`, para a venda aparecer com essa origem no relatório.

O aviso da eleição fica no parágrafo `aviso-eleicao`. Apague depois do segundo turno.

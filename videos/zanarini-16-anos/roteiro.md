# Reel explicativo: 16 anos depois (Zanarini e colegas, 2012)

Público principal: quem tem borderline ou convive com alguém que tem, e ouviu que borderline nunca melhora. Sem formação clínica.
Função: confiança.
Formato: 1080x1920, 60 fps, 35,5 s, voz sintetizada pt-BR-AntonioNeural (edge-tts), trilha baixa, legenda em faixa separada.

## Fonte (conferida no texto completo pelo PubMed)

Zanarini MC, Frankenburg FR, Reich DB, Fitzmaurice G. Attainment and stability of sustained symptomatic remission and recovery among patients with borderline personality disorder and axis II comparison subjects: a 16-year prospective follow-up study. Am J Psychiatry. 2012;169(5):476-483. DOI 10.1176/appi.ajp.2011.11101550. PMID 22737693. PMC3509999.

| O que o vídeo diz | O que o artigo diz |
|---|---|
| 290 pessoas internadas com borderline | 290 inpatients que preenchiam DIB-R e DSM-III-R |
| Por 16 anos, ouvidas a cada dois anos | oito reavaliações separadas por 24 meses |
| 99 em cada 100 ficaram dois anos ou mais sem o diagnóstico | taxa cumulativa de remissão de 2 anos: 99% |
| Trabalho ou estudo constante, ao menos um amigo ou parceiro próximo | recuperação: GAF 61 ou mais; remissão + ao menos uma relação de apoio emocional com amigo próximo ou parceiro + trabalhar ou estudar de forma consistente, competente, em tempo integral |
| Isso, com os sintomas em baixa, chegou para 60 em cada 100 | recuperação de 2 anos: 60% |
| E demorou mais | cerca de 10% recuperados no primeiro período possível, contra cerca de 30% em remissão; recuperação significativamente mais lenta |

Limites que o vídeo não esconde nem estende: todos começaram internados (o artigo diz que quem nunca foi internado pode ter evolução diferente); a maioria estava em tratamento ambulatorial não intensivo; os números valem para este estudo.

## Roteiro com tempos reais da voz

Tempos de fala medidos em -55 dB. Arquivo de máquina: `tempos.json` (por linha e por palavra). Legenda: `legenda.srt`.

| Linha | Fala (início -> fim) | Narração | Na tela |
|---|---|---|---|
| L01 | 0,66 -> 2,92 | Te disseram que borderline nunca melhora? | grade de 100 pontos cinza nasce; depois NUNCA MELHORA? |
| L02 | 3,65 -> 7,55 | Um estudo seguiu duzentas e noventa pessoas internadas com borderline. | câmera desce para o ponto vermelho da internação; 290 pessoas, internadas, Zanarini e colegas, 2012 |
| L03 | 7,98 -> 9,10 | Por dezesseis anos. | a linha do tempo anda para a direita, 8 marcas (uma a cada 2 anos), câmera acompanha; 16 anos |
| L04 | 10,28 -> 15,05 | Nesse tempo, noventa e nove em cada cem ficaram dois anos ou mais sem o diagnóstico. | recua para a grade; 99 pontos acendem em branco, 1 fica cinza; colchete embaixo; 99 em 100; 2 anos sem diagnóstico |
| L05 | 15,83 -> 18,58 | O estudo também mediu trabalho ou estudo constante. | aproxima de uma pessoa; metade de cima do anel vermelho; trabalho ou estudo |
| L06 | 18,96 -> 21,34 | E ter ao menos um amigo ou parceiro próximo. | metade de baixo fecha o anel; amigo ou parceiro |
| L07 | 21,96 -> 25,94 | Isso, com os sintomas em baixa, chegou para sessenta em cada cem. | recua; anéis vermelhos se espalham devagar pelas 6 primeiras linhas |
| L08 | 26,37 -> 27,40 | E demorou mais. | os anéis terminam de chegar; colchete vermelho à esquerda; 60 em 100 |
| L09 | 28,33 -> 30,51 | Os sintomas cederam para quase todos. | recua até o diagrama inteiro: linha do tempo, 99 brancos, 60 com anel |
| L10 | 30,99 -> 33,21 | Trabalho e vínculos levaram mais tempo. | rótulos saem; TRABALHO E VÍNCULOS LEVARAM MAIS TEMPO no topo; segura até 35,5 |

## O diagrama (layout fixo, uma só cena)

- Topo: linha do tempo de 16 anos, ponto vermelho na internação, uma marca a cada reavaliação.
- Centro: grade de 10 por 10. Cada ponto é uma pessoa em cada 100.
- Ponto branco: ficou dois anos ou mais sem o diagnóstico.
- Anel vermelho em volta do ponto: além disso, trabalho ou estudo constante e ao menos uma pessoa próxima.
- Colchete branco embaixo: 99 em 100. Colchete vermelho à esquerda: 60 em 100.
- A câmera só se aproxima e se afasta; nada muda de lugar.

## Trocar a voz pela sua

1. Grave cada linha da tabela num arquivo (`audio/L01.mp3` a `audio/L10.mp3`) ou substitua os arquivos atuais.
2. Rode `python3 montar_audio.py`: mede as pontas de cada fala, monta `audio/narracao.wav` e reescreve `tempos.json` e `legenda.srt`.
3. Rode `python3 build_page.py` e o render (`node render.js i 4` para i de 0 a 3, depois `finalizar.sh`). A animação se ajusta ao tamanho real de cada linha, porque cada movimento está preso ao início das linhas e a palavras específicas.

Se gravar tudo num take só, corte o take nas 10 linhas antes do passo 2.

# gradient maker

Gerador de gradientes estáticos e animados. Terceira ferramenta da família iniciada pelo
gri.d.maker; compartilha o mesmo sistema visual.

## Arquitetura

Tudo vive em `src/GradientMaker.jsx`: os tokens, o motor de render, os exportadores e a UI.
É um arquivo único de propósito — não quebrar em módulos sem pedir.

O render é canvas 2D e passa por uma função pura, `drawScene(ctx, W, H, phase, cfg, tiles, buf)`,
usada pelos três caminhos: preview, PNG e gravação de vídeo. Qualquer mudança de aparência
entra ali, nunca só no preview — senão o export deixa de bater com a tela.

**Loop sem emenda é invariante.** Todo movimento usa harmônicas inteiras da fase (`phase` em
0..1). Uma frequência fracionária quebra o loop do vídeo. Ao adicionar movimento novo, o termo
tem que ser periódico em `phase`.

**A distorção é warp de campo, não deformação de forma.** O gradiente é pintado num buffer e
passa por duas passadas de deslocamento (`warpPass`): colunas na vertical, depois linhas na
horizontal. Já tentamos deformar a silhueta dos blobs — não é isso que se quer.

Os exports precisam andar juntos. Mexeu no canvas, revise `buildSVG` e `buildCode`:
no SVG o equivalente do warp é `feTurbulence` + `feDisplacementMap`.

A marca usa Host Grotesk SemiBold embutida em base64 no `@font-face`, com subset só dos
caracteres de "gradient maker". Mudou o nome, rode `python tools/subset-font.py`.

## Sistema visual — regra dura

A interface segue o sistema do gri.d.maker. Ele não é sugestão: é o que mantém as três
ferramentas reconhecíveis como uma família.

- **Nunca usar Tailwind.** Todo o estilo vive num bloco `CSS` no topo do componente, em
  template literal, aplicado por um `<style>{CSS}</style>` na raiz. Classes com prefixo `gm-`.
- **Nunca escrever cor solta.** Toda cor sai de uma variável de tema (`--gm-ink2`, `--gm-cyan`,
  `--gm-mag`, `--gm-text`, `--gm-muted`, `--gm-line`). Um `#fff` fixo num hover quebra o tema claro
  — isso já aconteceu uma vez.
- **Raio de 2px em tudo.** Único raio do sistema. Nada de `border-radius` maior.
- **Mono para todo número**, sans para prosa e rótulo. Valor que muda de 9 para 10 não pode dançar.
- **Hover preenche**: fundo vira o acento, texto vira a cor de contraste. Não mudar só a borda.
- **Foco nunca removido**: `outline: 2px solid var(--gm-cyan)`, offset 1px (4px em slider).
- **Acento por natureza do controle**: ciano para estrutura (dimensão, malha, geometria),
  magenta para atributo (cor, opacidade, rotação, tempo).
- **Título de seção** em mono 9,5px, caixa alta, tracking `.18em`, ciano, seguido de régua de 1px.
- **Sem transição e sem animação de interface.** Movimento só existe na arte que o usuário produz.
- **Quebra única em 860px**: o painel de 312px deixa de ser lateral e empilha.
- Cada slider vem com campo numérico editável à direita, em mono, e a unidade em `muted`.

A referência escrita está em `assets/design-system.md`, os valores em `assets/tokens.css`.

## Idioma e escrita

Interface em português. Rótulo é substantivo direto, sem verbo: "Espaçamento", não
"Ajustar espaçamento". Termos técnicos de pré-impressão ficam como são: dpi, SVG, CMYK, spot.
Botão diz o que acontece, e o mesmo nome se repete no resultado.

## Restrições técnicas

- React 18 + Vite, sem roteador, sem gerenciador de estado.
- Nada de `localStorage`/`sessionStorage` — o estado vive em `useState`.
- Dependência nova só se for indispensável, e vale dizer antes.
- Antes de dar a tarefa por concluída, rode `npm run build`.

# gradient maker

Gerador de gradientes estáticos e animados. Mesma família das ferramentas
[gri.d.maker](https://github.com/gugaxd/gri.d.maker) e bento maker — mesmo sistema visual,
mesmos tokens.

## O que faz

- **Dois tipos de gradiente**: mesh (blobs suaves em movimento) e clássico (linear ou radial),
  com alternador.
- **Três controles de 0 a 100**: velocidade, turbulência e granulação — mais distorção no modo mesh.
- **Até 6 cores**, com campo hex editável, sorteio de paleta e presets.
- **Exportação**: PNG, SVG, vídeo (MP4 onde o navegador suporta, senão WebM) e código HTML/CSS
  pronto para colar, em versão estática ou animada.

### Como a distorção funciona

O gradiente é pintado num buffer e passa por duas passadas de deslocamento: as colunas são
empurradas na vertical, depois as linhas na horizontal, cada uma por uma soma de três senóides
de frequências diferentes. O campo de cor dobra em vincos contínuos — tecido, superfície de água.

Nos exports o equivalente é `feTurbulence` + `feDisplacementMap`. O SVG sai com o filtro aplicado
ao grupo dos blobs; o código animado anima o `baseFrequency` para manter a ondulação viva.
Chrome e Firefox renderizam bem; o Safari é irregular com displacement em HTML.

### Loop sem emenda

Todo o movimento usa harmônicas inteiras da fase, então um ciclo fecha exatamente onde começou.
O gravador de vídeo captura a duração de um ciclo — o arquivo repete sem corte visível.

## Rodando

```bash
npm install
npm run dev
```

Build de produção em `dist/`:

```bash
npm run build
```

### Deploy na Vercel

Framework preset **Vite**, build `npm run build`, output `dist`. Sem variáveis de ambiente.

## Sistema visual

Os tokens do gri.d.maker estão em `assets/tokens.css` e a referência escrita em
`assets/design-system.md`. Na ferramenta eles vivem inline, no bloco `CSS` de
`src/GradientMaker.jsx`, com `data-tema="escuro"` ou `"claro"` na raiz.

A marca usa Host Grotesk SemiBold, embutida como WOFF2 em base64 no mesmo bloco — 1,7 KB,
sem requisição de rede. O subset cobre só os caracteres de "gradient maker"; para mudar o nome,
rode `python tools/subset-font.py` e troque a string base64 do `@font-face`.

## Estrutura

```
src/GradientMaker.jsx   componente inteiro: render, warp, exports e UI
src/main.jsx            entrada React
src/index.css           reset mínimo
assets/                 tokens, referência do sistema visual e a fonte original
tools/subset-font.py    regera o subset da fonte
CLAUDE.md               regras do projeto para o Claude Code
```

# Angry Birds in Python

[YouTube Video]([https://www.youtube.com/](https://youtu.be/l9TEfjfvgp8))

![Alt text](/resources/images/imagem_2025-01-29_113849074.png?raw=true "angry-birds")

## Overview

Este é um jogo inspirado no Angry Birds, desenvolvido em Python, agora com suporte a controle por visão computacional e mouse. O jogo combina a mecânica clássica do Angry Birds com novas funcionalidades e controles modernos.

## Controles

### Visão Computacional (na tela de jogo):

- **Encostar polegar e indicador**: Seleciona o estilingue (equivalente ao clique do mouse).
- **Movimentar a mão com os dedos encostados**: Ajusta a intensidade e o ângulo do estilingue.
- **Soltar os dedos**: Lança o pássaro.
- **Tecla P**: Pausa ou retoma a detecção por visão computacional.

### Mouse (nas telas de "Level Cleared" e "Level Failed"):

- Use o mouse para reiniciar o nível ou avançar.

### Teclas adicionais:

- **S**: Ativa ou desativa a gravidade.
- **W**: Ativa ou desativa o muro.

## Níveis Especiais

Os níveis de 15 em diante são gerados aleatoriamente a partir dos elementos dos 14 níveis base. Isso inclui:

- Tipos e tamanhos de pássaros e porcos.
- Quantidades de pássaros e porcos.
- Combinações aleatórias de construções.

Para alterar os elementos dos 14 níveis base, modifique:

- `pig_size` e `bird_size` na classe `Resources`: Controlam os tamanhos dos porcos e pássaros.
- Níveis na classe `Level`: Customize diretamente as configurações dos níveis.
- Outros elementos nas classes pertinentes: Permite personalizar completamente o jogo.

## Requisitos

Certifique-se de instalar os pacotes necessários antes de jogar:

```bash
pip install -r requirements.txt

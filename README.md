# Visualizador do Algoritmo DDA

Um programa simples para ver como funciona o algoritmo DDA (Digital Differential Analyzer) que transforma linhas matemáticas em pixels na tela.

## O que faz

Este programa mostra visualmente como o computador desenha linhas na tela. Quando você quer desenhar uma linha do ponto A ao ponto B, o algoritmo DDA calcula quais quadradinhos (pixels) devem ser pintados para formar essa linha.

O programa te deixa:
- Escolher dois pontos (início e fim da linha)
- Ver quais pixels o algoritmo DDA escolheu (em azul)
- Comparar com a linha matemática perfeita (em vermelho tracejado)
- Ver as coordenadas de cada quadradinho da grade

## Como usar

1. **Instalar Python**: Você precisa ter Python instalado no seu computador
2. **Baixar o arquivo**: Pegue o arquivo `DDA.PY`
3. **Executar**: Abra o terminal/prompt e digite:
   ```
   python DDA.PY
   ```
4. **Usar o programa**:
   - Digite as coordenadas do ponto inicial (X e Y)
   - Digite as coordenadas do ponto final (X e Y)
   - Clique em "Executar Algoritmo DDA"
   - Veja o resultado na grade

## Exemplo

Se você colocar:
- Ponto inicial: (-5, -4)
- Ponto final: (5, 4)

O programa vai mostrar todos os quadradinhos que o algoritmo escolheu para formar a linha entre esses dois pontos.

## Para que serve

Este programa é útil para:
- Estudantes de computação gráfica
- Quem quer entender como o computador desenha linhas
- Professores explicando rasterização
- Curiosos sobre algoritmos gráficos

## Requisitos

- Python 3.6 ou mais novo
- Tkinter (já vem com o Python na maioria dos casos)

Se der erro de "tkinter não encontrado", no Linux você pode instalar com:
```
sudo apt-get install python3-tk
```

## Sobre o algoritmo

O DDA é um dos algoritmos mais básicos para desenhar linhas em computador. Ele funciona calculando pequenos passos e decidindo pixel por pixel onde a linha deve passar. É eficiente porque só usa somas (nada de multiplicações complicadas).

---

Programa feito para fins educacionais. Use à vontade!

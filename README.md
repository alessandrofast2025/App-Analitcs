# Analisador de Cardápios de Delivery

Esta aplicação analisa cardápios de plataformas de delivery como iFood, Uber Eats e Rappi, identificando pontos de melhoria para aumentar as vendas.

## Funcionalidades

- Análise de cardápios a partir da URL
- Identificação de itens sem descrição ou com descrições curtas
- Detecção de itens sem imagens
- Análise de preços e organização do cardápio
- Sugestões de melhorias baseadas em boas práticas do setor

## Requisitos

- Python 3.7+
- Flask
- Requests
- BeautifulSoup4

## Instalação

1. Clone este repositório
2. Instale as dependências:
4. Acesse http://localhost:5000 no seu navegador

## Como usar

1. Cole a URL do cardápio do seu restaurante no campo de entrada
2. Clique em "Analisar Cardápio"
3. Veja as sugestões de melhoria e implemente-as na sua plataforma

## Limitações

- A aplicação depende da estrutura HTML das plataformas de delivery, que pode mudar com o tempo
- Algumas plataformas podem bloquear scraping, o que pode afetar a funcionalidade
- A análise é baseada em heurísticas e pode não capturar todos os aspectos do seu cardápio

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.
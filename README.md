## Random_Quotes_Webscrapper
 Script Python para busca de citações em sites aleatórios encontrados através de pesquisa automática no Google.

### Requisitos
 Para que o script funcione é necessário ter instaladas as seguintes libs:
 - [Requests](https://pypi.org/project/requests/)
 - [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
 
---

### Como funciona?
 É realizada uma pesquisa no google utilizando `requests.get(url)` e `BeautifulSoup(url.content, "html.parser")` para analisar `tags <a>` e coletar os links resultantes. Cada link é limpo para que seja realizado um novo _request_ em cada respectivo site, possibilitando a coleta das citações. Esta coleta é realizada através de uma análise por `tags <p>` que são validadas e limpas para apresentação na tela. Por fim, uma seleção aleatória, utilizando `random.choice()`, é realizada para apresentar a citação na tela.
 
---

### Uso
 1. Execute o `main.py`.
 2. Pressione ENTER após a mensagem aparecer na tela.
 3. Repita quantas vezes quiser. :)
 
---

### Known issues
 O script ainda demora alguns segundos para coletar a quantidade de citações pré-estabelecida no código.

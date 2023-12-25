Meu objetivo foi desenvolver um app que identificaria similaridade entre produtos. Iniciei clonando o template do Data App e instalando as bibliotecas que seriam necessárias para a criação do app. Os dados dos produtos são acessados através do arquivo CSV gerado nas etapas anteriores, com todas as informações. Como bibliotecas, utilizei o [scikit-learn](https://scikit-learn.org/stable/) para machine learning e o ![bokeh](https://bokeh.org/) para visualização gráfica.

O app analisa a similaridade de produtos à um produto base selecionado pelo usuário. Após a análise, com o scikit-learn, uma lista com os produtos com maior similaridade ao produto base é gerada. Além disso, é identificada a categoria na qual há a maior parte dos produtos com similaridade. Após isso, um scatter plot com os scores de similaridades é gerado com o bokeh, possuindo um tooltip para visualização do produto e categoria que cada ponto representa. 

O app também também possui uma seção de geração de imagens dos produtos, utilizando o ![DALL-E 2](https://openai.com/dall-e-2) da OpenAI. A chamada para a API é feita sempre que o usuário seleciona um novo produto para ser apresentado, e o prompt enviado é o título do produto. Como resultado, a imagem gerada é apresentada em tela.

Link para o app: https://similarity-analyzer.streamlit.app/

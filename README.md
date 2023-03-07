# GTP-Chatbot
Neste repositório, você encontrará o código-fonte de um chatbot responsável por responder a comandos de um usuário em um chat privado. Para usá-lo, basta seguir os seguintes passos:

1. Instale o Python 3.6 ou superior;
2. Instale os pacotes necessários com o comando `pip install -r requirements.txt` ;
3. Clone este repositório;
4. Entre na pasta do repositório;
5. Execute o comando `python main.py` para iniciar o bot;
6. Adicione o bot ao seu servidor do Discord;
7. Envie um comando para o bot no chat privado.

## Comandos
O bot possui os seguintes comandos:

- `!source`: Retorna o link do repositório do projeto;
- `!author`: Retorna o nome e o e-mail do autor do projeto;
- `!run`: Retorna informações de um Pokémon aleatório;
    - `!run <pokemon_name>`: Retorna informações de um Pokémon com o nome especificado;
- `!help`: Retorna uma lista de comandos disponíveis;


## Notas
- Ao rodar o bot pela primeira vez, será criado um arquivo `.env` na raiz do projeto. Neste arquivo, você deve colocar o token do bot.
- Os desafios enfrentados ao longo do projeto estão descritos nos arquivos abaixo:
    - [`ensaio_0.md`](ensaios/ensaio_0.md);
    - [`ensaio_1.md`](ensaios/ensaio_1.md);

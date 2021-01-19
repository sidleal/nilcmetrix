text_metrics
============
Repositório para extração de métricas sobre textos em português.


Dependências
------------
- [PostgreSQL](https://www.postgresql.org/)
- [Python 3](http://python.org/)
- tools.zip (aprox 2gb) descompactada na raiz

Instale a base de dados do *Coh-Metrix-Dementia*, disponível na raiz desse projeto:

	$ pg_restore -d cohmetrix_pt_br /caminho/para/projeto/cohmetrix_pt_br

Instale os pacotes do python, opcionalmente em um [virtualenv](https://virtualenv.pypa.io/en/stable/):

	$ pip install -r text_metrics/requirements.txt


Configuração inicial
--------------------
- Adicione o caminho absoluto da pasta `text_metrics/` na variável de ambiente
  `PYTHONPATH`.
- Edite a variável `BASE_DIR` no arquivo `text_metrics/config.py` com o caminho
  para a pasta do projeto.


Como usar
---------
```python
import text_metrics

t = text_metrics.Text("insira aqui seu texto")
# ou de um arquivo
t = text_metrics.Text(filepath="caminho para um arquivo com o texto")

valores = text_metrics.all_metrics.values_for_text(t)
```

NILC-Metrix
============
NILC-Metrix gathers the metrics developed over more than a decade in NILC (Interinstitutional Center for Computational Linguistics), starting with Coh-Metrix-Port, (an adaptation of Coh-Metrix to Portuguese). The main purpose of these metrics is to assess cohesion, coherence and text complexity level. The release of March, 2021 makes available 200 metrics, refactored by Sidney Leal (based on source codes from Carolina Scarton, Andre Cunha and Nathan Hartmann), supported by Magali Duran. All advised by Sandra Aluísio.

License
-------
[AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html)

Citing this work:
-----------------
````
@article{NILCMetrix2021,
    author = {Sidney Evaldo Leal and Magali Sanchez Duran and Carolina Evaristo Scarton and Nathan Siegle Hartmann and Sandra Maria Aluísio},
    title = {NILC-Metrix: assessing the complexity of written and spoken language in Brazilian Portuguese},
    year = {2021},
    note = {https://arxiv.org/abs/2201.03445}
}
````

Mais detalhes:
--------------

NILC-Metrix agrupa as métricas desenvolvidas em mais de uma década no NILC, iniciadas com o Coh-Metrix-Port (uma adaptação da ferramenta Coh-Metrix para o Português Brasileiro). O foco principal das métricas é calcular coesão, coerência e nível de complexidade textual.
Essa versão disponibiliza 200 métricas, detalhadas em [http://fw.nilc.icmc.usp.br:23380/metrixdoc](http://fw.nilc.icmc.usp.br:23380/metrixdoc),
refatoradas por Sidney Leal (com base nos códigos de Carolina Scarton, Andre Cunha e Nathan Hartmann), apoiado por Magali Duran. Todos sob a orientação da professora Sandra Aluísio.


Esse projeto é um fork de: [https://github.com/nilc-nlp/coh-metrix-port](https://github.com/nilc-nlp/coh-metrix-port)

Dependências
------------
- [PostgreSQL](https://www.postgresql.org/)
- [Python 3](http://python.org/)
- [nilc-metrix-tools.zip](https://drive.google.com/file/d/1Ondvnz09RWDAX-1u3GIaXuAmkfKbGtqc/view?usp=sharing) (aprox 2gb) descompactada na raiz

Instale a base de dados do *Coh-Metrix-Dementia*, disponível na subpasta tools/postgres do nilc-metrix-tools.zip com o nome cohmetrix_pt_br (aprox. 15mb):

	$ pg_restore -d cohmetrix_pt_br /caminho/para/projeto/cohmetrix_pt_br

Instale os pacotes do python, opcionalmente em um [virtualenv](https://virtualenv.pypa.io/en/stable/):

	$ pip install -r text_metrics/requirements.txt

Ou

```
$ pip3 install nltk
$ pip3 install numpy
$ pip3 install nlpnet
$ pip3 install gensim
$ pip3 install https://github.com/kpu/kenlm/archive/master.zip
$ pip3 install lxml
$ pip3 install psycopg2-binary
$ cd tools/idd3/ && python3 setup.py install
```


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

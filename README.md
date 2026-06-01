# Diagnóstico de Vendas, Entrega e Satisfação de um Marketplace

Projeto de análise de dados com SQL, SQLite e Excel usando dados públicos da Olist.

## Objetivo

Analisar vendas, atrasos de entrega, satisfação dos clientes e concentração de problemas em sellers e estados.

## Fonte dos dados

Dataset público: Brazilian E-Commerce Public Dataset by Olist, disponível no Kaggle.

## Perguntas de negócio

- Quais categorias vendem mais?
- Quais estados têm mais atrasos?
- Pedidos atrasados recebem avaliações piores?
- Quais vendedores concentram mais problemas?
- Que ações o negócio deveria priorizar?

## Status

Fase 2: importação dos CSVs brutos para SQLite.

## Estrutura inicial

```text
data/raw/olist/              # CSVs brutos baixados do Kaggle
data/processed/              # banco SQLite gerado localmente
docs/                        # documentação do projeto
outputs/                     # arquivos pequenos de validação e saídas analíticas
scripts/                     # scripts de preparação e análise
sql/                         # consultas SQL do projeto
```

## Execução da importação

```powershell
python scripts/import_olist_to_sqlite.py
```

Esse comando gera:

```text
data/processed/olist_marketplace.db
outputs/import_summary.csv
```

Mais detalhes em [docs/importacao_sqlite.md](docs/importacao_sqlite.md).

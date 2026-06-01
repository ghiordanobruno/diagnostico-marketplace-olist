# Importacao dos CSVs para SQLite

## Objetivo

Criar um banco SQLite local a partir dos arquivos CSV brutos da Olist.

Esta etapa transforma os arquivos separados em tabelas consultaveis com SQL, sem alterar os dados originais.

## Entrada

Os arquivos CSV devem estar em:

```text
data/raw/olist/
```

## Saidas

O script gera:

```text
data/processed/olist_marketplace.db
outputs/import_summary.csv
```

O arquivo `.db` e gerado localmente e nao deve ser enviado ao GitHub. O arquivo `outputs/import_summary.csv` e pequeno e serve como evidencia da importacao.

## Comando

```powershell
python scripts/import_olist_to_sqlite.py
```

## Comando com caminhos customizados

```powershell
python scripts/import_olist_to_sqlite.py --raw-dir data/raw/olist --output-db data/processed/olist_marketplace.db --summary-output outputs/import_summary.csv
```

## Tabelas geradas

| CSV | Tabela SQLite |
|---|---|
| `olist_customers_dataset.csv` | `customers` |
| `olist_geolocation_dataset.csv` | `geolocation` |
| `olist_order_items_dataset.csv` | `order_items` |
| `olist_order_payments_dataset.csv` | `order_payments` |
| `olist_order_reviews_dataset.csv` | `order_reviews` |
| `olist_orders_dataset.csv` | `orders` |
| `olist_products_dataset.csv` | `products` |
| `olist_sellers_dataset.csv` | `sellers` |
| `product_category_name_translation.csv` | `product_category_name_translation` |

## Decisao tecnica

As colunas sao importadas inicialmente como texto para preservar os dados brutos. Conversoes de datas, valores numericos e indicadores serao feitas nas consultas SQL analiticas.

Essa abordagem separa duas responsabilidades:

- ingestao: carregar os dados sem modificar o conteudo original;
- analise: aplicar regras de negocio, conversoes e calculos de KPIs.

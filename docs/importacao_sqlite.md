# Importação dos CSVs para SQLite

## Objetivo

Criar um banco SQLite local a partir dos arquivos CSV brutos da Olist.

Esta etapa transforma os arquivos separados em tabelas consultáveis com SQL, sem alterar os dados originais.

## Entrada

Os arquivos CSV devem estar em:

```text
data/raw/olist/
```

## Saídas

O script gera:

```text
data/processed/olist_marketplace.db
outputs/import_summary.csv
```

O arquivo `.db` é gerado localmente e nao deve ser enviado ao GitHub. O arquivo `outputs/import_summary.csv` é pequeno e serve como evidência da importação.

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

## Decisão técnica

As colunas são importadas inicialmente como texto para preservar os dados brutos. Conversões de datas, valores numéricos e indicadores serão feitas nas consultas SQL analíticas.

Essa abordagem separa duas responsabilidades:

- ingestão: carregar os dados sem modificar o conteudo original;
- análise: aplicar regras de negócio, conversões e cálculos de KPIs.

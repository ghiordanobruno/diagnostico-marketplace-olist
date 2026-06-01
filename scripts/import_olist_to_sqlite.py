import argparse
import csv
import sqlite3
from pathlib import Path


DEFAULT_TABLES = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "product_category_name_translation",
}


def quote_identifier(identifier):
    return '"' + identifier.replace('"', '""') + '"'


def create_table(connection, table_name, fieldnames):
    columns_sql = ", ".join(f"{quote_identifier(column)} TEXT" for column in fieldnames)
    connection.execute(f"DROP TABLE IF EXISTS {quote_identifier(table_name)}")
    connection.execute(f"CREATE TABLE {quote_identifier(table_name)} ({columns_sql})")


def insert_rows(connection, table_name, fieldnames, rows):
    placeholders = ", ".join("?" for _ in fieldnames)
    columns_sql = ", ".join(quote_identifier(column) for column in fieldnames)
    sql = (
        f"INSERT INTO {quote_identifier(table_name)} ({columns_sql}) "
        f"VALUES ({placeholders})"
    )
    connection.executemany(sql, rows)


def import_csv(connection, csv_path, table_name, batch_size):
    with csv_path.open("r", encoding="utf-8", newline="") as source_file:
        reader = csv.DictReader(source_file)
        if not reader.fieldnames:
            raise ValueError(f"Arquivo sem cabecalho: {csv_path}")

        fieldnames = reader.fieldnames
        create_table(connection, table_name, fieldnames)

        row_count = 0
        batch = []
        for row in reader:
            batch.append([row.get(column) for column in fieldnames])
            if len(batch) >= batch_size:
                insert_rows(connection, table_name, fieldnames, batch)
                row_count += len(batch)
                batch = []

        if batch:
            insert_rows(connection, table_name, fieldnames, batch)
            row_count += len(batch)

    return {
        "csv_file": csv_path.name,
        "table_name": table_name,
        "columns": len(fieldnames),
        "rows": row_count,
    }


def write_import_summary(summary_path, summaries):
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with summary_path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(
            output_file,
            fieldnames=["csv_file", "table_name", "columns", "rows"],
        )
        writer.writeheader()
        writer.writerows(summaries)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Importa os CSVs publicos da Olist para um banco SQLite."
    )
    parser.add_argument(
        "--raw-dir",
        default="data/raw/olist",
        help="Pasta onde estao os CSVs brutos da Olist.",
    )
    parser.add_argument(
        "--output-db",
        default="data/processed/olist_marketplace.db",
        help="Caminho do banco SQLite que sera gerado.",
    )
    parser.add_argument(
        "--summary-output",
        default="outputs/import_summary.csv",
        help="CSV pequeno com a quantidade de linhas importadas por tabela.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5000,
        help="Quantidade de linhas inseridas por lote.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    raw_dir = Path(args.raw_dir)
    output_db = Path(args.output_db)
    summary_output = Path(args.summary_output)

    if not raw_dir.exists():
        raise FileNotFoundError(f"Pasta de dados brutos nao encontrada: {raw_dir}")

    missing_files = [
        filename for filename in DEFAULT_TABLES if not (raw_dir / filename).exists()
    ]
    if missing_files:
        missing_list = ", ".join(missing_files)
        raise FileNotFoundError(f"Arquivos CSV nao encontrados: {missing_list}")

    output_db.parent.mkdir(parents=True, exist_ok=True)
    if output_db.exists():
        output_db.unlink()

    summaries = []
    with sqlite3.connect(output_db) as connection:
        connection.execute("PRAGMA journal_mode = OFF")
        connection.execute("PRAGMA synchronous = OFF")
        connection.execute("PRAGMA temp_store = MEMORY")

        for filename, table_name in DEFAULT_TABLES.items():
            csv_path = raw_dir / filename
            summary = import_csv(connection, csv_path, table_name, args.batch_size)
            summaries.append(summary)
            print(
                f"{summary['table_name']}: "
                f"{summary['rows']} linhas, {summary['columns']} colunas"
            )

    write_import_summary(summary_output, summaries)
    print(f"\nBanco criado em: {output_db}")
    print(f"Resumo criado em: {summary_output}")


if __name__ == "__main__":
    main()

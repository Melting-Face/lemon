import pandas as pd
import awswrangler as wr

from datetime import datetime
from fastapi import APIRouter

from constants import (
    AWS_CATALOG_DBNAME,
    AWS_CALALOG_TABLELIST,
)

router = APIRouter(
    prefix='/insert',
    tags=['insert'],
    responses={404: {'description': 'Not Found'}}
)


@router.get('/')
async def insert_home():
    return 'insert'


@router.post('/{table_name}')
async def insert(table_name: str, items: list):
    model = AWS_CALALOG_TABLELIST.get(table_name, None)
    if not model:
        return 'no model in server'
    print(items)
    table_existed = wr.catalog.does_table_exist(
        database=AWS_CATALOG_DBNAME,
        table=table_name,
    )

    input_date = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

    model_column_types = {}

    for field_name, field_attr in model.schema()['properties'].items():
        field_type = field_attr.get('type')
        field_length = field_attr.get('maxLength', None)
        if field_type == 'number':
            field_type = 'decimal'
        elif field_type == 'string' and field_length:
            field_type = f'varchar({field_length})'

        model_column_types.update({field_name: field_type})

    if not table_existed:
        wr.catalog.create_parquet_table(
            database=AWS_CATALOG_DBNAME,
            table=table_name,
            path=f's3://{AWS_CATALOG_DBNAME}/{table_name}/',
            compression='gzip',
            columns_types=model_column_types
        )
    df = pd.DataFrame([model(**item).dict() for item in items])
    df.to_parquet(
        f's3://{AWS_CATALOG_DBNAME}/{table_name}/{input_date}.parquet.gzip',
        compression="gzip"
    )
    return f'{table_name}'

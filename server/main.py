import uvicorn

import pandas as pd

from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:9999",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Article(BaseModel):
    title: str
    subTitle: str
    article: str


@app.post('/insert/articles')
async def insert_article(articles: List[Article]):
    df = pd.DataFrame([article.dict() for article in articles])
    print(df)
    df.to_parquet(
        's3://test-product-host/articles/article.parquet.gzip',
        compression='gzip'
    )
    return 'hello'


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9999)

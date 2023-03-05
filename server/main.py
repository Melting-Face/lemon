import uvicorn
import awswrangler as wr

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import insert
from constants import AWS_CATALOG_DBNAME

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

app.include_router(insert.router)


@app.get('/test')
async def test():
    return 'test'


if __name__ == "__main__":
    databases = wr.catalog.databases()
    if AWS_CATALOG_DBNAME not in databases['Database'].values:
        wr.catalog.create_database(name=AWS_CATALOG_DBNAME)
    uvicorn.run(app, host="0.0.0.0", port=9999)

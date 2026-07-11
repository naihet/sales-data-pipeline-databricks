# Sales Data Pipeline with Databricks

## Tech Stack

- PySpark
- Databricks
- Delta Lake
- Spark SQL

## Project Architecture

```mermaid
flowchart LR
    A[Raw CSV]
    B[Bronze Delta]
    C[Quality Check]
    D[Silver]
    E[Gold]
    F[Dashboard]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
```

## Current Progress

- Bronze Layer
- Silver Layer
- Gold Layer

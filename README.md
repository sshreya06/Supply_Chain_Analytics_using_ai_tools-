# Supply Chain Analytics Using AI Tools

End-to-end pipeline analyzing order fulfillment performance and revenue loss for a fictional retail company.

## Architecture

```
Email (Raw Data) → n8n ETL → Supabase (PostgreSQL) → Quadratic (Python) → Insights
```

## Tech Stack

- **Supabase** — PostgreSQL data warehouse (star schema)
- **n8n** — Automated ETL from email attachments
- **Quadratic** — Python/Pandas transformations and analysis

## Key Features

- OTIF (On-Time In-Full) analysis
- Revenue loss quantification
- USD → INR currency conversion
- Star-schema joins across orders, products, customers
- Daily automated refresh via n8n

## Folder Structure

```
supabase/       → Schema & SQL queries
n8n/            → Exported workflow JSON
quadratic/      → Python transformation scripts
data_samples/   → Sample CSVs for testing
```

## Quick Start

1. Create a Supabase project and run `supabase/schema.sql`
2. Import `n8n/workflow.json` and configure your email + Supabase credentials
3. Open Quadratic, paste `quadratic/transformations.py`, and set your `SUPABASE_URL` and `SUPABASE_KEY`
4. Run cells in order — data flows from the warehouse into aggregated KPI outputs

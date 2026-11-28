
# Phase 4 — Grocery Price Collection Platform

## 1. Project Overview

Build a grocery price collection and comparison platform focused initially on the Quebec market.

The objective is to collect grocery product information and prices from multiple retailers, standardize the data, identify equivalent products, and generate weekly price comparison reports in CSV format.

### Initial Retailers
- IGA
- Metro
- Maxi

### Project Objectives
- Collect grocery product catalogs and prices.
- Compare equivalent products across retailers.
- Track price changes over time.
- Identify promotional prices.
- Calculate normalized unit prices.
- Generate structured CSV exports.
- Build a historical grocery price database.

## 2. Initial Scope

| Parameter | Initial target |
|---|---|
| Geographic market | Quebec, Canada |
| Retailers | IGA, Metro, Maxi |
| Collection frequency | Weekly |
| Currency | CAD |
| Initial product categories | 5 |
| Initial product catalog | 100 products |
| Storage | SQLite |
| Export format | CSV |

### Initial Product Categories

| Category | Target products |
|---|---:|
| Dairy and eggs | 20 |
| Meat and poultry | 20 |
| Fruits and vegetables | 20 |
| Bakery | 20 |
| Pantry | 20 |
| **Total** | **100** |

The initial objective is to identify 100 distinct products and measure their availability and comparability across the three retailers.

## 3. Data Acquisition Strategy

The project will use a modular data acquisition architecture.

### Primary Investigation: épiceries.ca API

Investigate the possibility of using the publicly documented, read-only API from épiceries.ca.

Potential data includes:
- Product information.
- Retailer-specific prices.
- Store-specific pricing.
- Unit prices.
- Historical price information.
- Product search capabilities.

Before implementation:
- Review API documentation and usage conditions.
- Validate data coverage.
- Verify price accuracy against retailer websites.
- Confirm commercial usage permissions if applicable.
- Respect rate limits and caching requirements.

### Secondary Strategy: Retailer-Specific Connectors

If the third-party API does not provide sufficient coverage or accuracy, develop separate authorized connectors for each retailer.

Cloudflare and other access restrictions must not be circumvented. Use authorized feeds, APIs, or retailer-approved access methods.

The architecture must allow data sources to be replaced without rebuilding the entire application.

## 4. Technical Architecture

### Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.12+ |
| HTTP requests | Requests |
| Data processing | Pandas |
| Data validation | Pydantic |
| Database | SQLite |
| Scheduling | GitHub Actions or cron |
| Version control | Git |
| Output | CSV |

### Application Architecture

```text
GROCERY DATA SOURCES
       |
       v
DATA ACQUISITION
  - Third-party API
  - Authorized retailer connectors
       |
       v
PYTHON INGESTION
  - Data retrieval
  - JSON validation
  - Error handling
  - Source tracking
       |
       v
DATA PROCESSING
  - Product normalization
  - Product matching
  - Duplicate detection
  - Price validation
  - Unit price calculation
       |
       v
SQLITE DATABASE
  - Retailers
  - Stores
  - Products
  - Price observations
  - Collection runs
       |
       v
DATA EXPORT
  - products.csv
  - price_history.csv
  - price_comparison.csv
  - collection_report.csv
```

## 5. Database Design

Five primary tables will be implemented.

| Table | Responsibility |
|---|---|
| retailers | Retailer information |
| stores | Individual store locations |
| products | Canonical product catalog |
| price_observations | Historical product prices |
| collection_runs | Collection execution logs |

### Product Data

Each product should contain:
- Internal product ID.
- Retailer product ID.
- Barcode / UPC, when available.
- Product name.
- Brand.
- Category.
- Package size.
- Package unit.
- Normalized product identity.

### Price Observation Data

Each price observation should contain:
- Product ID.
- Retailer ID.
- Store ID, when available.
- Regular price.
- Promotional price.
- Currency.
- Unit price.
- Availability.
- Source.
- Original observation date.
- Collection timestamp.

**Important:** Product identity and price observations must be stored separately. One product can have multiple prices across retailers, locations and collection dates.

## 6. Product Matching and Price Normalization

Product matching is a critical part of the project.

The matching strategy will follow this priority:

1. Exact barcode / UPC match.
2. Brand + product type + package size.
3. Normalized product name + package size.
4. Manual review of uncertain matches.

Similar product names must not automatically be treated as identical products.

### Unit Price Normalization

Calculate comparable prices using standardized units:
- Dollars per 100 g.
- Dollars per 100 ml.
- Dollars per unit.
- Dollars per kilogram or litre where appropriate.

Both package price and normalized unit price must be retained.

## 7. CSV Deliverables

The first implementation must generate three primary CSV files.

### products.csv

Contains the canonical product catalog.

```text
product_id
barcode
product_name
brand
category
package_size
package_unit
```

### price_history.csv

Contains historical price observations.

```text
product_id
retailer
store_id
regular_price
sale_price
unit_price
currency
availability
source
observed_at
collected_at
```

### price_comparison.csv

Contains a cross-retailer price comparison.

```text
product_id
product_name
package_size
iga_price
metro_price
maxi_price
lowest_price
lowest_price_retailer
comparison_date
```

All CSV files must use consistent encoding, decimal formatting and date formats.

## 8. Implementation Roadmap

### Week 1 — Data Acquisition and Foundation
- Investigate API access and usage conditions.
- Define the database schema.
- Create the Python project structure.
- Implement the first data collector.
- Retrieve sample products and prices.

### Week 2 — Data Processing
- Implement product normalization.
- Develop product matching.
- Implement duplicate detection.
- Calculate normalized unit prices.
- Validate pricing information.

### Week 3 — Data Exports
- Implement CSV generation.
- Generate product catalog exports.
- Generate historical price exports.
- Generate retailer comparison reports.
- Implement data-quality checks.

### Week 4 — Automation
- Implement weekly scheduling.
- Add execution logging.
- Add error handling and retry policies.
- Validate collection consistency.
- Produce the first historical dataset.

## 9. MVP-01 Acceptance Criteria

The first working version must demonstrate that it can:

- Connect to an authorized data source.
- Retrieve products from IGA, Metro and Maxi.
- Collect product names, package sizes and prices.
- Preserve source and observation dates.
- Identify equivalent products across retailers.
- Calculate normalized unit prices.
- Store information in SQLite.
- Export products.csv.
- Export price_history.csv.
- Export price_comparison.csv.
- Produce collection logs and a data-quality report.

## 10. Future Enhancements

After the MVP is validated, consider:
- Additional grocery retailers.
- More Quebec regions and store locations.
- Automated product matching.
- Historical price trend analysis.
- Promotional price detection.
- Grocery basket price comparisons.
- Inflation monitoring.
- Interactive dashboards.
- Automated weekly reports.

## 11. Architectural Principles

1. **Source independence:** Data sources must be replaceable without changing the core application.
2. **Historical preservation:** Never overwrite previous price observations.
3. **Data quality:** Incorrect product matches are worse than missing matches.
4. **Geographic accuracy:** Prices must retain their store or regional context.
5. **Reproducibility:** Every collection run must be logged.
6. **Compliance:** Only use authorized data access methods.
7. **Scalability:** Start with SQLite and modular Python components, keeping future database migration possible.

## 12. Definition of Success

Phase 4 will be considered successful when the platform can reliably collect, normalize, store and compare grocery prices from IGA, Metro and Maxi on a weekly basis.

The primary deliverable is not the scraping mechanism itself.

It is a reliable, structured and historically traceable grocery price database that can support future comparison, reporting and analytics applications.

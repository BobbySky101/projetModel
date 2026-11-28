
# Smart Meal Planner
## Technical Architecture

# 1. Recommended Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python 3.12+ | Core application |
| API | FastAPI | Application endpoints |
| AI | LLM with tool calling | Natural-language interaction |
| Recipe data | Spoonacular / Edamam | Recipe discovery |
| Recipe storage | SQLite | Recipe persistence |
| Grocery data | Existing Phase 4 | Product prices |
| Validation | Pydantic | Structured information |
| Processing | Pandas | Ingredient aggregation |
| Optimization | Google OR-Tools | Basket optimization |
| ORM | SQLAlchemy | Database access |
| Scheduling | GitHub Actions / cron | Weekly tasks |
| Frontend | Streamlit | Initial interface |
| Testing | Pytest | Automated testing |
| Version control | Git | Source management |

# 2. Application Structure

```text
smart-meal-planner/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   └── schemas/
│   │
│   ├── agent/
│   │   ├── orchestrator.py
│   │   ├── prompts.py
│   │   ├── tools.py
│   │   └── response_builder.py
│   │
│   ├── recipes/
│   │   ├── providers/
│   │   │   ├── spoonacular.py
│   │   │   └── edamam.py
│   │   ├── importer.py
│   │   ├── search.py
│   │   └── manager.py
│   │
│   ├── ingredients/
│   │   ├── normalizer.py
│   │   ├── unit_converter.py
│   │   ├── matcher.py
│   │   └── substitutions.py
│   │
│   ├── preferences/
│   │   ├── profile.py
│   │   ├── preferences.py
│   │   └── pantry.py
│   │
│   ├── meal_planning/
│   │   ├── planner.py
│   │   ├── recipe_selector.py
│   │   ├── scoring.py
│   │   └── calendar.py
│   │
│   ├── groceries/
│   │   ├── collectors/
│   │   ├── product_matcher.py
│   │   ├── price_comparator.py
│   │   └── shopping_list.py
│   │
│   ├── optimization/
│   │   ├── basket_optimizer.py
│   │   ├── trip_optimizer.py
│   │   └── cost_calculator.py
│   │
│   ├── database/
│   │   ├── models.py
│   │   ├── repository.py
│   │   └── migrations/
│   │
│   └── exports/
│       ├── csv_exporter.py
│       └── weekly_report.py
│
├── frontend/
│   └── streamlit_app.py
│
├── data/
│   ├── exports/
│   └── imports/
│
├── tests/
│
├── config/
│   └── settings.py
│
├── .env.example
├── requirements.txt
├── main.py
└── README.md
```

# 3. Architectural Separation

Maintain three distinct layers.

| Layer | Responsibility |
|---|---|
| AI layer | Understand requests and make recommendations |
| Business logic | Calculate quantities, match products and optimize costs |
| Data layer | Store and retrieve structured information |

The AI calls business services through structured tools.

Business services execute deterministic calculations.

The database stores validated information.

# 4. Important Technical Principles

- Use SQLAlchemy for database access.
- Use Pydantic for validation.
- Use migrations to evolve the database.
- Keep recipe providers replaceable.
- Keep grocery collectors independent of business logic.
- Cache imported recipe information where permitted.
- Retain historical price observations.
- Keep API credentials outside source control.
- Use automated tests for calculations and optimization.
- Use structured logs for collection and agent runs.

# 5. Data Collection Considerations

Recipe collection:
- Respect API licensing and storage conditions.
- Preserve recipe attribution.
- Avoid unauthorized redistribution of copyrighted instructions.

Grocery collection:
- Use authorized data sources and interfaces.
- Respect retailer terms and access restrictions.
- Do not rely on bypassing Cloudflare protections.
- Maintain price observation timestamps.
- Identify stale or uncertain prices.

# 6. AI Integration

The AI agent should expose structured tools such as:

- search_recipes()
- get_recipe_details()
- get_pantry_inventory()
- generate_meal_plan()
- calculate_ingredient_requirements()
- match_grocery_products()
- compare_grocery_prices()
- optimize_weekly_shopping()
- save_weekly_plan()
- export_grocery_list()

The AI should coordinate the workflow rather than perform financial calculations itself.

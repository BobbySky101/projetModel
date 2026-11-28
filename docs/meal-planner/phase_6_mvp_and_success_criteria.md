
# Smart Meal Planner
## MVP-01, Success Criteria & Open Decisions

# 1. MVP-01: Recipe-to-Grocery Prototype

**Objective:** Prove the complete data flow before developing the autonomous AI agent.

## Input

- Three saved recipes.
- Four servings per recipe.
- One mandatory ingredient: salmon.
- Sample pantry inventory.
- CAD $150 budget.

## Processing

1. Retrieve recipes.
2. Normalize ingredients.
3. Scale quantities to four servings.
4. Aggregate duplicate ingredients.
5. Deduct pantry inventory.
6. Match ingredients to grocery products.
7. Retrieve retailer prices.
8. Calculate the grocery basket.

## Output Files

```text
data/exports/
├── recipes.csv
├── ingredients.csv
├── weekly_meal_plan.csv
├── grocery_list.csv
├── price_comparison.csv
└── weekly_budget_report.csv
```

## MVP-01 Acceptance Criteria

| Test | Expected result |
|---|---|
| Recipe retrieval | Retrieve at least 3 recipes |
| Serving adjustment | Correctly scale quantities |
| Ingredient normalization | Identify duplicate ingredients |
| Pantry deduction | Exclude sufficient inventory |
| Product matching | Find equivalent grocery products |
| Price retrieval | Retrieve prices with timestamps |
| Budget calculation | Calculate actual package purchase costs |
| CSV export | Generate all required files |

MVP-01 is successful when the entire workflow runs locally with one command.

---

# 2. Risks and Mitigation

| Risk | Proposed solution |
|---|---|
| Recipe API costs | Compare providers and cache recipes |
| Copyright and licensing | Preserve attribution and respect usage rights |
| Ingredient matching errors | Confidence scores and manual review |
| Inaccurate grocery prices | Track timestamps and source reliability |
| Food quantity errors | Standardized units and ingredient-aware conversions |
| Product availability | Flag unavailable or uncertain products |
| Budget overruns | Validate budgets and propose alternatives |
| AI calculation errors | Use deterministic Python services |

---

# 3. Success Metrics

| Metric | Initial target |
|---|---|
| Weekly meals generated | 7 |
| Budget compliance | Within $150 when feasible |
| Ingredient matching | At least 90% for supported products |
| Manual grocery corrections | Decreasing over time |
| Shopping trips | 1–2 preferred |
| Recipe reuse | Avoid excessive repetition |
| Price traceability | 100% of priced items |
| Weekly planning time | Under 10 minutes of user interaction |

These are proposed engineering targets, not guaranteed results.

---

# 4. Remaining Decisions

The following requirements need confirmation.

| Question | Options |
|---|---|
| Budget scope | Seven dinners only / All weekly groceries |
| Recipe languages | French / English / Both |
| Initial interface | Streamlit / CLI / Full web application |
| Shopping geography | Postal code / Entire city / Flexible |

## Provisional Assumptions

Until confirmed:

- Budget covers seven dinners.
- Recipe database supports French and English.
- Streamlit is the initial interface.
- Shopping is restricted to one local shopping area.

---

# 5. Final Architectural Recommendation

Build an ingredient-centric system.

Do not build a recipe application that happens to generate shopping lists.

Build a platform where:

- Recipes describe what to cook.
- Ingredients describe what is required.
- Pantry inventory describes what is available.
- Grocery products describe what can be purchased.
- Prices describe the cost of purchases.
- The optimization engine determines the best purchasing strategy.
- The AI agent coordinates the entire experience.

This architecture supports future extensions:

- Nutritional goals.
- Weekly spending analytics.
- Automatic pantry replenishment.
- Lunch and breakfast planning.
- Food waste tracking.
- Recipe personalization.
- Automated grocery list generation.

## First Development Priority

Build MVP-01: the Recipe-to-Grocery Prototype.

Validate the data flow before implementing the autonomous AI agent.

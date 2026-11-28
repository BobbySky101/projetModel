
# Smart Meal Planner
## Implementation Roadmap

# Phase 1: Recipe Library

### Objectives
Build a centralized recipe database.

### Deliverables
- Recipe provider integration.
- Recipe importer.
- Recipe database.
- Ingredient extraction.
- Recipe search and categorization.

### Completion test
Search for recipes containing salmon and retrieve structured ingredient lists for at least 20 recipes.

---

# Phase 2: Ingredients and Pantry

### Objectives
Create standardized ingredient identities and inventory management.

### Deliverables
- Canonical ingredient catalog.
- English/French aliases.
- Measurement conversions.
- Pantry inventory.
- Ingredient normalization.

### Completion test
Import recipes with different ingredient descriptions and correctly identify shared ingredients.

---

# Phase 3: Meal Planning

### Objectives
Build the seven-dinner weekly planning engine.

### Deliverables
- Weekly planning service.
- Recipe scoring.
- Variety constraints.
- Ingredient aggregation.
- Optional leftover management.

### Completion test
Generate seven dinners for four people while respecting a mandatory ingredient and a $150 budget target.

---

# Phase 4: Grocery Price Intelligence

### Objectives
Integrate the existing grocery price comparison infrastructure.

### Deliverables
- IGA integration.
- Metro integration.
- Maxi integration.
- Ingredient-to-product matching.
- Price freshness checks.
- Package-size calculations.
- Product availability.

### Completion test
Match a sample shopping list to purchasable products and compare prices across retailers.

### Existing Phase 4 Adjustments
The existing price collection project remains valid.

However, its responsibility changes from general price comparison to ingredient-driven product matching and basket pricing.

The grocery database must connect to the canonical ingredient catalog.

---

# Phase 5: Shopping Optimization

### Objectives
Optimize basket costs and grocery trips.

### Deliverables
- Basket cost calculation.
- Store allocation.
- Trip optimization.
- Waste estimation.
- Alternative shopping strategies.

### Completion test
Compare one-store and two-store strategies and explain the recommended option.

---

# Phase 6: AI Agent and Interface

### Objectives
Connect the modules through a conversational interface.

### Deliverables
- Conversational interface.
- Tool calling.
- Weekly plan approval.
- Recipe substitution.
- Grocery list management.
- Plan persistence.

### Completion test
Generate and approve a complete weekly meal plan using one natural-language request.

---

# Phase 7: Personalization

### Objectives
Improve recommendations through historical user data.

### Deliverables
- Recipe ratings.
- Cooking history.
- Actual grocery expenses.
- Pantry consumption tracking.
- Food waste feedback.

### Completion test
Use previous weekly feedback to improve subsequent meal recommendations.

---

# Development Priority

| Phase | Priority |
|---|---|
| Phase 1 | Critical |
| Phase 2 | Critical |
| Phase 3 | Critical |
| Phase 4 | Critical |
| Phase 5 | High |
| Phase 6 | High |
| Phase 7 | Later |

Develop and validate each phase before introducing the next major component.

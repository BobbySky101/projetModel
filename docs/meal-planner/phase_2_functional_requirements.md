
# Smart Meal Planner
## Functional Requirements

# FR-01: Recipe Management

**Objective:** Maintain a searchable and reusable recipe database.

### Capabilities
- Import recipes from supported APIs.
- Import recipes from URLs where permitted.
- Manually create and edit recipes.
- Store ingredients, quantities and units.
- Store cooking instructions and preparation times.
- Categorize recipes by cuisine and meal type.
- Search by ingredient, theme and category.
- Rate recipes and mark favorites.
- Track previously used recipes.
- Preserve source attribution and usage rights.

### Initial providers
- Spoonacular
- Edamam
- Personal recipe imports

### Recipe attributes
- recipe_id
- name
- description
- source
- source_url
- cuisine
- prep_time
- cook_time
- servings
- difficulty
- rating
- is_favorite

### Acceptance criteria
Retrieve, save, search and reuse recipes without duplicating records.

---

# FR-02: Ingredient Management

**Objective:** Create a standardized ingredient catalog connecting recipes to grocery products.

### Capabilities
- Standardize ingredient names.
- Support French and English aliases.
- Convert measurement units.
- Distinguish weight, volume and individual quantities.
- Support ingredient substitutions.
- Identify difficult-to-match ingredients.
- Link ingredients to grocery products.
- Preserve original ingredient descriptions.

Example aliases:
- Yellow onion
- Onion, yellow
- Oignon jaune
- Chopped yellow onion

### Example ingredient catalog

| Ingredient | Quantity | Unit |
|---|---:|---|
| Chicken breast | 500 | g |
| Yellow onion | 2 | units |
| Olive oil | 30 | ml |
| Garlic | 3 | cloves |

Conversions must be ingredient-aware. Weight-to-volume conversions require appropriate density information.

### Acceptance criteria
Different ingredient descriptions can be normalized and linked to shared canonical ingredients.

---

# FR-03: Weekly Meal Planning

**Objective:** Generate seven dinners based on the user's weekly request.

### Inputs
- Weekly theme.
- Mandatory ingredients.
- Number of meals.
- Household size.
- Budget.
- Cuisine preferences.
- Dietary restrictions.
- Maximum preparation time.
- Leftover preferences.
- Previously selected meals.

### Capabilities
- Search the recipe database.
- Filter unsuitable recipes.
- Rank recipes based on preferences.
- Select seven recipes.
- Respect mandatory ingredients.
- Avoid excessive repetition.
- Optimize ingredient reuse.
- Account for leftover opportunities.
- Generate a weekly calendar.
- Allow individual recipe replacement.
- Recalculate affected grocery requirements.

### Initial meal scoring

| Criterion | Weight |
|---|---:|
| Personal preferences | 25% |
| Budget compatibility | 25% |
| Ingredient reuse | 15% |
| Meal variety | 15% |
| Nutrition balance | 10% |
| Preparation convenience | 10% |

Hard constraints, such as dietary restrictions and mandatory ingredients, must be enforced separately.

### Acceptance criteria
Generate seven dinners respecting household size, mandatory ingredients, preferences and budget constraints.

---

# FR-04: Pantry and Inventory Management

**Objective:** Avoid unnecessary purchases and reduce food waste.

### Capabilities
- Add pantry ingredients.
- Record approximate quantities.
- Update quantities after cooking.
- Track expiration dates.
- Identify ingredients needing replenishment.
- Deduct inventory from grocery requirements.
- Track leftover ingredients.

### Example

| Ingredient | Available | Required | To purchase |
|---|---:|---:|---:|
| Rice | 500 g | 900 g | 400 g |
| Olive oil | 250 ml | 100 ml | 0 |
| Garlic | 2 cloves | 5 cloves | 3 cloves |

### Acceptance criteria
Exclude ingredients already available in sufficient quantities.

---

# FR-05: Grocery Price Intelligence

**Objective:** Identify purchasable products and their prices.

### Initial retailers
- IGA
- Metro
- Maxi

Reuse the existing Phase 4 grocery price collection infrastructure.

### Capabilities
- Retrieve authorized product and price data.
- Match ingredients to retail products.
- Compare equivalent products.
- Calculate unit prices.
- Identify promotions.
- Account for package sizes.
- Check availability.
- Retain historical prices.
- Identify stale observations.

### Pricing distinctions
1. Recipe ingredient quantity.
2. Grocery package quantity.
3. Package purchase price.
4. Unit price.
5. Estimated consumed cost.

### Acceptance criteria
Match ingredients to products and compare retailer prices with traceable timestamps.

---

# FR-06: Grocery List Generation

**Objective:** Convert the weekly plan into a consolidated shopping list.

### Capabilities
- Aggregate ingredients across recipes.
- Deduplicate ingredients.
- Convert quantities into standard units.
- Subtract pantry inventory.
- Match remaining ingredients to products.
- Calculate package quantities.
- Group by grocery category.
- Group by retailer.
- Allow manual additions and removals.
- Export CSV.

### Grocery categories
- Fruits and vegetables
- Meat and seafood
- Dairy and eggs
- Bakery
- Pantry
- Frozen foods
- Household supplies

### Acceptance criteria
Generate a consolidated list with quantities, products, retailers and estimated costs.

---

# FR-07: Shopping and Trip Optimization

**Objective:** Balance price, convenience and food waste.

### Shopping strategies

**One store:** Optimize convenience and total basket cost.

**Two stores:** Optimize savings while limiting additional trips.

**Three stores:** Consider all retailers, package sizes and availability.

### Capabilities
- Calculate basket cost per retailer.
- Calculate mixed-store basket costs.
- Respect maximum store count.
- Consider package sizes and leftovers.
- Consider product availability.
- Show savings compared with single-store shopping.
- Recommend the best overall strategy.

### Initial parameters

| Parameter | Setting |
|---|---|
| Maximum stores | 2 |
| Optimization | Balanced |
| Food waste penalty | Enabled |
| Brand flexibility | Enabled |
| Promotions | Considered |
| Stale prices | Flagged |

### Optimization objective

Minimize:

Product costs + Food waste costs + Convenience penalties

Subject to:
- Required ingredients are covered.
- Package quantities are sufficient.
- Products are available.
- Budget is respected where feasible.
- Maximum store count is respected.

### Acceptance criteria
Compare one-store and two-store strategies and explain the recommended option.

---

# FR-08: AI Orchestration

**Objective:** Provide a natural-language interface to the platform.

### Capabilities
- Interpret weekly requests.
- Identify missing information.
- Search recipes.
- Invoke meal-planning services.
- Retrieve pantry inventory.
- Invoke grocery price comparison.
- Request shopping optimization.
- Present recommendations.
- Handle substitutions.
- Save approved plans.

### Responsibilities

AI:
- Interpret requests.
- Recommend recipes.
- Coordinate services.
- Explain recommendations.

Python services:
- Calculate quantities.
- Convert units.
- Aggregate ingredients.
- Match products.
- Calculate prices.
- Validate budgets.
- Optimize shopping.
- Manage database operations.

The AI must not invent prices or silently modify approved plans.

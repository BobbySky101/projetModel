
# Smart Meal Planner
## Workflows & Data Architecture

# 1. User Workflows

## Workflow A: Weekly Meal Planning

1. User submits weekly request.
2. System interprets preferences and constraints.
3. Search recipe database.
4. Filter and rank recipes.
5. Build seven-day meal plan.
6. Calculate ingredient quantities.
7. Check pantry inventory.
8. Generate grocery requirements.
9. Retrieve grocery prices.
10. Optimize basket and store selection.
11. Present meal plan and shopping list.
12. User approves or requests modifications.
13. Save approved plan.

## Workflow B: Recipe Replacement

1. User requests an alternative recipe.
2. Agent searches suitable alternatives.
3. Check weekly constraints.
4. Replace selected recipe.
5. Recalculate affected ingredient quantities.
6. Update grocery list.
7. Recalculate prices.
8. Update shopping recommendation.
9. Preserve other selected meals.

## Workflow C: Grocery Shopping Completion

1. User marks purchased items.
2. Actual prices are entered or imported.
3. Pantry quantities are updated.
4. Unpurchased items remain outstanding.
5. Actual spending is recorded.
6. Estimated and actual costs are compared.

## Workflow D: Post-Week Feedback

Collect feedback about:
- Recipes enjoyed.
- Recipes to repeat.
- Unused ingredients.
- Quantity accuracy.
- Budget compliance.

Use feedback to improve future recommendations.

---

# 2. Database Architecture

## Main Tables

| Group | Tables |
|---|---|
| Recipes | recipes, recipe_ingredients, recipe_instructions, recipe_tags |
| Ingredients | ingredients, ingredient_aliases, ingredient_substitutions |
| Personalization | user_profiles, user_preferences, pantry_inventory |
| Grocery | retailers, stores, products, product_ingredients, price_observations |
| Planning | meal_plans, planned_meals, shopping_lists, shopping_list_items |
| Optimization | shopping_trips, shopping_trip_items |
| Operations | collection_runs, agent_runs, user_feedback |

## Entity Relationships

- One recipe contains multiple recipe ingredients.
- One ingredient can appear in multiple recipes.
- One ingredient can have multiple aliases.
- One ingredient can correspond to multiple grocery products.
- One retailer sells multiple grocery products.
- One product can have multiple price observations.
- One store can have multiple price observations.
- One meal plan contains multiple planned meals.
- One meal plan generates one or more shopping lists.
- One shopping list contains multiple shopping list items.
- One user profile owns multiple pantry inventory items.

## Data Integrity

Every imported record should retain:
- Original source.
- Source URL or identifier.
- Import timestamp.
- Validation status.
- Update timestamp.

Historical prices must not be overwritten. New observations should be stored separately.

---

# 3. Example Weekly Request

"Plan my meals for next week.

Theme:
Mediterranean and Asian cuisine.

Requirements:
- Seven dinners.
- Include salmon at least once.
- Cooking time under 45 minutes.
- Avoid repeating the same protein too frequently.
- Budget: $150 CAD.

Leftovers:
Optional. Suggest reuse opportunities.

Shopping:
Compare IGA, Metro and Maxi.
Prefer two stores maximum.
Balance price, convenience and food waste."

## Expected Output

A. Weekly meal calendar.

B. Recipe details and cooking instructions.

C. Consolidated grocery list.

D. Recommended retailers.

E. Estimated basket cost.

F. Budget summary.

G. Price freshness warnings.

H. CSV exports.

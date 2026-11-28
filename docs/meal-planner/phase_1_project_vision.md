
# Smart Meal Planner
## Project Vision & Scope

**Version:** 1.0  
**Status:** Requirements Definition  
**Market:** Quebec, Canada  
**Currency:** CAD

## 1. Product Vision

Build a personal AI-powered meal-planning platform that generates weekly dinner plans based on user preferences, themes, required ingredients, pantry inventory and grocery budgets.

The platform should automatically:

1. Find suitable recipes.
2. Build a balanced weekly meal plan.
3. Calculate ingredient quantities.
4. Deduct ingredients already available.
5. Match ingredients to grocery products.
6. Compare prices across IGA, Metro and Maxi.
7. Optimize the grocery basket and store selection.
8. Generate a consolidated shopping list.
9. Preserve weekly plans and historical prices.
10. Learn from user feedback.

## 2. Default Configuration

| Parameter | Default |
|---|---|
| Household size | 3–4 people |
| Planning frequency | Weekly |
| Number of meals | 7 dinners |
| Weekly grocery budget | $150 CAD |
| Optimization strategy | Balanced |
| Leftovers | Optional |
| Initial retailers | IGA, Metro, Maxi |
| Initial market | Quebec, Canada |

Default serving size: 4 people, adjustable to 3.

The $150 budget initially covers the seven planned dinners, subject to final confirmation.

## 3. Product Architecture

The application consists of eight functional modules:

1. Recipe Management
2. Ingredient Management
3. Weekly Meal Planning
4. Pantry and Inventory Management
5. Grocery Price Intelligence
6. Grocery List Generation
7. Shopping and Trip Optimization
8. AI Orchestration

## 4. Core Architectural Principle

The system must be ingredient-centric rather than recipe-centric.

- Recipes describe what the user wants to cook.
- Ingredients describe what is required.
- Pantry inventory describes what is already available.
- Grocery products describe what can be purchased.
- Prices describe the cost of those purchases.
- The optimization engine determines the best purchasing strategy.
- The AI agent coordinates these components.

## 5. Long-Term Vision

The platform should eventually support:

- Nutritional goals.
- Weekly spending analytics.
- Automatic pantry replenishment.
- Lunch and breakfast planning.
- Food waste tracking.
- Recipe personalization.
- Automated grocery list generation.

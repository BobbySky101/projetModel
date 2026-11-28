# # ⚠️ IMPORTANT: This script requires the following packages installed via pip:
# # pip install playwright camoufox

# from playwright.sync_api import sync_playwright
# # pip install playwright camoufox

# from playwright.sync_api import sync_playwright
# from camoufox.sync_api import NewContext
# import json
# import time

# 🔒 TARGET URL - Replace this with your Cloudflare-protected URL
TARGET_URL = "https://bot.sannysoft.com/"  # ← CHANGE THIS

from camoufox.sync_api import Camoufox

with Camoufox(headless=True) as browser:
    page = browser.new_page()
    page.goto("https://example.com")


# class CloudflareBypassScraper:
#     """
#     Scraper class using Playwright + Camoufox to bypass Cloudflare.
#     Uses official camoufox.sync_api.NewContext API for fingerprint spoofing.
#     """

#     def __init__(self, target_url: str = None):
#         self.target_url = target_url or TARGET_URL
#         self.context: NewContext = None
#         self.browser = None

#     def scrape(self) -> dict | None:
#         """
#         Main scraping method using Camoufox to bypass Cloudflare.

#         Returns:
#             dict | None: Scraped data as JSON (or None if scraping fails).
#         """
#         try:
#             print(f"🚀 Starting scrape of {self.target_url}")

#             # Launch browser using Playwright sync API with Camoufox context
#             # NewContext is the official synchronous API from camoufox.sync_api
#             self.context = NewContext(
#                 browser=self.browser,
#                 os="windows",
#                 headless=False,                        # Run headlessly
#                 user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
#                 viewport={"width": 1920, "height": 1080},
#                 device_scale_factor=1.0,
#             )

#             print("✅ Camoufox context created (Official API: camoufox.sync_api.NewContext)")

#             # Navigate to target URL using the context's page
#             page = self.context.new_page()
#             print(f"🌐 Navigating to {self.target_url}...")

#             # Set a generous timeout for Cloudflare challenges (up to 2 minutes)
#             # Note: NewContext uses await internally even in sync context mode
#             # The Playwright actions are async underneath Camoufox's wrapper
#             page.goto(self.target_url, wait_until="networkidle", timeout=120000)

#             # Wait for dynamic content to load
#             try:
#                 page.wait_for_selector("body", state="visible", timeout=30000)
#             except Exception as e:
#                 print(f"⚠️ Warning: Could not find body element - {e}")

#             # Extract content from the page
#             content = page.inner_text("body")

#             # Parse JSON if the site returns JSON response
#             response_content = page.content()
#             try:
#                 data = json.loads(response_content)
#             except json.JSONDecodeError:
#                 print("⚠️ Response is not JSON, returning raw text")
#                 data = {"content": content}

#             print(f"✅ Successfully scraped {self.target_url}")

#             return data

#         except Exception as e:
#             print(f"❌ Scrape failed with error: {e}")
#             import traceback
#             traceback.print_exc()
#             return None
#         finally:
#             # Close browser context and cleanup resources
#             if self.browser:
#                 self.browser.stop()
#             if self.context:
#                 self.context.close()
#             print("🛑 Browser closed.")

#     def get_page_html(self) -> str:
#         """Returns the full HTML of the scraped page."""
#         try:
#             self.scrape()
#             page = self.context.new_page()
#             page.goto(self.target_url, timeout=60000)
#             return page.content()
#         except Exception as e:
#             print(f"Error getting HTML: {e}")
#             return None


# # Example usage (uncomment to run):
# if __name__ == "__main__":
#     # Replace with your actual target URL
#     scraper = CloudflareBypassScraper(target_url="https://bot.sannysoft.com/")

#     print("🔍 Starting Cloudflare bypass scrape...\n")

#     data = scraper.scrape()

#     if data:
#         print("\n📦 Scraped Data:")
#         print(f"Type: {type(data)}")
#         # Pretty print if it's a dict, otherwise print the content
#         if isinstance(data, dict):
#             for key, value in data.items():
#                 print(f"{key}: {value}")
#         else:
#             print(value[:500] if value else "Empty response")
#     else:
#         print("\n⚠️ No data retrieved.")
# import json
# import time

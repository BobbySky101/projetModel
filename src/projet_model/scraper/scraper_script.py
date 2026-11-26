# language python src/scraper_script.py
import requests
from bs4 import BeautifulSoup
import time

def scrape_metro_product(url):
    """
    Scrape product details from Metro.ca.
    Extracts name, brand, sale price, and regular price based on the provided HTML structure.
    
    Args:
        url (str): The URL of the product tile page.
        
    Returns:
        dict or list: Structured product data.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        scraped_data = []

        # TARGET SELECTOR: Find the main container holding the product tile data
        # Based on your note file, look for elements containing data-main-price
        items = soup.select('[data-main-price]')
        
        for item in items:
            # 1. Extract Price from data attribute (as requested)
            sale_price_attr = item.get('data-main-price', 'N/A')
            
            # 2. Extract Regular Price (nested text inside .pricing__before-price)
            regular_price_elem = item.find(class_='pricing__before-price')
            regular_price_text = regular_price_elem.find_next_sibling().get_text(strip=True) if regular_price_elem else "N/A"
            # Note: Metro often puts the price span right after the label. 
            # A more robust way for this specific structure is searching all spans in the sibling divs
            
            # Let's re-scan the entire item container for price numbers to be safe against layout changes
            regular_price_val = "N/A"
            sale_price_val = sale_price_attr
            
            # Helper to clean French currency strings (e.g., "13,99 $" -> 13.99)
            def clean_currency(s):
                if not s: return None
                # Remove $ and non-numeric chars except comma/dot
                cleaned = "".join(c for c in str(s) if c.isdigit() or c in ',.')
                try:
                    return float(cleaned.replace(',', '.')) # Handle French decimal comma
                except ValueError:
                    return "N/A"

            regular_price_val = clean_currency(regular_price_text)
            sale_price_val = clean_currency(sale_price_attr)


            # 3. Extract Title (.head__title)
            title_elem = item.find(class_='head__title')
            product_name = title_elem.get_text(strip=True) if title_elem else "No Title"

            # 4. Extract Brand (.head__brand)
            brand_elem = item.find(class_='head__brand')
            product_brand = brand_elem.get_text(strip=True) if brand_elem else "Unknown"

            scraped_data.append({
                'name': product_name,
                'brand': product_brand,
                'regular_price': regular_price_val,
                'sale_price': sale_price_val,
                'source_url': url
            })
            
        return scraped_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

if __name__ == "__main__":
    time.sleep(1)
    
    # Example URL format for Metro product page (adjust if necessary)
    # Often product pages are deep links. If scraping a listing page, 
    # you might need to find the 'data-uri' or similar anchor points first.
    target_url = "https://www.metro.ca/epicerie-en-ligne/recherche"  # Adjust to actual product detail URL
    
    # results = scrape_metro_product(target_url)
    
    # if results:
    #     print("\nScraped Metro Product Data:")
    #     for item in results:
    #         print(f"Brand: {item['brand']}")
    #         print(f"Product: {item['name']}")
    #         print(f"Regular Price: {item['regular_price']} €/$")
    #         print(f"Sale Price: {item['sale_price']} €/$")
    #         print("-" * 30)

    urls = [
        "https://www.metro.ca/",
        "https://www.metro.ca/epicerie-en-ligne/",
        "https://www.metro.ca/epicerie-en-ligne/recherche",
    ]
    for url in urls:
        try:
            response = requests.get(url, timeout=15)
            print(url, response.status_code)
        except requests.RequestException as e:
            print(url, e)

    response = requests.get(target_url)
    print("Status:", response.status_code)
    print("Headers:", response.headers)
    print("Response:", response.text[:1000])
    response.raise_for_status()
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys

BASE = "http://127.0.0.1:8000"
session = requests.Session()

critical_issues = 0
broken_assets = 0
missing_elements = 0
all_issues = []

def check_asset(url):
    try:
        # Using head for efficiency, but some servers might block it, so fallback to get
        r = session.head(url, timeout=5, allow_redirects=True)
        if r.status_code == 404:
            return False
        if r.status_code == 200:
            return True
        # Fallback to GET if HEAD failed/is not 200
        r = session.get(url, timeout=5, stream=True)
        return r.status_code == 200
    except:
        return False

def audit_page(path):
    global critical_issues, broken_assets, missing_elements
    full_url = urljoin(BASE, path)
    print(f"=====================================")
    print(f"PAGE: {path}")
    print(f"=====================================")

    try:
        response = session.get(full_url, timeout=5)
        status = response.status_code
        status_icon = "PASS" if status == 200 else "FAIL"
        print(f"Status    : {status_icon} {status}")
        
        if status != 200:
            critical_issues += 1
            all_issues.append(f"Critical: {path} returned {status}")
            print("-------------------------------------")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # CSS Files
        css_links = [urljoin(full_url, link['href']) for link in soup.find_all('link', rel='stylesheet') if link.get('href')]
        css_loaded = 0
        missing_css = []
        for css in css_links:
            if check_asset(css):
                css_loaded += 1
            else:
                missing_css.append(css.split('/')[-1])
        
        css_status = "PASS" if not missing_css else "FAIL"
        print(f"CSS Files : {css_status} {css_loaded}/{len(css_links)} loaded" + (f" (missing: {', '.join(missing_css)})" if missing_css else ""))
        broken_assets += len(missing_css)
        for m in missing_css:
            all_issues.append(f"Broken Asset (CSS): {m} on {path}")

        # JS Files
        js_scripts = [urljoin(full_url, script['src']) for script in soup.find_all('script', src=True)]
        js_loaded = 0
        missing_js = []
        for js in js_scripts:
            if check_asset(js):
                js_loaded += 1
            else:
                missing_js.append(js.split('/')[-1])
        
        js_status = "PASS" if not missing_js else "FAIL"
        print(f"JS Files  : {js_status} {js_loaded}/{len(js_scripts)} loaded" + (f" (missing: {', '.join(missing_js)})" if missing_js else ""))
        broken_assets += len(missing_js)
        for m in missing_js:
            all_issues.append(f"Broken Asset (JS): {m} on {path}")

        # Missing Images
        images = [urljoin(full_url, img['src']) for img in soup.find_all('img', src=True)]
        img_loaded = 0
        missing_img_count = 0
        for img in images:
            if check_asset(img):
                img_loaded += 1
            else:
                missing_img_count += 1
                all_issues.append(f"Broken Asset (IMG): {img} on {path}")
        
        img_status = "PASS" if missing_img_count == 0 else "FAIL"
        print(f"Images    : {img_status} {img_loaded}/{len(images)} loaded")
        broken_assets += missing_img_count

        # Broken Links
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            link_url = urljoin(full_url, href)
            parsed = urlparse(link_url)
            if parsed.netloc in ['', '127.0.0.1:8000', 'localhost:8000']:
                # Skip fragments or javascript links
                if href.startswith('#') or href.startswith('javascript:'):
                    continue
                try:
                    r = session.head(link_url, timeout=5, allow_redirects=True)
                    if r.status_code not in [200, 302, 301]:
                        all_issues.append(f"Broken Link: {href} on {path} returned {r.status_code}")
                        critical_issues += 1 # 404/500 links are critical as per requirements
                except:
                    pass

        # CSRF Check
        forms = soup.find_all('form')
        csrf_ok = True
        if forms:
            for form in forms:
                if not form.find('input', {'name': 'csrfmiddlewaretoken'}):
                    csrf_ok = False
                    break
        print(f"CSRF      : {'PASS' if csrf_ok else 'FAIL'} {'Present' if csrf_ok else 'Missing in form'}")
        if not csrf_ok:
            critical_issues += 1
            all_issues.append(f"Security: Missing CSRF token on {path}")

        # Key Elements Check
        elements_output = []
        
        # WhatsApp Widget (All pages)
        # Checking common patterns for WhatsApp widgets
        whatsapp = soup.find(id='whatsapp-widget') or soup.find(class_='whatsapp-widget') or soup.select_one('a[href*="wa.me"]')
        if whatsapp:
            elements_output.append("PASS WhatsApp widget found")
        else:
            elements_output.append("FAIL WhatsApp widget missing")
            missing_elements += 1
            all_issues.append(f"Missing Element: WhatsApp widget on {path}")

        if path == "/":
            hero = soup.find(class_='hero') or soup.find(id='hero') or soup.select_one('header, section.banner')
            if hero:
                elements_output.append("PASS Hero found")
            else:
                elements_output.append("FAIL Hero missing")
                missing_elements += 1
                all_issues.append(f"Missing Element: Hero section on homepage")
        
        if "product" in path:
            # Canvas chart
            canvas = soup.find('canvas')
            if canvas: elements_output.append("PASS Canvas chart found")
            else:
                elements_output.append("FAIL Canvas chart missing")
                missing_elements += 1
                all_issues.append(f"Missing Element: Canvas chart on {path}")
            
            # Wishlist button
            wishlist = soup.select_one('button:contains("Wishlist"), .wishlist-btn, #wishlist-btn, a[href*="wishlist"]')
            # bs4 doesn't support :contains natively in all versions, checking manually
            if not wishlist:
                for btn in soup.find_all(['button', 'a']):
                    if "wishlist" in btn.get_text().lower() or "wishlist" in str(btn.get('class', '')).lower() or "wishlist" in str(btn.get('id', '')).lower():
                        wishlist = btn
                        break
            if wishlist: elements_output.append("PASS Wishlist button found")
            else:
                elements_output.append("FAIL Wishlist button missing")
                missing_elements += 1
                all_issues.append(f"Missing Element: Wishlist button on {path}")

            # Quantity input
            qty = soup.select_one('input[name="quantity"], input[type="number"].qty, #quantity')
            if qty: elements_output.append("PASS Quantity input found")
            else:
                elements_output.append("FAIL Quantity input missing")
                missing_elements += 1
                all_issues.append(f"Missing Element: Quantity input on {path}")

            # Price Alert button
            price_alert = None
            for btn in soup.find_all(['button', 'a']):
                if "price alert" in btn.get_text().lower() or "price-alert" in str(btn.get('class', '')).lower() or "price-alert" in str(btn.get('id', '')).lower():
                    price_alert = btn
                    break
            if price_alert: elements_output.append("PASS Price Alert button found")
            else:
                elements_output.append("FAIL Price Alert button missing")
                missing_elements += 1
                all_issues.append(f"Missing Element: Price Alert button on {path}")

        if "cart" in path:
            # AJAX update (looking for script tags that might handle it or specific IDs)
            ajax = soup.select_one('#cart-update, .cart-update, script:contains("ajax"), script:contains("fetch")')
            # Fallback search in script text
            if not ajax:
                for script in soup.find_all('script'):
                    if script.string and ("ajax" in script.string.lower() or "fetch" in script.string.lower() or "update" in script.string.lower()):
                        ajax = script
                        break
            if ajax: elements_output.append("PASS AJAX update found")
            else:
                elements_output.append("FAIL AJAX update missing")
                missing_elements += 1
                all_issues.append(f"Missing Element: AJAX update on {path}")

        print("Elements  : " + "\n             ".join(elements_output))
        print("-------------------------------------")
        return soup
    except Exception as e:
        print(f"Error auditing {path}: {e}")
        critical_issues += 1
        all_issues.append(f"Critical: Error during audit of {path} - {e}")
        print("-------------------------------------")
        return None

def main():
    # 1. Homepage
    home_soup = audit_page("/")
    
    # 2. Login
    audit_page("/accounts/login/")
    
    # 3. Register
    audit_page("/accounts/register/")
    
    # 4. Cart
    audit_page("/accounts/cart/")
    
    # 5. First Product Page
    if home_soup:
        product_link = None
        for a in home_soup.find_all('a', href=True):
            if "/product/" in a['href']:
                product_link = a['href']
                break
        if product_link:
            audit_page(product_link)
        else:
            print("FAIL Could not find product link on homepage")
            all_issues.append("Critical: No product link found on homepage to audit")

    # Final Report
    print("\n=====================================")
    print("   COMPLETE ISSUE REPORT")
    print("=====================================")
    print(f"CRITICAL (500 errors/Broken Links/CSRF) : {critical_issues}")
    print(f"BROKEN ASSETS (404)                     : {broken_assets}")
    print(f"MISSING ELEMENTS                        : {missing_elements}")
    print("=====================================")
    if all_issues:
        for issue in all_issues:
            print(issue)
    else:
        print("No issues detected!")
    print("=====================================")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()

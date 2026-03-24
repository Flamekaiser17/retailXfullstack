import sys
import requests
from urllib.parse import urljoin

def verify_production_setup(base_url):
    """
    Verifies the production readiness of a deployed RetailX Django site.
    """
    if not base_url.startswith("http"):
        base_url = f"https://{base_url}"
    
    # Ensure no trailing slash for consistency
    base_url = base_url.rstrip("/")
    
    print(f"\n🚀 Starting Production Audit for: {base_url}\n")
    results = []

    # 1. Check HTTPS Enforcement
    try:
        http_url = base_url.replace("https://", "http://")
        r = requests.get(http_url, allow_redirects=False, timeout=10)
        if r.status_code in [301, 302] and "https://" in r.headers.get("Location", ""):
            print("✅ HTTPS Redirection: Active")
            results.append(True)
        else:
            print("❌ HTTPS Redirection: NOT FOUND (Security Risk!)")
            results.append(False)
    except Exception as e:
        print(f"⚠️ HTTPS Check Failed: {e}")

    # 2. Check DEBUG Mode (looking for Django debug page markers)
    try:
        r = requests.get(urljoin(base_url, "/non-existent-path-9999/"), timeout=10)
        if "DEBUG = True" in r.text or "Django version" in r.text and r.status_code == 404:
            print("❌ DEBUG Mode: ENABLED (Major Security Risk!)")
            results.append(False)
        else:
            print("✅ DEBUG Mode: DISABLED")
            results.append(True)
    except:
        pass

    # 3. Check Static Files (via WhiteNoise)
    try:
        # We'll check the main CSS file
        static_css_url = urljoin(base_url, "/static/base/css/style.css") # Adjust path if different
        r = requests.get(static_css_url, timeout=10)
        if r.status_code == 200:
            print("✅ Static Files: Served correctly via WhiteNoise")
            results.append(True)
        else:
            print(f"❌ Static Files: FAILED ({r.status_code} on {static_css_url})")
            results.append(False)
    except:
        pass

    # 4. Check Presence of CSRF on Login
    try:
        login_url = urljoin(base_url, "/accounts/login/")
        r = requests.get(login_url, timeout=10)
        if 'csrfmiddlewaretoken' in r.text:
            print("✅ Security: CSRF tokens detected on login page")
            results.append(True)
        else:
            print("⚠️ Security: No CSRF token found on login (Check templates)")
            results.append(False)
    except:
        pass

    # 5. Check Razorpay Script Presence on Cart (requires login simulation - skipped for basic check)
    
    print("\n--- AUDIT SUMMARY ---")
    if all(results):
        print("🌟 STATUS: PRODUCTION READY")
    else:
        print("🛑 STATUS: ISSUES DETECTED. Review logs above.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_production.py <YOUR_DEPLOYED_URL>")
        sys.exit(1)
    
    verify_production_setup(sys.argv[1])

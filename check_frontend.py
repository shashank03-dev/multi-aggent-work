from playwright.sync_api import sync_playwright
import os

def check_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("Navigating to http://localhost:8000...")
            page.goto('http://localhost:8000', wait_until='networkidle')
            print(f"Title: {page.title()}")
            
            # Check for main elements
            h1 = page.locator('h1').text_content()
            print(f"H1 content: {h1}")
            
            # Take a screenshot to verify visual state
            screenshot_path = 'frontend_check.png'
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            
            # Check if generate button is present
            btn = page.locator('#generate-btn')
            if btn.is_visible():
                print("Generate button is visible.")
            else:
                print("Generate button NOT visible.")
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    check_frontend()

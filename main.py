# Import Playwright sync API
from playwright.sync_api import sync_playwright
import csv
import os
import time

# Try to import python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Skip if python-dotenv is not installed

# Import Groq API
from groq import Groq

# Import email library
try:
    import yagmail
    YAGMAIL_AVAILABLE = True
except ImportError:
    YAGMAIL_AVAILABLE = False
    print("⚠️  yagmail library not installed, email push feature will be unavailable")
    print("   Install command: pip install yagmail")

def translate_title(title, client=None):
    """
    Translate English title to Chinese using Groq API
    Returns fake data if client is not configured
    """
    # Use fake data if no client
    if not client:
        # Fake data: simple placeholder translation
        fake_translations = [
            "AI breakthrough: new model performance improved by 50%",
            "Startup raises $100M in funding",
            "Open source project releases major update",
            "Tech giant announces new product",
            "Developer tools get major improvements"
        ]
        import random
        return f"[Fake Data] {random.choice(fake_translations)}"
    
    try:
        # Optimized prompt: make AI a professional tech translator
        system_prompt = """You are an experienced tech translation expert with 15 years of experience, specializing in translating Silicon Valley tech news headlines for Chinese readers.

[Core Principle: Meaning-based translation, not literal translation]

Translation Requirements:
1. **Must translate meaning, not literally**: Fully understand the core meaning of the title and express it in the most natural Chinese reading style. For example, "Show HN" should be translated appropriately, not literally
2. **Clear at a glance**: Chinese readers should immediately understand what happened. If it's funding, directly say the funding amount in Chinese; if it's a tech breakthrough, clearly state the breakthrough; if it's a product launch, clearly state the product launch
3. **Natural Chinese expression**:
   - Avoid redundant words
   - Use common Chinese verbs for tech news
   - Numbers in Chinese style
4. **Concise and powerful**: Keep titles within 15 characters, capture core information
5. **Accurate key information**: Company names, tech names, numbers must be accurate, but can be expressed in Chinese style

Only return the Chinese translation, no explanations."""
        
        user_prompt = f"Please translate the following English title: {title}"
        
        # Use Groq API call
        response = client.chat.completions.create(
            model='llama-3.1-8b-instant',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        # Extract response text
        result = response.choices[0].message.content.strip()
        
        # Clean up possible extra content
        if result.startswith('"') and result.endswith('"'):
            result = result[1:-1]
        
        return result
        
    except Exception as e:
        # Detailed error information
        error_msg = str(e)
        error_type = type(e).__name__
        print(f"⚠️  Translation failed [{error_type}]: {error_msg}")
        
        # Common error tips
        if "API_KEY" in error_msg.upper() or "authentication" in error_msg.lower():
            print("   💡 Tip: Please check if GROQ_API_KEY is correct")
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            print("   💡 Tip: API quota may be exhausted")
        elif "rate" in error_msg.lower():
            print("   💡 Tip: API request rate too high, please try again later")
        
        return f"[Translation Failed] {title}"

def main():
    # Get Groq API Key
    api_key = os.getenv('GROQ_API_KEY')
    client = None
    
    if not api_key:
        print("⚠️  GROQ_API_KEY environment variable not detected")
        print("💡 Tip: Create .env file and add GROQ_API_KEY=your_api_key_here")
        print("📝 Or set environment variable: set GROQ_API_KEY=your_api_key_here (Windows)")
        print("   Will use fake data demo function now...\n")
    else:
        print("✅ Groq API Key detected, initializing client...")
        # Initialize Groq API client
        client = Groq(api_key=api_key)
        print("✅ Client initialized successfully, will use llama-3.1-8b-instant model\n")
    
    # Use Playwright sync mode
    with sync_playwright() as p:
        # Launch chromium browser with headless mode disabled (open a real browser window)
        browser = p.chromium.launch(headless=False)
        # Create a new browser page
        page = browser.new_page()
        # Open target webpage
        page.goto('https://news.ycombinator.com/')
        
        # Wait for articles to load
        page.wait_for_selector('tr.athing', timeout=10000)
        
        # Select all article entries
        articles = page.query_selector_all('tr.athing')
        print(f"Found {len(articles)} article entries\n")
        print("=" * 60)
        
        results = []
        
        for idx, article in enumerate(articles, 1):
            # Try multiple possible selectors (Hacker News may have updated class names)
            title_elem = (
                article.query_selector('a.titlelink') or  # New selector
                article.query_selector('a.storylink') or  # Old selector
                article.query_selector('span.titleline > a') or  # Another possibility
                article.query_selector('td.title > a')  # Fallback selector
            )
            
            # Skip if not found
            if not title_elem:
                continue
                
            # Get title text and link
            title = title_elem.inner_text()
            link = title_elem.get_attribute('href')
            
            # Handle relative links
            if link and link.startswith('item?'):
                link = 'https://news.ycombinator.com/' + link
            elif link and not link.startswith('http'):
                link = 'https://news.ycombinator.com/' + link
            
            # Use AI to translate title
            print(f"[{idx}] Translating...")
            chinese_title = translate_title(title, client)
            
            results.append([title, link, chinese_title])
            
            # Print to screen (display Chinese translation)
            print(f"📰 English Title: {title}")
            print(f"🇨🇳 Chinese Translation: {chinese_title}")
            print(f"🔗 Link: {link}")
            print("-" * 60)
        
        # Save to CSV file
        with open('hacker_news.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            # Write header (with Chinese translation column)
            writer.writerow(['Title', 'Link', 'Chinese Translation'])
            # Write content
            writer.writerows(results)
        
        print(f"\n✅ Successfully saved {len(results)} entries to hacker_news.csv")
        print("📁 CSV file contains: Title, Link, Chinese Translation columns")
        
        # Send email push
        email_user = os.getenv('EMAIL_USER')
        email_pass = os.getenv('EMAIL_PASS')
        email_receiver = os.getenv('EMAIL_RECEIVER')
        
        if YAGMAIL_AVAILABLE and email_user and email_pass and email_receiver:
            try:
                print("\n📧 Sending email push...")
                
                # Generate HTML email content (top 10)
                top_10 = results[:10]
                
                # Use inline styles to avoid CSS parsing issues
                html_content = '<html><head><meta charset="UTF-8"></head><body>'
                html_content += '<h2 style="color: #ff6600;">📰 Today\'s Hacker News Tech Digest</h2>'
                html_content += '<p>Here are the top 10 tech news stories today:</p>'
                html_content += '<ul style="list-style: none; padding: 0;">'
                
                for idx, (title, link, chinese_title) in enumerate(top_10, 1):
                    # Ensure titles with translation failures are displayed normally
                    # If translation failed or contains failure marker, show English title; otherwise show Chinese translation
                    if chinese_title and '[Translation Failed]' not in chinese_title and '[Fake Data]' not in chinese_title:
                        display_title = chinese_title
                    else:
                        display_title = title
                    
                    # Escape HTML special characters
                    display_title_escaped = display_title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    title_escaped = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    
                    html_content += f'<li style="margin-bottom: 20px; padding: 15px; background-color: #f9f9f9; border-left: 4px solid #ff6600;">'
                    html_content += f'<div style="color: #666; font-size: 0.9em; margin-bottom: 8px;"><strong>{idx}. {display_title_escaped}</strong></div>'
                    html_content += f'<div style="font-weight: bold; color: #333; margin-bottom: 5px;">{title_escaped}</div>'
                    html_content += f'<div><a href="{link}" target="_blank" style="color: #0066cc; text-decoration: none;">🔗 Read Original</a></div>'
                    html_content += '</li>'
                
                html_content += '</ul>'
                html_content += '<p style="color: #999; font-size: 0.9em; margin-top: 30px;">Data Source: <a href="https://news.ycombinator.com/" target="_blank" style="color: #0066cc;">Hacker News</a></p>'
                html_content += '</body></html>'
                
                # Send email
                yag = yagmail.SMTP(user=email_user, password=email_pass)
                yag.send(
                    to=email_receiver,
                    subject='📰 Today\'s Hacker News Tech Digest',
                    contents=html_content
                )
                print(f"✅ Email successfully sent to: {email_receiver}")
                
            except Exception as e:
                print(f"⚠️  Email sending failed: {e}")
        else:
            if not YAGMAIL_AVAILABLE:
                print("⚠️  yagmail library not installed, skipping email push")
            elif not email_user or not email_pass or not email_receiver:
                print("⚠️  Email configuration incomplete, skipping email push")
                print("💡 Tip: Add EMAIL_USER, EMAIL_PASS, EMAIL_RECEIVER to .env file")
        
        print("\n⏰ Browser will close automatically in 10 seconds...")
        
        # Countdown display
        for i in range(10, 0, -1):
            print(f"   Closing in {i} seconds...", end='\r')
            time.sleep(1)
        print("   Closing browser...")
        
        # Close browser
        browser.close()

if __name__ == '__main__':
    main()

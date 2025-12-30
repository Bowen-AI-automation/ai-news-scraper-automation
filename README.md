# Hacker News Intelligent Scraper 🚀

Automatically scrapes trending articles from Hacker News and translates them using AI, so you can quickly understand what's happening in Silicon Valley!

## ✨ Features

- 🔍 Automatically scrapes Hacker News front page articles
- 🤖 Uses Groq API to intelligently translate titles
- 📊 Saves results as CSV file (includes English title, link, and translated title)
- 🖥️ Real-time display of translation results
- 📧 Optional email push notifications (top 10 articles)
- 💡 Supports demo mode with fake data (works without API Key)

## 📦 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browser

```bash
playwright install chromium
```

## 🔑 API Key Configuration

### Method 1: Using .env File (Recommended)

1. Create a `.env` file in the project root directory
2. Add the following content:
   ```
   # Groq API Configuration
   GROQ_API_KEY=your_groq_api_key_here
   
   # Email Push Configuration (Optional)
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_app_password
   EMAIL_RECEIVER=receiver@example.com
   ```
3. Replace the placeholder values with your actual credentials

For detailed setup instructions, see [API_KEY_SETUP.md](API_KEY_SETUP.md)

### Method 2: Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your_api_key_here"
```

**Windows (CMD):**
```cmd
set GROQ_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export GROQ_API_KEY="your_api_key_here"
```

## 🚀 Usage

```bash
python boss_stealer.py
```

## 📝 Output

- **Terminal Display**: Each article displays English title, translated title, and link
- **CSV File**: Saved as `hacker_news.csv`, containing three columns:
  - Title (English)
  - Link
  - Translated Title

## 💰 Cost Information

Using Groq API:
- Model: llama-3.1-8b-instant (fast and cost-effective)
- Each title translation consumes approximately 0.0001-0.0002 USD
- 30 articles cost approximately 0.003-0.006 USD
- Groq provides generous free tier limits

If no API Key is configured, the program will use fake data for demonstration.

## 📧 Email Push Feature

The program can automatically send the top 10 articles to your email. To enable this feature:

1. Install yagmail: `pip install yagmail`
2. Configure email credentials in `.env` file (see API_KEY_SETUP.md for details)
3. The program will automatically send HTML-formatted email with top 10 articles

## 🔒 Security Notes

- **Never commit `.env` file to Git** - it contains sensitive credentials
- The `.env` file is already included in `.gitignore`
- Use `.env.example` as a template (without real credentials)
- Keep your API keys secure and never share them publicly

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This project is for educational purposes only. Please respect Hacker News's terms of service and rate limits when using this scraper.

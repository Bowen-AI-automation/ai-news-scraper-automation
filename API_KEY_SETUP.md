# Configuration Guide

## Method 1: Using .env File (Recommended)

1. Copy `.env.example` to `.env` in the project root directory
2. Open `.env` file and replace the placeholder values with your actual credentials:
   ```
   # Groq API Configuration
   GROQ_API_KEY=your_groq_api_key_here
   
   # Email Push Configuration (Optional)
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_app_password
   EMAIL_RECEIVER=receiver@example.com
   ```

## Method 2: Set Environment Variables

### Windows (PowerShell)
```powershell
$env:GROQ_API_KEY="your_groq_api_key_here"
```

### Windows (CMD)
```cmd
set GROQ_API_KEY=your_groq_api_key_here
```

### Linux/Mac
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

## Getting Groq API Key

1. Visit https://console.groq.com/
2. Sign in or create an account
3. Navigate to API Keys page
4. Click "Create API Key"
5. Copy the generated API Key (keep it secure)

## Email Configuration

### Gmail Setup

1. **Enable Two-Factor Authentication**: Enable 2FA in your Google account settings
2. **Generate App-Specific Password**:
   - Visit https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter a name (e.g., "Hacker News Scraper")
   - Copy the generated 16-character password
   - Use this password in the `EMAIL_PASS` field of your `.env` file

3. **Configuration Example**:
   ```
   EMAIL_USER=yourname@gmail.com
   EMAIL_PASS=abcd efgh ijkl mnop  # App-specific password (remove spaces)
   EMAIL_RECEIVER=receiver@example.com
   ```

### Other Email Providers

For email providers other than Gmail, you typically need to:

- **Enable App Passwords or Authorization Codes**: Most email providers require app-specific passwords for third-party applications
- **Check Provider Documentation**: Refer to your email provider's documentation for SMTP settings and authentication requirements
- **Common Providers**:
  - **Outlook/Hotmail**: Use app password from Microsoft account settings
  - **Yahoo Mail**: Generate app password from account security settings
  - **Custom SMTP**: Configure using your provider's SMTP server settings

## Important Notes

- The `.env` file is already added to `.gitignore` and will not be committed to Git
- If no API Key is configured, the program will use fake data for demonstration
- If email is not configured, the program will skip the email push feature
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Model used: llama-3.1-8b-instant (provided by Groq, fast with generous free tier)

## Security Best Practices

1. **Never commit `.env` file** - It contains sensitive credentials
2. **Use `.env.example` as a template** - Share configuration structure without real values
3. **Keep API keys secure** - Don't share them publicly or in screenshots
4. **Rotate keys regularly** - If a key is exposed, regenerate it immediately
5. **Use environment variables in production** - For deployment, use secure environment variable management

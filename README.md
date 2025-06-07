# SecureAI Threads Auto Poster

Automated Threads posting system for sharing content about secured LLM solutions for Malaysian businesses.

## Features

- 📅 Automated scheduling (daily, hourly, weekly)
- 🎯 Targeted content for Malaysian businesses
- 🔒 Secure LLM and AI compliance focus
- 📊 Logging and monitoring
- 🎲 Random or sequential posting
- 🛠️ Easy CLI management
- 🚀 GitHub Actions automation

## Setup

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your .env file:**
   ```bash
   cp .env.template .env
   # Edit .env with your actual Threads API credentials
   ```

3. **Test API connection:**
   ```bash
   python cli.py test
   ```

### GitHub Actions Setup

1. **Fork/Clone this repository to GitHub**

2. **Set up GitHub Secrets:**
   Go to your repository → Settings → Secrets and variables → Actions
   
   Add these secrets:
   - `THREADS_APP_ID`: Your Threads App ID
   - `THREADS_APP_SECRET`: Your Threads App Secret  
   - `THREADS_USER_ID`: Your Threads User ID
   - `THREADS_LONG_LIVED_TOKEN`: Your long-lived access token

3. **Enable GitHub Actions:**
   - Go to Actions tab in your repository
   - Enable workflows if prompted
   
4. **Automated Posting:**
   - Posts automatically run daily at 10:00 AM Malaysia time
   - View logs in Actions tab
   - Manually trigger posting via "Run workflow" button

## Usage

### CLI Commands

- **List all posts:**
  ```bash
  python cli.py list
  ```

- **Post a single message:**
  ```bash
  python cli.py post              # Post next in sequence
  python cli.py post --id 5       # Post specific ID
  ```

- **Start automated scheduler:**
  ```bash
  python cli.py schedule
  ```

### GitHub Actions Workflows

- **Auto Post to Threads** - Daily automated posting
- **Test Threads API** - Manual testing without posting

### Direct Python Usage

```python
from threads_autoposter import ThreadsAutoPoster

poster = ThreadsAutoPoster()

# Post single
poster.post_single(1)  # By ID
poster.post_single()   # Next in sequence

# Run scheduler
poster.run_scheduler()
```

## Content Configuration

Edit `posts_content.json` to:
- Add new posts
- Modify posting schedule
- Change hashtags and categories
- Adjust settings

### Post Structure
```json
{
  "id": 1,
  "content": "Your post content with emojis 🇲🇾",
  "hashtags": ["#SecureAI", "#Malaysia"],
  "category": "introduction"
}
```

## Scheduling Configuration

Current settings (in `posts_content.json`):
- **Frequency:** Daily
- **Time:** 10:00 (Kuala Lumpur time)
- **Order:** Random (can be changed to sequential)

## Content Categories

1. **Fear Introduction** - Data sovereignty awareness
2. **Compliance Fear** - PDPA and regulatory risks
3. **Benefits with Fear** - Performance vs. security trade-offs
4. **Industry Fear** - Sector-specific risks
5. **Security Comparison** - Local vs. foreign solutions
6. **Scalability Fear** - Growth with security concerns
7. **Case Study Fear** - Real-world consequences
8. **Strategy Fear** - Decision-making risks

## Monitoring

- **Local:** Logs saved to `threads_poster.log`
- **GitHub Actions:** 
  - View workflow runs in Actions tab
  - Download log artifacts for detailed analysis
  - Email notifications for failed runs (configurable)

## Security Notes

- ✅ Environment variables are stored as GitHub Secrets
- ✅ `.env` file is excluded from repository
- ✅ API tokens are never exposed in logs
- ✅ Automated token refresh handling

## Troubleshooting

### Local Issues

1. **API Connection Failed:**
   - Check your tokens in `.env`
   - Verify token expiration dates
   - Test with `python cli.py test`

2. **Posts Not Publishing:**
   - Check logs in `threads_poster.log`
   - Verify content length limits
   - Ensure proper API permissions

### GitHub Actions Issues

1. **Workflow Fails:**
   - Check GitHub Secrets are set correctly
   - Review workflow logs in Actions tab
   - Ensure repository has Actions enabled

2. **Posts Not Appearing:**
   - Verify Threads account permissions
   - Check if long-lived token expired
   - Review uploaded log artifacts

## Manual Posting

To post immediately without waiting for scheduled time:
- **Locally:** `python cli.py post`
- **GitHub:** Go to Actions → "Auto Post to Threads" → "Run workflow"
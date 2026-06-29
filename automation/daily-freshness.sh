#!/bin/bash
# ⚡ LINETOGEL Daily Freshness Cron Script
# Run: bash automation/daily-freshness.sh
# Cron: 0 2 * * * cd /path/to/linetogel && bash automation/daily-freshness.sh

set -e

REPO_DIR="/root/.openclaw-autoclaw/workspace/linetogel"
LOG_FILE="/tmp/linetogel-cron.log"
TODAY=$(date +%Y-%m-%d)

echo "========================================" | tee -a "$LOG_FILE"
echo "🔄 LINETOGEL Daily Freshness — $TODAY" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

cd "$REPO_DIR"

# 1. Run the auto-SEO system
echo "📊 Running auto-SEO system..." | tee -a "$LOG_FILE"
python3 automation/system.py 2>&1 | tee -a "$LOG_FILE"

# 2. Update lastmod in sitemap
echo "📅 Updating sitemap lastmod dates..." | tee -a "$LOG_FILE"
python3 -c "
import re
from datetime import date
today = date.today().isoformat()
with open('sitemap.xml', 'r') as f:
    sitemap = f.read()
sitemap = re.sub(r'<lastmod>[^<]+</lastmod>', f'<lastmod>{today}</lastmod>', sitemap)
with open('sitemap.xml', 'w') as f:
    f.write(sitemap)
print(f'  ✅ Sitemap dates updated to {today}')
" 2>&1 | tee -a "$LOG_FILE"

# 3. Ping search engines
echo "📡 Pinging search engines..." | tee -a "$LOG_FILE"
curl -s -o /dev/null -w "  Google: HTTP %{http_code}\n" \
  "https://www.google.com/ping?sitemap=https://linetogel-pi.vercel.app/sitemap.xml" 2>&1 | tee -a "$LOG_FILE"
curl -s -o /dev/null -w "  Bing: HTTP %{http_code}\n" \
  "https://www.bing.com/ping?sitemap=https://linetogel-pi.vercel.app/sitemap.xml" 2>&1 | tee -a "$LOG_FILE"

# 4. Commit & push if changes
if [[ -n $(git status --porcelain) ]]; then
    echo "📦 Changes detected — committing..." | tee -a "$LOG_FILE"
    git add -A
    git commit -m "🔄 Auto-freshness update — $TODAY
- Sitemap lastmod updated
- Content dates refreshed
- Auto-SEO system check complete" 2>&1 | tee -a "$LOG_FILE"
    git push origin main 2>&1 | tee -a "$LOG_FILE"
    echo "  ✅ Changes committed & pushed" | tee -a "$LOG_FILE"
else
    echo "  ⏭ No changes to commit" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "✅ Daily freshness complete — $TODAY" | tee -a "$LOG_FILE"
echo "Vercel will auto-deploy" | tee -a "$LOG_FILE"

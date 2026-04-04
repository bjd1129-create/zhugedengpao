#!/bin/bash
# DataViz - push trading data with proxy
export HTTPS_PROXY="http://127.0.0.1:7897"
export http_proxy="http://127.0.0.1:7897"
cd /Users/bjd/Desktop/ZhugeDengpao-Team
git add trading.html data/trading/portfolio.json 2>/dev/null
if git diff --cached --quiet; then
    echo "No changes to push"
else
    git commit -m "dataviz: update $(date +%H:%M)" 2>/dev/null
    git push origin main 2>/dev/null
    echo "Pushed ✅"
fi

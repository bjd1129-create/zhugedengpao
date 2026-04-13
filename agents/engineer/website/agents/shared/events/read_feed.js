(function() {
  const FEED_URL = './data/live_feed.json';
  const STATUS_URL = './data/office_status.json';

  async function loadFeed() {
    try {
      const [feedRes, statusRes] = await Promise.all([
        fetch(FEED_URL),
        fetch(STATUS_URL)
      ]);
      const events = await feedRes.json();
      const status = await statusRes.json();
      renderAll(events, status);
    } catch (err) {
      console.warn('数据加载失败，使用兜底数据');
      renderFallback();
    }
  }

  function renderAll(events, status) {
    const feed = document.getElementById('live-feed');
    if (!feed) return;

    const items = (events || []).slice(0, 5).map(e =>
      `<div class="feed-item">
        <span class="feed-agent">${e.agent || '系统'}</span>
        <span class="feed-msg">${e.msg || ''}</span>
        <span class="feed-time">${e.time || '刚刚'}</span>
      </div>`
    ).join('');

    feed.innerHTML = items || '<p>暂无活动</p>';

    const dot = document.getElementById('status-dot');
    if (dot) {
      const onlineAgents = Object.values(status.agents || {}).filter(a => a.status === 'online').length;
      dot.className = onlineAgents > 0 ? 'status-dot online' : 'status-dot offline';
    }
  }

  function renderFallback() {
    const feed = document.getElementById('live-feed');
    if (feed) {
      feed.innerHTML = '<p class="feed-item"><span class="feed-msg">⚠️ 数据同步中，请稍后刷新</span></p>';
    }
  }

  document.addEventListener('DOMContentLoaded', loadFeed);
  setInterval(loadFeed, 30000);
})();

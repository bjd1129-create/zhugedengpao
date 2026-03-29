/* ================================
   诸葛灯泡 — Warm Home JS
   温暖光点 + 柔和气泡动画
   ================================ */

(function () {
  'use strict';

  /* ---- Nav scroll effect ---- */
  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => {
      nav.classList.toggle('scrolled', window.scrollY > 20);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---- Scroll Reveal ---- */
  const revealEls = document.querySelectorAll('.reveal, .step, .insight-item, .log-entry');
  if (revealEls.length) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );
    revealEls.forEach((el) => observer.observe(el));
  }

  /* ---- Active nav link ---- */
  const path = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-links a');
  navLinks.forEach((link) => {
    const href = link.getAttribute('href');
    if (
      href === path ||
      (href === 'index.html' && (path === '/' || path.endsWith('/'))) ||
      (path.startsWith('/') && href.startsWith('/') && path.startsWith(href.replace('.html', '')))
    ) {
      link.classList.add('active');
    }
  });

  /* ---- Radar bar animation ---- */
  const radarBars = document.querySelectorAll('.radar-bar');
  if (radarBars.length) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const bar = entry.target;
            const target = bar.dataset.width;
            bar.style.width = target + '%';
            observer.unobserve(bar);
          }
        });
      },
      { threshold: 0.2 }
    );
    radarBars.forEach((bar) => observer.observe(bar));
  }

  /* ================================
     AGENT NETWORK CANVAS — Warm Bubbles
     ================================ */
  const canvas = document.getElementById('agent-network-canvas');
  if (canvas) {
    // Populate agent pills
    const agents = ['Radar','Ink','Forge','Spark','Coin','Shield','Link','Canvas','Sower','Bridge'];
    const nodesContainer = document.getElementById('agent-nodes');
    if (nodesContainer) {
      agents.forEach(name => {
        const pill = document.createElement('span');
        pill.className = 'agent-node-pill';
        pill.textContent = name;
        nodesContainer.appendChild(pill);
      });
    }

    const ctx = canvas.getContext('2d');
    let W, H, nodes = [], bubbles = [], raf;

    // Warm color palette
    const WARM_CORAL = '232,114,74';
    const WARM_LIGHT = '255,154,108';
    const WARM_GOLD  = '255,179,71';
    const WARM_GREEN = '124,184,122';

    const COLORS = [
      `rgba(${WARM_CORAL},`,
      `rgba(${WARM_LIGHT},`,
      `rgba(${WARM_GOLD},`,
      `rgba(${WARM_GREEN},`,
    ];

    const BULB_COLOR = '#E8724A';
    const BUBBLE_COUNT = 20;
    const NODE_COUNT = 10;

    function rgbaPref(c) { return c; }

    function resize() {
      const rect = canvas.parentElement.getBoundingClientRect();
      W = canvas.width  = rect.width * devicePixelRatio;
      H = canvas.height = rect.height * devicePixelRatio;
      canvas.style.width  = rect.width + 'px';
      canvas.style.height = rect.height + 'px';
      ctx.scale(devicePixelRatio, devicePixelRatio);
      W = rect.width;
      H = rect.height;
    }

    function initNodes() {
      nodes = [];
      const margin = 70;
      for (let i = 0; i < NODE_COUNT; i++) {
        nodes.push({
          x: margin + Math.random() * (W - margin * 2),
          y: margin + Math.random() * (H - margin * 2),
          vx: (Math.random() - 0.5) * 0.22,
          vy: (Math.random() - 0.5) * 0.22,
          r: 4 + Math.random() * 3,
          baseR: 4 + Math.random() * 3,
          pulse: Math.random() * Math.PI * 2,
          pulseSpeed: 0.01 + Math.random() * 0.008,
          opacity: 0.55 + Math.random() * 0.35,
          colorIdx: Math.floor(Math.random() * COLORS.length),
        });
      }
    }

    function initBubbles() {
      bubbles = [];
      for (let i = 0; i < BUBBLE_COUNT; i++) {
        spawnBubble();
      }
    }

    function spawnBubble() {
      bubbles.push({
        x: Math.random() * W,
        y: H + 20 + Math.random() * 60,
        r: 3 + Math.random() * 8,
        speed: 0.3 + Math.random() * 0.5,
        wobble: Math.random() * Math.PI * 2,
        wobbleSpeed: 0.015 + Math.random() * 0.01,
        wobbleAmp: 0.4 + Math.random() * 0.6,
        opacity: 0.08 + Math.random() * 0.12,
        colorIdx: Math.floor(Math.random() * COLORS.length),
      });
    }

    function drawBackground() {
      // Warm cream background
      ctx.fillStyle = '#FFFBF5';
      ctx.fillRect(0, 0, W, H);

      // Subtle warm radial gradient in center
      const grad = ctx.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, Math.max(W, H) * 0.6);
      grad.addColorStop(0, 'rgba(255,243,224,0.4)');
      grad.addColorStop(1, 'rgba(255,251,245,0)');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, W, H);
    }

    function drawBubble(b) {
      const ci = COLORS[b.colorIdx];

      // Soft glow halo
      const grad = ctx.createRadialGradient(b.x, b.y, 0, b.x, b.y, b.r * 2.5);
      grad.addColorStop(0, ci + (b.opacity * 0.8) + ')');
      grad.addColorStop(0.5, ci + (b.opacity * 0.3) + ')');
      grad.addColorStop(1, ci + '0)');
      ctx.beginPath();
      ctx.arc(b.x, b.y, b.r * 2.5, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      // Bubble body
      ctx.beginPath();
      ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
      ctx.fillStyle = ci + (b.opacity * 0.5) + ')';
      ctx.fill();

      // Highlight spot (top-left)
      ctx.beginPath();
      ctx.arc(b.x - b.r * 0.3, b.y - b.r * 0.3, b.r * 0.25, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,255,255,0.5)';
      ctx.globalAlpha = b.opacity;
      ctx.fill();
      ctx.globalAlpha = 1;
    }

    function drawNode(n) {
      const ci = COLORS[n.colorIdx];
      const breathe = Math.sin(n.pulse) * 0.5 + 0.5;
      n.pulse += n.pulseSpeed;

      const r = n.baseR + breathe * 2;

      // Warm glow
      const grad = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, r * 4);
      grad.addColorStop(0, ci + (n.opacity * 0.2) + ')');
      grad.addColorStop(1, ci + '0)');
      ctx.beginPath();
      ctx.arc(n.x, n.y, r * 4, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      // Core dot
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fillStyle = BULB_COLOR;
      ctx.globalAlpha = n.opacity * (0.6 + breathe * 0.4);
      ctx.fill();
      ctx.globalAlpha = 1;

      // Inner highlight
      ctx.beginPath();
      ctx.arc(n.x - r * 0.25, n.y - r * 0.25, r * 0.35, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,255,255,0.55)';
      ctx.globalAlpha = n.opacity * (0.2 + breathe * 0.3);
      ctx.fill();
      ctx.globalAlpha = 1;
    }

    function drawEdge(a, b) {
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      const maxDist = 180;
      if (dist > maxDist) return;

      const t = 1 - dist / maxDist;
      const ci = COLORS[a.colorIdx];
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.strokeStyle = ci + (t * 0.25) + ')';
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    function updateBubbles() {
      for (let i = bubbles.length - 1; i >= 0; i--) {
        const b = bubbles[i];
        b.y -= b.speed;
        b.wobble += b.wobbleSpeed;
        b.x += Math.sin(b.wobble) * b.wobbleAmp;

        if (b.y < -b.r * 3) {
          bubbles.splice(i, 1);
          spawnBubble();
        }
      }
      while (bubbles.length < BUBBLE_COUNT) spawnBubble();
    }

    function updateNodes() {
      nodes.forEach(n => {
        n.x += n.vx;
        n.y += n.vy;
        n.pulse += n.pulseSpeed;

        const margin = 50;
        if (n.x < margin) { n.vx = Math.abs(n.vx); }
        if (n.x > W - margin) { n.vx = -Math.abs(n.vx); }
        if (n.y < margin) { n.vy = Math.abs(n.vy); }
        if (n.y > H - margin) { n.vy = -Math.abs(n.vy); }
      });
    }

    function loop() {
      ctx.clearRect(0, 0, W, H);
      drawBackground();

      // Edges
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          drawEdge(nodes[i], nodes[j]);
        }
      }

      // Bubbles (behind nodes)
      bubbles.forEach(drawBubble);

      // Nodes on top
      nodes.forEach(drawNode);

      updateNodes();
      updateBubbles();

      raf = requestAnimationFrame(loop);
    }

    const ro = new ResizeObserver(() => {
      cancelAnimationFrame(raf);
      resize();
      initNodes();
      initBubbles();
      loop();
    });
    ro.observe(canvas.parentElement);

    resize();
    initNodes();
    initBubbles();
    loop();
  }

  /* ================================
     PARTICLE CANVAS (office.html) — Warm Living Room
     ================================ */
  const officeCanvas = document.getElementById('particle-canvas');
  if (officeCanvas) {
    const ctx = officeCanvas.getContext('2d');
    let W, H, nodes = [], particles = [], raf;

    const WARM_CORAL = '232,114,74';
    const WARM_LIGHT = '255,154,108';
    const WARM_GOLD  = '255,179,71';
    const WARM_GREEN = '124,184,122';

    const COLORS = [WARM_CORAL, WARM_LIGHT, WARM_GOLD, WARM_GREEN];

    function rrgba(c, a) { return `rgba(${c},${a})`; }

    function resize() {
      W = officeCanvas.width  = window.innerWidth;
      H = officeCanvas.height = window.innerHeight;
    }

    function initNodes() {
      nodes = [];
      for (let i = 0; i < 12; i++) {
        nodes.push({
          x: 60 + Math.random() * (W - 120),
          y: 60 + Math.random() * (H - 160),
          vx: (Math.random() - 0.5) * 0.15,
          vy: (Math.random() - 0.5) * 0.15,
          r: 3 + Math.random() * 3,
          baseR: 3 + Math.random() * 3,
          alpha: 0.4 + Math.random() * 0.4,
          phase: Math.random() * Math.PI * 2,
          phaseSpeed: 0.01 + Math.random() * 0.008,
          colorIdx: Math.floor(Math.random() * COLORS.length),
          fixed: false,
        });
      }

      // Anchored warm nodes
      const anchors = [
        { x: W * 0.2, y: H * 0.35 },
        { x: W * 0.55, y: H * 0.25 },
        { x: W * 0.8, y: H * 0.45 },
        { x: W * 0.38, y: H * 0.65 },
      ];
      anchors.forEach((a, i) => {
        nodes.push({
          x: a.x, y: a.y,
          vx: 0, vy: 0,
          r: 5 + i,
          baseR: 5 + i,
          alpha: 0.65,
          phase: i * 1.2,
          phaseSpeed: 0.016,
          colorIdx: 0,
          fixed: true,
          fixedX: a.x,
          fixedY: a.y,
        });
      });
    }

    function spawnBubble() {
      if (nodes.length < 2) return;
      const from = nodes[Math.floor(Math.random() * nodes.length)];
      let to = nodes[Math.floor(Math.random() * nodes.length)];
      if (to === from) to = nodes[(nodes.indexOf(to) + 1) % nodes.length];
      particles.push({
        from, to,
        progress: 0,
        speed: 0.003 + Math.random() * 0.003,
        size: 3 + Math.random() * 5,
        alpha: 0.3 + Math.random() * 0.4,
        trail: [],
        type: 'bubble',
      });
    }

    function spawnGlow() {
      const n = nodes[Math.floor(Math.random() * nodes.length)];
      particles.push({
        x: n.x, y: n.y,
        vx: (Math.random() - 0.5) * 1.5,
        vy: -0.5 - Math.random() * 1,
        life: 1,
        decay: 0.012 + Math.random() * 0.01,
        size: 4 + Math.random() * 5,
        colorIdx: n.colorIdx,
        type: 'glow',
      });
    }

    function drawBackground() {
      ctx.fillStyle = '#FFFBF5';
      ctx.fillRect(0, 0, W, H);

      const grad = ctx.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, Math.max(W, H) * 0.6);
      grad.addColorStop(0, 'rgba(255,243,224,0.35)');
      grad.addColorStop(1, 'rgba(255,251,245,0)');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, W, H);
    }

    function drawLine(a, b) {
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      const maxDist = Math.min(W, H) * 0.5;
      if (dist > maxDist) return;

      const t = 1 - dist / maxDist;
      const c = COLORS[a.colorIdx];
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.strokeStyle = rrgba(c, t * 0.15);
      ctx.lineWidth = 0.8;
      ctx.stroke();
    }

    function drawNode(n) {
      const breathe = Math.sin(n.phase) * 0.5 + 0.5;
      n.phase += n.phaseSpeed;

      const c = COLORS[n.colorIdx];
      const r = n.baseR + breathe * 2;

      const grad = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, r * 4);
      grad.addColorStop(0, rrgba(c, n.alpha * 0.2));
      grad.addColorStop(1, rrgba(c, 0));
      ctx.beginPath();
      ctx.arc(n.x, n.y, r * 4, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fillStyle = '#E8724A';
      ctx.globalAlpha = n.alpha * (0.5 + breathe * 0.5);
      ctx.fill();
      ctx.globalAlpha = 1;

      ctx.beginPath();
      ctx.arc(n.x - r * 0.25, n.y - r * 0.25, r * 0.3, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,255,255,0.5)';
      ctx.globalAlpha = n.alpha * (0.2 + breathe * 0.3);
      ctx.fill();
      ctx.globalAlpha = 1;
    }

    function drawBubble(p) {
      const x = p.from.x + (p.to.x - p.from.x) * p.progress;
      const y = p.from.y + (p.to.y - p.from.y) * p.progress;

      p.trail.push({ x, y });
      if (p.trail.length > 10) p.trail.shift();

      // Bubble trail
      p.trail.forEach((pt, i) => {
        const ta = (i / p.trail.length) * p.alpha * 0.25;
        const ci = COLORS[p.from.colorIdx];
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, p.size * 0.3 * (i / p.trail.length), 0, Math.PI * 2);
        ctx.fillStyle = rrgba(ci, ta);
        ctx.fill();
      });

      const c = COLORS[p.from.colorIdx];
      const headAlpha = p.alpha * Math.max(0, 1 - Math.abs(p.progress - 0.5) * 1.5);

      const grad = ctx.createRadialGradient(x, y, 0, x, y, p.size * 4);
      grad.addColorStop(0, rrgba(c, headAlpha * 0.5));
      grad.addColorStop(1, rrgba(c, 0));
      ctx.beginPath();
      ctx.arc(x, y, p.size * 4, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      ctx.beginPath();
      ctx.arc(x, y, p.size * 0.5, 0, Math.PI * 2);
      ctx.fillStyle = '#E8724A';
      ctx.globalAlpha = headAlpha;
      ctx.fill();
      ctx.globalAlpha = 1;
    }

    function drawGlow(p) {
      const c = COLORS[p.colorIdx];
      const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.size * 3);
      grad.addColorStop(0, rrgba(c, p.life * 0.35));
      grad.addColorStop(1, rrgba(c, 0));
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size * 3, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size * 0.4, 0, Math.PI * 2);
      ctx.fillStyle = '#FF9A6C';
      ctx.globalAlpha = p.life * 0.7;
      ctx.fill();
      ctx.globalAlpha = 1;
    }

    function update() {
      nodes.forEach(n => {
        if (n.fixed) {
          n.phase += n.phaseSpeed;
          n.x = n.fixedX + Math.sin(n.phase * 0.5) * 12;
          n.y = n.fixedY + Math.cos(n.phase * 0.4) * 8;
        } else {
          n.x += n.vx;
          n.y += n.vy;
          n.phase += n.phaseSpeed;
          const margin = 40;
          if (n.x < margin) { n.vx = Math.abs(n.vx); }
          if (n.x > W - margin) { n.vx = -Math.abs(n.vx); }
          if (n.y < margin) { n.vy = Math.abs(n.vy); }
          if (n.y > H - margin) { n.vy = -Math.abs(n.vy); }
        }
      });

      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        if (p.type === 'bubble') {
          p.progress += p.speed;
          if (p.progress >= 1) {
            p.from = p.to;
            p.to = nodes[Math.floor(Math.random() * nodes.length)];
            p.progress = 0;
            p.trail = [];
          }
        } else if (p.type === 'glow') {
          p.x += p.vx;
          p.y += p.vy;
          p.life -= p.decay;
          if (p.life <= 0) particles.splice(i, 1);
        }
      }

      if (Math.random() < 0.03) spawnGlow();
      while (particles.filter(p => p.type === 'bubble').length < 14) spawnBubble();
    }

    function draw() {
      ctx.clearRect(0, 0, W, H);
      drawBackground();

      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          drawLine(nodes[i], nodes[j]);
        }
      }

      particles.filter(p => p.type === 'bubble').forEach(drawBubble);
      nodes.forEach(drawNode);
      particles.filter(p => p.type === 'glow').forEach(drawGlow);

      update();
      raf = requestAnimationFrame(draw);
    }

    const ro = new ResizeObserver(() => {
      cancelAnimationFrame(raf);
      resize();
      initNodes();
      particles = [];
      draw();
    });
    ro.observe(document.body);

    resize();
    initNodes();
    draw();
  }

})();

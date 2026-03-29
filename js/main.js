/* ================================
   ZhugeDengpao — Main JS
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
     AGENT NETWORK CANVAS ANIMATION
     ================================ */
  const canvas = document.getElementById('agent-network-canvas');
  if (canvas) {
    // Populate agent pills
    const agents = ['Radar','Ink','Forge','Spark','Coin','Shield','Link','Canvas','Sower','Bridge'];
    const nodesContainer = document.getElementById('agent-nodes');
    agents.forEach(name => {
      const pill = document.createElement('span');
      pill.className = 'agent-node-pill';
      pill.textContent = name;
      nodesContainer.appendChild(pill);
    });

    const ctx = canvas.getContext('2d');
    let W, H, nodes = [], particles = [], raf;
    const AGENT_COUNT = 10;
    const MAX_DIST = 200;
    const PARTICLE_COUNT = 25;
    const AMBER = '245,197,24';
    const AMBER_DIM = 'rgba(245,197,24,';
    const BULB_GLOW = '#f5c518';

    function resize() {
      const rect = canvas.parentElement.getBoundingClientRect();
      W = canvas.width = rect.width * devicePixelRatio;
      H = canvas.height = rect.height * devicePixelRatio;
      canvas.style.width = rect.width + 'px';
      canvas.style.height = rect.height + 'px';
      ctx.scale(devicePixelRatio, devicePixelRatio);
      W = rect.width;
      H = rect.height;
    }

    function initNodes() {
      nodes = [];
      const margin = 60;
      for (let i = 0; i < AGENT_COUNT; i++) {
        nodes.push({
          x: margin + Math.random() * (W - margin * 2),
          y: margin + Math.random() * (H - margin * 2),
          vx: (Math.random() - 0.5) * 0.25,
          vy: (Math.random() - 0.5) * 0.25,
          r: 4 + Math.random() * 3,
          pulse: Math.random() * Math.PI * 2,
          pulseSpeed: 0.012 + Math.random() * 0.008,
          opacity: 0.6 + Math.random() * 0.4,
          isHub: i === 0, // first node slightly bigger (like a central coordinator)
        });
      }
    }

    function initParticles() {
      particles = [];
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        spawnParticle();
      }
    }

    function spawnParticle() {
      // Choose a random node as origin
      const from = nodes[Math.floor(Math.random() * nodes.length)];
      particles.push({
        from,
        to: nodes[Math.floor(Math.random() * nodes.length)],
        progress: 0,
        speed: 0.003 + Math.random() * 0.004,
        size: 1.5 + Math.random() * 1.5,
        opacity: 0.3 + Math.random() * 0.5,
      });
    }

    function drawNode(n) {
      const pulse = Math.sin(n.pulse) * 0.5 + 0.5;
      const glowR = n.r + pulse * 8 + (n.isHub ? 6 : 0);
      const alpha = n.opacity * (0.4 + pulse * 0.3);

      // Outer glow
      const grad = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, glowR * 2.5);
      grad.addColorStop(0, AMBER_DIM + (alpha * 0.25) + ')');
      grad.addColorStop(1, 'rgba(245,197,24,0)');
      ctx.beginPath();
      ctx.arc(n.x, n.y, glowR * 2.5, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      // Core dot
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r + pulse * 1.5, 0, Math.PI * 2);
      ctx.fillStyle = BULB_GLOW;
      ctx.globalAlpha = 0.7 + pulse * 0.3;
      ctx.fill();
      ctx.globalAlpha = 1;

      // Center bright spot
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r * 0.4, 0, Math.PI * 2);
      ctx.fillStyle = '#fff';
      ctx.globalAlpha = 0.4 + pulse * 0.3;
      ctx.fill();
      ctx.globalAlpha = 1;
    }

    function drawEdge(a, b, opacity) {
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist > MAX_DIST) return;

      const t = 1 - dist / MAX_DIST;
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.strokeStyle = AMBER_DIM + (opacity * t * 0.5) + ')';
      ctx.lineWidth = 0.8;
      ctx.stroke();
    }

    function drawParticle(p) {
      const x = p.from.x + (p.to.x - p.from.x) * p.progress;
      const y = p.from.y + (p.to.y - p.from.y) * p.progress;
      const alpha = p.opacity * (1 - Math.abs(p.progress - 0.5) * 2);

      // Soft trail
      const grad = ctx.createRadialGradient(x, y, 0, x, y, p.size * 3);
      grad.addColorStop(0, AMBER_DIM + alpha + ')');
      grad.addColorStop(1, 'rgba(245,197,24,0)');
      ctx.beginPath();
      ctx.arc(x, y, p.size * 3, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      // Bright core
      ctx.beginPath();
      ctx.arc(x, y, p.size * 0.5, 0, Math.PI * 2);
      ctx.fillStyle = BULB_GLOW;
      ctx.globalAlpha = alpha;
      ctx.fill();
      ctx.globalAlpha = 1;
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

    function updateParticles() {
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.progress += p.speed;
        if (p.progress >= 1) {
          // Retarget
          p.from = p.to;
          p.to = nodes[Math.floor(Math.random() * nodes.length)];
          p.progress = 0;
        }
      }
      // Maintain count
      while (particles.length < PARTICLE_COUNT) spawnParticle();
    }

    function drawBackground() {
      // Subtle vignette
      const grad = ctx.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, Math.max(W, H) * 0.7);
      grad.addColorStop(0, 'rgba(10,10,11,0)');
      grad.addColorStop(1, 'rgba(10,10,11,0.5)');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, W, H);
    }

    function loop() {
      ctx.clearRect(0, 0, W, H);

      // Dim base
      ctx.fillStyle = '#0a0a0b';
      ctx.fillRect(0, 0, W, H);

      drawBackground();

      // Edges
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          drawEdge(nodes[i], nodes[j], 0.4);
        }
      }

      // Particles
      particles.forEach(drawParticle);

      // Nodes on top
      nodes.forEach(drawNode);

      updateNodes();
      updateParticles();

      raf = requestAnimationFrame(loop);
    }

    const ro = new ResizeObserver(() => {
      cancelAnimationFrame(raf);
      resize();
      initNodes();
      initParticles();
      loop();
    });
    ro.observe(canvas.parentElement);

    resize();
    initNodes();
    initParticles();
    loop();
  }

})();

// ─── CONSULT — Main JavaScript ─────────────────────────
document.addEventListener('DOMContentLoaded', function() {

  // ─── Mobile Navigation Toggle ─────────────────────────
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.navbar-links');

  if (navToggle) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
      const icon = navToggle.querySelector('i');
      icon.classList.toggle('fa-bars');
      icon.classList.toggle('fa-times');
    });
  }

  // ─── Auto-dismiss messages ────────────────────────────
  const messages = document.querySelectorAll('.message');
  messages.forEach((msg, index) => {
    setTimeout(() => {
      msg.style.animation = 'slideOut 0.3s ease-in forwards';
      setTimeout(() => msg.remove(), 300);
    }, 4000 + (index * 500));

    msg.addEventListener('click', () => {
      msg.style.animation = 'slideOut 0.3s ease-in forwards';
      setTimeout(() => msg.remove(), 300);
    });
  });

  // ─── Scroll animations ───────────────────────────────
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.card, .stat-card, .step').forEach(el => {
    el.style.opacity = '0';
    observer.observe(el);
  });

  // ─── Star rating interactive ──────────────────────────
  const ratingInput = document.querySelector('input[name="rating"]');
  if (ratingInput) {
    const starsContainer = document.createElement('div');
    starsContainer.className = 'stars-interactive';
    starsContainer.style.cssText = 'display:flex;gap:8px;cursor:pointer;font-size:1.5rem;margin-bottom:8px;';

    for (let i = 1; i <= 5; i++) {
      const star = document.createElement('i');
      star.className = 'fas fa-star';
      star.style.color = 'var(--text-muted)';
      star.dataset.value = i;
      star.addEventListener('click', () => {
        ratingInput.value = i;
        starsContainer.querySelectorAll('i').forEach((s, idx) => {
          s.style.color = idx < i ? 'var(--accent-warning)' : 'var(--text-muted)';
        });
      });
      star.addEventListener('mouseenter', () => {
        starsContainer.querySelectorAll('i').forEach((s, idx) => {
          s.style.color = idx < i ? 'var(--accent-warning)' : 'var(--text-muted)';
        });
      });
      starsContainer.appendChild(star);
    }

    starsContainer.addEventListener('mouseleave', () => {
      const val = parseInt(ratingInput.value) || 0;
      starsContainer.querySelectorAll('i').forEach((s, idx) => {
        s.style.color = idx < val ? 'var(--accent-warning)' : 'var(--text-muted)';
      });
    });

    ratingInput.parentNode.insertBefore(starsContainer, ratingInput);
    ratingInput.style.display = 'none';
  }

  // ─── Video consultation placeholder ───────────────────
  const startVideoBtn = document.getElementById('startVideoBtn');
  if (startVideoBtn) {
    startVideoBtn.addEventListener('click', async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        const localVideo = document.getElementById('localVideo');
        if (localVideo) {
          localVideo.srcObject = stream;
          localVideo.play();
          document.getElementById('localPlaceholder')?.remove();
        }
        startVideoBtn.innerHTML = '<i class="fas fa-video"></i>';
        startVideoBtn.style.background = 'var(--accent-success)';
      } catch (err) {
        alert('Camera access denied or unavailable.');
      }
    });
  }

  const endVideoBtn = document.getElementById('endVideoBtn');
  if (endVideoBtn) {
    endVideoBtn.addEventListener('click', () => {
      const localVideo = document.getElementById('localVideo');
      if (localVideo && localVideo.srcObject) {
        localVideo.srcObject.getTracks().forEach(track => track.stop());
        localVideo.srcObject = null;
      }
      window.history.back();
    });
  }

  // ─── Smooth scroll on page ────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
  });

});

// ─── SlideOut Animation (CSS injected) ───────────────────
const slideOutStyle = document.createElement('style');
slideOutStyle.textContent = `
  @keyframes slideOut {
    to { transform: translateX(120%); opacity: 0; }
  }
`;
document.head.appendChild(slideOutStyle);

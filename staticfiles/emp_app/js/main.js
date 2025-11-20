// ============================================
// CLAUDE.AI INSPIRED NAVIGATION - MOBILE MENU
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuClose = document.getElementById('mobileMenuClose');
    const body = document.body;

    // Open Mobile Menu
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.add('active');
            body.classList.add('menu-open');
        });
    }

    // Close Mobile Menu
    if (mobileMenuClose) {
        mobileMenuClose.addEventListener('click', function() {
            mobileMenu.classList.remove('active');
            body.classList.remove('menu-open');
        });
    }

    // Close on Overlay Click
    if (mobileMenu) {
        mobileMenu.addEventListener('click', function(e) {
            if (e.target === mobileMenu) {
                mobileMenu.classList.remove('active');
                body.classList.remove('menu-open');
            }
        });
    }

    // Close on Escape Key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
            mobileMenu.classList.remove('active');
            body.classList.remove('menu-open');
        }
    });

    // Close menu when clicking on a link
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link, .mobile-nav-link-sub');
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', function() {
            setTimeout(() => {
                mobileMenu.classList.remove('active');
                body.classList.remove('menu-open');
            }, 200);
        });
    });
});

// ============================================
// NAVBAR SCROLL EFFECT
// ============================================

let lastScroll = 0;
const navbar = document.querySelector('.navbar-claude');

window.addEventListener('scroll', function() {
    const currentScroll = window.pageYOffset;

    // Add shadow on scroll
    if (currentScroll > 10) {
        navbar.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.08)';
    } else {
        navbar.style.boxShadow = 'none';
    }

    lastScroll = currentScroll;
});

// ============================================
// SMOOTH SCROLL FOR ANCHOR LINKS
// ============================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '#main-content') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

/* ============================================
   EMPLOYEEHUB - Main JavaScript
   ============================================ */

// Initialize on DOM Load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    initNavbar();
    initAnimations();
    initFormValidation();
    initSearchFunctionality();
    initTooltips();
    initScrollAnimations();
    initThemeToggle();
    initNotifications();
}

/* ============================================
   Navbar Functionality
   ============================================ */

function initNavbar() {
    const navbar = document.querySelector('.navbar-custom');
    if (!navbar) return;

    // Scroll effect
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });

    // Close mobile menu when clicking a nav link
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const mobileNavLinks = document.querySelectorAll('.navbar-collapse .nav-link, .navbar-collapse .dropdown-item');

    mobileNavLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                if (bsCollapse) {
                    bsCollapse.hide();
                }
            }
        });
    });

    // Active link highlighting
    const navLinks = document.querySelectorAll('.nav-link-custom');
    const currentPath = window.location.pathname;

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

/* ============================================
   Animation Initialization
   ============================================ */

function initAnimations() {
    // Stagger animations for cards
    const cards = document.querySelectorAll('.card-modern, .employee-card, .stat-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate-fade-in-up');
    });

    // Hero animations
    const heroTitle = document.querySelector('.hero-title');
    const heroSubtitle = document.querySelector('.hero-subtitle');
    const heroCta = document.querySelector('.hero-cta');

    if (heroTitle) heroTitle.classList.add('animate-fade-in-down');
    if (heroSubtitle) heroSubtitle.classList.add('animate-fade-in-up');
    if (heroCta) {
        heroCta.style.animationDelay = '0.3s';
        heroCta.classList.add('animate-scale-in');
    }
}

/* ============================================
   Scroll Animations
   ============================================ */

function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animateElements = document.querySelectorAll('.animate-on-scroll');
    animateElements.forEach(el => observer.observe(el));
}

/* ============================================
   Form Validation & Enhancement
   ============================================ */

function initFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required], select[required]');

        inputs.forEach(input => {
            // Real-time validation
            input.addEventListener('blur', () => {
                validateInput(input);
            });

            // Remove error on input
            input.addEventListener('input', () => {
                removeError(input);
            });
        });

        // Form submission
        form.addEventListener('submit', (e) => {
            let isValid = true;

            inputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill in all required fields correctly', 'warning');
            }
        });
    });
}

function validateInput(input) {
    const value = input.value.trim();

    if (input.hasAttribute('required') && !value) {
        showError(input, 'This field is required');
        return false;
    }

    if (input.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showError(input, 'Please enter a valid email');
            return false;
        }
    }

    if (input.type === 'number' && value) {
        if (isNaN(value) || value < 0) {
            showError(input, 'Please enter a valid number');
            return false;
        }
    }

    if (input.type === 'tel' && value) {
        const phoneRegex = /^\d{10}$/;
        if (!phoneRegex.test(value.replace(/\D/g, ''))) {
            showError(input, 'Please enter a valid 10-digit phone number');
            return false;
        }
    }

    removeError(input);
    return true;
}

function showError(input, message) {
    removeError(input);

    input.classList.add('is-invalid');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.textContent = message;
    errorDiv.style.color = '#f5576c';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.25rem';

    input.parentNode.appendChild(errorDiv);
}

function removeError(input) {
    input.classList.remove('is-invalid');
    const errorDiv = input.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

/* ============================================
   Search Functionality
   ============================================ */

function initSearchFunctionality() {
    const searchInput = document.querySelector('.search-input');
    const searchableItems = document.querySelectorAll('.searchable-item');

    if (!searchInput || searchableItems.length === 0) return;

    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();

        searchableItems.forEach(item => {
            const text = item.textContent.toLowerCase();

            if (text.includes(searchTerm)) {
                item.style.display = '';
                item.classList.add('animate-fade-in-up');
            } else {
                item.style.display = 'none';
            }
        });

        // Show "no results" message
        const visibleItems = Array.from(searchableItems).filter(item => item.style.display !== 'none');

        let noResultsMsg = document.querySelector('.no-results-message');

        if (visibleItems.length === 0) {
            if (!noResultsMsg) {
                noResultsMsg = document.createElement('div');
                noResultsMsg.className = 'no-results-message text-center py-5';
                noResultsMsg.innerHTML = `
                    <div class="animate-fade-in-up">
                        <i class="fas fa-search fa-3x mb-3" style="color: #cbd5e0;"></i>
                        <p class="text-muted">No results found for "${searchTerm}"</p>
                    </div>
                `;
                searchableItems[0].parentNode.appendChild(noResultsMsg);
            }
        } else {
            if (noResultsMsg) {
                noResultsMsg.remove();
            }
        }
    });
}

/* ============================================
   Live Table Filtering
   ============================================ */

function initTableFilter() {
    const filterInputs = document.querySelectorAll('.filter-input');
    const tableRows = document.querySelectorAll('.filter-table tbody tr');

    if (filterInputs.length === 0 || tableRows.length === 0) return;

    filterInputs.forEach(input => {
        input.addEventListener('input', () => {
            const filters = {};

            filterInputs.forEach(inp => {
                if (inp.value) {
                    filters[inp.dataset.column] = inp.value.toLowerCase();
                }
            });

            tableRows.forEach(row => {
                let shouldShow = true;

                for (const [column, value] of Object.entries(filters)) {
                    const cell = row.querySelector(`td[data-column="${column}"]`);
                    if (cell && !cell.textContent.toLowerCase().includes(value)) {
                        shouldShow = false;
                        break;
                    }
                }

                row.style.display = shouldShow ? '' : 'none';
                if (shouldShow) {
                    row.classList.add('animate-fade-in-up');
                }
            });
        });
    });
}

/* ============================================
   Tooltips
   ============================================ */

function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/* ============================================
   Theme Toggle (Optional)
   ============================================ */

function initThemeToggle() {
    const themeToggle = document.querySelector('.theme-toggle');
    if (!themeToggle) return;

    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);

    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
}

/* ============================================
   Notifications
   ============================================ */

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-modern alert-dismissible fade show`;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';

    notification.innerHTML = `
        <strong>${message}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

function initNotifications() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) closeBtn.click();
        }, 5000);
    });
}

/* ============================================
   Modal Utilities
   ============================================ */

function showConfirmModal(title, message, onConfirm) {
    const modalHtml = `
        <div class="modal fade modal-modern" id="confirmModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>${message}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-gradient" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-gradient" id="confirmBtn">Confirm</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('confirmModal'));

    document.getElementById('confirmBtn').addEventListener('click', () => {
        onConfirm();
        modal.hide();
    });

    modal.show();

    document.getElementById('confirmModal').addEventListener('hidden.bs.modal', () => {
        document.getElementById('confirmModal').remove();
    });
}

/* ============================================
   Count Up Animation
   ============================================ */

function animateCountUp(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;

        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Initialize count up for stat cards
document.querySelectorAll('.stat-value').forEach(stat => {
    const target = parseInt(stat.getAttribute('data-target') || stat.textContent);
    if (!isNaN(target)) {
        stat.textContent = '0';

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCountUp(stat, target);
                    observer.unobserve(stat);
                }
            });
        });

        observer.observe(stat);
    }
});

/* ============================================
   Smooth Scroll
   ============================================ */

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '') {
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

/* ============================================
   Loading States
   ============================================ */

function showLoading(button) {
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    button.dataset.originalText = originalText;
}

function hideLoading(button) {
    button.disabled = false;
    button.innerHTML = button.dataset.originalText || 'Submit';
}

// Apply loading to form submissions
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn) {
            showLoading(submitBtn);
        }
    });
});

/* ============================================
   Copy to Clipboard
   ============================================ */

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy', 'danger');
    });
}

/* ============================================
   Export Utilities
   ============================================ */

// Make functions available globally
window.EmployeeHub = {
    showNotification,
    showConfirmModal,
    showLoading,
    hideLoading,
    copyToClipboard,
    animateCountUp
};

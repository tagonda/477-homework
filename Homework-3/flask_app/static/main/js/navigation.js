/**
 * Navigation menu functionality for mobile responsive design
 */
const menuToggle = document.querySelector('.nav__menu-toggle');
const navLinks = document.querySelector('.nav__links');

/**
 * Toggle the mobile navigation menu open/closed
 */
const toggleMenu = () => {
    // Toggle the active state of the menu button
    menuToggle.classList.toggle('nav__menu-toggle--active');
    
    // Toggle the open state of the navigation links
    navLinks.classList.toggle('nav__links--open');
};

/**
 * Close the mobile menu when a link is clicked
 */
const closeMobileMenu = () => {
    if (navLinks.classList.contains('nav__links--open')) {
        menuToggle.classList.remove('nav__menu-toggle--active');
        navLinks.classList.remove('nav__links--open');
    }
};

/**
 * Handle responsive behavior on window resize
 */
const handleResize = () => {
    const windowWidth = window.innerWidth;
    
    // If screen is larger than mobile breakpoint and menu is open, close it
    if (windowWidth > 650 && navLinks.classList.contains('nav__links--open')) {
        menuToggle.classList.remove('nav__menu-toggle--active');
        navLinks.classList.remove('nav__links--open');
    }
};

// Event listeners
if (menuToggle) {
    menuToggle.addEventListener('click', toggleMenu);
}

// Add click event to all nav links to close menu on mobile
const allNavLinks = document.querySelectorAll('.nav__link');
allNavLinks.forEach(link => {
    link.addEventListener('click', closeMobileMenu);
});

// Handle window resize events with debouncing for performance
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(handleResize, 250);
});
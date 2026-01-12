/**
 * Feedback form functionality
 */

const feedbackToggleBtn = document.getElementById('feedbackToggleBtn');
const feedbackOverlay = document.getElementById('feedbackOverlay');
const feedbackCloseBtn = document.getElementById('feedbackCloseBtn');

/**
 * Open the feedback form
 */
const openFeedbackForm = () => {
    feedbackOverlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent scrolling when form is open
};

/**
 * Close the feedback form
 */
const closeFeedbackForm = () => {
    feedbackOverlay.classList.remove('active');
    document.body.style.overflow = ''; // Re-enable scrolling
};

/**
 * Close form when clicking outside of it
 */
const handleOverlayClick = (e) => {
    if (e.target === feedbackOverlay) {
        closeFeedbackForm();
    }
};

/**
 * Close form on Escape key press
 */
const handleEscapeKey = (e) => {
    if (e.key === 'Escape' && feedbackOverlay.classList.contains('active')) {
        closeFeedbackForm();
    }
};

// Event Listeners
if (feedbackToggleBtn) {
    feedbackToggleBtn.addEventListener('click', openFeedbackForm);
}

if (feedbackCloseBtn) {
    feedbackCloseBtn.addEventListener('click', closeFeedbackForm);
}

if (feedbackOverlay) {
    feedbackOverlay.addEventListener('click', handleOverlayClick);
}

document.addEventListener('keydown', handleEscapeKey);
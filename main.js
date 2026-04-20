/**
 * Main JavaScript - LBB88 GitHub Pages Site
 * ==========================================
 */

/**
 * Initialize the application when DOM is ready
 */
function init() {
  console.log('Site initialized');
}

// Run on DOMContentLoaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

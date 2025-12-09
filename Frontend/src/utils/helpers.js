// src/utils/helpers.js

/**
 * Generates the Tailwind CSS class string for navigation links, 
 * applying the 'active' style if the current view matches the link's viewName.
 * * @param {string} viewName - The name of the view (e.g., 'chat', 'profile').
 * @param {string} currentView - The currently active view state from App.jsx.
 * @returns {string} The combined CSS class string.
 */
export const getNavLinkClass = (viewName, currentView) => {
    return `w-full text-left flex items-center space-x-3 p-2 rounded-lg transition duration-150 
       ${currentView === viewName ? 'bg-slate-700 text-slate-100 font-semibold' : 'text-slate-300 hover:bg-slate-700'}`;
};

// You can add other global utility functions here, such as date formatting or error handling helpers.
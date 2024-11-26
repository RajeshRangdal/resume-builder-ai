// Utility functions for form handling and validation
const utils = {
  validateEmail: (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  },

  validatePhone: (phone) => {
    const re = /^\+?[\d\s-]{10,}$/;
    return re.test(phone);
  },

  validateRequired: (value) => {
    return value.trim().length > 0;
  },

  validateURL: (url) => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  },

  createElementWithClasses: (tag, classes) => {
    const element = document.createElement(tag);
    if (classes) {
      element.className = classes;
    }
    return element;
  },

  showError: (element, message) => {
    const errorDiv = utils.createElementWithClasses(
      "div",
      "alert alert-danger mt-2"
    );
    errorDiv.textContent = message;
    element.parentNode.appendChild(errorDiv);
    setTimeout(() => errorDiv.remove(), 3000);
  },

  formatDate: (date) => {
    return new Date(date).toLocaleDateString("en-US", {
      month: "short",
      year: "numeric",
    });
  },
};

// Export utils object
window.utils = utils;

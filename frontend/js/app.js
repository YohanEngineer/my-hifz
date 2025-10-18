/**
 * My Hifz Planner - Frontend Application
 * Handles form validation, API communication, and PDF generation
 */

// Configuration
const CONFIG = {
    API_BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000'
        : `http://${window.location.hostname}:8000`,
    API_ENDPOINT: '/api/v1/plan/generate'
};

// DOM Elements
const elements = {
    form: null,
    generateBtn: null,
    alertContainer: null,
    loadingSpinner: null,
    pagesPerPeriod: null,
    periodType: null,
    startPage: null,
    order: null
};

/**
 * Initialize the application
 */
function init() {
    // Cache DOM elements
    elements.form = document.getElementById('planningForm');
    elements.generateBtn = document.getElementById('generateBtn');
    elements.alertContainer = document.getElementById('alertContainer');
    elements.loadingSpinner = document.getElementById('loadingSpinner');
    elements.pagesPerPeriod = document.getElementById('pagesPerPeriod');
    elements.periodType = document.getElementById('periodType');
    elements.startPage = document.getElementById('startPage');
    elements.order = document.getElementById('order');

    // Add event listeners
    elements.form.addEventListener('submit', handleFormSubmit);

    // Add input validation listeners
    elements.pagesPerPeriod.addEventListener('input', validatePagesInput);
    elements.startPage.addEventListener('input', validateStartPageInput);

    console.log('My Hifz Planner initialized');
}

/**
 * Handle form submission
 * @param {Event} event - Form submit event
 */
async function handleFormSubmit(event) {
    event.preventDefault();

    // Validate form
    if (!validateForm()) {
        showAlert('Veuillez corriger les erreurs dans le formulaire', 'danger');
        return;
    }

    // Get form data
    const formData = getFormData();

    // Show loading state
    setLoadingState(true);

    try {
        // Call API to generate PDF
        await generatePDF(formData);
        showAlert('Votre planning a été généré avec succès !', 'success');
    } catch (error) {
        console.error('Error generating PDF:', error);
        showAlert(
            'Une erreur est survenue lors de la génération du planning. Veuillez réessayer.',
            'danger'
        );
    } finally {
        setLoadingState(false);
    }
}

/**
 * Validate the form
 * @returns {boolean} - True if form is valid
 */
function validateForm() {
    let isValid = true;

    // Remove previous validation states
    elements.form.classList.remove('was-validated');

    // Validate pages per period
    const pages = parseInt(elements.pagesPerPeriod.value);
    if (isNaN(pages) || pages < 1 || pages > 604) {
        elements.pagesPerPeriod.classList.add('is-invalid');
        isValid = false;
    } else {
        elements.pagesPerPeriod.classList.remove('is-invalid');
        elements.pagesPerPeriod.classList.add('is-valid');
    }

    // Validate start page
    const startPage = parseInt(elements.startPage.value);
    if (isNaN(startPage) || startPage < 1 || startPage > 604) {
        elements.startPage.classList.add('is-invalid');
        isValid = false;
    } else {
        elements.startPage.classList.remove('is-invalid');
        elements.startPage.classList.add('is-valid');
    }

    // Add Bootstrap validation class
    elements.form.classList.add('was-validated');

    return isValid;
}

/**
 * Validate pages per period input
 */
function validatePagesInput() {
    const value = parseInt(this.value);
    if (isNaN(value) || value < 1 || value > 604) {
        this.classList.add('is-invalid');
        this.classList.remove('is-valid');
    } else {
        this.classList.remove('is-invalid');
        this.classList.add('is-valid');
    }
}

/**
 * Validate start page input
 */
function validateStartPageInput() {
    const value = parseInt(this.value);
    if (isNaN(value) || value < 1 || value > 604) {
        this.classList.add('is-invalid');
        this.classList.remove('is-valid');
    } else {
        this.classList.remove('is-invalid');
        this.classList.add('is-valid');
    }
}

/**
 * Get form data
 * @returns {Object} - Form data object
 */
function getFormData() {
    return {
        pages_per_period: parseInt(elements.pagesPerPeriod.value),
        period_type: elements.periodType.value,
        start_page: parseInt(elements.startPage.value),
        order: elements.order.value
    };
}

/**
 * Generate PDF by calling the API
 * @param {Object} data - Planning settings
 */
async function generatePDF(data) {
    const url = `${CONFIG.API_BASE_URL}${CONFIG.API_ENDPOINT}`;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        // Get the PDF blob
        const blob = await response.blob();

        // Create download link
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;

        // Generate filename with date
        const date = new Date().toISOString().split('T')[0];
        const periodType = data.period_type === 'Daily' ? 'Quotidien' : 'Hebdomadaire';
        link.download = `Planning_Hifz_${periodType}_${date}.pdf`;

        // Trigger download
        document.body.appendChild(link);
        link.click();

        // Cleanup
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);

        // Announce to screen readers
        announceToScreenReader('Le fichier PDF a été téléchargé avec succès');

    } catch (error) {
        console.error('Error in generatePDF:', error);
        throw error;
    }
}

/**
 * Set loading state
 * @param {boolean} isLoading - Whether to show loading state
 */
function setLoadingState(isLoading) {
    if (isLoading) {
        // Show full-screen loading spinner
        elements.loadingSpinner.classList.remove('d-none');
        // Hide the form to prevent any interaction
        elements.form.style.opacity = '0.5';
        elements.form.style.pointerEvents = 'none';
        // Announce to screen readers
        announceToScreenReader('Génération du planning en cours, veuillez patienter');
    } else {
        // Hide loading spinner
        elements.loadingSpinner.classList.add('d-none');
        // Restore form
        elements.form.style.opacity = '1';
        elements.form.style.pointerEvents = 'auto';
    }
}

/**
 * Show alert message
 * @param {string} message - Alert message
 * @param {string} type - Alert type (success, danger, info, warning)
 */
function showAlert(message, type = 'info') {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="bi bi-${getAlertIcon(type)} me-2" aria-hidden="true"></i>
            <strong>${message}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fermer"></button>
        </div>
    `;

    elements.alertContainer.innerHTML = alertHTML;

    // Auto-dismiss success alerts after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            const alert = elements.alertContainer.querySelector('.alert');
            if (alert) {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                bsAlert.close();
            }
        }, 5000);
    }

    // Scroll to alert
    elements.alertContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    // Announce to screen readers
    announceToScreenReader(message);
}

/**
 * Get Bootstrap icon for alert type
 * @param {string} type - Alert type
 * @returns {string} - Icon class
 */
function getAlertIcon(type) {
    const icons = {
        success: 'check-circle-fill',
        danger: 'exclamation-triangle-fill',
        warning: 'exclamation-circle-fill',
        info: 'info-circle-fill'
    };
    return icons[type] || icons.info;
}

/**
 * Announce message to screen readers
 * @param {string} message - Message to announce
 */
function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.className = 'visually-hidden';
    announcement.textContent = message;

    document.body.appendChild(announcement);

    // Remove after announcement
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

/**
 * Handle API connection errors
 */
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);

    if (event.reason && event.reason.message && event.reason.message.includes('fetch')) {
        showAlert(
            'Impossible de se connecter au serveur. Veuillez vérifier que le serveur est en cours d\'exécution.',
            'danger'
        );
    }
});

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

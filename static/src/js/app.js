// Main JavaScript file for Django project
import axios from 'axios';
import Chart from 'chart.js/auto';

// Configure axios defaults
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

// Export for use in templates
window.axios = axios;
window.Chart = Chart;







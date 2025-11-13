/* ============================================================
   Dashboard de Leituras - Scripts Principais
   ============================================================ */

/**
 * Tema do aplicativo
 */
class ThemeManager {
    constructor() {
        this.htmlElement = document.documentElement;
        this.themeToggleBtn = document.getElementById('theme-toggle-btn');
        this.init();
    }

    init() {
        // Carrega tema salvo ou usa preferência do sistema
        const savedTheme = localStorage.getItem('theme') || 
                          (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        this.applyTheme(savedTheme);

        // Evento para alternar tema
        if (this.themeToggleBtn) {
            this.themeToggleBtn.addEventListener('click', () => this.toggle());
        }
    }

    applyTheme(theme) {
        this.htmlElement.setAttribute('data-bs-theme', theme);
        if (this.themeToggleBtn) {
            this.themeToggleBtn.textContent = theme === 'dark' ? 'brightness_7' : 'brightness_4';
        }
    }

    toggle() {
        const currentTheme = this.htmlElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', newTheme);
        this.applyTheme(newTheme);
    }
}

/**
 * Gerenciador de Gráficos
 */
class ChartManager {
    constructor() {
        this.charts = {};
        this.init();
    }

    init() {
        // Espera Chart.js estar disponível
        if (typeof Chart !== 'undefined') {
            this.initCharts();
        }
    }

    /**
     * Inicializa gráficos na página
     */
    initCharts() {
        const temperatureChartCanvas = document.getElementById('temperatureChart');
        const currentDataChartCanvas = document.getElementById('currentChart');

        if (temperatureChartCanvas) {
            this.createTemperatureChart(temperatureChartCanvas);
        }

        if (currentDataChartCanvas) {
            this.createCurrentChart(currentDataChartCanvas);
        }
    }

    /**
     * Cria gráfico de temperatura
     */
    createTemperatureChart(canvas) {
        this.fetchChartData('/api/chart-data/', (data) => {
            const ctx = canvas.getContext('2d');
            
            this.charts.temperature = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Temperatura (°C)',
                        data: data.temperatura,
                        borderColor: '#0d6efd',
                        backgroundColor: 'rgba(13, 110, 253, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.3,
                        pointRadius: 3,
                        pointHoverRadius: 5,
                        pointBackgroundColor: '#0d6efd',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            labels: {
                                font: { size: 12, weight: 'bold' },
                                padding: 15,
                            }
                        },
                        title: {
                            display: true,
                            text: 'Histórico de Temperatura'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            ticks: {
                                callback: function(value) {
                                    return value + ' °C';
                                }
                            }
                        }
                    }
                }
            });
        });
    }

    /**
     * Cria gráfico de corrente
     */
    createCurrentChart(canvas) {
        this.fetchChartData('/api/chart-data/', (data) => {
            const ctx = canvas.getContext('2d');
            
            this.charts.current = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Corrente (A)',
                        data: data.corrente,
                        backgroundColor: [
                            'rgba(25, 135, 84, 0.7)',
                            'rgba(13, 110, 253, 0.7)',
                            'rgba(255, 193, 7, 0.7)',
                        ],
                        borderColor: [
                            '#198754',
                            '#0d6efd',
                            '#ffc107',
                        ],
                        borderWidth: 2,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            labels: { font: { size: 12, weight: 'bold' } }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return value + ' A';
                                }
                            }
                        }
                    }
                }
            });
        });
    }

    /**
     * Busca dados para gráficos via AJAX
     */
    fetchChartData(url, callback) {
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => callback(data))
        .catch(error => console.error('Erro ao buscar dados do gráfico:', error));
    }

    /**
     * Atualiza gráficos com novos dados
     */
    updateCharts(data) {
        if (this.charts.temperature) {
            this.charts.temperature.data.labels = data.labels;
            this.charts.temperature.data.datasets[0].data = data.temperatura;
            this.charts.temperature.update();
        }

        if (this.charts.current) {
            this.charts.current.data.labels = data.labels;
            this.charts.current.data.datasets[0].data = data.corrente;
            this.charts.current.update();
        }
    }
}

/**
 * Gerenciador de Filtros
 */
class FilterManager {
    constructor() {
        this.filterForm = document.getElementById('filter-form');
        this.init();
    }

    init() {
        if (this.filterForm) {
            this.filterForm.addEventListener('submit', (e) => this.handleFilterSubmit(e));
        }
    }

    handleFilterSubmit(e) {
        e.preventDefault();
        
        // Coleta dados dos filtros
        const formData = new FormData(this.filterForm);
        const params = new URLSearchParams(formData);

        // Redireciona com os parâmetros
        window.location.href = `?${params.toString()}`;
    }

    /**
     * Limpa todos os filtros
     */
    clearFilters() {
        if (this.filterForm) {
            this.filterForm.reset();
            window.location.href = window.location.pathname;
        }
    }
}

/**
 * Utilitários gerais
 */
class Utils {
    /**
     * Formata data para brasileiro
     */
    static formatDate(dateString) {
        const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
        return new Date(dateString).toLocaleDateString('pt-BR', options);
    }

    /**
     * Formata número com separadores
     */
    static formatNumber(num, decimals = 2) {
        return num.toLocaleString('pt-BR', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
    }

    /**
     * Mostra notificação temporária
     */
    static showNotification(message, type = 'info', duration = 3000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
        `;

        const container = document.querySelector('.container-fluid') || document.body;
        container.insertBefore(alertDiv, container.firstChild);

        if (duration > 0) {
            setTimeout(() => alertDiv.remove(), duration);
        }
    }

    /**
     * Valida email
     */
    static validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    /**
     * Copia texto para clipboard
     */
    static copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            Utils.showNotification('Texto copiado!', 'success', 2000);
        }).catch(err => {
            console.error('Erro ao copiar:', err);
        });
    }
}

/**
 * Inicialização na carga do DOM
 */
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa o gerenciador de temas
    new ThemeManager();

    // Inicializa gráficos
    new ChartManager();

    // Inicializa filtros
    new FilterManager();

    // Oculta alertas após 5 segundos
    document.querySelectorAll('.alert:not(.alert-permanent)').forEach(alert => {
        setTimeout(() => {
            new window.bootstrap.Alert(alert).close();
        }, 5000);
    });

    console.log('Dashboard inicializado com sucesso!');
});

/**
 * Exportações para uso global
 */
window.Dashboard = {
    Theme: ThemeManager,
    Charts: ChartManager,
    Filters: FilterManager,
    Utils: Utils
};

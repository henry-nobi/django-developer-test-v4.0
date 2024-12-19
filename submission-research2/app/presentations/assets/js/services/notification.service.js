class NotificationService {
    constructor() {
        this.defaultConfig = {
            position: 'top-right',
            duration: 3000,
            closable: true,
            animation: true,
            stack: true,
            maxStack: 3,
            pauseOnHover: true,
            theme: 'light'
        };

        this.queue = [];
        this.activeToasts = [];
        this.container = this.createContainer();
    }

    createContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3 z-50';
        container.setAttribute('role', 'alert');
        container.setAttribute('aria-live', 'polite');
        container.setAttribute('aria-atomic', 'true');
        document.body.appendChild(container);
        return container;
    }

    createToast(message, type, customConfig = {}) {
        const config = { ...this.defaultConfig, ...customConfig };
        const toast = document.createElement('div');
        toast.className = `toast toast-${type} fade`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        const header = document.createElement('div');
        header.className = 'toast-header';
        
        const logo = document.createElement('img');
        logo.src = '/assets/images/logo-sm.png';
        logo.className = 'rounded me-2';
        logo.height = 16;
        logo.alt = 'toast header';
        
        const title = document.createElement('strong');
        title.className = 'me-auto';
        title.textContent = this.getTitleByType(type);

        const timeSpan = document.createElement('small');
        timeSpan.className = 'text-body-secondary';
        timeSpan.textContent = '';

        const body = document.createElement('div');
        body.className = 'toast-body';
        body.textContent = message;
        
        header.appendChild(logo);
        header.appendChild(title);
        header.appendChild(timeSpan);

        if (config.closable) {
            const closeBtn = document.createElement('button');
            closeBtn.className = 'btn-close';
            closeBtn.setAttribute('data-bs-dismiss', 'toast');
            closeBtn.setAttribute('aria-label', 'Close');
            closeBtn.onclick = () => this.removeToast(toast);
            header.appendChild(closeBtn);
        }

        toast.appendChild(header);
        toast.appendChild(body);

        return toast;
    }

    show(message, type, customConfig = {}) {
        const toast = this.createToast(message, type, customConfig);
        
        if (this.defaultConfig.stack) {
            if (this.activeToasts.length >= this.defaultConfig.maxStack) {
                this.queue.push({ toast, type, message, customConfig });
                return;
            }
            this.activeToasts.push(toast);
        }

        this.container.appendChild(toast);
        toast.classList.add('show');

        if (this.defaultConfig.duration) {
            setTimeout(() => {
                this.removeToast(toast);
            }, this.defaultConfig.duration);
        }
    }

    removeToast(toast) {
        toast.classList.remove('show');
        setTimeout(() => {
            this.container.removeChild(toast);
            const index = this.activeToasts.indexOf(toast);
            if (index > -1) {
                this.activeToasts.splice(index, 1);
                if (this.queue.length > 0) {
                    const next = this.queue.shift();
                    this.show(next.message, next.type, next.customConfig);
                }
            }
        }, 300);
    }

    success(message, config = {}) {
        this.show(message, 'success', config);
    }

    error(message, config = {}) {
        this.show(message, 'error', config);
    }

    warning(message, config = {}) {
        this.show(message, 'warning', config);
    }

    info(message, config = {}) {
        this.show(message, 'info', config);
    }

    getIconClass(type) {
        const icons = {
            success: 'bi bi-check-circle-fill text-success',
            error: 'bi bi-x-circle-fill text-danger',
            warning: 'bi bi-exclamation-triangle-fill text-warning',
            info: 'bi bi-info-circle-fill text-info'
        };
        return icons[type] || icons.info;
    }

    getTitleByType(type) {
        const titles = {
            success: 'Success',
            error: 'Error',
            warning: 'Warning',
            info: 'Information'
        };
        return titles[type] || titles.info;
    }

    configure(config) {
        this.defaultConfig = { ...this.defaultConfig, ...config };
    }
}

// Export for use in other files
window.AppNotification = new NotificationService();

/* Usage Examples:

// Basic usage
AppNotification.success('Operation completed successfully');
AppNotification.error('An error occurred');
AppNotification.warning('Please review your input');
AppNotification.info('System is updating');

// With custom configuration
AppNotification.success('Custom notification', {
    position: 'bottom-right',
    duration: 3000,
    theme: 'dark'
});

// Global configuration
AppNotification.configure({
    position: 'top-center',
    duration: 4000,
    maxStack: 5
});

*/

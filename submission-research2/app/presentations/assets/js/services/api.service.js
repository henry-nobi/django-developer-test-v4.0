class ApiService {
    static BASE_URL = '/api/v1';
    static currentProfileId = null;

    static async request(endpoint, options = {}) {
        try {
            const defaultHeaders = {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken(),
            };

            // Add Authorization header if token exists
            const token = localStorage.getItem('authToken');
            if (token) {
                defaultHeaders['Authorization'] = `Token ${token}`;
            }

            // Add current profile ID header
            if (this.currentProfileId) {
                defaultHeaders['X-Profile-Id'] = this.currentProfileId;
            }

            const response = await fetch(`${this.BASE_URL}${endpoint}`, {
                ...options,
                headers: {
                    ...defaultHeaders,
                    ...options.headers,
                },
                credentials: 'include',
            });

            if (!response.ok) {
                if (response?.status === 401 && endpoint !== '/auth/login/') {
                    // Token is invalid, redirect to login
                    window.location.href = '/auth-login';
                    return null;
                }
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Auth endpoints
    static async login(email, password) {
        const response = await this.request('/auth/login/', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        return response;
    }


    static async resetPassword(email) {
        return this.request('/auth/reset-password/', {
            method: 'POST',
            body: JSON.stringify({ email })
        });
    }

    static async resetPasswordConfirm(uid, token, password) {
        return this.request('/auth/reset-password-confirm/', {
            method: 'POST',
            body: JSON.stringify({ uid, token, new_password: password })
        });
    }

    // User endpoints
    static async getCurrentUser() {
        return this.request('/user/me/');
    }

    static async updateUser(userId, data) {
        return this.request(`/user/${userId}/update/`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    // Profile endpoints
    static async getProfile(profileId) {
        return this.request(`/user-profile/${profileId}/`);
    }

    static async updateProfile(profileId, data) {
        return this.request(`/user-profile/${profileId}/`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    // Helper methods
    static getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    static async changePassword(currentPassword, newPassword) {
        return this.request('/user/change-password/', {
            method: 'POST',
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword
            })
        });

    }

    static async getUserProfiles() {
        return this.request('/user/profiles/');
    }

    static async switchProfile(profileId) {
        this.currentProfileId = profileId;
        localStorage.setItem('currentProfileId', profileId);
        // Reload the page to update the UI
        window.location.reload();
    }

    // Add method to initialize the current profile ID
    static initializeProfile() {
        this.currentProfileId = localStorage.getItem('currentProfileId');
    }
}

// Initialize the current profile ID when the API service is loaded
ApiService.initializeProfile();

// Export for use in other files
window.ApiService = ApiService; 
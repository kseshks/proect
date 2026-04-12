const API_URL = "http://127.0.0.1:8000";

function getToken() {
    return localStorage.getItem("access_token");
}

function setToken(token) {
    localStorage.setItem("access_token", token);
}

function getUserType() {
    return localStorage.getItem("user_type");
}

function setUserType(userType) {
    localStorage.setItem("user_type", userType);
}

function clearAuth() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_type");
}

async function apiRequest(path, options = {}) {
    const headers = {
        ...(options.headers || {})
    };

    const token = getToken();

    if (!(options.body instanceof FormData)) {
        headers["Content-Type"] = "application/json";
    }

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}${path}`, {
        ...options,
        headers
    });

    if (!response.ok) {
        let errorMessage = "Ошибка запроса";

        try {
            const errorData = await response.json();
            errorMessage = errorData.detail || errorMessage;
        } catch (e) {}

        throw new Error(errorMessage);
    }

    const contentType = response.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
        return response.json();
    }

    return null;
}
async function login(identifier, password) {
    const data = await apiRequest("/auth/login", {
        method: "POST",
        body: JSON.stringify({
            username: identifier,
            password: password
        })
    });

    setToken(data.access_token);
    setUserType(data.user_type);

    return data;
}

function logout() {
    clearAuth();
    window.location.href = "../index.html";
}
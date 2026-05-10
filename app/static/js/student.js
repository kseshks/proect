async function loadStudentTopics() {
    return apiRequest("/student/topics");
}

async function loadStudentTopic(topicId) {
    return apiRequest(`/student/topics/${topicId}`);
}

async function loadStudentDialog(topicId) {
    return apiRequest(`/student/topics/${topicId}/dialog`);
}

async function askStudentQuestion(topicId, questionId) {
    return apiRequest(`/student/topics/${topicId}/ask`, {
        method: "POST",
        body: JSON.stringify({
            question_id: questionId
        })
    });
}

function setSelectedTopic(topicId) {
    localStorage.setItem("selected_topic_id", String(topicId));
}

function getSelectedTopic() {
    return localStorage.getItem("selected_topic_id");
}

async function askCustomQuestion(topicId, questionText) {
    return apiRequest(`/student/topics/${topicId}/ask/custom`, {
        method: "POST",
        body: JSON.stringify({ question_text: questionText })
    });
}

async function loadStudentTopics() {
    return apiRequest("/student/topics");
}

// Получение конкретной темы
async function loadStudentTopic(topicId) {
    return apiRequest(`/student/topics/${topicId}`);
}

// Получение диалога по теме
async function loadStudentDialog(topicId) {
    return apiRequest(`/student/topics/${topicId}/dialog`);
}

// Задать вопрос по теме
async function askStudentQuestion(topicId, questionId) {
    return apiRequest(`/student/topics/${topicId}/ask`, {
        method: "POST",
        body: JSON.stringify({
            question_id: questionId
        })
    });
}

// Задать свой вопрос по теме
async function askCustomQuestion(topicId, questionText) {
    return apiRequest(`/student/topics/${topicId}/ask/custom`, {
        method: "POST",
        body: JSON.stringify({ question_text: questionText })
    });
}

// ===== НОВЫЕ ФУНКЦИИ =====

// Получение разделов, назначенных ученику (целиком)
async function loadStudentSections() {
    return apiRequest("/student/sections");
}

// Получение всех тем раздела (для отображения в развернутом разделе)
async function loadSectionTopics(sectionId) {
    return apiRequest(`/student/sections/${sectionId}/topics`);
}

// ==================== РАБОТА С ВЫБРАННОЙ ТЕМОЙ ====================

function setSelectedTopic(topicId) {
    localStorage.setItem("selected_topic_id", String(topicId));
}

function getSelectedTopic() {
    return localStorage.getItem("selected_topic_id");
}
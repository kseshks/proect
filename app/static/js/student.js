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

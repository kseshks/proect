async function loadTeacherClasses() {
    return apiRequest("/teacher/classes");
}

async function loadTeacherClassStudents(classId) {
    return apiRequest(`/teacher/classes/${classId}/students`);
}

async function createTeacherClass(name) {
    return apiRequest("/teacher/classes", {
        method: "POST",
        body: JSON.stringify({ name })
    });
}

async function deleteTeacherClass(classId) {
    return apiRequest(`/teacher/classes/${classId}`, {
        method: "DELETE"
    });
}

async function generateTeacherStudents(classId, count) {
    return apiRequest(`/teacher/classes/${classId}/students/generate`, {
        method: "POST",
        body: JSON.stringify({ count })
    });
}

async function deleteTeacherStudent(studentId) {
    return apiRequest(`/teacher/students/${studentId}`, {
        method: "DELETE"
    });
}

async function loadTeacherTopics() {
    return apiRequest("/teacher/topics");
}

async function loadTeacherTopic(topicId) {
    return apiRequest(`/teacher/topics/${topicId}`);
}

async function createTeacherTopic(title, description = null) {
    return apiRequest("/teacher/topics", {
        method: "POST",
        body: JSON.stringify({
            title,
            description
        })
    });
}

async function deleteTeacherTopic(topicId) {
    return apiRequest(`/teacher/topics/${topicId}`, {
        method: "DELETE"
    });
}

async function loadTeacherTopicQuestions(topicId) {
    return apiRequest(`/teacher/topics/${topicId}/questions`);
}

async function addTeacherTopicQuestions(topicId, questions) {
    return apiRequest(`/teacher/topics/${topicId}/questions`, {
        method: "POST",
        body: JSON.stringify({
            questions
        })
    });
}

async function assignTeacherTopic(topicId, classIds = [], studentNumbers = []) {
    return apiRequest(`/teacher/topics/${topicId}/assign`, {
        method: "POST",
        body: JSON.stringify({
            class_ids: classIds,
            student_numbers: studentNumbers
        })
    });
}

async function uploadTeacherTopicFile(topicId, file) {
    const formData = new FormData();
    formData.append("file", file);

    return apiRequest(`/teacher/topics/${topicId}/materials/file`, {
        method: "POST",
        body: formData
    });
}

async function addTeacherTopicLink(topicId, title, url) {
    return apiRequest(`/teacher/topics/${topicId}/materials/link`, {
        method: "POST",
        body: JSON.stringify({
            title,
            url
        })
    });
}

async function loadTeacherRatings() {
    return apiRequest("/teacher/ratings/students");
}

async function loadTeacherRatingsByClass(classId) {
    return apiRequest(`/teacher/ratings/students/${classId}`);
}

async function loadTeacherOverallRatings() {
    return apiRequest("/teacher/ratings/overall");
}

// Загрузка материалов темы
async function loadTeacherTopicMaterials(topicId) {
    return apiRequest(`/teacher/topics/${topicId}/materials`);
}

// Удаление материала
async function deleteTeacherMaterial(materialId) {
    return apiRequest(`/teacher/materials/${materialId}`, {
        method: "DELETE"
    });
}

// Удаление вопроса
async function deleteTeacherQuestion(questionId) {
    return apiRequest(`/teacher/questions/${questionId}`, {
        method: "DELETE"
    });
}

async function loadTopicAssignments(topicId) {
    return apiRequest(`/teacher/topics/${topicId}/assignments`);
}

// Разделы
async function loadTeacherSections() {
    return apiRequest("/teacher/sections");
}
async function createTeacherSection(title, description) {
    return apiRequest("/teacher/sections", { method: "POST", body: JSON.stringify({ title, description }) });
}
async function loadSectionTopics(sectionId) {
    return apiRequest(`/teacher/sections/${sectionId}/topics`);
}
async function createTopicInSection(sectionId, title, description) {
    return apiRequest(`/teacher/sections/${sectionId}/topics`, { method: "POST", body: JSON.stringify({ title, description }) });
}
async function assignSection(sectionId, classIds, studentNumbers) {
    return apiRequest(`/teacher/sections/${sectionId}/assign`, { method: "POST", body: JSON.stringify({ class_ids: classIds, student_numbers: studentNumbers }) });
}
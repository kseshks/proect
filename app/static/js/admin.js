async function loadAdminTeachers() {
    return apiRequest("/admin/teachers");
}

async function generateAdminTeachers(count) {
    return apiRequest("/admin/teachers/generate", {
        method: "POST",
        body: JSON.stringify({ count })
    });
}

async function deleteAdminTeacher(teacherId) {
    return apiRequest(`/admin/teachers/${teacherId}`, {
        method: "DELETE"
    });
}

async function loadAdminClasses() {
    return apiRequest("/admin/classes");
}

async function createAdminClass(name, teacherId = null) {
    return apiRequest("/admin/classes", {
        method: "POST",
        body: JSON.stringify({
            name,
            teacher_id: teacherId
        })
    });
}

async function loadAdminClass(classId) {
    return apiRequest(`/admin/classes/${classId}`);
}

async function deleteAdminClass(classId) {
    return apiRequest(`/admin/classes/${classId}`, {
        method: "DELETE"
    });
}

async function loadAdminClassStudents(classId) {
    return apiRequest(`/admin/classes/${classId}/students`);
}

async function loadAdminStudents() {
    return apiRequest("/admin/students");
}

async function generateAdminStudents(className, count) {
    return apiRequest("/admin/students/generate", {
        method: "POST",
        body: JSON.stringify({
            class_name: className,
            count
        })
    });
}

async function deleteAdminStudent(studentId) {
    return apiRequest(`/admin/students/${studentId}`, {
        method: "DELETE"
    });
}
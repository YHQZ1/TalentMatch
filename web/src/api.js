const BASE_URL = "http://127.0.0.1:8000/api/v1";

/**
 * Scan resumes using TalentMatch backend
 */
export async function scanResumes({ jobDescription, files, priorities }) {
  const formData = new FormData();

  // Required
  formData.append("job_description", jobDescription);

  // Optional priorities (must match backend names exactly)
  formData.append("skills_priority", priorities.skills);
  formData.append("experience_priority", priorities.experience);
  formData.append("education_priority", priorities.education);
  formData.append("relevance_priority", priorities.relevance);

  // Files
  files.forEach((file) => {
    formData.append("files", file);
  });

  const res = await fetch("http://127.0.0.1:8000/api/v1/scan/pdf", {
    method: "POST",
    body: formData, // IMPORTANT: no headers
  });

  if (!res.ok) {
    const err = await res.json();
    throw err;
  }

  return res.json();
}

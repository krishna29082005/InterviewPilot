const BASE_URL = "http://127.0.0.1:8000";

/* ===========================
   Authentication
=========================== */

export interface SignupData {
  name: string;
  email: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
}

export async function signupUser(data: SignupData) {
  const response = await fetch(`${BASE_URL}/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.detail || "Signup failed.");
  }

  return result;
}

export async function loginUser(
  data: LoginData
): Promise<LoginResponse> {
  const formData = new URLSearchParams();

  formData.append("username", data.email);
  formData.append("password", data.password);

  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  });

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.detail || "Login failed.");
  }

  return result;
}

export async function getCurrentUser(
  token: string
): Promise<User> {
  const response = await fetch(`${BASE_URL}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.detail || "Failed to fetch user.");
  }

  return result;
}

/* ===========================
   Resume
=========================== */

export interface ResumeInfo {
  filename: string;
  size: number;
  uploaded_at: string;
  analysis?: any;
}

export async function uploadResume(
  file: File,
  token: string
) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${BASE_URL}/resume/upload`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    }
  );

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.detail || "Upload failed.");
  }

  return result;
}

export async function getResumeInfo(
  token: string
): Promise<ResumeInfo> {
  const response = await fetch(
    `${BASE_URL}/resume/info`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.detail || "Failed to fetch resume.");
  }

  return result;
}

export async function deleteResume(
  token: string
) {
  const response = await fetch(
    `${BASE_URL}/resume/delete`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.detail || "Failed to delete resume.");
  }

  return result;
}

export async function downloadResume(
  token: string
) {
  const response = await fetch(
    `${BASE_URL}/resume/download`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error("Download failed.");
  }

  const blob = await response.blob();

  const url = window.URL.createObjectURL(blob);

  const link = document.createElement("a");

  link.href = url;
  link.download = "Resume.pdf";

  document.body.appendChild(link);

  link.click();

  link.remove();

  window.URL.revokeObjectURL(url);
}

export async function analyzeJobMatch(
  jobDescription: string,
  token: string
): Promise<JobMatchAnalysis> {
  const response = await fetch(`${BASE_URL}/job-match/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      job_description: jobDescription,
    }),
  });

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.detail || "Failed to analyze job match.");
  }

  return result;
}

/* ===========================
   ATS Analysis
=========================== */
export interface RecommendedRole {
  role: string;
  match_level: "High" | "Medium" | "Low" | string;
  reasons: string[];
}

export interface ATSAnalysis {
  ats_score: number;
  summary: string;
  strengths: string[];
  weaknesses: string[];
  missing_keywords: string[];
  formatting_issues: string[];
  recommendations?: string[];
  improvement_suggestions?: string[];
  recommended_roles: RecommendedRole[];
}

export async function getATSAnalysis(
  token: string
): Promise<ATSAnalysis> {
  const response = await fetch(
    `${BASE_URL}/ats/analysis`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const result = await response.json();

  if (!response.ok) {
    throw new Error(
      result.detail || "Failed to fetch ATS analysis."
    );
  }

  return result;
}


export interface JobMatchAnalysis {
  match_score: number;
  summary: string;
  matching_skills: string[];
  missing_skills: string[];
  matching_keywords: string[];
  missing_keywords: string[];
  strengths: string[];
  gaps: string[];
  recommendations: string[];
}

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
  analysis: any;
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

/**
 * Download resume.
 *
 * NOTE:
 * Since your backend expects JWT in the Authorization header,
 * this function will be updated later to use fetch + blob.
 */
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
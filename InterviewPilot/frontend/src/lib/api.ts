const BASE_URL = "http://127.0.0.1:8000";

export interface SignupData {
  name: string;
  email: string;
  password: string;
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

export interface LoginData {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
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

export interface User {
  id: number;
  username: string;
  email: string;
}

export async function getCurrentUser(
  token: string
): Promise<User> {
  const response = await fetch(`${BASE_URL}/auth/me`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  console.log("Status:", response.status);

  const result = await response.json();
  console.log("Response:", result);

  if (!response.ok) {
    throw new Error(result.detail || "Failed to fetch user.");
  }

  return result;
}
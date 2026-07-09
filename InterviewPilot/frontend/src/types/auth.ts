export interface User {
  id: number;
  name?: string;
  email: string;
}

export interface AuthResponse {
  user?: User;
  token?: string;
  error?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface SignupData {
  name?: string;
  email: string;
  password: string;
}

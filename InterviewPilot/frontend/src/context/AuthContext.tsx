"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { User, getCurrentUser } from "@/lib/api";

interface AuthContextType {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  login: (token: string, user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

export function AuthProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  // Restore token when the app starts
useEffect(() => {
  async function initializeAuth() {
    const storedToken = localStorage.getItem("access_token");

    if (!storedToken) {
      setIsLoading(false);
      return;
    }

    try {
      setToken(storedToken);

      const currentUser = await getCurrentUser(storedToken);

      setUser(currentUser);
    } catch {
      localStorage.removeItem("access_token");
      setToken(null);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }

  initializeAuth();
}, []);

  const login = (
  newToken: string,
  currentUser: User
) => {
  localStorage.setItem("access_token", newToken);

  setToken(newToken);
  setUser(currentUser);
};

  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
      token,
      user,
      isAuthenticated: !!token,
      isLoading,
      login,
      logout,
  }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used inside an AuthProvider."
    );
  }

  return context;
}
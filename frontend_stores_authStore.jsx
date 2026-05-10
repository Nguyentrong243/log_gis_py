// React: Auth Store (Zustand)
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: (user, token) => {
        set({ user, token, isAuthenticated: true });
        localStorage.setItem('auth_token', token);
      },

      logout: () => {
        set({ user: null, token: null, isAuthenticated: false });
        localStorage.removeItem('auth_token');
      },

      setUser: (user) => set({ user }),

      getToken: () => localStorage.getItem('auth_token'),

      isAdmin: () => {
        const { user } = useAuthStore.getState();
        return user?.role === 'super_admin';
      },

      isWarehouseAdmin: () => {
        const { user } = useAuthStore.getState();
        return user?.role === 'warehouse_admin';
      }
    }),
    {
      name: 'auth-storage'
    }
  )
);

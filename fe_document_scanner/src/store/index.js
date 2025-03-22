import { create } from 'zustand';

export const useLoading = create((set) => ({
  loading: false,
  setLoading: (status) => set({ loading: status }),
}));

export const useShowUpload = create((set) => ({
    isShow: false,
    setIsShow: (status) => set({ isShow: status }),
  }));


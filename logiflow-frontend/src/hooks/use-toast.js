// src/hooks/use-toast.js
import { toast } from 'sonner';

// Named export
export const useToast = () => {
  return toast;
};

// Default export da ekleyelim
export default useToast;

// Ayrıca toast'u da export et (gerekirse)
export { toast };

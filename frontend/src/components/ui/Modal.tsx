import { useEffect, useRef, type ReactNode } from 'react';
import { X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

export function Modal({
  isOpen,
  onClose,
  title,
  children,
  className = '',
  size = 'md',
}: ModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (isOpen) dialog.showModal();
    else dialog.close();
  }, [isOpen]);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    const handleClose = () => onClose();
    dialog.addEventListener('close', handleClose);
    return () => dialog.removeEventListener('close', handleClose);
  }, [onClose]);

  const sizes: Record<string, string> = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <dialog
          ref={dialogRef}
          className={`${sizes[size]} w-full border-0 bg-transparent p-0 text-text-primary backdrop:bg-black/50 backdrop:backdrop-blur-sm ${className}`}
          onClick={(e) => {
            if (e.target === dialogRef.current) onClose();
          }}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.96, y: 8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: 8 }}
            transition={{ duration: 0.2 }}
            className="rounded-2xl border border-border bg-surface p-6 shadow-lg"
          >
            {title && (
              <div className="mb-4 flex items-center justify-between">
                <h3 className="font-display text-lg font-semibold">{title}</h3>
                <button
                  onClick={onClose}
                  className="rounded-lg p-1.5 text-text-secondary transition-colors hover:bg-border hover:text-text-primary"
                  aria-label="Close"
                >
                  <X size={16} />
                </button>
              </div>
            )}
            {children}
          </motion.div>
        </dialog>
      )}
    </AnimatePresence>
  );
}

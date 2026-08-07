import { getInitials, avatarHue } from '../../utils/candidateUtils';

interface AvatarProps {
  name: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  src?: string;
  className?: string;
}

export function Avatar({ name, size = 'md', src, className = '' }: AvatarProps) {
  const sizes: Record<string, string> = {
    sm: 'h-8 w-8 text-xs',
    md: 'h-10 w-10 text-sm',
    lg: 'h-14 w-14 text-base',
    xl: 'h-20 w-20 text-xl',
  };

  const hue = avatarHue(name);

  if (src) {
    return (
      <img
        src={src}
        alt={name}
        className={`rounded-full object-cover ${sizes[size]} ${className}`}
      />
    );
  }

  return (
    <div
      className={`flex shrink-0 items-center justify-center rounded-full font-display font-semibold text-white ${sizes[size]} ${className}`}
      style={{
        background: `linear-gradient(135deg, hsl(${hue} 45% 42%), hsl(${(hue + 40) % 360} 50% 32%))`,
      }}
      aria-hidden
    >
      {getInitials(name)}
    </div>
  );
}

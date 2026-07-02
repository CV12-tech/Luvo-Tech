interface WordmarkProps {
  className?: string;
}

/**
 * Text-based placeholder wordmark. Swap for a real logo asset by replacing
 * this component's markup — the surrounding layout does not depend on it
 * being text.
 */
export default function Wordmark({ className = "" }: WordmarkProps) {
  return (
    <span
      className={`font-display text-xl font-semibold tracking-tight text-text-primary ${className}`}
    >
      LuVo{" "}
      <span className="text-accent-cyan text-glow">Tech</span>
    </span>
  );
}

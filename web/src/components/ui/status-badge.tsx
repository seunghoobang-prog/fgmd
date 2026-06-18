import { APPLICATION_STATUS } from "@/lib/constants";
import { cn } from "@/lib/utils";

export function StatusBadge({ status }: { status: keyof typeof APPLICATION_STATUS }) {
  const config = APPLICATION_STATUS[status];
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium",
        config.color,
      )}
    >
      {config.label}
    </span>
  );
}
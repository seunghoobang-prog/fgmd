export const REGIONS = ["서울", "오산", "전라", "경상", "충청"] as const;

export type Region = (typeof REGIONS)[number];

export const APPLICATION_STATUS = {
  pending: { label: "대기", color: "bg-amber-100 text-amber-800 border-amber-200" },
  approved: { label: "승인", color: "bg-emerald-100 text-emerald-800 border-emerald-200" },
  rejected: { label: "반려", color: "bg-red-100 text-red-800 border-red-200" },
} as const;

export type ApplicationStatus = keyof typeof APPLICATION_STATUS;
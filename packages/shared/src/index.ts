export const providerIds = ["mit_ocw", "open_yale"] as const;
export type ProviderId = (typeof providerIds)[number];

export const courseModes = ["full_learn", "assisted", "reference_only", "unsupported"] as const;
export type CourseMode = (typeof courseModes)[number];

export const jobStatuses = ["queued", "running", "paused", "completed", "failed", "cancelled", "retrying"] as const;
export type JobStatus = (typeof jobStatuses)[number];

export interface LicenseInfo {
  code?: string | null;
  name?: string | null;
  url?: string | null;
  attribution_required: boolean;
  noncommercial: boolean;
  sharealike: boolean;
  third_party_exceptions_possible: boolean;
  notes?: string | null;
}

export interface RawCourseRecord {
  provider_id: ProviderId | string;
  provider_course_id: string;
  canonical_url: string;
  title: string;
  course_number?: string | null;
  department?: string | null;
  instructors: string[];
  term?: string | null;
  level?: string | null;
  description?: string | null;
  topics: string[];
  license: LicenseInfo;
  raw_metadata: Record<string, unknown>;
}

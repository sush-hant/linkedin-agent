export type PostDraft = {
  draft_id: string;
  topic_id: string;
  style: string;
  content: string;
  hashtags: string[];
  citations: string[];
};

export type ImageDraft = {
  image_id: string;
  draft_id: string;
  prompt: string;
  file_path: string;
  size: string;
};

const API = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
const API_KEY = process.env.NEXT_PUBLIC_AGENT_API_KEY ?? "dev-key";

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      "x-api-key": API_KEY,
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`API ${path} failed: ${res.status}`);
  return res.json() as Promise<T>;
}

export const api = {
  runPipeline: () => req<{ status: string }>("/pipeline/run", { method: "POST" }),
  listDrafts: () => req<PostDraft[]>("/review/drafts"),
  listImages: () => req<ImageDraft[]>("/review/images"),
  approveDraft: (draft_id: string, edited_content: string) =>
    req<{ published_id: string }>("/review/approve", {
      method: "POST",
      body: JSON.stringify({ draft_id, edited_content }),
    }),
  recordFeedback: (payload: {
    published_id: string;
    impressions: number;
    comments: number;
    reposts: number;
    saves: number;
    quality: "poor" | "average" | "good";
    notes: string;
    recorded_at: string;
  }) => req<{ status: string }>("/feedback/record", { method: "POST", body: JSON.stringify(payload) }),
};

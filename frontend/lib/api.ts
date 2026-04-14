const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    next: { revalidate: 300 },
    ...options,
  });
  if (!res.ok) throw new Error(`API error ${res.status}: ${path}`);
  return res.json();
}

export interface Concept {
  id: number;
  term: string;
  definition: string | null;
}

export interface ConceptMention {
  episodeID: string;
  title: string;
  publishedAt: string | null;
  thumbnail: string | null;
  timestamp: number | null;
}

export interface ConceptDetail extends Concept {
  mentions: ConceptMention[];
}

export interface Profile {
  id: number;
  name: string;
  type: "person" | "club" | "organisation" | "body";
  description: string | null;
}

export interface ProfileMention {
  episodeID: string;
  title: string;
  publishedAt: string | null;
  thumbnail: string | null;
  timestamp: number | null;
}

export interface ProfileDetail extends Profile {
  mentions: ProfileMention[];
}

export interface Episode {
  youtubeID: string;
  title: string;
  publishedAt: string | null;
  duration: string | null;
  thumbnail: string | null;
  description: string | null;
}

export function formatTimestamp(seconds: number | null): string {
  if (seconds === null || seconds === undefined) return "";
  const s = Math.floor(seconds);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

export function youtubeURL(youtubeID: string, timestamp?: number | null): string {
  const base = `https://www.youtube.com/watch?v=${youtubeID}`;
  return timestamp ? `${base}&t=${Math.floor(timestamp)}s` : base;
}

export const api = {
  concepts: {
    list: (params?: { search?: string; page?: number; limit?: number }) => {
      const q = new URLSearchParams();
      if (params?.search) q.set("search", params.search);
      if (params?.page) q.set("page", String(params.page));
      if (params?.limit) q.set("limit", String(params.limit));
      return apiFetch<{ total: number; page: number; limit: number; concepts: Concept[] }>(
        `/api/concepts?${q}`
      );
    },
    get: (id: number) => apiFetch<ConceptDetail>(`/api/concepts/${id}`),
  },
  profiles: {
    list: (params?: { search?: string; type?: string; page?: number; limit?: number }) => {
      const q = new URLSearchParams();
      if (params?.search) q.set("search", params.search);
      if (params?.type) q.set("type", params.type);
      if (params?.page) q.set("page", String(params.page));
      if (params?.limit) q.set("limit", String(params.limit));
      return apiFetch<{ total: number; page: number; limit: number; profiles: Profile[] }>(
        `/api/profiles?${q}`
      );
    },
    get: (id: number) => apiFetch<ProfileDetail>(`/api/profiles/${id}`),
  },
  episodes: {
    list: (params?: { page?: number; limit?: number }) => {
      const q = new URLSearchParams();
      if (params?.page) q.set("page", String(params.page));
      if (params?.limit) q.set("limit", String(params.limit));
      return apiFetch<{ total: number; page: number; limit: number; episodes: Episode[] }>(
        `/api/episodes?${q}`
      );
    },
  },
};

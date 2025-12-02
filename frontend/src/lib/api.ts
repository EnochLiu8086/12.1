import type {
  GuardResult,
  ModerationRequest,
  PipelineRequest,
  PipelineResponse,
} from "../types/models";

// 前端与后端通常部署在同一域名下，直接使用相对路径即可。
// 如需自定义网关地址，可以在此处改为从全局变量读取。
const API_BASE_URL = "";

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      // 尝试从后端读取更详细的错误信息
      const data = (await response.json()) as { detail?: unknown };
      if (data?.detail) {
        message = typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail);
      }
    } catch {
      // ignore JSON parse errors, keep default message
    }
    throw new Error(message);
  }

  return (await response.json()) as T;
}

export async function runPipeline(
  payload: PipelineRequest,
): Promise<PipelineResponse> {
  const response = await fetch(`${API_BASE_URL}/api/pipeline/run`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  return handleResponse<PipelineResponse>(response);
}

export async function moderateOnly(
  payload: ModerationRequest,
): Promise<GuardResult> {
  const response = await fetch(`${API_BASE_URL}/api/moderate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  return handleResponse<GuardResult>(response);
}



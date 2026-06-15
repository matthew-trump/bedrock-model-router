import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { App } from "./App";

const modelsResponse = {
  models: [
    {
      key: "nova-lite",
      model_id: "amazon.nova-lite-v1:0",
      label: "Amazon Nova Lite",
      provider: "Amazon",
    },
    {
      key: "claude-haiku",
      model_id: "anthropic.claude-3-5-haiku-20241022-v1:0",
      label: "Claude 3.5 Haiku",
      provider: "Anthropic",
    },
  ],
};

function jsonResponse(body: unknown, init: ResponseInit = {}) {
  return new Response(JSON.stringify(body), {
    status: init.status ?? 200,
    headers: { "Content-Type": "application/json", ...init.headers },
  });
}

beforeEach(() => {
  vi.stubGlobal("fetch", vi.fn());
});

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("App", () => {
  it("loads and displays the model selector options", async () => {
    vi.mocked(fetch).mockResolvedValueOnce(jsonResponse(modelsResponse));

    render(<App />);

    expect(await screen.findByRole("option", { name: "Amazon Nova Lite (Amazon)" })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "Claude 3.5 Haiku (Anthropic)" })).toBeInTheDocument();
    expect(fetch).toHaveBeenCalledWith("http://127.0.0.1:18000/api/models");
  });

  it("submits a prompt and renders the model response", async () => {
    let resolveChat: (response: Response) => void;
    const chatResponse = new Promise<Response>((resolve) => {
      resolveChat = resolve;
    });

    vi.mocked(fetch)
      .mockResolvedValueOnce(jsonResponse(modelsResponse))
      .mockReturnValueOnce(chatResponse);

    render(<App />);

    await screen.findByRole("option", { name: "Amazon Nova Lite (Amazon)" });
    await userEvent.selectOptions(screen.getByLabelText("Model"), "claude-haiku");
    await userEvent.type(screen.getByPlaceholderText("Ask a model..."), "hello");
    await userEvent.click(screen.getByRole("button", { name: "Send" }));

    expect(await screen.findByRole("button", { name: "Sending..." })).toBeDisabled();

    resolveChat!(
      jsonResponse({
        model_key: "claude-haiku",
        model_id: "anthropic.claude-3-5-haiku-20241022-v1:0",
        message: "Stub Bedrock response",
      }),
    );

    expect(await screen.findByText("Stub Bedrock response")).toBeInTheDocument();

    expect(fetch).toHaveBeenLastCalledWith("http://127.0.0.1:18000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model_key: "claude-haiku", message: "hello" }),
    });
  });

  it("disables send when the prompt is blank", async () => {
    vi.mocked(fetch).mockResolvedValueOnce(jsonResponse(modelsResponse));

    render(<App />);

    expect(await screen.findByRole("button", { name: "Send" })).toBeDisabled();
  });

  it("renders an error when model loading fails", async () => {
    vi.mocked(fetch).mockResolvedValueOnce(jsonResponse({ detail: "failed" }, { status: 500 }));

    render(<App />);

    expect(await screen.findByText("Model request failed with 500")).toBeInTheDocument();
  });

  it("renders an error when chat submission fails", async () => {
    vi.mocked(fetch)
      .mockResolvedValueOnce(jsonResponse(modelsResponse))
      .mockResolvedValueOnce(jsonResponse({ detail: "Unsupported model_key" }, { status: 400 }));

    render(<App />);

    await screen.findByRole("option", { name: "Amazon Nova Lite (Amazon)" });
    await userEvent.type(screen.getByPlaceholderText("Ask a model..."), "hello");
    await userEvent.click(screen.getByRole("button", { name: "Send" }));

    expect(await screen.findByText("Unsupported model_key")).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Send" })).toBeEnabled();
    });
  });
});

import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

import { API_BASE_URL } from "./api";

type ModelInfo = {
  key: string;
  model_id: string;
  label: string;
  provider: string;
};

function App() {
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [selectedModel, setSelectedModel] = useState("nova-lite");
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function loadModels() {
      try {
        const res = await fetch(`${API_BASE_URL}/api/models`);
        if (!res.ok) {
          throw new Error(`Model request failed with ${res.status}`);
        }

        const data = await res.json();
        setModels(data.models ?? []);
        if (data.models?.[0]?.key) {
          setSelectedModel(data.models[0].key);
        }
      } catch (event) {
        setError(event instanceof Error ? event.message : "Unable to load models");
      }
    }

    loadModels();
  }, []);

  async function sendPrompt() {
    setError("");
    setResponse("");
    setIsLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ model_key: selectedModel, message: prompt }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail ?? `Chat request failed with ${res.status}`);
      }

      setResponse(data.message ?? JSON.stringify(data, null, 2));
    } catch (event) {
      setError(event instanceof Error ? event.message : "Unable to send prompt");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: 800, margin: "2rem auto", fontFamily: "system-ui" }}>
      <h1>Bedrock Model Router</h1>
      <label>
        Model
        <select
          style={{ display: "block", margin: "0.5rem 0 1rem", padding: "0.4rem" }}
          value={selectedModel}
          onChange={(event) => setSelectedModel(event.target.value)}
        >
          {models.map((model) => (
            <option key={model.key} value={model.key}>
              {model.label} ({model.provider})
            </option>
          ))}
        </select>
      </label>
      <textarea
        style={{ width: "100%", height: 120 }}
        value={prompt}
        onChange={(event) => setPrompt(event.target.value)}
        placeholder="Ask a model..."
      />
      <br />
      <button disabled={isLoading || prompt.trim().length === 0} onClick={sendPrompt}>
        {isLoading ? "Sending..." : "Send"}
      </button>
      {error ? <p style={{ color: "crimson" }}>{error}</p> : null}
      <h2>Response</h2>
      <pre style={{ whiteSpace: "pre-wrap" }}>{response}</pre>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);

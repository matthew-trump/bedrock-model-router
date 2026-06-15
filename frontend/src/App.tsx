import React, { useState } from "react";
import { createRoot } from "react-dom/client";

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");

  async function sendPrompt() {
    const res = await fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model_key: "nova-lite", message: prompt }),
    });

    const data = await res.json();
    setResponse(data.message ?? JSON.stringify(data, null, 2));
  }

  return (
    <main style={{ maxWidth: 800, margin: "2rem auto", fontFamily: "system-ui" }}>
      <h1>Bedrock Model Router</h1>
      <textarea
        style={{ width: "100%", height: 120 }}
        value={prompt}
        onChange={(event) => setPrompt(event.target.value)}
        placeholder="Ask a model..."
      />
      <br />
      <button onClick={sendPrompt}>Send</button>
      <h2>Response</h2>
      <pre style={{ whiteSpace: "pre-wrap" }}>{response}</pre>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);

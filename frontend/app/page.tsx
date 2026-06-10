"use client";
import { useState } from "react";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<{role: string, text: string, route?: string}[]>([]);
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function send() {
    if (!question.trim()) return;
    const q = question;
    setMessages((m) => [...m, { role: "user", text: q }]);
    setQuestion("");
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/agent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const data = await res.json();
      setMessages((m) => [...m, { role: "assistant", text: data.answer, route: data.route }]);
    } catch (e) {
      setMessages((m) => [...m, { role: "assistant", text: "Error reaching server." }]);
    } finally {
      setLoading(false);
    }
  }

  async function login() {
    const res = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (res.ok) {
      const data = await res.json();
      setToken(data.access_token);
    } else {
      alert("Login failed");
    }
  }

  return (
    <main className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">FastAPI Docs Assistant</h1>

      {!token ? (
        <div className="flex gap-2 mb-4">
          <input className="border rounded px-2 py-1 flex-1" placeholder="email"
            value={email} onChange={(e) => setEmail(e.target.value)} />
          <input className="border rounded px-2 py-1 flex-1" placeholder="password" type="password"
            value={password} onChange={(e) => setPassword(e.target.value)} />
          <button onClick={login} className="bg-blue-600 text-white rounded px-3">Login</button>
        </div>
      ) : (
        <div className="text-sm text-green-600 mb-4">✓ Logged in</div>
      )}

      <div className="space-y-2 mb-4">
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
            {m.route && <span className="text-xs text-gray-400 mr-2">[{m.route}]</span>}
            <span className="inline-block bg-gray-100 rounded px-3 py-2">{m.text}</span>
          </div>
        ))}
        {loading && <div className="text-left text-gray-400">Thinking…</div>}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 border rounded px-3 py-2"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Ask about FastAPI..."
        />
        <button onClick={send} className="bg-black text-white rounded px-4">Send</button>
      </div>
    </main>
  );
}
"use client";
import { useState } from "react";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<{role: string, text: string, route?: string}[]>([]);
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!question.trim()) return;
    const q = question;
    setMessages((m) => [...m, { role: "user", text: q }]);
    setQuestion("");
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/agent", {
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

  return (
    <main className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">FastAPI Docs Assistant</h1>
      <div className="space-y-2 mb-4">
        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "text-right" : "text-left"}>
            <span className="inline-block bg-gray-100 rounded px-3 py-2">{m.text}</span>
          </div>
        ))}
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
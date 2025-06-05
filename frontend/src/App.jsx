import { useState, useRef, useEffect } from "react";
import axios from "axios";

function Section({ title, children }) {
  return (
    <div className="bg-white shadow-md rounded-xl p-6 space-y-4">
      <h2 className="text-xl font-semibold text-gray-800">{title}</h2>
      {children}
    </div>
  );
}

function App() {
  const [summary, setSummary] = useState("");
  const [query, setQuery] = useState("");
  const [queryResponse, setQueryResponse] = useState("");
  const [notes, setNotes] = useState([]);
  const [noteInput, setNoteInput] = useState("");
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatMessages]);

  const handleFileUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await axios.post("http://localhost:8000/upload", formData);
      setSummary(res.data.summary);
    } catch (err) {
      console.error("Upload error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleQuery = async () => {
    if (!query) return;
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/websearch", {
        query,
      });
      setQueryResponse(res.data.response);
    } catch (err) {
      console.error("Query error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddNote = async () => {
    if (!noteInput) return;
    try {
      await axios.post("http://localhost:8000/notes", { note: noteInput });
      setNotes([...notes, noteInput]);
      setNoteInput("");
    } catch (err) {
      console.error("Note error:", err);
    }
  };

  const handleChat = async () => {
    if (!chatInput) return;
    const updatedMessages = [
      ...chatMessages,
      { role: "user", content: chatInput },
    ];
    setChatMessages(updatedMessages);
    setChatInput("");
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/chat", {
        messages: updatedMessages,
      });
      setChatMessages([
        ...updatedMessages,
        { role: "assistant", content: res.data.response },
      ]);
    } catch (err) {
      console.error("Chat error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 space-y-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-center text-blue-700">SynthesiTalk</h1>

      {/* PDF Upload */}
      <Section title="PDF Summarization">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Upload PDF</label>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4 file:rounded-md
              file:border-0 file:text-sm file:font-semibold
              file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          <button
            onClick={handleFileUpload}
            className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? "Summarizing..." : "Upload and Summarize"}
          </button>
        </div>
        {summary && (
          <div className="prose bg-gray-50 p-4 rounded-md max-w-none">
            <h3>Summary</h3>
            <p>{summary}</p>
          </div>
        )}
      </Section>

      {/* Web Search */}
      <Section title="Web Search">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about something..."
          className="w-full p-2 border rounded"
        />
        <button
          onClick={handleQuery}
          className="mt-2 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          disabled={loading}
        >
          {loading ? "Searching..." : "Search"}
        </button>
        {queryResponse && (
          <div className="bg-gray-50 p-4 mt-3 rounded-md">
            <p>{queryResponse}</p>
          </div>
        )}
      </Section>

      {/* Notes */}
      <Section title="Note Taking">
        <input
          type="text"
          value={noteInput}
          onChange={(e) => setNoteInput(e.target.value)}
          placeholder="Add a new note"
          className="w-full p-2 border rounded"
        />
        <button
          onClick={handleAddNote}
          className="mt-2 px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
        >
          Save Note
        </button>
        {notes.length > 0 && (
          <ul className="list-disc ml-6 mt-3 text-gray-700">
            {notes.map((note, idx) => (
              <li key={idx}>{note}</li>
            ))}
          </ul>
        )}
      </Section>

      {/* Chat */}
      <Section title="Chat">
        <div className="max-h-64 overflow-y-auto bg-gray-50 p-3 rounded space-y-2">
          {chatMessages.map((msg, i) => (
            <div
              key={i}
              className={`p-2 rounded-md ${
                msg.role === "user"
                  ? "bg-blue-100 text-right text-blue-900"
                  : "bg-gray-200 text-left text-gray-800"
              }`}
            >
              <span className="font-semibold capitalize">{msg.role}:</span>{" "}
              {msg.content}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
        <div className="flex mt-2 space-x-2">
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-grow p-2 border rounded"
          />
          <button
            onClick={handleChat}
            className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
            disabled={loading}
          >
            {loading ? "Sending..." : "Send"}
          </button>
        </div>
      </Section>
    </div>
  );
}

export default App;

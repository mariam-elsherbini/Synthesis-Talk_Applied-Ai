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

// Component to render markdown-style text
function MarkdownRenderer({ content }) {
  const formatMarkdown = (text) => {
    return text
      .split('\n')
      .map((line, index) => {
        // Handle headings
        if (line.startsWith('### ')) {
          return <h3 key={index} className="text-lg font-semibold text-gray-800 mt-4 mb-2">{line.substring(4)}</h3>;
        }
        if (line.startsWith('## ')) {
          return <h2 key={index} className="text-xl font-bold text-gray-900 mt-6 mb-3">{line.substring(3)}</h2>;
        }
        if (line.startsWith('# ')) {
          return <h1 key={index} className="text-2xl font-bold text-gray-900 mt-6 mb-4">{line.substring(2)}</h1>;
        }
        
        // Handle bullet points
        if (line.startsWith('- ') || line.startsWith('* ')) {
          return (
            <li key={index} className="ml-4 text-gray-700 mb-1">
              {formatInlineMarkdown(line.substring(2))}
            </li>
          );
        }
        
        // Handle numbered lists
        if (/^\d+\.\s/.test(line)) {
          return (
            <li key={index} className="ml-4 text-gray-700 mb-1 list-decimal">
              {formatInlineMarkdown(line.replace(/^\d+\.\s/, ''))}
            </li>
          );
        }
        
        // Handle empty lines
        if (line.trim() === '') {
          return <br key={index} />;
        }
        
        // Handle regular paragraphs
        return (
          <p key={index} className="text-gray-700 mb-2 leading-relaxed">
            {formatInlineMarkdown(line)}
          </p>
        );
      });
  };

  const formatInlineMarkdown = (text) => {
    // Handle bold text
    return text.split(/(\*\*.*?\*\*)/).map((part, index) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={index} className="font-semibold text-gray-900">{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  return <div className="space-y-1">{formatMarkdown(content)}</div>;
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
  const [summaryType, setSummaryType] = useState("standard"); // New state for summary type

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
    formData.append("summary_type", summaryType); // Send summary type to backend
    
    try {
      const res = await axios.post("http://localhost:8000/upload", formData);
      setSummary(res.data.summary);
    } catch (err) {
      console.error("Upload error:", err);
      setSummary("Error occurred while processing the file.");
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
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Summary Type</label>
            <select
              value={summaryType}
              onChange={(e) => setSummaryType(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="standard">Standard Summary</option>
              <option value="bullet">Bullet Point Summary</option>
              <option value="detailed">Detailed Analysis</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Upload PDF</label>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files[0])}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4 file:rounded-md
                file:border-0 file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
            <button
              onClick={handleFileUpload}
              className="mt-3 px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading || !file}
            >
              {loading ? "Processing..." : "Upload and Summarize"}
            </button>
          </div>
        </div>
        
        {summary && (
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 mt-4">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-800">Document Summary</h3>
              <button
                onClick={() => navigator.clipboard.writeText(summary)}
                className="px-3 py-1 text-sm bg-gray-200 hover:bg-gray-300 rounded-md"
              >
                Copy
              </button>
            </div>
            <div className="prose max-w-none">
              <MarkdownRenderer content={summary} />
            </div>
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
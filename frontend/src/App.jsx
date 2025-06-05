import { useState } from "react";
import axios from "axios";

function App() {
  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState([]);
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [noteTopic, setNoteTopic] = useState("");
  const [noteContent, setNoteContent] = useState("");
  const [notes, setNotes] = useState([]);
  const [explainQuery, setExplainQuery] = useState("");
  const [explanation, setExplanation] = useState("");
  const [reasonPrompt, setReasonPrompt] = useState("");
  const [reasoningResult, setReasoningResult] = useState("");
  const [pdfContent, setPdfContent] = useState("");
  const [pdfFilename, setPdfFilename] = useState("output.pdf");

  const sendChat = async () => {
    const updatedMessages = [...chatMessages, { role: "user", content: chatInput }];
    const res = await axios.post("http://localhost:8000/chat", { messages: updatedMessages });
    updatedMessages.push(res.data.choices[0].message);
    setChatMessages(updatedMessages);
    setChatInput("");
  };

  const uploadFile = async () => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post("http://localhost:8000/upload", formData);
    setSummary(res.data.summary);
  };

  const searchWeb = async () => {
    const res = await axios.get(`http://localhost:8000/search?query=${query}`);
    setSearchResults(res.data);
  };

  const saveNote = async () => {
    await axios.post("http://localhost:8000/note", { topic: noteTopic, content: noteContent });
    const notesRes = await axios.get("http://localhost:8000/notes");
    setNotes(notesRes.data);
  };

  const explainConcept = async () => {
    const res = await axios.get(`http://localhost:8000/explain?query=${explainQuery}`);
    setExplanation(res.data.explanation);
  };

  const doReasoning = async () => {
    const res = await axios.post("http://localhost:8000/reason", { prompt: reasonPrompt });
    setReasoningResult(res.data.result);
  };

  const exportPDF = async () => {
    await axios.post("http://localhost:8000/export", {
      filename: pdfFilename,
      content: pdfContent
    });
    alert("PDF exported on server!");
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-center">🧠 SynthesiTalk Frontend</h1>

      {/* Chat Interface */}
      <div className="space-y-2">
        <h2 className="text-xl font-semibold">Chat</h2>
        <div className="border p-4 h-48 overflow-y-auto bg-gray-50 rounded">
          {chatMessages.map((msg, i) => (
            <p key={i}><b>{msg.role}:</b> {msg.content}</p>
          ))}
        </div>
        <div className="flex gap-2">
          <input
            className="border p-2 flex-1"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            placeholder="Type message..."
          />
          <button className="bg-blue-600 text-white px-4 rounded" onClick={sendChat}>
            Send
          </button>
        </div>
      </div>

      {/* PDF Upload */}
      <div className="space-y-2">
        <h2 className="text-xl font-semibold">Upload PDF</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button className="bg-green-600 text-white px-4 rounded ml-2" onClick={uploadFile}>
          Upload & Summarize
        </button>
        {summary && (
          <div className="bg-gray-100 p-3 rounded mt-2">
            <strong>Summary:</strong> {summary}
          </div>
        )}
      </div>

      {/* Web Search */}
      <div className="space-y-2">
        <h2 className="text-xl font-semibold">Web Search</h2>
        <input
          className="border p-2 w-full"
          placeholder="Search the web..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button className="bg-purple-600 text-white px-4 rounded mt-1" onClick={searchWeb}>
          Search
        </button>
        <ul className="list-disc ml-6">
          {searchResults.map((res, i) => (
            <li key={i}>
              <a href={res.link} className="text-blue-600 underline" target="_blank" rel="noreferrer">
                {res.title}
              </a>
            </li>
          ))}
        </ul>
      </div>

      {/* Notes */}
      <div className="space-y-2">
        <h2 className="text-xl font-semibold">Notes</h2>
        <input
          className="border p-2 w-full"
          placeholder="Topic"
          value={noteTopic}
          onChange={(e) => setNoteTopic(e.target.value)}
        />
        <textarea
          className="border p-2 w-full mt-1"
          placeholder="Note content"
          value={noteContent}
          onChange={(e) => setNoteContent(e.target.value)}
        />
        <button className="bg-yellow-600 text-white px-4 rounded mt-1" onClick={saveNote}>
          Save Note
        </button>
        <ul className="list-disc ml-6">
          {notes.map((note, i) => (
            <li key={i}><strong>{note.topic}:</strong> {note.content}</li>
          ))}
        </ul>
      </div>

      {/* Explain */}
      <div className="space-y-2">
        <h2 className="text-xl font-semibold">Explain Concept</h2>
        <input
          className="border p-2 w-full"
          placeholder="What do you want explained?"
          value={explainQuery}
          onChange={(e) => setExplainQuery(e.target.value)}
        />
        <button className="bg-indigo-600 text-white px-4 rounded mt-1" onClick={explainConcept}>
          Explain
        </button>
        {explanation && <div className="bg-gray-100 p-3 rounded mt-2">{explanation}</div>}
      </div>

      {/* Reasoning */}
      <div className="space-y-2">
        <h2 className="text-xl font-semibold">Reasoning Tool</h2>
        <textarea
          className="border p-2 w-full"
          placeholder="Ask something that needs step-by-step reasoning..."
          value={reasonPrompt}
          onChange={(e) => setReasonPrompt(e.target.value)}
        />
        <button className="bg-pink-600 text-white px-4 rounded mt-1" onClick={doReasoning}>
          Run Reasoning
        </button>
        {reasoningResult && <div className="bg-gray-100 p-3 rounded mt-2">{reasoningResult}</div>}
      </div>

      {/* Export */}
      <div className="space-y-2">
        <h2 className="text-xl font-semibold">Export to PDF</h2>
        <input
          className="border p-2 w-full"
          placeholder="Filename (e.g., notes.pdf)"
          value={pdfFilename}
          onChange={(e) => setPdfFilename(e.target.value)}
        />
        <textarea
          className="border p-2 w-full mt-1"
          placeholder="Content to export"
          value={pdfContent}
          onChange={(e) => setPdfContent(e.target.value)}
        />
        <button className="bg-gray-700 text-white px-4 rounded mt-1" onClick={exportPDF}>
          Export
        </button>
      </div>
    </div>
  );
}

export default App;
import os
import json
import logging
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import PyPDF2
import io
from dataclasses import dataclass

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ToolResult:
    """Data class for tool execution results"""
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Optional[Dict] = None

class ToolManager:
    """Manages available tools for the LLM to use"""
    
    def __init__(self):
        self.tools = {}
        self.register_default_tools()
    
    def register_tool(self, name: str, func: Callable, description: str, parameters: Dict):
        """Register a new tool"""
        self.tools[name] = {
            'function': func,
            'description': description,
            'parameters': parameters
        }
    
    def register_default_tools(self):
        """Register default research tools"""
        
        # Document analysis tool
        self.register_tool(
            name="analyze_document",
            func=self._analyze_document,
            description="Extract and analyze content from uploaded documents",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the document file"},
                    "analysis_type": {"type": "string", "enum": ["summary", "key_points", "detailed"], "description": "Type of analysis to perform"}
                },
                "required": ["file_path", "analysis_type"]
            }
        )
        
        # Web search tool
        self.register_tool(
            name="web_search",
            func=self._web_search,
            description="Search the web for information on a given topic",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "num_results": {"type": "integer", "description": "Number of results to return", "default": 5}
                },
                "required": ["query"]
            }
        )
        
        # Note-taking tool
        self.register_tool(
            name="save_note",
            func=self._save_note,
            description="Save important information as a structured note",
            parameters={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Note title"},
                    "content": {"type": "string", "description": "Note content"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for categorization"}
                },
                "required": ["title", "content"]
            }
        )
        
        # Explanation tool
        self.register_tool(
            name="explain_concept",
            func=self._explain_concept,
            description="Provide detailed explanation of a concept or topic",
            parameters={
                "type": "object",
                "properties": {
                    "concept": {"type": "string", "description": "The concept to explain"},
                    "level": {"type": "string", "enum": ["basic", "intermediate", "advanced"], "description": "Explanation level"}
                },
                "required": ["concept"]
            }
        )
    
    def _analyze_document(self, file_path: str, analysis_type: str = "summary") -> ToolResult:
        """Analyze document content"""
        try:
            if not os.path.exists(file_path):
                return ToolResult(success=False, error=f"File not found: {file_path}")
            
            content = ""
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.pdf':
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        content += page.extract_text() + "\n"
            elif file_ext == '.txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
            else:
                return ToolResult(success=False, error=f"Unsupported file type: {file_ext}")
            
            # Perform analysis based on type
            if analysis_type == "summary":
                # Extract first few paragraphs as summary
                paragraphs = content.split('\n\n')[:3]
                result = '\n\n'.join(paragraphs)
            elif analysis_type == "key_points":
                # Extract sentences that might be key points
                sentences = content.split('.')
                key_sentences = [s.strip() for s in sentences if len(s.strip()) > 50 and len(s.strip()) < 200][:5]
                result = '\n• '.join([''] + key_sentences)
            else:  # detailed
                result = content
            
            return ToolResult(
                success=True,
                data=result,
                metadata={"file_type": file_ext, "content_length": len(content)}
            )
            
        except Exception as e:
            logger.error(f"Document analysis error: {str(e)}")
            return ToolResult(success=False, error=str(e))
    
    def _web_search(self, query: str, num_results: int = 5) -> ToolResult:
        """Simple web search implementation"""
        try:
            # This is a simplified implementation
            # In a real application, you'd use a proper search API like Google Custom Search
            search_url = f"https://duckduckgo.com/html/?q={query}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            # For now, return mock results
            mock_results = [
                {
                    "title": f"Search result for: {query}",
                    "url": "https://example.com",
                    "snippet": f"This is a mock search result for the query '{query}'. In a real implementation, this would contain actual search results."
                }
            ]
            
            return ToolResult(
                success=True,
                data=mock_results[:num_results],
                metadata={"query": query, "num_results": len(mock_results)}
            )
            
        except Exception as e:
            logger.error(f"Web search error: {str(e)}")
            return ToolResult(success=False, error=str(e))
    
    def _save_note(self, title: str, content: str, tags: List[str] = None) -> ToolResult:
        """Save a note to the notes system"""
        try:
            note = {
                "id": datetime.now().isoformat(),
                "title": title,
                "content": content,
                "tags": tags or [],
                "created_at": datetime.now().isoformat()
            }
            
            # Save to a simple JSON file (in production, use a proper database)
            notes_file = "research_notes.json"
            notes = []
            
            if os.path.exists(notes_file):
                with open(notes_file, 'r') as f:
                    notes = json.load(f)
            
            notes.append(note)
            
            with open(notes_file, 'w') as f:
                json.dump(notes, f, indent=2)
            
            return ToolResult(success=True, data=note)
            
        except Exception as e:
            logger.error(f"Note saving error: {str(e)}")
            return ToolResult(success=False, error=str(e))
    
    def _explain_concept(self, concept: str, level: str = "intermediate") -> ToolResult:
        """Provide explanation of a concept"""
        try:
            explanation_prompt = f"""
            Explain the concept of '{concept}' at a {level} level.
            Provide a clear, structured explanation that includes:
            1. Definition
            2. Key characteristics
            3. Examples or applications
            4. Related concepts
            """
            
            return ToolResult(
                success=True,
                data=explanation_prompt,
                metadata={"concept": concept, "level": level}
            )
            
        except Exception as e:
            logger.error(f"Concept explanation error: {str(e)}")
            return ToolResult(success=False, error=str(e))
    
    def get_tool_definitions(self) -> List[Dict]:
        """Get tool definitions in OpenAI function calling format"""
        tool_defs = []
        for name, tool in self.tools.items():
            tool_defs.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool['description'],
                    "parameters": tool['parameters']
                }
            })
        return tool_defs
    
    def execute_tool(self, name: str, arguments: Dict) -> ToolResult:
        """Execute a tool by name with given arguments"""
        if name not in self.tools:
            return ToolResult(success=False, error=f"Tool '{name}' not found")
        
        try:
            result = self.tools[name]['function'](**arguments)
            return result
        except Exception as e:
            logger.error(f"Tool execution error for {name}: {str(e)}")
            return ToolResult(success=False, error=str(e))

class ConversationManager:
    """Manages conversation history and context"""
    
    def __init__(self, max_history: int = 20):
        self.messages = []
        self.max_history = max_history
        self.context = {}
    
    def add_message(self, role: str, content: str, metadata: Dict = None):
        """Add a message to the conversation history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.messages.append(message)
        self._trim_history()
    
    def _trim_history(self):
        """Keep only the most recent messages"""
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def get_messages_for_api(self) -> List[Dict]:
        """Get messages in format suitable for OpenAI API"""
        return [{"role": msg["role"], "content": msg["content"]} for msg in self.messages]
    
    def update_context(self, key: str, value: Any):
        """Update conversation context"""
        self.context[key] = value
    
    def get_context_summary(self) -> str:
        """Get a summary of the current context"""
        if not self.context:
            return "No specific context established."
        
        summary_parts = []
        for key, value in self.context.items():
            summary_parts.append(f"{key}: {value}")
        
        return "Current context: " + "; ".join(summary_parts)

class ReasoningEngine:
    """Implements reasoning techniques like Chain of Thought and ReAct"""
    
    @staticmethod
    def chain_of_thought_prompt(question: str, context: str = "") -> str:
        """Generate a Chain of Thought prompt"""
        return f"""
        Let's approach this step by step.

        Question: {question}
        
        {f"Context: {context}" if context else ""}
        
        Please think through this systematically:
        1. First, let me understand what is being asked
        2. What information do I need to answer this question?
        3. What steps should I follow to reach a conclusion?
        4. Let me work through each step carefully
        5. Finally, what is my conclusion?

        Think step by step:
        """
    
    @staticmethod
    def react_prompt(question: str, available_tools: List[str]) -> str:
        """Generate a ReAct (Reasoning + Acting) prompt"""
        tools_list = ", ".join(available_tools)
        return f"""
        I need to answer this question: {question}

        I have access to these tools: {tools_list}

        I will use the ReAct approach - Reasoning and Acting in turns:

        Thought: Let me think about what I need to do to answer this question.
        Action: [I'll choose an appropriate tool if needed]
        Observation: [I'll analyze the results]
        Thought: [I'll reason about what I learned]
        ... (continue as needed)
        Final Answer: [My conclusion based on reasoning and actions]

        Let me start:
        """

class SynthesisTalkLLM:
    """Main LLM integration class for SynthesisTalk"""
    
    def __init__(self):
        self.model_server = os.getenv('MODEL_SERVER', 'NGU').upper()
        self._setup_client()
        self.tool_manager = ToolManager()
        self.conversation_manager = ConversationManager()
        self.reasoning_engine = ReasoningEngine()
        
        # System prompt for research assistant
        self.system_prompt = """
        You are SynthesisTalk, an intelligent research assistant that helps users explore complex topics through interactive conversation.

        Your capabilities include:
        - Analyzing documents and extracting key information
        - Searching for additional information on the web
        - Connecting related concepts across different sources
        - Generating insights based on patterns in information
        - Taking and organizing notes
        - Explaining complex concepts clearly

        When users ask questions:
        1. Consider what tools might be helpful
        2. Use reasoning techniques to approach complex problems
        3. Provide clear, well-structured responses
        4. Maintain conversation context across multiple turns
        5. Suggest follow-up questions or areas for deeper exploration

        Always be helpful, accurate, and focus on facilitating deep research and understanding.
        """
    
    def _setup_client(self):
        """Setup the OpenAI client based on configuration"""
        if self.model_server == "GROQ":
            api_key = os.getenv('GROQ_API_KEY')
            base_url = os.getenv('GROQ_BASE_URL')
            self.model = os.getenv('GROQ_MODEL')
        elif self.model_server == "NGU":
            api_key = os.getenv('NGU_API_KEY')
            base_url = os.getenv('NGU_BASE_URL')
            self.model = os.getenv('NGU_MODEL')
        else:
            raise ValueError(f"Unsupported MODEL_SERVER: {self.model_server}")
        
        if not api_key:
            raise ValueError(f"API key not found for {self.model_server}")
        
        self.client = OpenAI(api_key=api_key, base_url=base_url)
    
    def chat(self, user_message: str, use_tools: bool = True, reasoning_type: str = None) -> Dict[str, Any]:
        """Main chat interface with tool support and reasoning"""
        try:
            # Add user message to conversation
            self.conversation_manager.add_message("user", user_message)
            
            # Prepare messages for API
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add context summary if available
            context_summary = self.conversation_manager.get_context_summary()
            if context_summary != "No specific context established.":
                messages.append({"role": "system", "content": context_summary})
            
            # Apply reasoning technique if specified
            if reasoning_type == "chain_of_thought":
                enhanced_message = self.reasoning_engine.chain_of_thought_prompt(
                    user_message, context_summary
                )
                messages.append({"role": "user", "content": enhanced_message})
            elif reasoning_type == "react":
                available_tools = list(self.tool_manager.tools.keys())
                enhanced_message = self.reasoning_engine.react_prompt(
                    user_message, available_tools
                )
                messages.append({"role": "user", "content": enhanced_message})
            else:
                messages.extend(self.conversation_manager.get_messages_for_api())
            
            # Prepare request parameters
            request_params = {
                "model": self.model,
                "messages": messages
            }
            
            # Add tools if enabled
            if use_tools:
                request_params["tools"] = self.tool_manager.get_tool_definitions()
                request_params["tool_choice"] = "auto"
            
            # Make API call
            response = self.client.chat.completions.create(**request_params)
            
            assistant_message = response.choices[0].message
            tool_calls = getattr(assistant_message, 'tool_calls', None)
            
            # Handle tool calls if present
            tool_results = []
            if tool_calls:
                for tool_call in tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
                    result = self.tool_manager.execute_tool(tool_name, tool_args)
                    tool_results.append({
                        "tool": tool_name,
                        "args": tool_args,
                        "result": result
                    })
                    
                    # Add tool result to conversation
                    if result.success:
                        messages.append({
                            "role": "tool",
                            "content": str(result.data),
                            "tool_call_id": tool_call.id
                        })
                
                # Get final response after tool execution
                if tool_results:
                    final_response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages
                    )
                    assistant_message = final_response.choices[0].message
            
            # Add assistant response to conversation
            self.conversation_manager.add_message(
                "assistant", 
                assistant_message.content,
                {"tool_calls": len(tool_calls) if tool_calls else 0}
            )
            
            return {
                "response": assistant_message.content,
                "tool_results": tool_results,
                "reasoning_type": reasoning_type,
                "context": self.conversation_manager.context
            }
            
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            return {
                "response": f"I encountered an error: {str(e)}",
                "tool_results": [],
                "error": str(e)
            }
    
    def analyze_document(self, file_path: str, analysis_type: str = "summary") -> Dict[str, Any]:
        """Analyze a document and update conversation context"""
        result = self.tool_manager.execute_tool("analyze_document", {
            "file_path": file_path,
            "analysis_type": analysis_type
        })
        
        if result.success:
            # Update context with document information
            self.conversation_manager.update_context("current_document", file_path)
            self.conversation_manager.update_context("document_analysis", analysis_type)
        
        return {
            "success": result.success,
            "content": result.data if result.success else None,
            "error": result.error,
            "metadata": result.metadata
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the current conversation history"""
        return self.messages
    
    def clear_conversation(self):
        """Clear conversation history and context"""
        self.conversation_manager = ConversationManager()
    
    def export_research_notes(self) -> List[Dict]:
        """Export all saved research notes"""
        notes_file = "research_notes.json"
        if os.path.exists(notes_file):
            try:
                with open(notes_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error reading notes: {str(e)}")
                return []
        return []

# Convenience function for simple usage
def ask_llm(user_message: str, use_tools: bool = True, reasoning_type: str = None) -> str:
    """Simple interface for basic LLM interaction"""
    llm = SynthesisTalkLLM()
    result = llm.chat(user_message, use_tools, reasoning_type)
    return result["response"]

# Example usage and testing
if __name__ == "__main__":
    # Initialize the LLM system
    llm = SynthesisTalkLLM()
    
    # Test basic conversation
    print("Testing basic conversation...")
    response = llm.chat("Hello! I'm interested in learning about artificial intelligence.")
    print(f"Response: {response['response']}")
    
    # Test with Chain of Thought reasoning
    print("\nTesting Chain of Thought reasoning...")
    response = llm.chat(
        "What are the main challenges in implementing AI in healthcare?",
        reasoning_type="chain_of_thought"
    )
    print(f"Response: {response['response']}")
    
    # Test document analysis (if a test document exists)
    print("\nTesting document analysis...")
    test_doc = "test_document.txt"
    if os.path.exists(test_doc):
        doc_result = llm.analyze_document(test_doc, "summary")
        print(f"Document analysis result: {doc_result}")
    
    print("\nLLM Integration system ready!")
# DevBrain - AI-Powered Mind Mapping for Developers

## Inspiration

As developers, we constantly juggle complex projects with scattered notes, lost context, and endless task lists. Traditional tools like **Notion** are too linear, mind maps lack AI assistance, and **ChatGPT** doesn't understand our project structure. We wanted **one unified workspace** that combines:
- **Obsidian's** visual graphs  
- **Notion's** organization  
- **ChatGPT's** intelligence  

So we built **DevBrain** - a smart workspace where ideas transform into actionable hierarchies with AI guidance at every step.

---

## What it does

DevBrain is an **AI-powered mind mapping tool** that helps developers break down complex projects into manageable hierarchies. Users can:

- 🗺️ **Visualize projects** in dual modes:
  - **Tree View** - Hierarchical layout using Dagre algorithm
  - **Graph View** - Interactive force-directed network (D3.js physics)

- 🤖 **Chat with AI** about specific nodes with full project context using **Google Gemini 2.0 Flash**

- 📚 **Upload documentation** (PDFs, TXT, MD files) to ground AI responses in your knowledge base

- ⚡ **Track progress** with status indicators:
  - 🔴 Not Started  
  - 🟡 In Progress  
  - 🟢 Completed  

- 💾 **Auto-save everything** to a persistent SQLite database with hierarchical structure

- ⌨️ **Use keyboard shortcuts** and command palette for lightning-fast navigation

Think of it as a **smart project planner** where every idea becomes a node, every node has AI guidance, and the entire structure visualizes itself.

---

## How we built it

### **Frontend Stack**
```javascript
// Core Framework
React 19.2 + Vite

// State Management  
Zustand (lightweight alternative to Redux)

// Visualization Libraries
React Flow 11.11     // Tree view with custom nodes
Dagre 0.8.5         // Layout algorithm for hierarchy
React Force Graph 2D // Physics-based network graph

// UI/UX
Framer Motion 12.23  // Smooth animations
Lucide React 0.562   // Icon library
```

**Key Frontend Features:**
- Custom node components with glassmorphic design
- Real-time state synchronization with backend
- Keyboard shortcuts (`Cmd+K` for command palette)
- Connection status monitoring
- Smooth view transitions between Tree and Graph modes

### **Backend Stack**
```python
# Framework
Django 4.2
Django REST Framework 3.14

# Database
SQLite (with recursive queries for tree traversal)

# AI Integration  
Google Generative AI 0.3.0 (Gemini 2.0 Flash)

# File Processing
PyPDF2 3.0.1        # PDF text extraction
python-docx 0.8.11   # Word document parsing

# Utilities
django-cors-headers 4.0.0  # CORS configuration
python-decouple 3.8        # Environment variables
```

**Key Backend Features:**
- RESTful API with proper serialization
- Cascade delete operations maintaining referential integrity
- Knowledge base file upload system
- Chat message persistence per node
- User authentication and project ownership

### **Database Schema**
We use **SQLite with recursive queries** to handle hierarchical tree structures:

```sql
-- Example: Get all descendants of a node
WITH RECURSIVE tree AS (
  SELECT * FROM nodes WHERE id = 'parent-id'
  UNION ALL
  SELECT n.* FROM nodes n 
  JOIN tree t ON n.parent_id = t.id
)
SELECT * FROM tree;
```

**Models:**
- `Project` - Root container for mind maps
- `Node` - Individual mind map nodes with parent-child relationships
- `Edge` - Connections between nodes
- `KnowledgeBase` - Uploaded files (PDF, TXT, MD)
- `ChatMessage` - AI conversation history per node

### **Architecture**

```
┌─────────────────┐         ┌──────────────────┐
│   React App     │◄───────►│  Django Backend  │
│   (Vite:5173)   │  REST   │  (Django:8000)   │
├─────────────────┤         ├──────────────────┤
│ • Zustand Store │         │ • SQLite DB      │
│ • React Flow    │         │ • DRF API        │
│ • Force Graph   │         │ • Gemini AI      │
└─────────────────┘         └──────────────────┘
```

---

## Challenges we ran into

### **1. Hierarchical Data Synchronization**

**Problem:** Keeping React Flow's internal state in sync with the backend database was complex. When deleting a parent node with 50+ children, we encountered race conditions where the frontend updated before the backend cascade delete completed.

**Solution:** Implemented a **"backend-first" mutation pattern**:
- All state changes go through the API first
- Frontend updates only after successful backend response
- Optimistic updates with rollback on failure

```javascript
// Before: Direct state mutation
setNodes(nodes.filter(n => n.id !== nodeId));

// After: Backend-first with Zustand
await deleteNode(nodeId);  // API call
useStore.getState().removeNode(nodeId);  // Update after success
```

### **2. Graph Layout Performance**

**Problem:** With 100+ nodes, the force-directed layout hit \\( O(n^2) \\) complexity calculating repulsive forces between all node pairs. Frame rate dropped to ~15 FPS.

**Solution:** Implemented the **Barnes-Hut algorithm** to optimize complexity:

$$
F_{repulsive} = k \frac{1}{d^2}
$$

Where \\( d \\) is distance between nodes, reducing complexity from \\( O(n^2) \\) to \\( O(n \log n) \\).

Also switched from **SVG rendering to Canvas** for better performance with many nodes.

### **3. AI Context Grounding**

**Problem:** Generic AI responses like "That's a great idea!" weren't useful. We needed the AI to reference uploaded documentation and understand the project hierarchy.

**Solution:** Built a **knowledge base system**:
1. Parse uploaded PDFs/DOCX to extract text
2. Store content in database with file metadata
3. When user asks a question, search relevant documents
4. Send context to Gemini API alongside the query

```python
# Simplified AI service with context
def chat_with_context(node, user_message):
    # Get knowledge base content
    kb_docs = KnowledgeBase.objects.filter(project=node.project)
    context = "\n".join([doc.content for doc in kb_docs])
    
    # Build prompt with context
    prompt = f"""
    Project Context: {context}
    Node: {node.label}
    Question: {user_message}
    """
    
    return gemini.generate_content(prompt)
```

### **4. Cascade Delete Edge Cases**

**Problem:** Deleting a parent with deeply nested children (5+ levels) caused `IntegrityError` due to foreign key constraints.

**Solution:** Implemented **recursive bottom-up deletion** in Django model:

```python
class Node(models.Model):
    def delete(self, *args, **kwargs):
        # Get all descendants recursively
        descendants = self.get_all_descendants()
        
        # Delete from leaf nodes up to parent
        for node in reversed(descendants):
            super(Node, node).delete(*args, **kwargs)
            
        # Finally delete self
        super().delete(*args, **kwargs)
```

---

## Accomplishments that we're proud of

✨ **Seamless dual visualization** - Users can instantly switch between Tree and Graph views while maintaining full state and position

🎨 **Beautiful glassmorphic UI** - iOS-inspired design with backdrop blur, smooth animations, and dark theme that makes project planning actually enjoyable

🤖 **Context-aware AI** - Unlike generic chatbots, our AI understands your project hierarchy, uploaded documentation, and provides relevant suggestions

⚡ **Zero data loss** - Every change auto-saves to SQLite, cascade deletes work perfectly even with 100+ nested nodes, and we handle edge cases gracefully

🚀 **Production-ready architecture** - Proper authentication, environment variable configuration for API keys, CORS setup, and error handling

---

## What we learned

### **React Flow Internals**
- Building custom node components with interactive handles
- Implementing layout algorithms (Dagre for tree, force-directed for graph)
- Managing complex state with node positions, edges, and selections
- Performance optimization with memoization and virtualization

### **Force-Directed Graph Algorithms**
- D3.js physics simulations (charge, link, collision forces)
- Barnes-Hut approximation for \\( O(n \log n) \\) performance
- Canvas rendering vs SVG for large datasets
- Stabilization algorithms to prevent endless oscillation

### **Django Recursive Queries**
- Using `WITH RECURSIVE` Common Table Expressions for tree traversal
- Efficient queries for getting all descendants/ancestors
- Maintaining referential integrity in hierarchical data
- Optimizing cascade operations

### **AI Integration Patterns**
- Context grounding with knowledge base documents
- Prompt engineering for structured responses
- Handling API rate limits and timeouts
- Streaming responses for better UX

### **System Design**
- Building persistent hierarchical structures with SQLite
- Implementing cascade operations that maintain data consistency
- Real-time synchronization between frontend and backend
- Graceful degradation when services are unavailable

### **UX Polish Matters**
Small details make huge differences:
- Keyboard shortcuts (`Cmd+K`, `Esc`, `N`) improve productivity by 3x
- Command palette with fuzzy search reduces friction
- Smooth animations with Framer Motion make the app feel responsive
- Glassmorphic design creates visual hierarchy and focus

---

## What's next for DevBrain

### 🔄 **Real-time Collaboration**
- Multi-user editing with WebSockets
- Operational transformation for conflict resolution
- Live cursors showing teammates' activity
- Comment threads on nodes

### 📤 **Export Functionality**
- Convert mind maps to **Markdown** (compatible with Obsidian)
- Export to **JSON** for programmatic access
- Generate **PDF reports** with hierarchy visualization
- **Mermaid diagram** export for documentation

### 📱 **Mobile App**
- React Native version for iOS/Android
- Offline-first architecture with sync
- Touch gestures for graph manipulation
- Voice input for quick node creation

### 🎯 **Advanced AI Features**
- **Automatic task breakdown** - AI suggests subtasks for any node
- **Time estimation** - ML model predicts completion time based on history
- **Risk analysis** - Identify blockers and dependencies
- **Smart suggestions** - AI recommends next steps based on project status

### 🔗 **Integrations**
- **GitHub sync** - Import issues as nodes, link PRs to tasks
- **Jira/Linear** - Two-way sync with project management tools
- **Notion** - Import databases as mind map hierarchies
- **Google Drive** - Auto-upload knowledge base from Drive folders

### 🎨 **Customization**
- **Custom themes** - Light mode, high contrast, custom color schemes
- **Node styling** - Icons, colors, shapes per node type
- **Layout preferences** - Horizontal vs vertical tree, force strength tuning
- **Plugin system** - Community extensions for custom features

### ⏪ **Undo/Redo System**
- Full command history with `Ctrl+Z` / `Ctrl+Shift+Z`
- Timeline view of all changes
- Branch from any point in history
- Autosave with version snapshots

---

## Try it yourself!

```bash
# Clone the repository
git clone https://github.com/shams909/DevBrain.git
cd DevBrain

# Backend setup
cd the-architect/backend/backend
pip install -r requirements.txt
python manage.py migrate
python manage.py create_default_user  # Creates admin user
python manage.py runserver

# Frontend setup (new terminal)
cd the-architect/frontend
npm install
npm run dev

# Open http://localhost:5173
# Login: admin / admin123
```

**Get your Gemini API key:** [Google AI Studio](https://makersuite.google.com/app/apikey)

---

**Built with ❤️ using React, Django, and Google Gemini AI**

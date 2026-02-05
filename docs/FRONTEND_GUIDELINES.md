# Frontend Design System & Guidelines

## 1. Design Principles
### Core Principles
1. **Simplicity**: deeply technical tool, simple interface.
2. **Feedback**: Always show when the engine is "thinking" or "running".
3. **Clarity**: Clearly distinguish User input from AI output.

---

## 2. Design Tokens (Streamlit Theme)
Since we are using Streamlit, we rely on the `config.toml` or system theme, but we enforce these defaults:

### Color Palette
- **Primary**: Lightning Blue (#FF4B4B default, customized to #3b82f6 for "System" feel).
- **Background**: Dark Mode (Preferred for Engineering Tools).
- **Text**: Sans-Serif (Inter/Roboto).

### Components
#### Chat Interface
- **User Message**: Aligned Right, Distinct background.
- **AI Message**: Aligned Left, Neutral background.
- **Status Indicators**:
  - Green (✅): Engine Online.
  - Red (❌): Engine Offline/Error.

---

## 3. Component Library
### Sidebar (Control Panel)
- **Status Box**: Success/Error message.
- **Settings**: Slider for `max_tokens`.
- **Benchmark Info**: Static text showing current model.

### Chat Area
- **Input**: `st.chat_input` pinned to bottom.
- **History**: `st.chat_message` container with scroll.

---

## 4. Interaction Guidelines
### Generating State
- While the API is processing:
  - Display "Running..." spinner or progressive loading.
  - Disable input if necessary (optional for Streamlit).

### Error Feedback
- If API fails:
  - Show `st.error` banner.
  - Suggest "Check API Console".

---

## 5. Responsive Design
- Streamlit handles mobile/desktop responsiveness automatically.
- Ensure sidebar collapses gracefully on mobile.

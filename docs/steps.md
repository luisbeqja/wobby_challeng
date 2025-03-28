## 📚 **Online research**

- How to extract questions from a conversation? 
  - use The regex ([^?]*\?) captures any sequence of characters that ends with a question mark.
  - Use library like spaCy to extract questions
  - Use LLM to extract questions
  
### Cascade Approach Overview
- Initial Extraction with Regex:
Quickly filter out messages that clearly end with a question mark.

- Secondary Filtering with spaCy:
Process the remaining messages with spaCy to detect questions that might not end with “?”.

- Final Check with LLM:
Apply an LLM to analyze any ambiguous messages that weren’t classified in the earlier steps.

"""Simple RAG (Retrieval-Augmented Generation) for documents."""
import PyPDF2
import io
from typing import List, Dict, Tuple


class SimpleRAG:
    """Lightweight RAG using keyword search (no embeddings)."""

    def __init__(self):
        self.documents = {}  # filename -> text content

    def add_pdf(self, pdf_file, filename: str) -> str:
        """Extract text from PDF and store."""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""

            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"

            self.documents[filename] = text
            return f"✓ Extracted {len(pdf_reader.pages)} pages from {filename}"

        except Exception as e:
            return f"❌ Error processing PDF: {str(e)}"

    def add_text(self, content: str, filename: str) -> str:
        """Add text document."""
        self.documents[filename] = content
        return f"✓ Added {filename}"

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, str]]:
        """Search documents using keyword matching."""
        results = []
        query_lower = query.lower()

        for filename, text in self.documents.items():
            # Simple keyword search: find lines containing query keywords
            lines = text.split("\n")
            matching_lines = [
                line for line in lines
                if query_lower in line.lower() and len(line.strip()) > 0
            ]

            if matching_lines:
                # Take first matching line
                snippet = matching_lines[0][:200]  # Limit to 200 chars
                results.append({
                    "source": filename,
                    "snippet": snippet,
                    "relevance": "keyword_match"
                })

        # Return top K results
        return results[:top_k]

    def get_document_list(self) -> List[str]:
        """List all documents."""
        return list(self.documents.keys())

    def get_document_content(self, filename: str) -> str:
        """Get full content of a document."""
        return self.documents.get(filename, "")


def extract_specifications_from_text(text: str) -> Dict[str, List[str]]:
    """
    Extract potential equipment specifications from text.

    Looks for patterns like "capacity: 500 kW", "efficiency: 90%", etc.
    """
    specs = {
        "equipment_names": [],
        "capacities": [],
        "efficiencies": [],
        "voltages": [],
        "other": []
    }

    lines = text.split("\n")
    for line in lines:
        lower_line = line.lower()

        # Look for keywords
        if any(term in lower_line for term in ["bess", "battery", "energy storage"]):
            if "capacity" in lower_line or "kwh" in lower_line or "mwh" in lower_line:
                specs["capacities"].append(line.strip())

        if "efficiency" in lower_line or "%" in line:
            specs["efficiencies"].append(line.strip())

        if any(term in lower_line for term in ["voltage", "kv", "v"]):
            specs["voltages"].append(line.strip())

        if any(term in lower_line for term in ["pv", "solar", "panel", "inverter"]):
            if "capacity" in lower_line or "kw" in lower_line:
                specs["capacities"].append(line.strip())

    return specs

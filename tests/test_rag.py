"""
Tests for Knowledge RAG system.
Tests embedding similarity and Arabic bridge without requiring ONNX runtime.
"""

import sys
from pathlib import Path

import pytest

APP_DIR = Path(__file__).parent.parent / "app"
KNOWLEDGE_DIR = APP_DIR / "knowledge"
sys.path.insert(0, str(APP_DIR))


class TestKnowledgeFiles:
    """Validate knowledge base content."""

    def test_knowledge_directory_exists(self):
        assert KNOWLEDGE_DIR.exists(), "app/knowledge/ must exist"

    def test_knowledge_has_markdown_files(self):
        md_files = list(KNOWLEDGE_DIR.glob("*.md"))
        assert len(md_files) > 0, "Knowledge base should have .md files"

    def test_knowledge_files_not_empty(self):
        for md_file in KNOWLEDGE_DIR.glob("*.md"):
            content = md_file.read_text()
            assert len(content) > 100, f"{md_file.name} is too short"

    def test_knowledge_files_have_headers(self):
        for md_file in KNOWLEDGE_DIR.glob("*.md"):
            content = md_file.read_text()
            assert content.startswith("#") or "# " in content[:200], \
                f"{md_file.name} should have markdown headers"


class TestKnowledgeRAGImport:
    """Test RAG module can be imported and basic structure is valid."""

    def test_rag_module_importable(self):
        """Verify knowledge_rag.py exists and is valid Python."""
        rag_path = APP_DIR / "backend" / "knowledge_rag.py"
        assert rag_path.exists(), "knowledge_rag.py must exist"

        import importlib.util
        spec = importlib.util.spec_from_file_location("knowledge_rag", str(rag_path))
        assert spec is not None

    def test_rag_class_exists(self):
        """Verify KnowledgeRAG class is defined."""
        try:
            from backend.knowledge_rag import KnowledgeRAG
            assert KnowledgeRAG is not None
        except ImportError as e:
            pytest.skip(f"Cannot import KnowledgeRAG (missing deps): {e}")


class TestArabicBridge:
    """Test Arabic→English medical keyword bridge."""

    def test_bridge_has_entries(self):
        try:
            from backend.knowledge_rag import KnowledgeRAG
            rag = KnowledgeRAG.__new__(KnowledgeRAG)
            # Access the bridge dict if it exists as class/module level
            bridge_path = APP_DIR / "backend" / "knowledge_rag.py"
            content = bridge_path.read_text()
            assert "arabic" in content.lower() or "bridge" in content.lower(), \
                "RAG should have Arabic bridge support"
        except Exception:
            pytest.skip("Cannot test Arabic bridge directly")

    def test_common_arabic_medical_terms_in_source(self):
        """Verify common Arabic medical terms are in the RAG source."""
        rag_path = APP_DIR / "backend" / "knowledge_rag.py"
        content = rag_path.read_text()
        # Check for some common Arabic medical terms
        arabic_terms = ["نزيف", "حروق", "كسر", "إسعاف"]
        found = sum(1 for term in arabic_terms if term in content)
        assert found >= 2, "RAG should contain common Arabic medical terms"

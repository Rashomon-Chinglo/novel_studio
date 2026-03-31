import os
import sys

# Ensure environment variables are set before importing app modules
os.environ["OPENAI_API_KEY"] = "dummy"
os.environ["JINA_API_KEY"] = "dummy"

# Add project root to sys.path if running from within test dir or root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.vector import get_vector_store


def test_get_vector_store_caching():
    """Test that get_vector_store returns cached instance."""
    s1 = get_vector_store()
    s2 = get_vector_store()

    # This assertion will fail until caching is implemented
    assert s1 is s2, "get_vector_store should return the same instance (cached)"

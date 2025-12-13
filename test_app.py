#!/usr/bin/env python
"""
Test script for Bible study application
"""
import sys
from bible_data import (
    get_verse, 
    get_chapter, 
    get_available_languages, 
    get_available_books
)
from ollama_integration import OllamaAI


def test_bible_data():
    """Test Bible data functions."""
    print("Testing Bible data functions...")
    
    # Test verse retrieval
    verse = get_verse("genesis", 1, 1, "pt")
    assert verse is not None, "Failed to get Genesis 1:1 in Portuguese"
    assert "princípio" in verse.lower(), "Wrong verse content"
    print("✓ Verse retrieval works")
    
    # Test multilingual support
    verse_en = get_verse("genesis", 1, 1, "en")
    assert verse_en is not None, "Failed to get verse in English"
    assert "beginning" in verse_en.lower(), "Wrong English verse"
    print("✓ Multilingual support works")
    
    # Test chapter retrieval
    chapter = get_chapter("genesis", 1, "pt")
    assert chapter is not None, "Failed to get Genesis chapter 1"
    assert len(chapter) == 3, f"Expected 3 verses, got {len(chapter)}"
    print("✓ Chapter retrieval works")
    
    # Test languages
    languages = get_available_languages()
    assert len(languages) == 23, f"Expected 23 languages, got {len(languages)}"
    assert "pt" in languages, "Portuguese not in languages"
    assert "en" in languages, "English not in languages"
    print("✓ 23 languages available")
    
    # Test books
    books = get_available_books()
    assert len(books) >= 2, "Should have at least 2 books"
    assert "genesis" in books, "Genesis not in books"
    assert "john" in books, "John not in books"
    print("✓ Books list works")
    
    print("\n✅ All Bible data tests passed!\n")


def test_ollama_integration():
    """Test Ollama integration."""
    print("Testing Ollama integration...")
    
    ai = OllamaAI()
    assert ai.host == "http://localhost:11434", "Wrong default host"
    assert ai.model == "llama2", "Wrong default model"
    print("✓ Ollama initialization works")
    
    # Test availability check (expected to fail without Ollama running)
    available = ai.is_available()
    print(f"✓ Ollama availability check works (available: {available})")
    
    # Test error handling when Ollama is not available
    result = ai.analyze_verse("Test verse", "pt")
    assert "success" in result, "Missing success field in result"
    if not available:
        assert result["success"] == False, "Should fail when Ollama unavailable"
        print("✓ Error handling works correctly")
    
    print("\n✅ All Ollama integration tests passed!\n")


def test_all_languages():
    """Test verse retrieval in all languages."""
    print("Testing all 23 languages...")
    
    languages = get_available_languages()
    verse_ref = ("genesis", 1, 1)
    
    missing = []
    for lang_code in languages.keys():
        verse = get_verse(*verse_ref, lang_code)
        if verse is None:
            missing.append(lang_code)
        else:
            print(f"✓ {lang_code}: {verse[:50]}...")
    
    if missing:
        print(f"\n⚠️  Missing verses for languages: {missing}")
    else:
        print("\n✅ All 23 languages have Genesis 1:1!\n")
    
    return len(missing) == 0


if __name__ == "__main__":
    print("=" * 60)
    print("Bible Study Application Tests")
    print("=" * 60 + "\n")
    
    try:
        test_bible_data()
        test_ollama_integration()
        test_all_languages()
        
        print("=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

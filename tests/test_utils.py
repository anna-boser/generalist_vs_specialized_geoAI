#!/usr/bin/env python3
"""
Simple tests for the utils module.

Run with: python test_utils.py
"""

import tempfile
from pathlib import Path
import sys

# Add project root to path so we can import from src

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import setup_logging, load_data_config


def test_setup_logging():
    """Test logging setup functionality."""
    print("Testing setup_logging...")
    
    # Test 1: Default behavior (should create log file with script name)
    logger = setup_logging()
    
    # Check that logger was created
    assert logger is not None
    print("✓ Logger created successfully")
    
    # Test logging
    logger.info("Test message")
    print("✓ Log message sent")
    
    # Check that log file was created
    expected_log = Path(__file__).with_suffix('.log')
    assert expected_log.exists(), f"Log file not found: {expected_log}"
    print(f"✓ Log file created: {expected_log}")
    
    # Clean up
    expected_log.unlink()
    print("✓ Cleaned up log file")


def test_setup_logging_custom_file():
    """Test logging with custom log file."""
    print("\nTesting setup_logging with custom file...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        custom_log = Path(temp_dir) / "custom.log"
        
        logger = setup_logging(log_file=str(custom_log))
        
        # Test logging
        logger.info("Custom log test")
        
        # Check that custom log file was created
        assert custom_log.exists(), f"Custom log file not found: {custom_log}"
        print(f"✓ Custom log file created: {custom_log}")
        
        # Check content
        content = custom_log.read_text()
        assert "Custom log test" in content
        print("✓ Log content verified")


def test_load_data_config():
    """Test config loading functionality."""
    print("\nTesting load_data_config...")
    
    # Test 1: Load existing config
    config = load_data_config()
    
    # Should return a dictionary
    assert isinstance(config, dict)
    print("✓ Config loaded as dictionary")
    
    # Check for expected keys
    if config:
        print(f"✓ Found config keys: {list(config.keys())}")
    else:
        print("✓ Empty config (no data.yaml or empty file)")


def test_load_data_config_missing():
    """Test config loading when file is missing."""
    print("\nTesting load_data_config with missing file...")
    
    # Temporarily rename config file
    config_path = Path("configs/data.yaml")
    backup_path = Path("configs/data.yaml.backup")
    
    if config_path.exists():
        config_path.rename(backup_path)
    
    try:
        config = load_data_config()
        assert isinstance(config, dict)
        assert len(config) == 0  # Should be empty
        print("✓ Handles missing config file gracefully")
    finally:
        # Restore config file
        if backup_path.exists():
            backup_path.rename(config_path)


def test_logging_integration():
    """Test that logging works with real file operations."""
    print("\nTesting logging integration...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        log_file = Path(temp_dir) / "integration.log"
        
        logger = setup_logging(log_file=str(log_file))
        
        # Test different log levels
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        # Check file content
        content = log_file.read_text()
        
        assert "Info message" in content
        assert "Warning message" in content
        assert "Error message" in content
        assert "INFO" in content
        assert "WARNING" in content
        assert "ERROR" in content
        
        print("✓ All log levels working correctly")


def main():
    """Run all tests."""
    print("Running utils tests...")
    print("=" * 50)
    
    try:
        test_setup_logging()
        test_setup_logging_custom_file()
        test_load_data_config()
        test_load_data_config_missing()
        test_logging_integration()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

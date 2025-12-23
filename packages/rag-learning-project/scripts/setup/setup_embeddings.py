"""Setup script for Voyage AI embeddings integration."""
import os
import sys
import subprocess


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def check_python_version():
    """Check if Python version is compatible."""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print("✅ Python version is compatible")
    return True


def install_dependencies():
    """Install required dependencies."""
    print_header("Installing Dependencies")
    
    dependencies = [
        "voyageai>=0.2.0",
        "langchain-text-splitters>=0.0.1",
        "pymongo>=4.6.0",
        "python-dotenv>=1.0.0"
    ]
    
    print("Installing packages:")
    for dep in dependencies:
        print(f"  - {dep}")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade"
        ] + dependencies)
        print("\n✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to install dependencies: {e}")
        return False


def check_env_file():
    """Check if .env file exists and has required keys."""
    print_header("Checking Environment Configuration")
    
    env_path = ".env"
    env_example_path = ".env.example"
    
    if not os.path.exists(env_path):
        print(f"⚠️  .env file not found")
        
        if os.path.exists(env_example_path):
            print(f"📝 Creating .env from {env_example_path}")
            try:
                with open(env_example_path, 'r') as src:
                    content = src.read()
                with open(env_path, 'w') as dst:
                    dst.write(content)
                print("✅ .env file created")
            except Exception as e:
                print(f"❌ Failed to create .env: {e}")
                return False
        else:
            print("❌ .env.example not found")
            return False
    
    # Check for required keys
    with open(env_path, 'r') as f:
        content = f.read()
    
    required_keys = ["MONGODB_URI", "VOYAGE_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        if key not in content or f"{key}=your_" in content or f"{key}=" not in content:
            missing_keys.append(key)
    
    if missing_keys:
        print(f"\n⚠️  The following keys need to be configured in .env:")
        for key in missing_keys:
            if key == "VOYAGE_API_KEY":
                print(f"  - {key}: Get from https://www.voyageai.com")
            elif key == "MONGODB_URI":
                print(f"  - {key}: Get from MongoDB Atlas")
        print(f"\n📝 Edit .env file and add your API keys")
        return False
    
    print("✅ .env file is configured")
    return True


def test_imports():
    """Test if all required modules can be imported."""
    print_header("Testing Imports")
    
    modules = [
        ("voyageai", "Voyage AI"),
        ("langchain_text_splitters", "LangChain Text Splitters"),
        ("pymongo", "PyMongo"),
        ("dotenv", "Python Dotenv")
    ]
    
    all_ok = True
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name} - not installed")
            all_ok = False
    
    return all_ok


def run_tests():
    """Run the embedding test suite."""
    print_header("Running Test Suite")
    
    test_script = os.path.join("tests", "integration", "test_embeddings.py")
    
    if not os.path.exists(test_script):
        print(f"⚠️  Test script not found: {test_script}")
        return False
    
    print(f"Running: {test_script}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, test_script],
            cwd=os.getcwd(),
            capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False


def main():
    """Main setup function."""
    print("\n" + "🚀 "*20)
    print("  VOYAGE AI EMBEDDINGS - SETUP WIZARD")
    print("🚀 "*20)
    
    steps = [
        ("Python Version Check", check_python_version),
        ("Install Dependencies", install_dependencies),
        ("Environment Configuration", check_env_file),
        ("Test Imports", test_imports),
    ]
    
    results = []
    
    for step_name, step_func in steps:
        result = step_func()
        results.append((step_name, result))
        
        if not result and step_name != "Environment Configuration":
            print(f"\n⚠️  Setup cannot continue due to errors in: {step_name}")
            break
    
    # Summary
    print_header("Setup Summary")
    
    for step_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {step_name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Make sure your API keys are configured in .env")
        print("2. Run tests: python tests/integration/test_embeddings.py")
        print("3. Run example: python scripts/demos/example_with_embeddings.py")
        print("\nFor more info, see: docs/embeddings/QUICKSTART_EMBEDDINGS.md")
    else:
        print("\n⚠️  Setup completed with warnings")
        print("\nPlease:")
        print("1. Configure your API keys in .env file")
        print("   - VOYAGE_API_KEY: Get from https://www.voyageai.com")
        print("   - MONGODB_URI: Get from MongoDB Atlas")
        print("2. Run this script again to verify")
        print("\nFor help, see: docs/embeddings/QUICKSTART_EMBEDDINGS.md")
    
    # Offer to run tests if everything is set up
    if all_passed:
        print("\n" + "-"*60)
        response = input("Would you like to run the test suite now? (y/n): ")
        if response.lower() in ['y', 'yes']:
            run_tests()


if __name__ == "__main__":
    main()

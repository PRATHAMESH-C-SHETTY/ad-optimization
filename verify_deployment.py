#!/usr/bin/env python3
"""
Deployment Verification Script
Use this to verify your project is ready for Netlify deployment
"""

import os
import sys
import subprocess
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_status(message, status=True):
    """Print status message with color"""
    symbol = f"{Colors.GREEN}✓{Colors.END}" if status else f"{Colors.RED}✗{Colors.END}"
    print(f"{symbol} {message}")

def print_info(message):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    exists = os.path.isfile(filepath)
    print_status(f"{description}: {filepath}", exists)
    return exists

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    exists = os.path.isdir(dirpath)
    print_status(f"{description}: {dirpath}", exists)
    return exists

def check_python_packages():
    """Check if required Python packages are installed"""
    print(f"\n{Colors.BLUE}Checking Python Packages...{Colors.END}")
    
    required_packages = [
        'Flask', 'pandas', 'numpy', 'sklearn', 'flask_sqlalchemy', 'flask_login'
    ]
    
    all_good = True
    for package in required_packages:
        try:
            __import__(package.lower().replace('_', '-'))
            print_status(f"Package '{package}' installed")
        except ImportError:
            print_status(f"Package '{package}' NOT found", False)
            all_good = False
    
    return all_good

def check_requirements_file():
    """Check requirements.txt"""
    print(f"\n{Colors.BLUE}Checking Requirements File...{Colors.END}")
    
    if not os.path.isfile('requirements.txt'):
        print_status("requirements.txt found", False)
        return False
    
    print_status("requirements.txt found")
    
    # Check for key packages
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    key_packages = ['Flask', 'pandas', 'scikit-learn', 'SQLAlchemy']
    for package in key_packages:
        if package.lower() in content.lower():
            print_status(f"  - {package} in requirements.txt")
        else:
            print_status(f"  - {package} in requirements.txt", False)
    
    return True

def check_netlify_config():
    """Check Netlify configuration"""
    print(f"\n{Colors.BLUE}Checking Netlify Configuration...{Colors.END}")
    
    checks = [
        ('netlify.toml', 'Netlify configuration file'),
        ('netlify/functions/app.py', 'Netlify serverless function'),
        ('package.json', 'Node.js package configuration'),
        ('runtime.txt', 'Python runtime specification'),
        ('.env.example', 'Environment variables example'),
    ]
    
    all_good = True
    for filepath, description in checks:
        if not check_file_exists(filepath, description):
            all_good = False
    
    return all_good

def check_deployment_docs():
    """Check deployment documentation"""
    print(f"\n{Colors.BLUE}Checking Deployment Documentation...{Colors.END}")
    
    docs = [
        ('NETLIFY_DEPLOYMENT_GUIDE.md', 'Netlify deployment guide'),
        ('QUICK_DEPLOY.md', 'Quick deployment guide'),
        ('DEPLOYMENT_CHECKLIST.md', 'Deployment checklist'),
        ('ALTERNATIVE_DEPLOYMENT.md', 'Alternative deployment options'),
    ]
    
    all_good = True
    for filepath, description in docs:
        if not check_file_exists(filepath, description):
            all_good = False
    
    return all_good

def check_git_setup():
    """Check Git setup"""
    print(f"\n{Colors.BLUE}Checking Git Configuration...{Colors.END}")
    
    if not os.path.isdir('.git'):
        print_status("Git repository found", False)
        return False
    
    print_status("Git repository found")
    
    try:
        result = subprocess.run(['git', 'status'], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        print_status("Git status check successful")
        return True
    except:
        print_status("Git status check failed", False)
        return False

def check_directory_structure():
    """Check project directory structure"""
    print(f"\n{Colors.BLUE}Checking Directory Structure...{Colors.END}")
    
    required_dirs = [
        ('static', 'Static files directory'),
        ('templates', 'HTML templates directory'),
        ('datasets', 'Data files directory'),
        ('models', 'ML models directory'),
        ('routes', 'Flask routes directory'),
        ('analytics', 'Analytics modules directory'),
        ('utils', 'Utility modules directory'),
        ('netlify/functions', 'Netlify functions directory'),
    ]
    
    all_good = True
    for dirpath, description in required_dirs:
        if not check_directory_exists(dirpath, description):
            all_good = False
    
    return all_good

def check_config():
    """Check application configuration"""
    print(f"\n{Colors.BLUE}Checking Application Configuration...{Colors.END}")
    
    try:
        from config import Config
        print_status("Config class imported successfully")
        
        # Check for required attributes
        required_attrs = ['SECRET_KEY', 'SQLALCHEMY_DATABASE_URI', 'UPLOAD_FOLDER']
        for attr in required_attrs:
            if hasattr(Config, attr):
                print_status(f"  - Config.{attr} defined")
            else:
                print_status(f"  - Config.{attr} defined", False)
        
        return True
    except ImportError as e:
        print_status(f"Config import failed: {e}", False)
        return False

def check_app_initialization():
    """Check if Flask app initializes correctly"""
    print(f"\n{Colors.BLUE}Checking Flask App Initialization...{Colors.END}")
    
    try:
        from app import create_app
        app = create_app()
        print_status("Flask app created successfully")
        
        # Check blueprints
        if app.blueprints:
            print_status(f"  Found {len(app.blueprints)} blueprints")
            for bp_name in app.blueprints:
                print(f"    - {bp_name}")
        
        return True
    except Exception as e:
        print_status(f"Flask app initialization failed: {e}", False)
        return False

def check_environment_variables():
    """Check environment variables setup"""
    print(f"\n{Colors.BLUE}Checking Environment Variables...{Colors.END}")
    
    required_vars = [
        'FLASK_ENV',
        'FLASK_APP',
        'SECRET_KEY',
        'DATABASE_URL',
    ]
    
    missing = []
    for var in required_vars:
        if os.environ.get(var):
            print_status(f"  - {var} set")
        else:
            print_warning(f"  - {var} not set (will use defaults)")
            missing.append(var)
    
    if missing:
        print_info(f"Set these in Netlify dashboard environment variables: {', '.join(missing)}")
    
    return True

def generate_report(results):
    """Generate summary report"""
    print(f"\n{Colors.BLUE}{'='*50}")
    print(f"DEPLOYMENT VERIFICATION REPORT")
    print(f"{'='*50}{Colors.END}\n")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    print(f"{Colors.GREEN}Passed: {passed}/{total}{Colors.END}")
    if failed > 0:
        print(f"{Colors.RED}Failed: {failed}/{total}{Colors.END}")
    
    if failed == 0:
        print(f"\n{Colors.GREEN}✓ Your project is ready for Netlify deployment!{Colors.END}")
        print_info("Next steps:")
        print_info("  1. Push to GitHub: git push origin main")
        print_info("  2. Go to https://netlify.com")
        print_info("  3. Connect your GitHub repository")
        print_info("  4. Follow QUICK_DEPLOY.md for complete setup")
    else:
        print(f"\n{Colors.RED}✗ Please fix the failed checks before deploying{Colors.END}")
        print_info("Review the items marked with ✗ above")
    
    print()

def main():
    """Run all checks"""
    print(f"{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║   Ad Optimization Platform - Deployment Verification   ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    # Change to project directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    results = {
        'Directory Structure': check_directory_structure(),
        'Netlify Configuration': check_netlify_config(),
        'Requirements File': check_requirements_file(),
        'Deployment Documentation': check_deployment_docs(),
        'Git Setup': check_git_setup(),
        'Configuration': check_config(),
        'App Initialization': check_app_initialization(),
        'Environment Variables': check_environment_variables(),
        'Python Packages': check_python_packages(),
    }
    
    generate_report(results)
    
    # Return exit code based on results
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()

"""
🚀 PyCon 25 Hackathon System Launcher
Intelligent Support Ticket Assignment System

Quick launcher for all system components and demos.
"""

import sys
import os
import subprocess
from pathlib import Path


def print_banner():
    """Print the system banner"""
    print("🏆" + "="*60 + "🏆")
    print("   PyCon 25 Hackathon Submission")
    print("   Intelligent Support Ticket Assignment System") 
    print("   by Sudhanshu")
    print("🏆" + "="*60 + "🏆")
    print()


def print_menu():
    """Print the main menu"""
    print("🚀 Choose what to run:")
    print()
    print("   1️⃣  GUI Application (Full System)")
    print("   2️⃣  Interactive Demo (All Features)")
    print("   3️⃣  Comprehensive Testing")
    print("   4️⃣  Priority Analyzer Only")
    print("   5️⃣  Assignment System Only")
    print("   6️⃣  Data Validator Only")
    print("   7️⃣  View System Status")
    print("   8️⃣  View Test Results")
    print("   9️⃣  Help & Documentation")
    print("   0️⃣  Exit")
    print()


def run_gui():
    """Launch the GUI application"""
    print("🎨 Launching GUI Application...")
    print("   (This will open the full system interface)")
    print()
    try:
        result = subprocess.run([sys.executable, "gui_application.py"], 
                              cwd=Path.cwd(), capture_output=False)
        if result.returncode == 0:
            print("✅ GUI application completed successfully")
        else:
            print("❌ GUI application encountered an error")
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")


def run_demo():
    """Launch the interactive demo"""
    print("🎭 Launching Interactive Demo...")
    print("   (This will demonstrate all system features)")
    print()
    try:
        result = subprocess.run([sys.executable, "hackathon_demo.py"], 
                              cwd=Path.cwd(), capture_output=False)
        if result.returncode == 0:
            print("✅ Demo completed successfully")
        else:
            print("❌ Demo encountered an error")
    except Exception as e:
        print(f"❌ Error launching demo: {e}")


def run_tests():
    """Run comprehensive testing"""
    print("🧪 Running Comprehensive Tests...")
    print("   (This will test all system components)")
    print()
    try:
        result = subprocess.run([sys.executable, "comprehensive_test.py"], 
                              cwd=Path.cwd(), capture_output=False)
        if result.returncode == 0:
            print("✅ Tests completed successfully")
        else:
            print("❌ Tests encountered errors")
    except Exception as e:
        print(f"❌ Error running tests: {e}")


def run_priority_analyzer():
    """Run priority analyzer only"""
    print("🔥 Running Priority Analyzer...")
    print("   (Testing priority detection on dataset)")
    print()
    try:
        result = subprocess.run([sys.executable, "priority_analyzer.py"], 
                              cwd=Path.cwd(), capture_output=False)
        if result.returncode == 0:
            print("✅ Priority analyzer completed successfully")
        else:
            print("❌ Priority analyzer encountered an error")
    except Exception as e:
        print(f"❌ Error running priority analyzer: {e}")


def run_assignment_system():
    """Run assignment system only"""
    print("🎯 Running Assignment System...")
    print("   (Processing full ticket assignment)")
    print()
    try:
        result = subprocess.run([sys.executable, "ticket_assignment_system.py"], 
                              cwd=Path.cwd(), capture_output=False)
        if result.returncode == 0:
            print("✅ Assignment system completed successfully")
        else:
            print("❌ Assignment system encountered an error")
    except Exception as e:
        print(f"❌ Error running assignment system: {e}")


def run_validator():
    """Run data validator only"""
    print("🔍 Running Data Validator...")
    print("   (Validating dataset quality)")
    print()
    try:
        result = subprocess.run([sys.executable, "enhanced_validator.py"], 
                              cwd=Path.cwd(), capture_output=False)
        if result.returncode == 0:
            print("✅ Data validator completed successfully")
        else:
            print("❌ Data validator encountered an error")
    except Exception as e:
        print(f"❌ Error running data validator: {e}")


def show_status():
    """Show system status and file information"""
    print("📊 System Status")
    print("-" * 40)
    
    # Check files
    required_files = [
        "dataset.json",
        "priority_analyzer.py", 
        "ticket_assignment_system.py",
        "enhanced_validator.py",
        "gui_application.py",
        "comprehensive_test.py",
        "hackathon_demo.py"
    ]
    
    output_files = [
        "output_result.json",
        "detailed_assignment_report.json", 
        "comprehensive_test_report.json"
    ]
    
    print("📁 Core Files:")
    for file in required_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            print(f"   ✅ {file} ({size:,} bytes)")
        else:
            print(f"   ❌ {file} (missing)")
    
    print("\n📄 Output Files:")
    for file in output_files:
        if Path(file).exists():
            size = Path(file).stat().st_size
            modified = Path(file).stat().st_mtime
            from datetime import datetime
            mod_time = datetime.fromtimestamp(modified).strftime("%Y-%m-%d %H:%M:%S")
            print(f"   ✅ {file} ({size:,} bytes, modified: {mod_time})")
        else:
            print(f"   ⏳ {file} (not generated yet)")
    
    # Check Python environment
    print(f"\n🐍 Python Environment:")
    print(f"   Version: {sys.version}")
    print(f"   Executable: {sys.executable}")
    
    # Check imports
    print(f"\n📦 Required Packages:")
    packages = ["tkinter", "matplotlib", "seaborn", "pandas"]
    for package in packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (not installed)")


def show_test_results():
    """Show latest test results"""
    print("📈 Latest Test Results")
    print("-" * 40)
    
    test_file = Path("comprehensive_test_report.json")
    if test_file.exists():
        try:
            import json
            with open(test_file, 'r') as f:
                results = json.load(f)
            
            summary = results.get('test_summary', {})
            print(f"🧪 Test Summary (from {results.get('test_timestamp', 'unknown')}):")
            print(f"   • Validation Tests: {summary.get('validation_tests', 0)}")
            print(f"   • Priority Tests: {summary.get('priority_tests', 0)}")
            print(f"   • Assignment Tests: {summary.get('assignment_tests', 0)}")
            print(f"   • Performance Tests: {summary.get('performance_tests', 0)}")
            print(f"   • Edge Case Tests: {summary.get('edge_case_tests', 0)}")
            
            # Show performance summary if available
            perf = results.get('performance_summary', {})
            if perf:
                print(f"\n⚡ Performance Summary:")
                print(f"   • Max Dataset: {perf.get('largest_dataset_tested', 'N/A')} tickets")
                print(f"   • Avg Validation Time: {perf.get('avg_validation_time', 0):.3f}s")
                print(f"   • Avg Assignment Time: {perf.get('avg_assignment_time', 0):.3f}s")
            
            # Show recommendations
            recommendations = results.get('recommendations', [])
            if recommendations:
                print(f"\n💡 Recommendations:")
                for rec in recommendations[:3]:
                    print(f"   • {rec}")
                    
        except Exception as e:
            print(f"❌ Error reading test results: {e}")
    else:
        print("⏳ No test results found. Run comprehensive tests first (option 3).")


def show_help():
    """Show help and documentation"""
    print("📚 Help & Documentation")
    print("-" * 40)
    print()
    print("🎯 What is this system?")
    print("   An intelligent support ticket assignment system that:")
    print("   • Analyzes ticket priority using keyword detection")
    print("   • Assigns tickets to best-matched agents")
    print("   • Validates data quality with 20+ rules") 
    print("   • Provides GUI interface and comprehensive testing")
    print()
    print("🚀 Quick Start:")
    print("   1. Run option 1 (GUI) for the complete system")
    print("   2. Run option 2 (Demo) to see all features")
    print("   3. Run option 3 (Tests) to validate everything works")
    print()
    print("📁 Key Files:")
    print("   • dataset.json - Sample data (100 tickets, 10 agents)")
    print("   • gui_application.py - Complete GUI interface")
    print("   • priority_analyzer.py - Keyword-based priority detection")
    print("   • ticket_assignment_system.py - Core assignment logic")
    print("   • enhanced_validator.py - Comprehensive data validation")
    print()
    print("📊 Output Files:")
    print("   • output_result.json - Assignment results")
    print("   • detailed_assignment_report.json - Analytics")
    print("   • comprehensive_test_report.json - Test results")
    print()
    print("🏆 For Hackathon Judges:")
    print("   • See HACKATHON_SUBMISSION.md for complete overview")
    print("   • Run the GUI (option 1) for visual demonstration")
    print("   • Run the demo (option 2) for feature walkthrough")
    print("   • Check test results (option 8) for validation")


def main():
    """Main launcher function"""
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input("🔥 Enter your choice (0-9): ").strip()
            print()
            
            if choice == "1":
                run_gui()
            elif choice == "2":
                run_demo()
            elif choice == "3":
                run_tests()
            elif choice == "4":
                run_priority_analyzer()
            elif choice == "5":
                run_assignment_system()
            elif choice == "6":
                run_validator()
            elif choice == "7":
                show_status()
            elif choice == "8":
                show_test_results()
            elif choice == "9":
                show_help()
            elif choice == "0":
                print("👋 Thank you for checking out our PyCon 25 Hackathon submission!")
                print("🏆 Intelligent Support Ticket Assignment System")
                print("✨ Built with ❤️ by Sudhanshu")
                break
            else:
                print("❌ Invalid choice. Please enter a number from 0-9.")
            
            print("\n" + "="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
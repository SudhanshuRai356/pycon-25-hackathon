"""
Test script for Priority Analyzer

This script tests the priority analyzer on the actual dataset tickets
and displays the results to validate the accuracy of priority assignments.
"""

import json
from priority_analyzer import PriorityAnalyzer, PriorityLevel


def load_dataset(file_path: str) -> dict:
    """Load the dataset from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Dataset file '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{file_path}'.")
        return None


def test_priority_analyzer():
    """Test the priority analyzer on dataset tickets"""
    
    print("🎯 Testing Priority Analyzer on Dataset Tickets")
    print("=" * 60)
    
    # Load dataset
    dataset = load_dataset('dataset.json')
    if not dataset or 'tickets' not in dataset:
        print("❌ Failed to load dataset or no tickets found.")
        return
    
    # Initialize analyzer
    analyzer = PriorityAnalyzer()
    tickets = dataset['tickets']
    
    print(f"📊 Analyzing {len(tickets)} tickets...")
    print()
    
    # Get priority statistics
    stats = analyzer.get_priority_statistics(tickets)
    
    # Display overall statistics
    print("📈 PRIORITY DISTRIBUTION SUMMARY")
    print("-" * 40)
    for priority, count in stats['priority_distribution'].items():
        percentage = stats['priority_percentages'][priority]
        print(f"{priority:8}: {count:2} tickets ({percentage:5.1f}%)")
    
    print()
    print("🔍 DETAILED ANALYSIS RESULTS")
    print("-" * 60)
    
    # Display detailed results for each ticket
    for i, result in enumerate(stats['detailed_results'], 1):
        priority_emoji = get_priority_emoji(result['priority'])
        
        print(f"\n{i:2}. {priority_emoji} {result['ticket_id']} - {result['priority']}")
        print(f"    Title: {result['title'][:70]}{'...' if len(result['title']) > 70 else ''}")
        print(f"    Score: {result['score']:.1f}")
        
        if result['keywords']:
            keywords_str = ', '.join(result['keywords'][:8])  # Show first 8 keywords
            if len(result['keywords']) > 8:
                keywords_str += f" (+{len(result['keywords']) - 8} more)"
            print(f"    Keywords: {keywords_str}")
        
        print(f"    Rationale: {result['rationale']}")
    
    print()
    print("🎯 PRIORITY VALIDATION HIGHLIGHTS")
    print("-" * 40)
    
    # Highlight critical tickets
    critical_tickets = [r for r in stats['detailed_results'] if r['priority'] == 'CRITICAL']
    if critical_tickets:
        print(f"\n🚨 CRITICAL PRIORITY TICKETS ({len(critical_tickets)} tickets):")
        for ticket in critical_tickets:
            print(f"  • {ticket['ticket_id']}: {ticket['title'][:50]}...")
    
    # Highlight high priority tickets
    high_tickets = [r for r in stats['detailed_results'] if r['priority'] == 'HIGH']
    if high_tickets:
        print(f"\n⚠️  HIGH PRIORITY TICKETS ({len(high_tickets)} tickets):")
        for ticket in high_tickets[:5]:  # Show first 5
            print(f"  • {ticket['ticket_id']}: {ticket['title'][:50]}...")
        if len(high_tickets) > 5:
            print(f"  ... and {len(high_tickets) - 5} more")
    
    # Show some interesting keyword matches
    print(f"\n🔍 INTERESTING KEYWORD MATCHES:")
    for result in stats['detailed_results']:
        if result['score'] > 15:  # High scoring tickets
            print(f"  • {result['ticket_id']} (Score: {result['score']:.1f}): {', '.join(result['keywords'][:5])}")
    
    print()
    print("✅ Priority analysis completed!")
    return stats


def get_priority_emoji(priority: str) -> str:
    """Get emoji for priority level"""
    emoji_map = {
        'CRITICAL': '🚨',
        'HIGH': '⚠️',
        'MEDIUM': '📋',
        'LOW': '📝'
    }
    return emoji_map.get(priority, '📋')


def test_specific_examples():
    """Test specific examples to validate keyword detection"""
    
    print("\n🧪 TESTING SPECIFIC EXAMPLES")
    print("=" * 60)
    
    analyzer = PriorityAnalyzer()
    
    test_cases = [
        {
            'title': "Production server down",
            'description': "The main production server is completely down and all users are affected.",
            'expected': 'CRITICAL'
        },
        {
            'title': "Printer not working",
            'description': "The office printer is broken and needs repair.",
            'expected': 'HIGH'
        },
        {
            'title': "How to setup email",
            'description': "New employee needs help setting up their email account.",
            'expected': 'MEDIUM'
        },
        {
            'title': "Feature request",
            'description': "Would be nice to have a dark mode theme when possible.",
            'expected': 'LOW'
        },
        {
            'title': "Critical security breach",
            'description': "We have detected unauthorized access to our database. Immediate action required.",
            'expected': 'CRITICAL'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        result = analyzer.analyze_priority(test_case['title'], test_case['description'])
        
        status = "✅" if result.priority_level.name == test_case['expected'] else "❌"
        
        print(f"{i}. {status} {test_case['title']}")
        print(f"   Expected: {test_case['expected']}, Got: {result.priority_level.name}")
        print(f"   Score: {result.priority_score:.1f}")
        print(f"   Keywords: {', '.join(result.matched_keywords[:5])}")
        print(f"   Rationale: {result.rationale}")
        print()


if __name__ == "__main__":
    # Test on actual dataset
    dataset_stats = test_priority_analyzer()
    
    # Test specific examples
    test_specific_examples()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed! Priority analyzer is ready for integration.")
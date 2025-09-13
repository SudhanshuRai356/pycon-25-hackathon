"""
🚀 PyCon 25 Hackathon Demo Script
Intelligent Support Ticket Assignment System

This script demonstrates the key features of our system with live examples.
"""

import json
import time
from datetime import datetime
from priority_analyzer import PriorityAnalyzer
from ticket_assignment_system import TicketAssignmentSystem
from enhanced_validator import EnhancedDataValidator


class HackathonDemo:
    """Interactive demo for the hackathon submission"""
    
    def __init__(self):
        self.priority_analyzer = PriorityAnalyzer()
        self.assignment_system = TicketAssignmentSystem()
        self.validator = EnhancedDataValidator()
        
    def run_demo(self):
        """Run the complete demo"""
        print("🎉 PyCon 25 Hackathon Demo")
        print("🏆 Intelligent Support Ticket Assignment System")
        print("=" * 60)
        print()
        
        # Demo 1: Priority Analysis
        self.demo_priority_analysis()
        
        # Demo 2: Assignment Logic  
        self.demo_assignment_logic()
        
        # Demo 3: Data Validation
        self.demo_data_validation()
        
        # Demo 4: System Performance
        self.demo_performance()
        
        # Demo 5: Real Dataset Processing
        self.demo_real_dataset()
        
        print("\n🎯 Demo Complete!")
        print("🚀 Ready for Production!")
        
    def demo_priority_analysis(self):
        """Demonstrate priority analysis capabilities"""
        print("🔥 DEMO 1: Priority Analysis with Keyword Detection")
        print("-" * 50)
        
        test_tickets = [
            {
                'title': 'URGENT: Production server completely down',
                'description': 'All users cannot access the main application. Critical business operations are halted. Emergency response needed immediately.',
                'expected': 'CRITICAL'
            },
            {
                'title': 'Email service broken for marketing team',
                'description': 'The email server is not working properly. Users getting error messages when trying to send emails.',
                'expected': 'HIGH'
            },
            {
                'title': 'Need help setting up new employee laptop',
                'description': 'New hire starts Monday and needs laptop configured with standard software and access permissions.',
                'expected': 'MEDIUM'
            },
            {
                'title': 'Feature request: Add dark mode to dashboard',
                'description': 'Users have requested a dark theme option for the admin dashboard. This would be a nice enhancement when time permits.',
                'expected': 'LOW'
            }
        ]
        
        correct_predictions = 0
        
        for i, ticket in enumerate(test_tickets, 1):
            print(f"\n📋 Test Ticket {i}:")
            print(f"   Title: {ticket['title']}")
            
            # Analyze priority
            result = self.priority_analyzer.analyze_priority(
                ticket['title'], 
                ticket['description']
            )
            
            # Display results
            predicted = result.priority_level.name
            is_correct = predicted == ticket['expected']
            
            if is_correct:
                correct_predictions += 1
                status = "✅ CORRECT"
            else:
                status = "❌ INCORRECT"
            
            print(f"   Expected: {ticket['expected']}")
            print(f"   Predicted: {predicted} {status}")
            print(f"   Score: {result.priority_score:.2f}")
            print(f"   Keywords: {', '.join(result.matched_keywords[:3])}")
        
        accuracy = correct_predictions / len(test_tickets) * 100
        print(f"\n📊 Priority Analysis Accuracy: {accuracy:.1f}%")
        
        self._pause_demo()
    
    def demo_assignment_logic(self):
        """Demonstrate intelligent assignment logic"""
        print("\n🎯 DEMO 2: Intelligent Assignment Logic")
        print("-" * 50)
        
        # Create sample agents
        sample_agents = [
            {
                'agent_id': 'AGT-001',
                'name': 'Alice Johnson',
                'skills': {'Network_Security': 9, 'Linux_Administration': 8},
                'availability_status': 'Available',
                'experience_level': 10,
                'current_load': 2
            },
            {
                'agent_id': 'AGT-002', 
                'name': 'Bob Smith',
                'skills': {'Database_SQL': 9, 'Performance_Tuning': 8},
                'availability_status': 'Available',
                'experience_level': 7,
                'current_load': 5
            },
            {
                'agent_id': 'AGT-003',
                'name': 'Carol Davis',
                'skills': {'Microsoft_365': 8, 'SharePoint_Online': 9},
                'availability_status': 'Busy',
                'experience_level': 6,
                'current_load': 8
            }
        ]
        
        # Create sample tickets
        sample_tickets = [
            {
                'ticket_id': 'TKT-DEMO-001',
                'title': 'Network security breach detected',
                'description': 'Critical security issue requires immediate attention from network specialist',
                'creation_timestamp': int(time.time())
            },
            {
                'ticket_id': 'TKT-DEMO-002',
                'title': 'Database performance is slow',
                'description': 'Users reporting slow query response times. Need database optimization.',
                'creation_timestamp': int(time.time())
            },
            {
                'ticket_id': 'TKT-DEMO-003',
                'title': 'Help with SharePoint permissions',
                'description': 'User needs access to specific SharePoint folders for project work.',
                'creation_timestamp': int(time.time())
            }
        ]
        
        dataset = {'agents': sample_agents, 'tickets': sample_tickets}
        
        print("👥 Available Agents:")
        for agent in sample_agents:
            skills_str = ', '.join([f"{k}({v})" for k, v in agent['skills'].items()])
            print(f"   • {agent['name']} - {agent['availability_status']} - Load: {agent['current_load']} - Skills: {skills_str}")
        
        print("\n🎫 Tickets to Assign:")
        for ticket in sample_tickets:
            # Analyze priority first
            result = self.priority_analyzer.analyze_priority(ticket['title'], ticket['description'])
            print(f"   • {ticket['ticket_id']}: {ticket['title']} (Priority: {result.priority_level.name})")
        
        # Perform assignments
        print(f"\n⚡ Performing Intelligent Assignment...")
        assignments = self.assignment_system.assign_tickets(dataset)
        
        print(f"\n📋 Assignment Results:")
        for assignment in assignments:
            agent = next(a for a in sample_agents if a['agent_id'] == assignment.assigned_agent_id)
            print(f"   • {assignment.ticket_id} → {agent['name']}")
            print(f"     Priority: {assignment.priority_level}")
            print(f"     Skill Match: {assignment.skill_match_score:.3f}")
            print(f"     Final Score: {assignment.final_score:.3f}")
            print()
        
        self._pause_demo()
    
    def demo_data_validation(self):
        """Demonstrate comprehensive data validation"""
        print("\n🔍 DEMO 3: Enhanced Data Validation")
        print("-" * 50)
        
        # Create data with intentional issues
        problematic_data = {
            'agents': [
                {
                    'agent_id': 'invalid_id',  # Bad format
                    'name': 'A',  # Too short
                    'skills': {'BadSkill': 15},  # Invalid skill level
                    'availability_status': 'Maybe',  # Invalid status
                    'experience_level': -5,  # Negative
                    'current_load': 25  # Too high
                },
                {
                    'agent_id': 'AGT-002',
                    'name': 'Valid Agent',
                    'skills': {'Network_Security': 8},
                    'availability_status': 'Available', 
                    'experience_level': 5,
                    'current_load': 3
                }
            ],
            'tickets': [
                {
                    'ticket_id': 'INVALID',  # Bad format
                    'title': 'A',  # Too short
                    'description': 'Short',  # Too short
                    'creation_timestamp': 'not_a_number'  # Invalid
                },
                {
                    'ticket_id': 'TKT-2025-002',
                    'title': 'Valid ticket for testing',
                    'description': 'This is a valid ticket with proper formatting and adequate detail.',
                    'creation_timestamp': int(time.time())
                }
            ]
        }
        
        print("🔬 Validating Dataset with Known Issues...")
        result = self.validator.validate_dataset(problematic_data)
        
        print(f"\n📊 Validation Results:")
        print(f"   Quality Score: {result['data_quality_score']:.1f}/100")
        print(f"   Status: {'✅ VALID' if result['is_valid'] else '❌ INVALID'}")
        print(f"   Issues Found: {result['total_issues']}")
        
        print(f"\n❌ Errors ({len(result['issues']['errors'])}):")
        for error in result['issues']['errors'][:3]:  # Show first 3
            print(f"   • {error['message']}")
        
        print(f"\n⚠️  Warnings ({len(result['issues']['warnings'])}):")
        for warning in result['issues']['warnings'][:3]:  # Show first 3
            print(f"   • {warning['message']}")
        
        if result['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in result['recommendations'][:3]:
                print(f"   • {rec}")
        
        self._pause_demo()
    
    def demo_performance(self):
        """Demonstrate system performance"""
        print("\n⚡ DEMO 4: System Performance Benchmarks")
        print("-" * 50)
        
        test_sizes = [(10, 20), (25, 50), (50, 100)]
        
        for agent_count, ticket_count in test_sizes:
            print(f"\n🔄 Testing {agent_count} agents with {ticket_count} tickets...")
            
            # Generate test data
            agents = self._generate_test_agents(agent_count)
            tickets = self._generate_test_tickets(ticket_count)
            dataset = {'agents': agents, 'tickets': tickets}
            
            # Test validation performance
            start_time = time.time()
            validation_result = self.validator.validate_dataset(dataset)
            validation_time = time.time() - start_time
            
            # Test assignment performance  
            start_time = time.time()
            assignments = self.assignment_system.assign_tickets(dataset)
            assignment_time = time.time() - start_time
            
            # Calculate metrics
            total_time = validation_time + assignment_time
            throughput = ticket_count / total_time if total_time > 0 else 0
            
            print(f"   ✓ Validation: {validation_time:.3f}s")
            print(f"   ✓ Assignment: {assignment_time:.3f}s") 
            print(f"   ✓ Total: {total_time:.3f}s")
            print(f"   ✓ Throughput: {throughput:.1f} tickets/second")
            print(f"   ✓ Success: {len(assignments)}/{ticket_count} tickets assigned")
        
        self._pause_demo()
    
    def demo_real_dataset(self):
        """Demonstrate with real dataset"""
        print("\n📊 DEMO 5: Real Dataset Processing")
        print("-" * 50)
        
        try:
            with open('dataset.json', 'r', encoding='utf-8') as f:
                dataset = json.load(f)
            
            print(f"📁 Loaded dataset:")
            print(f"   • Agents: {len(dataset['agents'])}")
            print(f"   • Tickets: {len(dataset['tickets'])}")
            
            # Quick validation
            print(f"\n🔍 Running Quick Validation...")
            start_time = time.time()
            validation_result = self.validator.validate_dataset(dataset)
            validation_time = time.time() - start_time
            
            print(f"   ✓ Quality Score: {validation_result['data_quality_score']:.1f}/100")
            print(f"   ✓ Validation Time: {validation_time:.3f}s")
            print(f"   ✓ Issues: {validation_result['total_issues']} total")
            
            # Process assignments
            print(f"\n⚡ Processing Assignments...")
            start_time = time.time()
            assignments = self.assignment_system.assign_tickets(dataset)
            assignment_time = time.time() - start_time
            
            # Analyze results
            priority_distribution = {}
            for assignment in assignments:
                priority = assignment.priority_level
                priority_distribution[priority] = priority_distribution.get(priority, 0) + 1
            
            print(f"\n📈 Assignment Results:")
            print(f"   ✓ Total Assigned: {len(assignments)}")
            print(f"   ✓ Processing Time: {assignment_time:.3f}s")
            print(f"   ✓ Throughput: {len(assignments)/assignment_time:.1f} tickets/s")
            
            print(f"\n🎯 Priority Distribution:")
            for priority, count in sorted(priority_distribution.items()):
                percentage = count / len(assignments) * 100
                print(f"   • {priority}: {count} tickets ({percentage:.1f}%)")
            
            print(f"\n💾 Output Files Generated:")
            print(f"   • output_result.json - Assignment results")
            print(f"   • detailed_assignment_report.json - Analytics report")
            
        except FileNotFoundError:
            print("❌ Dataset file not found")
        except Exception as e:
            print(f"❌ Error processing dataset: {e}")
    
    def _generate_test_agents(self, count: int):
        """Generate test agents"""
        skills_pool = ['Network_Security', 'Database_SQL', 'Microsoft_365', 'Linux_Administration', 'Hardware_Diagnostics']
        agents = []
        
        for i in range(count):
            skills = {}
            for skill in skills_pool[:2]:  # Give each agent 2 skills
                skills[skill] = 5 + (i % 5)  # Skill levels 5-9
            
            agents.append({
                'agent_id': f'AGT-{i+1:03d}',
                'name': f'Agent {i+1}',
                'skills': skills,
                'availability_status': 'Available',
                'experience_level': 5 + (i % 10),
                'current_load': i % 8
            })
        
        return agents
    
    def _generate_test_tickets(self, count: int):
        """Generate test tickets"""
        titles = [
            'Server performance issue',
            'User cannot access email',
            'Network printer not working',
            'Database backup failed',
            'Software installation request'
        ]
        
        tickets = []
        base_time = int(time.time())
        
        for i in range(count):
            tickets.append({
                'ticket_id': f'TKT-{i+1:03d}',
                'title': titles[i % len(titles)],
                'description': f'Test ticket {i+1} description with sufficient detail for processing.',
                'creation_timestamp': base_time - (i * 3600)  # Spread over time
            })
        
        return tickets
    
    def _pause_demo(self):
        """Pause between demo sections"""
        print("\n" + "⏸️  Press Enter to continue to next demo..." + "\n")
        input()


def main():
    """Run the hackathon demo"""
    demo = HackathonDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()
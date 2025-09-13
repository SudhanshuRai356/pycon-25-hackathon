"""
Comprehensive Test Suite for Enhanced Ticket Assignment System

This script tests the complete system with various data scenarios,
edge cases, and validation constraints.
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List
import random

# Import our modules
from enhanced_validator import EnhancedDataValidator
from priority_analyzer import PriorityAnalyzer
from ticket_assignment_system import TicketAssignmentSystem


class TestDataGenerator:
    """Generate test data with various scenarios"""
    
    def __init__(self):
        self.skill_categories = {
            'Networking': ['VPN_Troubleshooting', 'Firewall_Configuration', 'Network_Security'],
            'Systems': ['Linux_Administration', 'Windows_Server_2022', 'Hardware_Diagnostics'],
            'Cloud': ['Cloud_AWS', 'Virtualization_VMware', 'SaaS_Integrations'],
            'Security': ['Network_Security', 'Identity_Management', 'Firewall_Configuration'],
            'Database': ['Database_SQL', 'Data_Backup', 'Performance_Tuning'],
            'Applications': ['Microsoft_365', 'SharePoint_Online', 'PowerShell_Scripting']
        }
        
        self.ticket_scenarios = [
            # Critical scenarios
            {
                'priority': 'CRITICAL',
                'keywords': ['down', 'outage', 'critical', 'emergency', 'security breach'],
                'descriptions': [
                    "Production server is completely down and all users are affected",
                    "Critical security breach detected in our network infrastructure",
                    "Database server crashed and backup systems are failing",
                    "Network outage affecting entire building with business operations halted"
                ]
            },
            # High priority scenarios
            {
                'priority': 'HIGH',
                'keywords': ['broken', 'failing', 'not working', 'error', 'urgent'],
                'descriptions': [
                    "Email server is intermittently failing and users cannot send messages",
                    "VPN connection dropping frequently for remote workers",
                    "Printer network issues affecting multiple departments",
                    "User authentication problems with Active Directory"
                ]
            },
            # Medium priority scenarios
            {
                'priority': 'MEDIUM',
                'keywords': ['help', 'request', 'setup', 'configure', 'support'],
                'descriptions': [
                    "New employee needs laptop setup and software installation",
                    "Request for additional SharePoint permissions for project team",
                    "Help with configuring email client on mobile device",
                    "Software license request for Adobe Creative Suite"
                ]
            },
            # Low priority scenarios
            {
                'priority': 'LOW',
                'keywords': ['enhancement', 'feature request', 'optimization', 'when possible'],
                'descriptions': [
                    "Feature request for dark mode in company application",
                    "Optimization suggestion for database query performance",
                    "Request for additional dashboard widgets when convenient",
                    "Enhancement request for reporting functionality"
                ]
            }
        ]
    
    def generate_test_agents(self, count: int = 10, scenario: str = "normal") -> List[Dict]:
        """Generate test agents with different scenarios"""
        agents = []
        
        for i in range(count):
            agent_id = f"agent_{i+1:03d}"
            name = self._generate_agent_name()
            
            # Generate skills based on scenario
            if scenario == "normal":
                skills = self._generate_normal_skills()
            elif scenario == "specialized":
                skills = self._generate_specialized_skills()
            elif scenario == "unbalanced":
                skills = self._generate_unbalanced_skills()
            elif scenario == "minimal":
                skills = self._generate_minimal_skills()
            else:
                skills = self._generate_normal_skills()
            
            # Generate other attributes
            experience = random.randint(1, 20) if scenario != "minimal" else random.randint(0, 3)
            current_load = random.randint(0, 8) if scenario != "overloaded" else random.randint(8, 15)
            
            availability_options = ['Available', 'Busy', 'Offline', 'On Leave']
            if scenario == "unavailable":
                availability = random.choice(['Busy', 'Offline', 'On Leave'])
            else:
                availability = random.choices(availability_options, weights=[70, 20, 5, 5])[0]
            
            agent = {
                'agent_id': agent_id,
                'name': name,
                'skills': skills,
                'current_load': current_load,
                'availability_status': availability,
                'experience_level': experience
            }
            
            agents.append(agent)
        
        return agents
    
    def generate_test_tickets(self, count: int = 50, scenario: str = "normal") -> List[Dict]:
        """Generate test tickets with different scenarios"""
        tickets = []
        base_timestamp = int(datetime.now().timestamp()) - (30 * 24 * 60 * 60)  # 30 days ago
        
        for i in range(count):
            ticket_id = f"TKT-2025-{i+1:03d}"
            
            # Select scenario type
            if scenario == "critical_heavy":
                scenario_weights = [40, 30, 20, 10]  # More critical tickets
            elif scenario == "routine_heavy":
                scenario_weights = [10, 20, 40, 30]  # More routine tickets
            elif scenario == "mixed":
                scenario_weights = [25, 25, 25, 25]  # Even distribution
            else:
                scenario_weights = [20, 35, 35, 10]  # Normal distribution
            
            scenario_type = random.choices(self.ticket_scenarios, weights=scenario_weights)[0]
            
            # Generate title and description
            title = self._generate_ticket_title(scenario_type)
            description = self._generate_ticket_description(scenario_type)
            
            # Generate timestamp (spread over last 30 days)
            days_offset = random.randint(0, 30)
            hours_offset = random.randint(0, 23)
            timestamp = base_timestamp + (days_offset * 24 * 60 * 60) + (hours_offset * 60 * 60)
            
            ticket = {
                'ticket_id': ticket_id,
                'title': title,
                'description': description,
                'creation_timestamp': timestamp
            }
            
            tickets.append(ticket)
        
        return tickets
    
    def generate_edge_case_data(self) -> Dict:
        """Generate data with edge cases for testing validation"""
        return {
            'agents': [
                # Valid agent
                {
                    'agent_id': 'agent_001',
                    'name': 'John Doe',
                    'skills': {'Networking': 8, 'Security': 6},
                    'availability_status': 'Available',
                    'experience_level': 5,
                    'current_load': 3
                },
                # Agent with validation issues
                {
                    'agent_id': 'invalid_id',  # Invalid format
                    'name': 'A',  # Too short
                    'skills': {'BadSkill': 15},  # Invalid skill level
                    'availability_status': 'Maybe',  # Invalid status
                    'experience_level': -5,  # Negative experience
                    'current_load': 25  # Too high load
                },
                # Agent with missing fields
                {
                    'agent_id': 'agent_003',
                    'name': 'Jane Smith'
                    # Missing skills, availability, etc.
                },
                # Duplicate agent_id
                {
                    'agent_id': 'agent_001',  # Duplicate
                    'name': 'Another John',
                    'skills': {'Database': 7},
                    'availability_status': 'Available',
                    'experience_level': 10,
                    'current_load': 2
                }
            ],
            'tickets': [
                # Valid ticket
                {
                    'ticket_id': 'TKT-2025-001',
                    'title': 'Network connectivity issue',
                    'description': 'Users unable to access shared resources due to network connectivity problems',
                    'creation_timestamp': int(datetime.now().timestamp())
                },
                # Ticket with validation issues
                {
                    'ticket_id': 'INVALID',  # Invalid format
                    'title': 'A',  # Too short
                    'description': 'Short',  # Too short
                    'creation_timestamp': 'not_a_number'  # Invalid timestamp
                },
                # Ticket with missing fields
                {
                    'ticket_id': 'TKT-2025-003'
                    # Missing title, description, timestamp
                },
                # Future-dated ticket
                {
                    'ticket_id': 'TKT-2025-004',
                    'title': 'Future ticket for testing',
                    'description': 'This ticket is dated in the future to test validation',
                    'creation_timestamp': int((datetime.now() + timedelta(days=30)).timestamp())
                },
                # Duplicate ticket_id
                {
                    'ticket_id': 'TKT-2025-001',  # Duplicate
                    'title': 'Another network issue',
                    'description': 'Different network problem with same ID',
                    'creation_timestamp': int(datetime.now().timestamp())
                }
            ]
        }
    
    def _generate_agent_name(self) -> str:
        """Generate realistic agent names"""
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa', 
                      'Christopher', 'Jessica', 'Matthew', 'Ashley', 'Joshua', 'Amanda', 'Daniel']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
                     'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson']
        
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _generate_normal_skills(self) -> Dict:
        """Generate normal skill distribution"""
        skills = {}
        num_skills = random.randint(3, 7)
        
        # Select random categories
        categories = random.sample(list(self.skill_categories.keys()), 
                                 min(num_skills, len(self.skill_categories)))
        
        for category in categories:
            skill_options = self.skill_categories[category]
            skill = random.choice(skill_options)
            level = random.randint(4, 9)  # Most agents have mid to high skills
            skills[skill] = level
        
        return skills
    
    def _generate_specialized_skills(self) -> Dict:
        """Generate highly specialized skills (few but high-level)"""
        skills = {}
        category = random.choice(list(self.skill_categories.keys()))
        skill_options = self.skill_categories[category]
        
        # 1-3 skills but very high levels
        for skill in random.sample(skill_options, min(random.randint(1, 3), len(skill_options))):
            skills[skill] = random.randint(8, 10)
        
        return skills
    
    def _generate_unbalanced_skills(self) -> Dict:
        """Generate unbalanced skills (mix of very high and very low)"""
        skills = {}
        num_skills = random.randint(4, 8)
        
        all_skills = [skill for skill_list in self.skill_categories.values() for skill in skill_list]
        selected_skills = random.sample(all_skills, min(num_skills, len(all_skills)))
        
        for skill in selected_skills:
            # Either very high or very low
            level = random.choice([random.randint(1, 3), random.randint(8, 10)])
            skills[skill] = level
        
        return skills
    
    def _generate_minimal_skills(self) -> Dict:
        """Generate minimal skills (1-2 low-level skills)"""
        skills = {}
        num_skills = random.randint(1, 2)
        
        all_skills = [skill for skill_list in self.skill_categories.values() for skill in skill_list]
        selected_skills = random.sample(all_skills, num_skills)
        
        for skill in selected_skills:
            skills[skill] = random.randint(1, 4)
        
        return skills
    
    def _generate_ticket_title(self, scenario_type: Dict) -> str:
        """Generate realistic ticket titles"""
        keywords = scenario_type['keywords']
        
        title_templates = [
            f"Server {random.choice(keywords)} in production environment",
            f"User cannot access system - {random.choice(keywords)}",
            f"Network printer {random.choice(keywords)} - urgent attention needed",
            f"Database {random.choice(keywords)} affecting multiple applications",
            f"Email service {random.choice(keywords)} for entire department",
            f"VPN connection {random.choice(keywords)} for remote users",
            f"Application {random.choice(keywords)} - need immediate support",
            f"Hardware {random.choice(keywords)} - laptop replacement needed"
        ]
        
        return random.choice(title_templates)
    
    def _generate_ticket_description(self, scenario_type: Dict) -> str:
        """Generate realistic ticket descriptions"""
        base_descriptions = scenario_type['descriptions']
        base = random.choice(base_descriptions)
        
        # Add technical details
        technical_details = [
            "Error logs show connection timeout messages.",
            "Multiple users have reported the same issue.",
            "The problem started this morning around 9 AM.",
            "Restart attempts have been unsuccessful.",
            "No recent system changes or updates were made.",
            "The issue is affecting business operations.",
            "Temporary workarounds are not available.",
            "Similar incidents occurred last month."
        ]
        
        # Add 1-3 technical details
        additional_details = random.sample(technical_details, random.randint(1, 3))
        
        return f"{base}. {' '.join(additional_details)}"


class SystemTester:
    """Comprehensive system testing"""
    
    def __init__(self):
        self.validator = EnhancedDataValidator()
        self.priority_analyzer = PriorityAnalyzer()
        self.assignment_system = TicketAssignmentSystem()
        self.data_generator = TestDataGenerator()
        
        self.test_results = {
            'validation_tests': [],
            'priority_tests': [],
            'assignment_tests': [],
            'performance_tests': [],
            'edge_case_tests': []
        }
    
    def run_comprehensive_tests(self):
        """Run all test scenarios"""
        print("🧪 Starting Comprehensive System Testing")
        print("=" * 60)
        
        # Test 1: Data Validation
        print("\n1️⃣ Testing Data Validation...")
        self.test_data_validation()
        
        # Test 2: Priority Analysis
        print("\n2️⃣ Testing Priority Analysis...")
        self.test_priority_analysis()
        
        # Test 3: Assignment Logic
        print("\n3️⃣ Testing Assignment Logic...")
        self.test_assignment_logic()
        
        # Test 4: Performance Testing
        print("\n4️⃣ Testing Performance...")
        self.test_performance()
        
        # Test 5: Edge Cases
        print("\n5️⃣ Testing Edge Cases...")
        self.test_edge_cases()
        
        # Generate test report
        print("\n📊 Generating Test Report...")
        self.generate_test_report()
        
        print("\n✅ All tests completed!")
    
    def test_data_validation(self):
        """Test data validation with various scenarios"""
        test_scenarios = [
            ("Normal Dataset", "normal", "normal"),
            ("Specialized Agents", "specialized", "normal"),
            ("Critical Heavy Tickets", "normal", "critical_heavy"),
            ("Unavailable Agents", "unavailable", "normal"),
            ("Edge Cases", "edge_cases", "edge_cases")
        ]
        
        for scenario_name, agent_scenario, ticket_scenario in test_scenarios:
            print(f"  Testing: {scenario_name}")
            
            if scenario_name == "Edge Cases":
                dataset = self.data_generator.generate_edge_case_data()
            else:
                agents = self.data_generator.generate_test_agents(10, agent_scenario)
                tickets = self.data_generator.generate_test_tickets(25, ticket_scenario)
                dataset = {'agents': agents, 'tickets': tickets}
            
            # Run validation
            start_time = time.time()
            result = self.validator.validate_dataset(dataset)
            validation_time = time.time() - start_time
            
            self.test_results['validation_tests'].append({
                'scenario': scenario_name,
                'is_valid': result['is_valid'],
                'error_count': len(result['issues']['errors']),
                'warning_count': len(result['issues']['warnings']),
                'quality_score': result['data_quality_score'],
                'validation_time': validation_time,
                'recommendations_count': len(result['recommendations'])
            })
            
            print(f"    ✓ Quality Score: {result['data_quality_score']:.1f}/100")
            print(f"    ✓ Issues: {len(result['issues']['errors'])} errors, {len(result['issues']['warnings'])} warnings")
    
    def test_priority_analysis(self):
        """Test priority analysis accuracy"""
        test_cases = [
            ("Server completely down", "CRITICAL", ["down", "server"]),
            ("Email not working for user", "HIGH", ["not working", "email"]),
            ("Need help with setup", "MEDIUM", ["help", "setup"]),
            ("Feature request for enhancement", "LOW", ["feature request", "enhancement"]),
            ("URGENT: Production database crashed!", "CRITICAL", ["urgent", "crashed", "production", "database"]),
            ("Printer ink needs replacing", "MEDIUM", ["printer", "replacing"]),
            ("Security breach detected immediately", "CRITICAL", ["security breach", "immediately"]),
            ("Slow performance on laptop", "HIGH", ["slow", "performance", "laptop"])
        ]
        
        correct_predictions = 0
        
        for title, expected_priority, expected_keywords in test_cases:
            description = f"Test case for {title.lower()}. Multiple users affected. Need resolution."
            
            result = self.priority_analyzer.analyze_priority(title, description)
            predicted_priority = result.priority_level.name
            
            is_correct = predicted_priority == expected_priority
            if is_correct:
                correct_predictions += 1
            
            # Check keyword detection
            keywords_found = sum(1 for keyword in expected_keywords 
                               if keyword.lower() in [k.lower() for k in result.matched_keywords])
            
            self.test_results['priority_tests'].append({
                'title': title,
                'expected': expected_priority,
                'predicted': predicted_priority,
                'correct': is_correct,
                'score': result.priority_score,
                'keywords_expected': len(expected_keywords),
                'keywords_found': keywords_found,
                'keywords_detected': result.matched_keywords
            })
            
            status = "✓" if is_correct else "✗"
            print(f"  {status} {title}: {predicted_priority} (expected {expected_priority})")
        
        accuracy = correct_predictions / len(test_cases) * 100
        print(f"  📊 Priority Analysis Accuracy: {accuracy:.1f}%")
    
    def test_assignment_logic(self):
        """Test ticket assignment logic"""
        print("  Testing assignment scenarios...")
        
        scenarios = [
            ("Balanced Workload", "normal", "normal"),
            ("High Priority Focus", "normal", "critical_heavy"),
            ("Specialized Skills", "specialized", "normal"),
            ("Limited Availability", "unavailable", "normal")
        ]
        
        for scenario_name, agent_scenario, ticket_scenario in scenarios:
            print(f"    Testing: {scenario_name}")
            
            agents = self.data_generator.generate_test_agents(8, agent_scenario)
            tickets = self.data_generator.generate_test_tickets(20, ticket_scenario)
            dataset = {'agents': agents, 'tickets': tickets}
            
            start_time = time.time()
            assignments = self.assignment_system.assign_tickets(dataset)
            assignment_time = time.time() - start_time
            
            # Analyze assignment quality
            priority_distribution = {}
            agent_loads = {}
            skill_matches = []
            
            for assignment in assignments:
                # Priority distribution
                priority = assignment.priority_level
                priority_distribution[priority] = priority_distribution.get(priority, 0) + 1
                
                # Agent loads
                agent_id = assignment.assigned_agent_id
                agent_loads[agent_id] = agent_loads.get(agent_id, 0) + 1
                
                # Skill match scores
                skill_matches.append(assignment.skill_match_score)
            
            # Calculate metrics
            load_balance = self._calculate_load_balance(agent_loads)
            avg_skill_match = sum(skill_matches) / len(skill_matches) if skill_matches else 0
            
            self.test_results['assignment_tests'].append({
                'scenario': scenario_name,
                'total_assignments': len(assignments),
                'assignment_time': assignment_time,
                'priority_distribution': priority_distribution,
                'load_balance': load_balance,
                'avg_skill_match': avg_skill_match,
                'agent_utilization': len(agent_loads) / len(agents) * 100
            })
            
            print(f"      ✓ Assignments: {len(assignments)}")
            print(f"      ✓ Load Balance: {load_balance:.2f}")
            print(f"      ✓ Avg Skill Match: {avg_skill_match:.3f}")
    
    def test_performance(self):
        """Test system performance with large datasets"""
        dataset_sizes = [(50, 100), (100, 500), (200, 1000)]
        
        for agent_count, ticket_count in dataset_sizes:
            print(f"  Testing with {agent_count} agents, {ticket_count} tickets...")
            
            agents = self.data_generator.generate_test_agents(agent_count, "normal")
            tickets = self.data_generator.generate_test_tickets(ticket_count, "normal")
            dataset = {'agents': agents, 'tickets': tickets}
            
            # Test validation performance
            start_time = time.time()
            validation_result = self.validator.validate_dataset(dataset)
            validation_time = time.time() - start_time
            
            # Test assignment performance
            start_time = time.time()
            assignments = self.assignment_system.assign_tickets(dataset)
            assignment_time = time.time() - start_time
            
            # Calculate throughput
            validation_throughput = ticket_count / validation_time if validation_time > 0 else 0
            assignment_throughput = ticket_count / assignment_time if assignment_time > 0 else 0
            
            self.test_results['performance_tests'].append({
                'agent_count': agent_count,
                'ticket_count': ticket_count,
                'validation_time': validation_time,
                'assignment_time': assignment_time,
                'validation_throughput': validation_throughput,
                'assignment_throughput': assignment_throughput,
                'total_time': validation_time + assignment_time
            })
            
            print(f"    ✓ Validation: {validation_time:.2f}s ({validation_throughput:.1f} tickets/s)")
            print(f"    ✓ Assignment: {assignment_time:.2f}s ({assignment_throughput:.1f} tickets/s)")
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        edge_cases = [
            ("Empty Dataset", {}),
            ("No Agents", {'agents': [], 'tickets': [{'ticket_id': 'TKT-001', 'title': 'Test', 'description': 'Test desc', 'creation_timestamp': time.time()}]}),
            ("No Tickets", {'agents': [{'agent_id': 'agent_001', 'name': 'Test Agent', 'skills': {'Test': 5}, 'availability_status': 'Available', 'experience_level': 5, 'current_load': 0}], 'tickets': []}),
            ("All Unavailable Agents", {'agents': [{'agent_id': 'agent_001', 'name': 'Test Agent', 'skills': {'Test': 5}, 'availability_status': 'Offline', 'experience_level': 5, 'current_load': 0}], 'tickets': [{'ticket_id': 'TKT-001', 'title': 'Test', 'description': 'Test desc', 'creation_timestamp': time.time()}]}),
        ]
        
        for case_name, dataset in edge_cases:
            print(f"  Testing: {case_name}")
            
            try:
                # Test validation
                validation_result = self.validator.validate_dataset(dataset)
                validation_passed = True
                validation_error = None
            except Exception as e:
                validation_passed = False
                validation_error = str(e)
            
            try:
                # Test assignment (if validation passed)
                if validation_passed and dataset.get('agents') and dataset.get('tickets'):
                    assignments = self.assignment_system.assign_tickets(dataset)
                    assignment_passed = True
                    assignment_error = None
                    assignment_count = len(assignments)
                else:
                    assignment_passed = True  # Expected to skip
                    assignment_error = "Skipped due to invalid data"
                    assignment_count = 0
            except Exception as e:
                assignment_passed = False
                assignment_error = str(e)
                assignment_count = 0
            
            self.test_results['edge_case_tests'].append({
                'case': case_name,
                'validation_passed': validation_passed,
                'validation_error': validation_error,
                'assignment_passed': assignment_passed,
                'assignment_error': assignment_error,
                'assignment_count': assignment_count
            })
            
            v_status = "✓" if validation_passed else "✗"
            a_status = "✓" if assignment_passed else "✗"
            print(f"    {v_status} Validation | {a_status} Assignment")
    
    def _calculate_load_balance(self, agent_loads: Dict) -> float:
        """Calculate load balance score (1.0 = perfect balance)"""
        if not agent_loads:
            return 0.0
        
        loads = list(agent_loads.values())
        if len(loads) <= 1:
            return 1.0
        
        mean_load = sum(loads) / len(loads)
        variance = sum((load - mean_load) ** 2 for load in loads) / len(loads)
        
        # Convert to balance score (lower variance = better balance)
        max_variance = mean_load ** 2  # Worst case variance
        balance_score = 1.0 - (variance / max_variance) if max_variance > 0 else 1.0
        
        return max(0.0, balance_score)
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        report = {
            'test_timestamp': datetime.now().isoformat(),
            'test_summary': {
                'validation_tests': len(self.test_results['validation_tests']),
                'priority_tests': len(self.test_results['priority_tests']),
                'assignment_tests': len(self.test_results['assignment_tests']),
                'performance_tests': len(self.test_results['performance_tests']),
                'edge_case_tests': len(self.test_results['edge_case_tests'])
            },
            'detailed_results': self.test_results,
            'performance_summary': self._generate_performance_summary(),
            'recommendations': self._generate_test_recommendations()
        }
        
        # Save to file
        with open('comprehensive_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Test report saved to: comprehensive_test_report.json")
        
        # Print summary
        self._print_test_summary()
    
    def _generate_performance_summary(self) -> Dict:
        """Generate performance summary statistics"""
        if not self.test_results['performance_tests']:
            return {}
        
        validation_times = [t['validation_time'] for t in self.test_results['performance_tests']]
        assignment_times = [t['assignment_time'] for t in self.test_results['performance_tests']]
        
        return {
            'avg_validation_time': sum(validation_times) / len(validation_times),
            'max_validation_time': max(validation_times),
            'avg_assignment_time': sum(assignment_times) / len(assignment_times),
            'max_assignment_time': max(assignment_times),
            'largest_dataset_tested': max(t['ticket_count'] for t in self.test_results['performance_tests'])
        }
    
    def _generate_test_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Priority analysis accuracy
        if self.test_results['priority_tests']:
            correct_count = sum(1 for t in self.test_results['priority_tests'] if t['correct'])
            accuracy = correct_count / len(self.test_results['priority_tests']) * 100
            
            if accuracy < 80:
                recommendations.append("Consider refining priority analysis keywords for better accuracy")
        
        # Performance recommendations
        if self.test_results['performance_tests']:
            max_time = max(t['total_time'] for t in self.test_results['performance_tests'])
            if max_time > 10:
                recommendations.append("Consider optimization for large datasets (>10s processing time)")
        
        # Assignment quality
        if self.test_results['assignment_tests']:
            avg_balance = sum(t['load_balance'] for t in self.test_results['assignment_tests']) / len(self.test_results['assignment_tests'])
            if avg_balance < 0.7:
                recommendations.append("Improve load balancing algorithm for better workload distribution")
        
        # Edge case handling
        edge_case_failures = sum(1 for t in self.test_results['edge_case_tests'] 
                               if not t['validation_passed'] or not t['assignment_passed'])
        if edge_case_failures > 0:
            recommendations.append("Strengthen error handling for edge cases")
        
        return recommendations
    
    def _print_test_summary(self):
        """Print test summary to console"""
        print("\n📊 TEST SUMMARY")
        print("-" * 50)
        
        # Validation tests
        if self.test_results['validation_tests']:
            avg_quality = sum(t['quality_score'] for t in self.test_results['validation_tests']) / len(self.test_results['validation_tests'])
            print(f"Data Validation: {len(self.test_results['validation_tests'])} scenarios tested")
            print(f"  Average Quality Score: {avg_quality:.1f}/100")
        
        # Priority tests
        if self.test_results['priority_tests']:
            correct_count = sum(1 for t in self.test_results['priority_tests'] if t['correct'])
            accuracy = correct_count / len(self.test_results['priority_tests']) * 100
            print(f"Priority Analysis: {len(self.test_results['priority_tests'])} test cases")
            print(f"  Accuracy: {accuracy:.1f}%")
        
        # Assignment tests
        if self.test_results['assignment_tests']:
            avg_balance = sum(t['load_balance'] for t in self.test_results['assignment_tests']) / len(self.test_results['assignment_tests'])
            print(f"Assignment Logic: {len(self.test_results['assignment_tests'])} scenarios tested")
            print(f"  Average Load Balance: {avg_balance:.2f}")
        
        # Performance tests
        if self.test_results['performance_tests']:
            max_tickets = max(t['ticket_count'] for t in self.test_results['performance_tests'])
            max_time = max(t['total_time'] for t in self.test_results['performance_tests'])
            print(f"Performance: Up to {max_tickets} tickets tested")
            print(f"  Max Processing Time: {max_time:.2f}s")
        
        # Edge cases
        if self.test_results['edge_case_tests']:
            success_count = sum(1 for t in self.test_results['edge_case_tests'] 
                              if t['validation_passed'] and t['assignment_passed'])
            print(f"Edge Cases: {success_count}/{len(self.test_results['edge_case_tests'])} handled successfully")


def main():
    """Run comprehensive system testing"""
    tester = SystemTester()
    tester.run_comprehensive_tests()


if __name__ == "__main__":
    main()
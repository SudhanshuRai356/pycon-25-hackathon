"""
Intelligent Support Ticket Assignment System

This module integrates priority analysis with agent skill matching
to create an optimal ticket assignment system for the PyCon25 hackathon.
"""

import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import re
from priority_analyzer import PriorityAnalyzer, PriorityLevel


@dataclass
class AgentAssignment:
    """Result of ticket assignment"""
    ticket_id: str
    assigned_agent_id: str
    rationale: str
    priority_level: str
    priority_score: float
    skill_match_score: float
    workload_factor: float
    final_score: float


class TicketAssignmentSystem:
    """
    Intelligent ticket assignment system that combines priority analysis
    with agent skill matching and workload balancing.
    """
    
    def __init__(self):
        self.priority_analyzer = PriorityAnalyzer()
        self.skill_keywords = self._initialize_skill_keywords()
        
    def _initialize_skill_keywords(self) -> Dict[str, List[str]]:
        """
        Map technical keywords to agent skills.
        This helps match ticket descriptions to relevant agent skills.
        """
        return {
            'Networking': [
                'vpn', 'network', 'networking', 'router', 'switch', 'firewall',
                'dns', 'dhcp', 'tcp', 'ip', 'subnet', 'vlan', 'wifi', 'wireless',
                'connection', 'connectivity', 'ping', 'traceroute', 'bandwidth'
            ],
            'Linux_Administration': [
                'linux', 'ubuntu', 'centos', 'redhat', 'bash', 'shell', 'terminal',
                'ssh', 'sudo', 'chmod', 'chown', 'cron', 'systemd', 'apache',
                'nginx', 'mysql', 'postgresql', 'server', 'unix'
            ],
            'Cloud_AWS': [
                'aws', 'amazon', 'ec2', 's3', 'cloudformation', 'lambda',
                'rds', 'vpc', 'cloudwatch', 'iam', 'route53', 'elb',
                'auto scaling', 'azure', 'cloud', 'hosting'
            ],
            'VPN_Troubleshooting': [
                'vpn', 'tunnel', 'ipsec', 'l2tp', 'pptp', 'openvpn',
                'remote access', 'site-to-site', 'authentication',
                'concentrator', 'client', 'endpoint'
            ],
            'Hardware_Diagnostics': [
                'hardware', 'diagnostic', 'memory', 'ram', 'cpu', 'disk',
                'ssd', 'hdd', 'motherboard', 'power supply', 'fan',
                'temperature', 'bios', 'uefi', 'boot', 'POST'
            ],
            'Windows_Server_2022': [
                'windows server', 'server 2022', 'server 2019', 'server 2016',
                'iis', 'hyper-v', 'powershell', 'registry', 'event viewer',
                'services', 'roles', 'features'
            ],
            'Active_Directory': [
                'active directory', 'ad', 'domain controller', 'dc',
                'group policy', 'gpo', 'ldap', 'kerberos', 'ntlm',
                'forest', 'domain', 'ou', 'user account', 'computer account'
            ],
            'Virtualization_VMware': [
                'vmware', 'vsphere', 'vcenter', 'esxi', 'virtual machine',
                'vm', 'hypervisor', 'virtualization', 'snapshot',
                'vmotion', 'ha', 'drs'
            ],
            'Software_Licensing': [
                'license', 'licensing', 'activation', 'key', 'volume licensing',
                'cal', 'subscription', 'office 365', 'microsoft 365'
            ],
            'Network_Security': [
                'security', 'firewall', 'intrusion', 'malware', 'antivirus',
                'threat', 'vulnerability', 'patch', 'encryption',
                'certificate', 'ssl', 'tls'
            ],
            'Database_SQL': [
                'database', 'sql', 'mysql', 'postgresql', 'oracle',
                'sql server', 'query', 'table', 'index', 'backup',
                'restore', 'replication'
            ],
            'Firewall_Configuration': [
                'firewall', 'iptables', 'pfsense', 'checkpoint',
                'fortigate', 'cisco asa', 'rules', 'acl', 'port',
                'protocol', 'block', 'allow'
            ],
            'Identity_Management': [
                'identity', 'sso', 'saml', 'oauth', 'ldap',
                'authentication', 'authorization', 'mfa', '2fa',
                'identity provider', 'federation'
            ],
            'SaaS_Integrations': [
                'saas', 'integration', 'api', 'webhook', 'connector',
                'salesforce', 'servicenow', 'slack', 'teams',
                'sharepoint', 'onedrive'
            ],
            'Microsoft_365': [
                'microsoft 365', 'office 365', 'outlook', 'word',
                'excel', 'powerpoint', 'teams', 'sharepoint',
                'onedrive', 'exchange', 'azure ad'
            ],
            'SharePoint_Online': [
                'sharepoint', 'sharepoint online', 'site collection',
                'document library', 'list', 'workflow', 'permissions',
                'search', 'content type'
            ],
            'PowerShell_Scripting': [
                'powershell', 'script', 'cmdlet', 'pipeline',
                'automation', 'dsc', 'remoting', 'ise',
                'gallery', 'module'
            ],
            'Laptop_Repair': [
                'laptop', 'notebook', 'screen', 'keyboard', 'touchpad',
                'battery', 'charger', 'adapter', 'hinge', 'repair'
            ],
            'Printer_Support': [
                'printer', 'printing', 'toner', 'ink', 'paper jam',
                'queue', 'driver', 'spooler', 'network printer'
            ]
        }
    
    def assign_tickets(self, dataset: Dict) -> List[AgentAssignment]:
        """
        Main method to assign all tickets to appropriate agents.
        
        Args:
            dataset: Dictionary containing agents and tickets data
            
        Returns:
            List of AgentAssignment objects with assignments and rationales
        """
        agents = dataset.get('agents', [])
        tickets = dataset.get('tickets', [])
        
        assignments = []
        agent_workloads = {agent['agent_id']: agent.get('current_load', 0) for agent in agents}
        
        # Sort tickets by priority (critical first)
        prioritized_tickets = self._prioritize_tickets(tickets)
        
        for ticket in prioritized_tickets:
            assignment = self._assign_single_ticket(ticket, agents, agent_workloads)
            assignments.append(assignment)
            
            # Update agent workload
            agent_workloads[assignment.assigned_agent_id] += 1
            
        return assignments
    
    def _prioritize_tickets(self, tickets: List[Dict]) -> List[Dict]:
        """Sort tickets by priority level and score."""
        ticket_priorities = []
        
        for ticket in tickets:
            priority_result = self.priority_analyzer.analyze_priority(
                ticket.get('title', ''),
                ticket.get('description', '')
            )
            ticket_priorities.append((ticket, priority_result))
        
        # Sort by priority level (1=Critical, 2=High, etc.) then by score descending
        ticket_priorities.sort(key=lambda x: (x[1].priority_level.value, -x[1].priority_score))
        
        return [ticket for ticket, _ in ticket_priorities]
    
    def _assign_single_ticket(
        self, 
        ticket: Dict, 
        agents: List[Dict], 
        current_workloads: Dict[str, int]
    ) -> AgentAssignment:
        """
        Assign a single ticket to the best available agent.
        
        Args:
            ticket: Ticket dictionary
            agents: List of agent dictionaries
            current_workloads: Current workload for each agent
            
        Returns:
            AgentAssignment object
        """
        ticket_id = ticket.get('ticket_id', '')
        title = ticket.get('title', '')
        description = ticket.get('description', '')
        
        # Get priority analysis
        priority_result = self.priority_analyzer.analyze_priority(title, description)
        
        best_agent = None
        best_score = -1
        best_rationale = ""
        best_skill_score = 0
        best_workload_factor = 0
        
        for agent in agents:
            # Skip unavailable agents
            if agent.get('availability_status', '').lower() != 'available':
                continue
            
            # Calculate skill match score
            skill_score = self._calculate_skill_match(ticket, agent)
            
            # Calculate workload factor (lower workload = higher score)
            current_load = current_workloads.get(agent['agent_id'], 0)
            max_reasonable_load = 8  # Assume max 8 tickets per agent
            workload_factor = max(0, (max_reasonable_load - current_load) / max_reasonable_load)
            
            # Calculate experience bonus
            experience_bonus = min(agent.get('experience_level', 0) / 15, 1.0)  # Cap at 1.0
            
            # Priority urgency multiplier
            priority_multiplier = self._get_priority_multiplier(priority_result.priority_level)
            
            # Calculate final score
            final_score = (
                skill_score * 0.4 +           # 40% skill match
                workload_factor * 0.25 +      # 25% workload balance
                experience_bonus * 0.2 +      # 20% experience
                priority_multiplier * 0.15    # 15% priority consideration
            )
            
            if final_score > best_score:
                best_score = final_score
                best_agent = agent
                best_skill_score = skill_score
                best_workload_factor = workload_factor
                best_rationale = self._generate_assignment_rationale(
                    agent, skill_score, workload_factor, experience_bonus, 
                    priority_result, current_load
                )
        
        # Fallback to first available agent if no good match
        if best_agent is None:
            available_agents = [a for a in agents if a.get('availability_status', '').lower() == 'available']
            if available_agents:
                best_agent = available_agents[0]
                best_rationale = f"Assigned to {best_agent['name']} (first available agent) due to no strong skill matches."
            else:
                # Emergency fallback to any agent
                best_agent = agents[0] if agents else {'agent_id': 'agent_001', 'name': 'Default Agent'}
                best_rationale = "Emergency assignment - no available agents found."
        
        return AgentAssignment(
            ticket_id=ticket_id,
            assigned_agent_id=best_agent['agent_id'],
            rationale=best_rationale,
            priority_level=priority_result.priority_level.name,
            priority_score=priority_result.priority_score,
            skill_match_score=best_skill_score,
            workload_factor=best_workload_factor,
            final_score=best_score
        )
    
    def _calculate_skill_match(self, ticket: Dict, agent: Dict) -> float:
        """
        Calculate how well an agent's skills match a ticket's requirements.
        
        Returns a score between 0 and 1.
        """
        title = ticket.get('title', '').lower()
        description = ticket.get('description', '').lower()
        full_text = f"{title} {description}"
        
        agent_skills = agent.get('skills', {})
        total_score = 0
        matched_skills = 0
        
        for skill_name, skill_level in agent_skills.items():
            # Get keywords for this skill
            keywords = self.skill_keywords.get(skill_name, [])
            
            # Check if any keywords match the ticket
            keyword_matches = 0
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', full_text):
                    keyword_matches += 1
            
            if keyword_matches > 0:
                # Score based on skill level (0-10) and number of keyword matches
                skill_score = (skill_level / 10) * min(keyword_matches / 3, 1.0)
                total_score += skill_score
                matched_skills += 1
        
        # Normalize score
        if matched_skills == 0:
            return 0.0
        
        return min(total_score / matched_skills, 1.0)
    
    def _get_priority_multiplier(self, priority_level: PriorityLevel) -> float:
        """Get multiplier based on priority level for agent selection."""
        multipliers = {
            PriorityLevel.CRITICAL: 1.0,
            PriorityLevel.HIGH: 0.8,
            PriorityLevel.MEDIUM: 0.6,
            PriorityLevel.LOW: 0.4
        }
        return multipliers.get(priority_level, 0.6)
    
    def _generate_assignment_rationale(
        self,
        agent: Dict,
        skill_score: float,
        workload_factor: float,
        experience_bonus: float,
        priority_result,
        current_load: int
    ) -> str:
        """Generate human-readable rationale for the assignment."""
        name = agent.get('name', 'Unknown')
        agent_id = agent.get('agent_id', '')
        
        rationale_parts = [f"Assigned to {name} ({agent_id})"]
        
        # Skill match reasoning
        if skill_score > 0.7:
            rationale_parts.append("based on excellent skill match")
        elif skill_score > 0.4:
            rationale_parts.append("based on good skill match")
        elif skill_score > 0.1:
            rationale_parts.append("based on partial skill match")
        else:
            rationale_parts.append("due to availability")
        
        # Experience factor
        experience_level = agent.get('experience_level', 0)
        if experience_level >= 10:
            rationale_parts.append(f"and high experience level ({experience_level} years)")
        elif experience_level >= 5:
            rationale_parts.append(f"and good experience ({experience_level} years)")
        
        # Workload consideration
        if current_load <= 2:
            rationale_parts.append("with low current workload")
        elif current_load <= 4:
            rationale_parts.append("with moderate workload")
        elif current_load > 6:
            rationale_parts.append("despite high workload (best available)")
        
        # Priority consideration
        if priority_result.priority_level in [PriorityLevel.CRITICAL, PriorityLevel.HIGH]:
            rationale_parts.append(f"for this {priority_result.priority_level.name} priority ticket")
        
        return " ".join(rationale_parts) + "."
    
    def generate_output_file(self, assignments: List[AgentAssignment], output_path: str = 'output_result.json'):
        """
        Generate the required output file format for the hackathon.
        
        Args:
            assignments: List of AgentAssignment objects
            output_path: Path to save the output file
        """
        output_data = []
        
        for assignment in assignments:
            output_data.append({
                'ticket_id': assignment.ticket_id,
                'assigned_agent_id': assignment.assigned_agent_id,
                'rationale': assignment.rationale
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Output file generated: {output_path}")
        return output_path
    
    def generate_detailed_report(self, assignments: List[AgentAssignment], report_path: str = 'detailed_assignment_report.json'):
        """
        Generate a detailed report with all scoring information.
        
        Args:
            assignments: List of AgentAssignment objects
            report_path: Path to save the detailed report
        """
        report_data = {
            'summary': {
                'total_tickets': len(assignments),
                'priority_distribution': {},
                'agent_workload_distribution': {}
            },
            'assignments': []
        }
        
        # Calculate summary statistics
        priority_counts = {}
        agent_counts = {}
        
        for assignment in assignments:
            # Priority distribution
            priority = assignment.priority_level
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            # Agent workload distribution
            agent_id = assignment.assigned_agent_id
            agent_counts[agent_id] = agent_counts.get(agent_id, 0) + 1
            
            # Add to detailed assignments
            report_data['assignments'].append({
                'ticket_id': assignment.ticket_id,
                'assigned_agent_id': assignment.assigned_agent_id,
                'priority_level': assignment.priority_level,
                'priority_score': round(assignment.priority_score, 2),
                'skill_match_score': round(assignment.skill_match_score, 3),
                'workload_factor': round(assignment.workload_factor, 3),
                'final_score': round(assignment.final_score, 3),
                'rationale': assignment.rationale
            })
        
        report_data['summary']['priority_distribution'] = priority_counts
        report_data['summary']['agent_workload_distribution'] = agent_counts
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Detailed report generated: {report_path}")
        return report_path


def main():
    """Main function to run the ticket assignment system."""
    print("🎯 Intelligent Support Ticket Assignment System")
    print("=" * 60)
    
    # Load dataset
    try:
        with open('dataset.json', 'r', encoding='utf-8') as f:
            dataset = json.load(f)
    except FileNotFoundError:
        print("❌ Error: dataset.json not found!")
        return
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON in dataset.json!")
        return
    
    # Initialize assignment system
    assignment_system = TicketAssignmentSystem()
    
    # Assign all tickets
    print(f"📊 Processing {len(dataset.get('tickets', []))} tickets with {len(dataset.get('agents', []))} agents...")
    assignments = assignment_system.assign_tickets(dataset)
    
    # Generate output files
    assignment_system.generate_output_file(assignments)
    assignment_system.generate_detailed_report(assignments)
    
    # Print summary
    print(f"\n📈 ASSIGNMENT SUMMARY")
    print("-" * 40)
    
    priority_counts = {}
    agent_counts = {}
    
    for assignment in assignments:
        priority_counts[assignment.priority_level] = priority_counts.get(assignment.priority_level, 0) + 1
        agent_counts[assignment.assigned_agent_id] = agent_counts.get(assignment.assigned_agent_id, 0) + 1
    
    print("Priority Distribution:")
    for priority, count in sorted(priority_counts.items()):
        print(f"  {priority}: {count} tickets")
    
    print(f"\nAgent Workload Distribution:")
    for agent_id, count in sorted(agent_counts.items()):
        print(f"  {agent_id}: {count} tickets")
    
    print(f"\n✅ Assignment completed successfully!")
    print(f"📄 Check 'output_result.json' for the hackathon submission format")
    print(f"📊 Check 'detailed_assignment_report.json' for detailed analysis")


if __name__ == "__main__":
    main()
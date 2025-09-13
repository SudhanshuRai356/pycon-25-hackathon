"""
Enhanced Data Validation and Constraints Module

This module provides comprehensive data validation with advanced constraints
for the ticket assignment system.
"""

import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum


class ConstraintType(Enum):
    """Types of data constraints"""
    REQUIRED = "required"
    FORMAT = "format"
    RANGE = "range"
    UNIQUE = "unique"
    BUSINESS_RULE = "business_rule"
    REFERENCE = "reference"


@dataclass
class Constraint:
    """Data constraint definition"""
    field: str
    constraint_type: ConstraintType
    rule: str
    message: str
    severity: str = "error"  # error, warning, info


@dataclass
class ValidationIssue:
    """Individual validation issue"""
    severity: str
    message: str
    field: str
    value: any
    constraint: str
    suggestion: Optional[str] = None


class EnhancedDataValidator:
    """
    Enhanced data validator with comprehensive constraints and business rules
    """
    
    def __init__(self):
        self.constraints = self._define_constraints()
        self.business_rules = self._define_business_rules()
        
    def _define_constraints(self) -> List[Constraint]:
        """Define comprehensive data constraints"""
        return [
            # Agent constraints
            Constraint("agent_id", ConstraintType.REQUIRED, "not_empty", 
                      "Agent ID is required"),
            Constraint("agent_id", ConstraintType.FORMAT, r"^agent_\d{3}$", 
                      "Agent ID must follow format 'agent_XXX' where XXX is a 3-digit number"),
            Constraint("agent_id", ConstraintType.UNIQUE, "unique_in_dataset", 
                      "Agent ID must be unique across all agents"),
            
            Constraint("name", ConstraintType.REQUIRED, "not_empty", 
                      "Agent name is required"),
            Constraint("name", ConstraintType.FORMAT, r"^[A-Za-z\s]{2,50}$", 
                      "Agent name must be 2-50 characters, letters and spaces only"),
            
            Constraint("skills", ConstraintType.REQUIRED, "not_empty", 
                      "Agent must have at least one skill"),
            Constraint("skills", ConstraintType.BUSINESS_RULE, "skill_levels_valid", 
                      "All skill levels must be between 1 and 10"),
            Constraint("skills", ConstraintType.BUSINESS_RULE, "minimum_skills", 
                      "Agent should have at least 3 skills for effective assignment", "warning"),
            
            Constraint("availability_status", ConstraintType.REQUIRED, "not_empty", 
                      "Availability status is required"),
            Constraint("availability_status", ConstraintType.FORMAT, 
                      "^(Available|Busy|Offline|On Leave)$", 
                      "Availability must be: Available, Busy, Offline, or On Leave"),
            
            Constraint("experience_level", ConstraintType.REQUIRED, "numeric", 
                      "Experience level is required"),
            Constraint("experience_level", ConstraintType.RANGE, "0,50", 
                      "Experience level must be between 0 and 50 years"),
            
            Constraint("current_load", ConstraintType.RANGE, "0,20", 
                      "Current load must be between 0 and 20 tickets"),
            
            # Ticket constraints
            Constraint("ticket_id", ConstraintType.REQUIRED, "not_empty", 
                      "Ticket ID is required"),
            Constraint("ticket_id", ConstraintType.FORMAT, r"^TKT-\d{4}-\d{3}$", 
                      "Ticket ID must follow format 'TKT-YYYY-XXX'"),
            Constraint("ticket_id", ConstraintType.UNIQUE, "unique_in_dataset", 
                      "Ticket ID must be unique across all tickets"),
            
            Constraint("title", ConstraintType.REQUIRED, "not_empty", 
                      "Ticket title is required"),
            Constraint("title", ConstraintType.RANGE, "5,200", 
                      "Ticket title must be 5-200 characters"),
            Constraint("title", ConstraintType.BUSINESS_RULE, "no_placeholder_text", 
                      "Title should not contain placeholder text like 'TODO' or 'TBD'", "warning"),
            
            Constraint("description", ConstraintType.REQUIRED, "not_empty", 
                      "Ticket description is required"),
            Constraint("description", ConstraintType.RANGE, "10,5000", 
                      "Ticket description must be 10-5000 characters"),
            Constraint("description", ConstraintType.BUSINESS_RULE, "sufficient_detail", 
                      "Description should provide sufficient technical detail", "warning"),
            
            Constraint("creation_timestamp", ConstraintType.REQUIRED, "numeric", 
                      "Creation timestamp is required"),
            Constraint("creation_timestamp", ConstraintType.BUSINESS_RULE, "reasonable_date", 
                      "Creation timestamp should be within reasonable date range"),
        ]
    
    def _define_business_rules(self) -> Dict[str, callable]:
        """Define business rule validation functions"""
        return {
            "skill_levels_valid": self._validate_skill_levels,
            "minimum_skills": self._validate_minimum_skills,
            "no_placeholder_text": self._validate_no_placeholder_text,
            "sufficient_detail": self._validate_sufficient_detail,
            "reasonable_date": self._validate_reasonable_date,
            "agent_availability_balance": self._validate_agent_availability_balance,
            "workload_distribution": self._validate_workload_distribution,
            "skill_coverage": self._validate_skill_coverage,
            "ticket_priority_distribution": self._validate_ticket_priority_distribution,
        }
    
    def validate_dataset(self, dataset: Dict) -> Dict:
        """
        Comprehensive dataset validation with enhanced constraints
        
        Returns:
            Dictionary with validation results, issues, and recommendations
        """
        validation_result = {
            'is_valid': True,
            'total_issues': 0,
            'issues': {
                'errors': [],
                'warnings': [],
                'info': []
            },
            'summary': {},
            'recommendations': [],
            'data_quality_score': 0.0
        }
        
        # Validate structure
        structure_issues = self._validate_structure(dataset)
        self._add_issues(validation_result, structure_issues)
        
        if not dataset.get('agents') or not dataset.get('tickets'):
            validation_result['is_valid'] = False
            return validation_result
        
        # Validate agents
        agent_issues = self._validate_agents_enhanced(dataset['agents'])
        self._add_issues(validation_result, agent_issues)
        
        # Validate tickets
        ticket_issues = self._validate_tickets_enhanced(dataset['tickets'])
        self._add_issues(validation_result, ticket_issues)
        
        # Validate business rules
        business_issues = self._validate_business_rules_enhanced(dataset)
        self._add_issues(validation_result, business_issues)
        
        # Calculate data quality score
        validation_result['data_quality_score'] = self._calculate_quality_score(validation_result)
        
        # Generate recommendations
        validation_result['recommendations'] = self._generate_recommendations(dataset, validation_result)
        
        # Set overall validity
        validation_result['is_valid'] = len(validation_result['issues']['errors']) == 0
        validation_result['total_issues'] = sum(len(issues) for issues in validation_result['issues'].values())
        
        # Generate summary
        validation_result['summary'] = self._generate_summary(dataset, validation_result)
        
        return validation_result
    
    def _validate_structure(self, dataset: Dict) -> List[ValidationIssue]:
        """Validate basic dataset structure"""
        issues = []
        
        if not isinstance(dataset, dict):
            issues.append(ValidationIssue(
                "error", "Dataset must be a dictionary/object", "", dataset, "structure"
            ))
            return issues
        
        required_sections = ['agents', 'tickets']
        for section in required_sections:
            if section not in dataset:
                issues.append(ValidationIssue(
                    "error", f"Missing required section: {section}", section, None, "structure"
                ))
            elif not isinstance(dataset[section], list):
                issues.append(ValidationIssue(
                    "error", f"Section '{section}' must be a list", section, 
                    type(dataset[section]).__name__, "structure"
                ))
        
        return issues
    
    def _validate_agents_enhanced(self, agents: List[Dict]) -> List[ValidationIssue]:
        """Enhanced agent validation with comprehensive constraints"""
        issues = []
        agent_ids = set()
        
        if not agents:
            issues.append(ValidationIssue(
                "error", "No agents found in dataset", "agents", [], "data_missing"
            ))
            return issues
        
        for i, agent in enumerate(agents):
            agent_prefix = f"Agent {i+1}"
            
            # Apply all agent constraints
            for constraint in self.constraints:
                if constraint.field in ['agent_id', 'name', 'skills', 'availability_status', 
                                      'experience_level', 'current_load']:
                    constraint_issues = self._apply_constraint(agent, constraint, agent_prefix)
                    issues.extend(constraint_issues)
            
            # Unique ID tracking
            agent_id = agent.get('agent_id', '')
            if agent_id:
                if agent_id in agent_ids:
                    issues.append(ValidationIssue(
                        "error", f"{agent_prefix}: Duplicate agent_id '{agent_id}'", 
                        "agent_id", agent_id, "uniqueness"
                    ))
                else:
                    agent_ids.add(agent_id)
            
            # Advanced skill validation
            skills = agent.get('skills', {})
            if isinstance(skills, dict):
                skill_issues = self._validate_agent_skills(skills, agent_prefix)
                issues.extend(skill_issues)
            
            # Experience vs skills consistency
            experience = agent.get('experience_level', 0)
            if isinstance(experience, (int, float)) and skills:
                avg_skill = sum(skills.values()) / len(skills) if skills else 0
                if experience > 10 and avg_skill < 5:
                    issues.append(ValidationIssue(
                        "warning", 
                        f"{agent_prefix}: High experience ({experience} years) but low average skill level ({avg_skill:.1f})",
                        "experience_level", experience, "consistency",
                        "Consider increasing skill levels or reviewing experience"
                    ))
        
        return issues
    
    def _validate_tickets_enhanced(self, tickets: List[Dict]) -> List[ValidationIssue]:
        """Enhanced ticket validation with comprehensive constraints"""
        issues = []
        ticket_ids = set()
        
        if not tickets:
            issues.append(ValidationIssue(
                "error", "No tickets found in dataset", "tickets", [], "data_missing"
            ))
            return issues
        
        for i, ticket in enumerate(tickets):
            ticket_prefix = f"Ticket {i+1}"
            
            # Apply all ticket constraints
            for constraint in self.constraints:
                if constraint.field in ['ticket_id', 'title', 'description', 'creation_timestamp']:
                    constraint_issues = self._apply_constraint(ticket, constraint, ticket_prefix)
                    issues.extend(constraint_issues)
            
            # Unique ID tracking
            ticket_id = ticket.get('ticket_id', '')
            if ticket_id:
                if ticket_id in ticket_ids:
                    issues.append(ValidationIssue(
                        "error", f"{ticket_prefix}: Duplicate ticket_id '{ticket_id}'", 
                        "ticket_id", ticket_id, "uniqueness"
                    ))
                else:
                    ticket_ids.add(ticket_id)
            
            # Content quality checks
            title = ticket.get('title', '')
            description = ticket.get('description', '')
            
            # Check for meaningful content
            if title and description:
                combined_length = len(title) + len(description)
                if combined_length < 50:
                    issues.append(ValidationIssue(
                        "warning", 
                        f"{ticket_prefix}: Very short ticket content ({combined_length} chars total)",
                        "content", combined_length, "quality",
                        "Add more detailed description for better assignment"
                    ))
                
                # Check for technical keywords
                tech_keywords = ['error', 'fail', 'issue', 'problem', 'bug', 'broken', 'down', 
                               'server', 'network', 'database', 'software', 'hardware']
                combined_text = f"{title} {description}".lower()
                keyword_count = sum(1 for keyword in tech_keywords if keyword in combined_text)
                
                if keyword_count == 0:
                    issues.append(ValidationIssue(
                        "info", 
                        f"{ticket_prefix}: No technical keywords found, may affect priority analysis",
                        "content", combined_text[:100], "quality",
                        "Include technical keywords for better categorization"
                    ))
        
        return issues
    
    def _validate_business_rules_enhanced(self, dataset: Dict) -> List[ValidationIssue]:
        """Validate comprehensive business rules"""
        issues = []
        agents = dataset.get('agents', [])
        tickets = dataset.get('tickets', [])
        
        # Agent-to-ticket ratio
        if agents and tickets:
            ratio = len(tickets) / len(agents)
            if ratio > 15:
                issues.append(ValidationIssue(
                    "warning", 
                    f"High ticket-to-agent ratio ({ratio:.1f}:1), may cause agent overload",
                    "ratio", ratio, "business_rule",
                    "Consider adding more agents or reducing ticket volume"
                ))
            elif ratio < 2:
                issues.append(ValidationIssue(
                    "info", 
                    f"Low ticket-to-agent ratio ({ratio:.1f}:1), agents may be underutilized",
                    "ratio", ratio, "business_rule"
                ))
        
        # Availability balance
        if agents:
            available_count = sum(1 for a in agents if a.get('availability_status') == 'Available')
            availability_rate = available_count / len(agents)
            
            if availability_rate < 0.3:
                issues.append(ValidationIssue(
                    "error", 
                    f"Too few available agents ({availability_rate:.1%}), cannot handle workload",
                    "availability", availability_rate, "business_rule",
                    "Ensure at least 30% of agents are available"
                ))
            elif availability_rate < 0.5:
                issues.append(ValidationIssue(
                    "warning", 
                    f"Low agent availability ({availability_rate:.1%}), may impact response time",
                    "availability", availability_rate, "business_rule"
                ))
        
        # Skill diversity
        if agents:
            all_skills = set()
            for agent in agents:
                all_skills.update(agent.get('skills', {}).keys())
            
            if len(all_skills) < 5:
                issues.append(ValidationIssue(
                    "warning", 
                    f"Limited skill diversity ({len(all_skills)} unique skills)",
                    "skills", len(all_skills), "business_rule",
                    "Add agents with diverse skills for better coverage"
                ))
            
            # Check for critical skills
            critical_skills = ['Network_Security', 'Database_SQL', 'Hardware_Diagnostics']
            missing_critical = [skill for skill in critical_skills if skill not in all_skills]
            
            if missing_critical:
                issues.append(ValidationIssue(
                    "warning", 
                    f"Missing critical skills: {', '.join(missing_critical)}",
                    "critical_skills", missing_critical, "business_rule",
                    "Ensure coverage of critical skill areas"
                ))
        
        # Workload distribution
        if agents:
            loads = [agent.get('current_load', 0) for agent in agents]
            if loads:
                max_load = max(loads)
                min_load = min(loads)
                avg_load = sum(loads) / len(loads)
                
                if max_load - min_load > 10:
                    issues.append(ValidationIssue(
                        "warning", 
                        f"Uneven workload distribution (range: {min_load}-{max_load})",
                        "workload", max_load - min_load, "business_rule",
                        "Balance workload before running new assignments"
                    ))
                
                if avg_load > 8:
                    issues.append(ValidationIssue(
                        "warning", 
                        f"High average workload ({avg_load:.1f} tickets per agent)",
                        "workload", avg_load, "business_rule"
                    ))
        
        return issues
    
    def _apply_constraint(self, data: Dict, constraint: Constraint, prefix: str) -> List[ValidationIssue]:
        """Apply a single constraint to data item"""
        issues = []
        field_value = data.get(constraint.field)
        
        if constraint.constraint_type == ConstraintType.REQUIRED:
            if constraint.rule == "not_empty":
                if not field_value or (isinstance(field_value, str) and not field_value.strip()):
                    issues.append(ValidationIssue(
                        constraint.severity, f"{prefix}: {constraint.message}",
                        constraint.field, field_value, "required"
                    ))
            elif constraint.rule == "numeric":
                if not isinstance(field_value, (int, float)):
                    issues.append(ValidationIssue(
                        constraint.severity, f"{prefix}: {constraint.message}",
                        constraint.field, field_value, "required"
                    ))
        
        elif constraint.constraint_type == ConstraintType.FORMAT:
            if field_value and isinstance(field_value, str):
                if not re.match(constraint.rule, field_value):
                    issues.append(ValidationIssue(
                        constraint.severity, f"{prefix}: {constraint.message}",
                        constraint.field, field_value, "format"
                    ))
        
        elif constraint.constraint_type == ConstraintType.RANGE:
            if field_value is not None:
                if isinstance(field_value, str):
                    min_len, max_len = map(int, constraint.rule.split(','))
                    if not (min_len <= len(field_value) <= max_len):
                        issues.append(ValidationIssue(
                            constraint.severity, f"{prefix}: {constraint.message}",
                            constraint.field, len(field_value), "range"
                        ))
                elif isinstance(field_value, (int, float)):
                    min_val, max_val = map(float, constraint.rule.split(','))
                    if not (min_val <= field_value <= max_val):
                        issues.append(ValidationIssue(
                            constraint.severity, f"{prefix}: {constraint.message}",
                            constraint.field, field_value, "range"
                        ))
        
        elif constraint.constraint_type == ConstraintType.BUSINESS_RULE:
            if constraint.rule in self.business_rules:
                rule_issues = self.business_rules[constraint.rule](data, constraint, prefix)
                issues.extend(rule_issues)
        
        return issues
    
    def _validate_agent_skills(self, skills: Dict, prefix: str) -> List[ValidationIssue]:
        """Validate agent skills in detail"""
        issues = []
        
        if not skills:
            return issues
        
        for skill_name, skill_level in skills.items():
            # Skill name format
            if not re.match(r'^[A-Za-z_0-9]+$', skill_name):
                issues.append(ValidationIssue(
                    "warning", f"{prefix}: Skill name '{skill_name}' contains invalid characters",
                    "skills", skill_name, "format",
                    "Use alphanumeric characters and underscores only"
                ))
            
            # Skill level validation
            if not isinstance(skill_level, (int, float)):
                issues.append(ValidationIssue(
                    "error", f"{prefix}: Skill '{skill_name}' level must be numeric",
                    "skills", skill_level, "type"
                ))
            elif not (1 <= skill_level <= 10):
                issues.append(ValidationIssue(
                    "error", f"{prefix}: Skill '{skill_name}' level {skill_level} out of range (1-10)",
                    "skills", skill_level, "range"
                ))
        
        # Check for skill gaps
        important_categories = ['Network', 'Security', 'Database', 'Hardware', 'Software']
        has_category = {category: False for category in important_categories}
        
        for skill_name in skills.keys():
            for category in important_categories:
                if category.lower() in skill_name.lower():
                    has_category[category] = True
        
        missing_categories = [cat for cat, has in has_category.items() if not has]
        if len(missing_categories) >= 3:
            issues.append(ValidationIssue(
                "info", f"{prefix}: Limited skill coverage, missing: {', '.join(missing_categories)}",
                "skills", missing_categories, "coverage",
                "Consider adding skills in missing categories"
            ))
        
        return issues
    
    # Business rule validation methods
    def _validate_skill_levels(self, data: Dict, constraint: Constraint, prefix: str) -> List[ValidationIssue]:
        """Validate skill levels are within valid range"""
        issues = []
        skills = data.get('skills', {})
        
        if isinstance(skills, dict):
            for skill_name, skill_level in skills.items():
                if not isinstance(skill_level, (int, float)) or not (1 <= skill_level <= 10):
                    issues.append(ValidationIssue(
                        constraint.severity, f"{prefix}: {constraint.message} (skill: {skill_name})",
                        "skills", skill_level, "business_rule"
                    ))
        
        return issues
    
    def _validate_minimum_skills(self, data: Dict, constraint: Constraint, prefix: str) -> List[ValidationIssue]:
        """Validate agent has minimum number of skills"""
        issues = []
        skills = data.get('skills', {})
        
        if isinstance(skills, dict) and len(skills) < 3:
            issues.append(ValidationIssue(
                constraint.severity, f"{prefix}: {constraint.message} (has {len(skills)} skills)",
                "skills", len(skills), "business_rule",
                "Add more skills to improve assignment quality"
            ))
        
        return issues
    
    def _validate_no_placeholder_text(self, data: Dict, constraint: Constraint, prefix: str) -> List[ValidationIssue]:
        """Check for placeholder text in title"""
        issues = []
        title = data.get('title', '')
        
        if isinstance(title, str):
            placeholders = ['todo', 'tbd', 'placeholder', 'test', 'example']
            title_lower = title.lower()
            
            for placeholder in placeholders:
                if placeholder in title_lower:
                    issues.append(ValidationIssue(
                        constraint.severity, f"{prefix}: {constraint.message} (found: {placeholder})",
                        "title", title, "business_rule",
                        "Replace placeholder text with meaningful content"
                    ))
                    break
        
        return issues
    
    def _validate_sufficient_detail(self, data: Dict, constraint: Constraint, prefix: str) -> List[ValidationIssue]:
        """Validate description has sufficient technical detail"""
        issues = []
        description = data.get('description', '')
        
        if isinstance(description, str) and len(description) > 10:
            # Check for technical indicators
            tech_indicators = ['error', 'server', 'network', 'database', 'application', 
                             'user', 'system', 'issue', 'problem', 'failed', 'unable']
            
            description_lower = description.lower()
            indicator_count = sum(1 for indicator in tech_indicators if indicator in description_lower)
            
            if indicator_count < 2 and len(description) < 100:
                issues.append(ValidationIssue(
                    constraint.severity, f"{prefix}: {constraint.message}",
                    "description", len(description), "business_rule",
                    "Add more technical details and context"
                ))
        
        return issues
    
    def _validate_reasonable_date(self, data: Dict, constraint: Constraint, prefix: str) -> List[ValidationIssue]:
        """Validate timestamp is within reasonable range"""
        issues = []
        timestamp = data.get('creation_timestamp')
        
        if isinstance(timestamp, (int, float)):
            try:
                date = datetime.fromtimestamp(timestamp)
                now = datetime.now()
                
                # Check if date is too far in the past (more than 2 years)
                if date < now - timedelta(days=730):
                    issues.append(ValidationIssue(
                        "warning", f"{prefix}: Very old ticket ({date.strftime('%Y-%m-%d')})",
                        "creation_timestamp", timestamp, "business_rule"
                    ))
                
                # Check if date is in the future (more than 1 week)
                elif date > now + timedelta(days=7):
                    issues.append(ValidationIssue(
                        "warning", f"{prefix}: Future-dated ticket ({date.strftime('%Y-%m-%d')})",
                        "creation_timestamp", timestamp, "business_rule"
                    ))
                
            except (ValueError, OSError):
                issues.append(ValidationIssue(
                    "error", f"{prefix}: Invalid timestamp format",
                    "creation_timestamp", timestamp, "business_rule"
                ))
        
        return issues
    
    def _add_issues(self, result: Dict, issues: List[ValidationIssue]):
        """Add issues to validation result"""
        for issue in issues:
            result['issues'][issue.severity].append({
                'message': issue.message,
                'field': issue.field,
                'value': issue.value,
                'constraint': issue.constraint,
                'suggestion': issue.suggestion
            })
    
    def _calculate_quality_score(self, result: Dict) -> float:
        """Calculate overall data quality score (0-100)"""
        total_errors = len(result['issues']['errors'])
        total_warnings = len(result['issues']['warnings'])
        total_info = len(result['issues']['info'])
        
        # Base score
        score = 100.0
        
        # Deduct points for issues
        score -= total_errors * 10  # 10 points per error
        score -= total_warnings * 3  # 3 points per warning
        score -= total_info * 1  # 1 point per info issue
        
        return max(0.0, score)
    
    def _generate_recommendations(self, dataset: Dict, result: Dict) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        errors = result['issues']['errors']
        warnings = result['issues']['warnings']
        
        if errors:
            recommendations.append(f"Fix {len(errors)} critical errors before proceeding with assignment")
        
        if len(warnings) > 5:
            recommendations.append("Address data quality warnings to improve assignment accuracy")
        
        agents = dataset.get('agents', [])
        tickets = dataset.get('tickets', [])
        
        if agents and tickets:
            # Specific recommendations based on data
            available_agents = sum(1 for a in agents if a.get('availability_status') == 'Available')
            if available_agents < len(agents) * 0.5:
                recommendations.append("Increase agent availability to improve response times")
            
            # Skill recommendations
            all_skills = set()
            for agent in agents:
                all_skills.update(agent.get('skills', {}).keys())
            
            if len(all_skills) < len(agents) * 2:
                recommendations.append("Diversify agent skills for better ticket coverage")
            
            # Workload recommendations
            if len(tickets) / len(agents) > 10:
                recommendations.append("Consider adding more agents or prioritizing ticket resolution")
        
        if result['data_quality_score'] < 80:
            recommendations.append("Improve data quality to achieve better assignment results")
        
        return recommendations
    
    def _generate_summary(self, dataset: Dict, result: Dict) -> Dict:
        """Generate validation summary statistics"""
        agents = dataset.get('agents', [])
        tickets = dataset.get('tickets', [])
        
        return {
            'total_agents': len(agents),
            'total_tickets': len(tickets),
            'available_agents': sum(1 for a in agents if a.get('availability_status') == 'Available'),
            'unique_skills': len(set(skill for agent in agents for skill in agent.get('skills', {}).keys())),
            'error_count': len(result['issues']['errors']),
            'warning_count': len(result['issues']['warnings']),
            'info_count': len(result['issues']['info']),
            'data_quality_score': result['data_quality_score'],
            'validation_timestamp': datetime.now().isoformat()
        }


def main():
    """Example usage of enhanced validator"""
    validator = EnhancedDataValidator()
    
    # Example dataset validation
    try:
        with open('dataset.json', 'r') as f:
            dataset = json.load(f)
        
        result = validator.validate_dataset(dataset)
        
        print(f"Validation Result: {'PASSED' if result['is_valid'] else 'FAILED'}")
        print(f"Data Quality Score: {result['data_quality_score']:.1f}/100")
        print(f"Issues: {result['total_issues']} total")
        
        if result['recommendations']:
            print("\nRecommendations:")
            for rec in result['recommendations']:
                print(f"- {rec}")
        
    except FileNotFoundError:
        print("No dataset.json found for validation")


if __name__ == "__main__":
    main()
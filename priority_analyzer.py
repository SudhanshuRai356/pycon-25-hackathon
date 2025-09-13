"""
Priority Analyzer Module for Support Ticket Assignment System

This module analyzes ticket descriptions to detect urgency indicators
and assigns priority levels based on keywords and context.
"""

import re
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class PriorityLevel(Enum):
    """Priority levels for tickets"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


@dataclass
class PriorityResult:
    """Result of priority analysis"""
    priority_level: PriorityLevel
    priority_score: float
    matched_keywords: List[str]
    rationale: str


class PriorityAnalyzer:
    """
    Analyzes ticket descriptions to determine priority based on urgency keywords
    and contextual indicators.
    """
    
    def __init__(self):
        self.urgency_keywords = self._initialize_keywords()
        self.impact_multipliers = self._initialize_impact_multipliers()
        
    def _initialize_keywords(self) -> Dict[PriorityLevel, Dict[str, float]]:
        """
        Initialize keyword dictionaries with weights for each priority level.
        Higher weights indicate more urgent keywords.
        """
        return {
            PriorityLevel.CRITICAL: {
                # System/Service outages
                "down": 10.0,
                "outage": 10.0,
                "crashed": 9.0,
                "unreachable": 8.0,
                "offline": 8.0,
                "not responding": 8.0,
                "completely broken": 9.0,
                "total failure": 10.0,
                "system failure": 9.0,
                "service unavailable": 9.0,
                "cannot access": 7.0,
                "all users affected": 8.0,
                "widespread": 7.0,
                "business critical": 9.0,
                "production down": 10.0,
                "emergency": 10.0,
                "urgent": 8.0,
                "immediately": 8.0,
                "critical": 9.0,
                "severe": 8.0,
                "catastrophic": 10.0,
                # Security-related critical issues
                "security breach": 10.0,
                "hacked": 10.0,
                "malware": 9.0,
                "virus": 8.0,
                "data breach": 10.0,
                "unauthorized access": 9.0,
                "compromised": 9.0,
                # Infrastructure failures
                "server down": 9.0,
                "network down": 9.0,
                "database down": 10.0,
                "backup failed": 8.0,
                "corruption": 8.0,
                "data loss": 9.0,
            },
            
            PriorityLevel.HIGH: {
                "broken": 6.0,
                "failing": 6.0,
                "error": 5.0,
                "problems": 4.0,
                "issues": 4.0,
                "not working": 6.0,
                "malfunctioning": 6.0,
                "stuck": 5.0,
                "frozen": 6.0,
                "slow": 4.0,
                "performance": 4.0,
                "timeout": 5.0,
                "intermittent": 5.0,
                "frequent": 5.0,
                "multiple users": 5.0,
                "department affected": 6.0,
                "productivity impact": 6.0,
                "blocking": 6.0,
                "prevents work": 6.0,
                "deadline": 7.0,
                "presentation": 6.0,
                "meeting": 5.0,
                "client": 6.0,
                "customer": 6.0,
                "important": 5.0,
                "asap": 6.0,
                "soon": 4.0,
                "today": 5.0,
                "tomorrow": 6.0,
                # Authentication/Access issues
                "cannot login": 6.0,
                "access denied": 6.0,
                "locked out": 6.0,
                "authentication": 5.0,
                "permissions": 4.0,
                # Hardware issues
                "hardware failure": 7.0,
                "hardware": 4.0,
                "device": 3.0,
                "laptop": 3.0,
                "printer": 3.0,
            },
            
            PriorityLevel.MEDIUM: {
                "help": 2.0,
                "assistance": 2.0,
                "support": 2.0,
                "question": 2.0,
                "how to": 2.0,
                "configure": 2.0,
                "setup": 2.0,
                "install": 2.0,
                "update": 2.0,
                "upgrade": 2.0,
                "request": 2.0,
                "need": 2.0,
                "would like": 2.0,
                "minor": 1.0,
                "small": 1.0,
                "quick": 2.0,
                "whenever convenient": 1.0,
                "next week": 1.0,
                "training": 2.0,
                "documentation": 2.0,
                "clarification": 2.0,
                "guidance": 2.0,
                # Routine maintenance
                "maintenance": 2.0,
                "routine": 1.0,
                "scheduled": 1.0,
                "planned": 1.0,
            },
            
            PriorityLevel.LOW: {
                "enhancement": 1.0,
                "feature request": 1.0,
                "improvement": 1.0,
                "suggestion": 1.0,
                "optimization": 1.0,
                "nice to have": 0.5,
                "when possible": 0.5,
                "future": 0.5,
                "eventually": 0.5,
                "cosmetic": 0.5,
                "aesthetic": 0.5,
                "convenience": 1.0,
                "preference": 0.5,
                "general": 1.0,
                "information": 1.0,
                "inquiry": 1.0,
                "feedback": 1.0,
            }
        }
    
    def _initialize_impact_multipliers(self) -> Dict[str, float]:
        """
        Initialize impact multipliers based on scope and business impact.
        These multiply the base keyword scores.
        """
        return {
            # Scope multipliers
            "all users": 2.0,
            "entire": 2.0,
            "whole": 2.0,
            "company": 2.0,
            "organization": 2.0,
            "everyone": 2.0,
            "multiple departments": 1.8,
            "department": 1.5,
            "team": 1.3,
            "group": 1.3,
            "several users": 1.4,
            "many users": 1.4,
            
            # Business impact multipliers
            "revenue": 2.5,
            "business": 2.0,
            "production": 2.5,
            "customer": 2.0,
            "client": 2.0,
            "public": 2.0,
            "external": 1.8,
            "reputation": 2.0,
            "brand": 2.0,
            "compliance": 2.2,
            "audit": 2.0,
            "legal": 2.2,
            "regulatory": 2.2,
            
            # Time sensitivity multipliers
            "now": 1.8,
            "immediately": 2.0,
            "asap": 1.8,
            "urgent": 1.8,
            "today": 1.5,
            "this morning": 1.6,
            "right now": 2.0,
            "before": 1.5,
            "deadline": 1.8,
            "meeting": 1.4,
            "presentation": 1.6,
            "demo": 1.5,
            
            # Frequency multipliers (recurring issues are more serious)
            "again": 1.3,
            "repeatedly": 1.5,
            "frequently": 1.4,
            "constantly": 1.6,
            "always": 1.4,
            "continuous": 1.5,
            "ongoing": 1.4,
            "persistent": 1.4,
        }
    
    def analyze_priority(self, title: str, description: str) -> PriorityResult:
        """
        Analyze ticket title and description to determine priority.
        
        Args:
            title: The ticket title
            description: The ticket description
            
        Returns:
            PriorityResult with priority level, score, and rationale
        """
        # Combine title and description for analysis
        full_text = f"{title} {description}".lower()
        
        # Initialize tracking variables
        priority_scores = {level: 0.0 for level in PriorityLevel}
        matched_keywords = []
        impact_multiplier = 1.0
        
        # Analyze keywords for each priority level
        for priority_level, keywords in self.urgency_keywords.items():
            for keyword, weight in keywords.items():
                if self._find_keyword_in_text(keyword, full_text):
                    priority_scores[priority_level] += weight
                    matched_keywords.append(keyword)
        
        # Apply impact multipliers
        for impact_phrase, multiplier in self.impact_multipliers.items():
            if self._find_keyword_in_text(impact_phrase, full_text):
                impact_multiplier = max(impact_multiplier, multiplier)
        
        # Calculate final scores with impact multipliers
        final_scores = {
            level: score * impact_multiplier 
            for level, score in priority_scores.items()
        }
        
        # Determine the winning priority level
        winning_priority = self._determine_winning_priority(final_scores)
        final_score = final_scores[winning_priority]
        
        # Generate rationale
        rationale = self._generate_rationale(
            winning_priority, final_score, matched_keywords, impact_multiplier
        )
        
        return PriorityResult(
            priority_level=winning_priority,
            priority_score=final_score,
            matched_keywords=matched_keywords,
            rationale=rationale
        )
    
    def _find_keyword_in_text(self, keyword: str, text: str) -> bool:
        """
        Find keyword in text using case-insensitive regex with word boundaries.
        """
        # Create pattern with word boundaries for exact matches
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        return bool(re.search(pattern, text.lower()))
    
    def _determine_winning_priority(self, scores: Dict[PriorityLevel, float]) -> PriorityLevel:
        """
        Determine the winning priority based on scores.
        If no keywords match, default to MEDIUM priority.
        """
        # Find the priority level with the highest score
        max_score = max(scores.values())
        
        if max_score == 0:
            return PriorityLevel.MEDIUM  # Default when no keywords match
        
        # Return the priority level with the highest score
        for priority_level, score in scores.items():
            if score == max_score:
                return priority_level
        
        return PriorityLevel.MEDIUM  # Fallback
    
    def _generate_rationale(
        self, 
        priority: PriorityLevel, 
        score: float, 
        keywords: List[str], 
        multiplier: float
    ) -> str:
        """Generate human-readable rationale for the priority assignment."""
        rationale_parts = []
        
        # Base priority explanation
        rationale_parts.append(f"Assigned {priority.name} priority")
        
        if keywords:
            # Limit keywords shown in rationale
            shown_keywords = keywords[:5]  # Show max 5 keywords
            keyword_text = ", ".join([f"'{kw}'" for kw in shown_keywords])
            if len(keywords) > 5:
                keyword_text += f" and {len(keywords) - 5} more"
            rationale_parts.append(f"based on urgency indicators: {keyword_text}")
        
        if multiplier > 1.0:
            rationale_parts.append(f"with {multiplier:.1f}x impact multiplier for scope/business impact")
        
        rationale_parts.append(f"(Priority score: {score:.1f})")
        
        return " ".join(rationale_parts) + "."
    
    def get_priority_statistics(self, tickets: List[Dict]) -> Dict:
        """
        Analyze a list of tickets and return priority distribution statistics.
        """
        priority_counts = {level.name: 0 for level in PriorityLevel}
        total_tickets = len(tickets)
        
        detailed_results = []
        
        for ticket in tickets:
            result = self.analyze_priority(
                ticket.get('title', ''), 
                ticket.get('description', '')
            )
            priority_counts[result.priority_level.name] += 1
            
            detailed_results.append({
                'ticket_id': ticket.get('ticket_id'),
                'title': ticket.get('title'),
                'priority': result.priority_level.name,
                'score': result.priority_score,
                'keywords': result.matched_keywords,
                'rationale': result.rationale
            })
        
        return {
            'total_tickets': total_tickets,
            'priority_distribution': priority_counts,
            'priority_percentages': {
                level: (count / total_tickets * 100) if total_tickets > 0 else 0
                for level, count in priority_counts.items()
            },
            'detailed_results': detailed_results
        }


def main():
    """Example usage of the PriorityAnalyzer"""
    analyzer = PriorityAnalyzer()
    
    # Example ticket
    example_ticket = {
        'title': "VPN connection dropping intermittently for all remote users",
        'description': "Users connecting via the corporate VPN client are experiencing frequent, random disconnections. This issue seems to be widespread and is affecting multiple departments, particularly those using resource-intensive applications."
    }
    
    result = analyzer.analyze_priority(
        example_ticket['title'], 
        example_ticket['description']
    )
    
    print(f"Priority: {result.priority_level.name}")
    print(f"Score: {result.priority_score}")
    print(f"Keywords: {result.matched_keywords}")
    print(f"Rationale: {result.rationale}")


if __name__ == "__main__":
    main()
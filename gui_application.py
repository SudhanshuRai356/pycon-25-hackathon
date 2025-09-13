"""
Enhanced Ticket Assignment System GUI with Data Validation

A comprehensive GUI application for the PyCon25 Hackathon project with
advanced data validation, constraints, and interactive features.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from typing import Dict, List, Optional, Tuple
import re
from dataclasses import dataclass
from enum import Enum

# Import our custom modules
from priority_analyzer import PriorityAnalyzer, PriorityLevel
from ticket_assignment_system import TicketAssignmentSystem


@dataclass
class ValidationResult:
    """Result of data validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]


class DataValidator:
    """Enhanced data validation with comprehensive constraints"""
    
    def __init__(self):
        self.required_agent_fields = ['agent_id', 'name', 'skills', 'availability_status', 'experience_level']
        self.required_ticket_fields = ['ticket_id', 'title', 'description', 'creation_timestamp']
        self.valid_availability_statuses = ['Available', 'Busy', 'Offline', 'On Leave']
        self.skill_level_range = (1, 10)
        self.experience_level_range = (0, 50)
        self.max_current_load = 20
        
    def validate_dataset(self, dataset: Dict) -> ValidationResult:
        """Comprehensive dataset validation"""
        errors = []
        warnings = []
        
        # Check top-level structure
        if 'agents' not in dataset:
            errors.append("Missing 'agents' section in dataset")
        if 'tickets' not in dataset:
            errors.append("Missing 'tickets' section in dataset")
        
        if errors:  # Cannot continue without basic structure
            return ValidationResult(False, errors, warnings)
        
        # Validate agents
        agent_validation = self._validate_agents(dataset['agents'])
        errors.extend(agent_validation.errors)
        warnings.extend(agent_validation.warnings)
        
        # Validate tickets
        ticket_validation = self._validate_tickets(dataset['tickets'])
        errors.extend(ticket_validation.errors)
        warnings.extend(ticket_validation.warnings)
        
        # Cross-validation
        cross_validation = self._validate_cross_references(dataset)
        errors.extend(cross_validation.errors)
        warnings.extend(cross_validation.warnings)
        
        return ValidationResult(len(errors) == 0, errors, warnings)
    
    def _validate_agents(self, agents: List[Dict]) -> ValidationResult:
        """Validate agent data"""
        errors = []
        warnings = []
        
        if not agents:
            errors.append("No agents found in dataset")
            return ValidationResult(False, errors, warnings)
        
        agent_ids = set()
        
        for i, agent in enumerate(agents):
            prefix = f"Agent {i+1}"
            
            # Check required fields
            for field in self.required_agent_fields:
                if field not in agent:
                    errors.append(f"{prefix}: Missing required field '{field}'")
            
            # Validate agent_id
            agent_id = agent.get('agent_id', '')
            if not agent_id:
                errors.append(f"{prefix}: Empty agent_id")
            elif agent_id in agent_ids:
                errors.append(f"{prefix}: Duplicate agent_id '{agent_id}'")
            else:
                agent_ids.add(agent_id)
            
            if not re.match(r'^agent_\d{3}$', agent_id):
                warnings.append(f"{prefix}: agent_id '{agent_id}' doesn't follow expected format 'agent_XXX'")
            
            # Validate name
            name = agent.get('name', '')
            if not name or len(name.strip()) < 2:
                errors.append(f"{prefix}: Invalid or missing name")
            
            # Validate skills
            skills = agent.get('skills', {})
            if not isinstance(skills, dict):
                errors.append(f"{prefix}: Skills must be a dictionary")
            elif not skills:
                warnings.append(f"{prefix}: No skills defined")
            else:
                for skill_name, skill_level in skills.items():
                    if not isinstance(skill_level, (int, float)):
                        errors.append(f"{prefix}: Skill '{skill_name}' level must be numeric")
                    elif not (self.skill_level_range[0] <= skill_level <= self.skill_level_range[1]):
                        errors.append(f"{prefix}: Skill '{skill_name}' level {skill_level} out of range {self.skill_level_range}")
            
            # Validate availability status
            availability = agent.get('availability_status', '')
            if availability not in self.valid_availability_statuses:
                errors.append(f"{prefix}: Invalid availability_status '{availability}'. Must be one of {self.valid_availability_statuses}")
            
            # Validate experience level
            experience = agent.get('experience_level', 0)
            if not isinstance(experience, (int, float)):
                errors.append(f"{prefix}: experience_level must be numeric")
            elif not (self.experience_level_range[0] <= experience <= self.experience_level_range[1]):
                errors.append(f"{prefix}: experience_level {experience} out of range {self.experience_level_range}")
            
            # Validate current load
            current_load = agent.get('current_load', 0)
            if not isinstance(current_load, (int, float)):
                errors.append(f"{prefix}: current_load must be numeric")
            elif current_load < 0:
                errors.append(f"{prefix}: current_load cannot be negative")
            elif current_load > self.max_current_load:
                warnings.append(f"{prefix}: High current_load ({current_load}), may affect assignment quality")
        
        return ValidationResult(len(errors) == 0, errors, warnings)
    
    def _validate_tickets(self, tickets: List[Dict]) -> ValidationResult:
        """Validate ticket data"""
        errors = []
        warnings = []
        
        if not tickets:
            errors.append("No tickets found in dataset")
            return ValidationResult(False, errors, warnings)
        
        ticket_ids = set()
        
        for i, ticket in enumerate(tickets):
            prefix = f"Ticket {i+1}"
            
            # Check required fields
            for field in self.required_ticket_fields:
                if field not in ticket:
                    errors.append(f"{prefix}: Missing required field '{field}'")
            
            # Validate ticket_id
            ticket_id = ticket.get('ticket_id', '')
            if not ticket_id:
                errors.append(f"{prefix}: Empty ticket_id")
            elif ticket_id in ticket_ids:
                errors.append(f"{prefix}: Duplicate ticket_id '{ticket_id}'")
            else:
                ticket_ids.add(ticket_id)
            
            if not re.match(r'^TKT-\d{4}-\d{3}$', ticket_id):
                warnings.append(f"{prefix}: ticket_id '{ticket_id}' doesn't follow expected format 'TKT-YYYY-XXX'")
            
            # Validate title
            title = ticket.get('title', '')
            if not title or len(title.strip()) < 5:
                errors.append(f"{prefix}: Title too short or missing")
            elif len(title) > 200:
                warnings.append(f"{prefix}: Title very long ({len(title)} chars), consider shortening")
            
            # Validate description
            description = ticket.get('description', '')
            if not description or len(description.strip()) < 10:
                errors.append(f"{prefix}: Description too short or missing")
            elif len(description) > 5000:
                warnings.append(f"{prefix}: Description very long ({len(description)} chars)")
            
            # Validate timestamp
            timestamp = ticket.get('creation_timestamp')
            if not isinstance(timestamp, (int, float)):
                errors.append(f"{prefix}: creation_timestamp must be numeric (Unix timestamp)")
            else:
                # Check if timestamp is reasonable (not too far in past/future)
                now = datetime.now().timestamp()
                year_ago = now - (365 * 24 * 60 * 60)
                week_future = now + (7 * 24 * 60 * 60)
                
                if timestamp < year_ago:
                    warnings.append(f"{prefix}: Ticket created more than a year ago")
                elif timestamp > week_future:
                    warnings.append(f"{prefix}: Ticket created in the future")
        
        return ValidationResult(len(errors) == 0, errors, warnings)
    
    def _validate_cross_references(self, dataset: Dict) -> ValidationResult:
        """Validate cross-references and business logic"""
        errors = []
        warnings = []
        
        agents = dataset.get('agents', [])
        tickets = dataset.get('tickets', [])
        
        # Check agent-to-ticket ratio
        if len(agents) == 0:
            errors.append("Cannot assign tickets without any agents")
        elif len(tickets) / len(agents) > 15:
            warnings.append(f"High ticket-to-agent ratio ({len(tickets)}/{len(agents)}), may cause overload")
        
        # Check skill coverage
        all_skills = set()
        for agent in agents:
            all_skills.update(agent.get('skills', {}).keys())
        
        if len(all_skills) < 5:
            warnings.append("Limited skill diversity across agents, may affect assignment quality")
        
        # Check availability
        available_agents = [a for a in agents if a.get('availability_status') == 'Available']
        if len(available_agents) == 0:
            errors.append("No available agents for assignment")
        elif len(available_agents) / len(agents) < 0.5:
            warnings.append("Less than 50% of agents are available")
        
        return ValidationResult(len(errors) == 0, errors, warnings)


class TicketAssignmentGUI:
    """Enhanced GUI application with comprehensive features"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PyCon25 Hackathon - Intelligent Ticket Assignment System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.validator = DataValidator()
        self.priority_analyzer = PriorityAnalyzer()
        self.assignment_system = TicketAssignmentSystem()
        
        # Data storage
        self.dataset = None
        self.assignments = None
        self.filtered_assignments = None
        
        # Style configuration
        self.setup_styles()
        
        # Create GUI components
        self.create_widgets()
        
        # Load initial data
        self.load_initial_data()
    
    def setup_styles(self):
        """Configure modern styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors and fonts
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        style.configure('Success.TLabel', foreground='green', font=('Arial', 10, 'bold'))
        style.configure('Error.TLabel', foreground='red', font=('Arial', 10, 'bold'))
        style.configure('Warning.TLabel', foreground='orange', font=('Arial', 10, 'bold'))
        
        # Configure button styles
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        style.map('Action.TButton', background=[('active', '#0078d4')])
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_overview_tab()
        self.create_data_tab()
        self.create_assignment_tab()
        self.create_analysis_tab()
        self.create_validation_tab()
    
    def create_overview_tab(self):
        """Create overview/dashboard tab"""
        self.overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.overview_frame, text="📊 Overview")
        
        # Title
        title_label = ttk.Label(self.overview_frame, text="Intelligent Support Ticket Assignment System", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Quick stats frame
        stats_frame = ttk.LabelFrame(self.overview_frame, text="Quick Statistics", padding=15)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Create stats grid
        self.stats_vars = {
            'total_tickets': tk.StringVar(value="0"),
            'total_agents': tk.StringVar(value="0"),
            'critical_tickets': tk.StringVar(value="0"),
            'available_agents': tk.StringVar(value="0"),
            'avg_skills_per_agent': tk.StringVar(value="0"),
            'assignment_efficiency': tk.StringVar(value="0%")
        }
        
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill='x')
        
        stat_labels = [
            ("Total Tickets:", 'total_tickets'),
            ("Total Agents:", 'total_agents'),
            ("Critical Tickets:", 'critical_tickets'),
            ("Available Agents:", 'available_agents'),
            ("Avg Skills/Agent:", 'avg_skills_per_agent'),
            ("Assignment Efficiency:", 'assignment_efficiency')
        ]
        
        for i, (label, var_key) in enumerate(stat_labels):
            row, col = divmod(i, 3)
            ttk.Label(stats_grid, text=label, font=('Arial', 10, 'bold')).grid(row=row*2, column=col, sticky='w', padx=20, pady=5)
            ttk.Label(stats_grid, textvariable=self.stats_vars[var_key], font=('Arial', 12)).grid(row=row*2+1, column=col, sticky='w', padx=20)
        
        # Action buttons frame
        actions_frame = ttk.LabelFrame(self.overview_frame, text="Quick Actions", padding=15)
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        btn_frame = ttk.Frame(actions_frame)
        btn_frame.pack()
        
        ttk.Button(btn_frame, text="📁 Load Dataset", command=self.load_dataset, style='Action.TButton').pack(side='left', padx=10)
        ttk.Button(btn_frame, text="🎯 Run Assignment", command=self.run_assignment, style='Action.TButton').pack(side='left', padx=10)
        ttk.Button(btn_frame, text="✅ Validate Data", command=self.validate_data, style='Action.TButton').pack(side='left', padx=10)
        ttk.Button(btn_frame, text="💾 Export Results", command=self.export_results, style='Action.TButton').pack(side='left', padx=10)
        
        # Status frame
        self.status_frame = ttk.LabelFrame(self.overview_frame, text="System Status", padding=15)
        self.status_frame.pack(fill='x', padx=20, pady=10)
        
        self.status_var = tk.StringVar(value="Ready - Load dataset to begin")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, font=('Arial', 11))
        self.status_label.pack()
    
    def create_data_tab(self):
        """Create data viewing/editing tab"""
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="📋 Data")
        
        # Data type selector
        selector_frame = ttk.Frame(self.data_frame)
        selector_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(selector_frame, text="View:", font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        self.data_type_var = tk.StringVar(value="agents")
        data_types = [("👥 Agents", "agents"), ("🎫 Tickets", "tickets")]
        
        for text, value in data_types:
            ttk.Radiobutton(selector_frame, text=text, variable=self.data_type_var, 
                          value=value, command=self.refresh_data_view).pack(side='left', padx=10)
        
        # Search and filter frame
        filter_frame = ttk.Frame(self.data_frame)
        filter_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Search:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        ttk.Button(filter_frame, text="🔄 Refresh", command=self.refresh_data_view).pack(side='right', padx=5)
        
        # Data treeview
        tree_frame = ttk.Frame(self.data_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.data_tree = ttk.Treeview(tree_frame, selectmode='extended')
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.data_tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.data_tree.xview)
        self.data_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Pack treeview and scrollbars
        self.data_tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def create_assignment_tab(self):
        """Create assignment results tab"""
        self.assignment_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.assignment_frame, text="🎯 Assignments")
        
        # Controls frame
        controls_frame = ttk.Frame(self.assignment_frame)
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        # Priority filter
        ttk.Label(controls_frame, text="Priority Filter:").pack(side='left', padx=5)
        self.priority_filter_var = tk.StringVar(value="All")
        priority_combo = ttk.Combobox(controls_frame, textvariable=self.priority_filter_var, 
                                    values=["All", "CRITICAL", "HIGH", "MEDIUM", "LOW"], width=15)
        priority_combo.pack(side='left', padx=5)
        priority_combo.bind('<<ComboboxSelected>>', self.filter_assignments)
        
        # Agent filter
        ttk.Label(controls_frame, text="Agent:").pack(side='left', padx=(20, 5))
        self.agent_filter_var = tk.StringVar(value="All")
        self.agent_combo = ttk.Combobox(controls_frame, textvariable=self.agent_filter_var, width=20)
        self.agent_combo.pack(side='left', padx=5)
        self.agent_combo.bind('<<ComboboxSelected>>', self.filter_assignments)
        
        # Assignment treeview
        assignment_tree_frame = ttk.Frame(self.assignment_frame)
        assignment_tree_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.assignment_tree = ttk.Treeview(assignment_tree_frame, 
                                          columns=('Priority', 'Agent', 'Skill Score', 'Priority Score', 'Rationale'),
                                          show='tree headings')
        
        # Configure columns
        self.assignment_tree.heading('#0', text='Ticket ID')
        self.assignment_tree.heading('Priority', text='Priority')
        self.assignment_tree.heading('Agent', text='Assigned Agent')
        self.assignment_tree.heading('Skill Score', text='Skill Score')
        self.assignment_tree.heading('Priority Score', text='Priority Score')
        self.assignment_tree.heading('Rationale', text='Rationale')
        
        self.assignment_tree.column('#0', width=120)
        self.assignment_tree.column('Priority', width=80)
        self.assignment_tree.column('Agent', width=120)
        self.assignment_tree.column('Skill Score', width=100)
        self.assignment_tree.column('Priority Score', width=100)
        self.assignment_tree.column('Rationale', width=400)
        
        # Scrollbars for assignments
        v_scroll_assign = ttk.Scrollbar(assignment_tree_frame, orient='vertical', command=self.assignment_tree.yview)
        h_scroll_assign = ttk.Scrollbar(assignment_tree_frame, orient='horizontal', command=self.assignment_tree.xview)
        self.assignment_tree.configure(yscrollcommand=v_scroll_assign.set, xscrollcommand=h_scroll_assign.set)
        
        self.assignment_tree.grid(row=0, column=0, sticky='nsew')
        v_scroll_assign.grid(row=0, column=1, sticky='ns')
        h_scroll_assign.grid(row=1, column=0, sticky='ew')
        
        assignment_tree_frame.grid_rowconfigure(0, weight=1)
        assignment_tree_frame.grid_columnconfigure(0, weight=1)
        
        # Assignment summary
        summary_frame = ttk.LabelFrame(self.assignment_frame, text="Assignment Summary", padding=10)
        summary_frame.pack(fill='x', padx=10, pady=5)
        
        self.assignment_summary_var = tk.StringVar(value="No assignments yet")
        ttk.Label(summary_frame, textvariable=self.assignment_summary_var).pack()
    
    def create_analysis_tab(self):
        """Create analysis and visualization tab"""
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="📈 Analysis")
        
        # Chart selection frame
        chart_frame = ttk.Frame(self.analysis_frame)
        chart_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(chart_frame, text="Visualization:", font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        self.chart_type_var = tk.StringVar(value="priority_distribution")
        chart_types = [
            ("Priority Distribution", "priority_distribution"),
            ("Agent Workload", "agent_workload"),
            ("Skill Match Scores", "skill_scores"),
            ("Assignment Timeline", "timeline")
        ]
        
        for text, value in chart_types:
            ttk.Radiobutton(chart_frame, text=text, variable=self.chart_type_var, 
                          value=value, command=self.update_chart).pack(side='left', padx=10)
        
        # Chart canvas frame
        self.chart_frame = ttk.Frame(self.analysis_frame)
        self.chart_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Placeholder label
        self.chart_placeholder = ttk.Label(self.chart_frame, text="Run assignment to see visualizations", 
                                         font=('Arial', 12))
        self.chart_placeholder.pack(expand=True)
    
    def create_validation_tab(self):
        """Create data validation tab"""
        self.validation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.validation_frame, text="✅ Validation")
        
        # Validation controls
        controls_frame = ttk.Frame(self.validation_frame)
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(controls_frame, text="🔍 Run Validation", command=self.run_validation, 
                 style='Action.TButton').pack(side='left', padx=5)
        
        ttk.Button(controls_frame, text="📋 Export Report", command=self.export_validation_report, 
                 style='Action.TButton').pack(side='left', padx=5)
        
        # Validation results
        results_frame = ttk.LabelFrame(self.validation_frame, text="Validation Results", padding=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create text widget for results
        text_frame = ttk.Frame(results_frame)
        text_frame.pack(fill='both', expand=True)
        
        self.validation_text = tk.Text(text_frame, wrap='word', font=('Consolas', 10))
        validation_scroll = ttk.Scrollbar(text_frame, orient='vertical', command=self.validation_text.yview)
        self.validation_text.configure(yscrollcommand=validation_scroll.set)
        
        self.validation_text.pack(side='left', fill='both', expand=True)
        validation_scroll.pack(side='right', fill='y')
        
        # Configure text tags for colored output
        self.validation_text.tag_configure('error', foreground='red', font=('Consolas', 10, 'bold'))
        self.validation_text.tag_configure('warning', foreground='orange', font=('Consolas', 10, 'bold'))
        self.validation_text.tag_configure('success', foreground='green', font=('Consolas', 10, 'bold'))
        self.validation_text.tag_configure('info', foreground='blue', font=('Consolas', 10))
    
    def load_initial_data(self):
        """Load the default dataset.json if available"""
        try:
            with open('dataset.json', 'r', encoding='utf-8') as f:
                self.dataset = json.load(f)
            self.update_status("Dataset loaded successfully", "success")
            self.update_statistics()
            self.refresh_data_view()
            self.update_agent_filter()
        except FileNotFoundError:
            self.update_status("No dataset.json found - please load a dataset", "warning")
        except Exception as e:
            self.update_status(f"Error loading dataset: {str(e)}", "error")
    
    def load_dataset(self):
        """Load dataset from file dialog"""
        file_path = filedialog.askopenfilename(
            title="Select Dataset File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.dataset = json.load(f)
                self.update_status(f"Dataset loaded: {file_path}", "success")
                self.update_statistics()
                self.refresh_data_view()
                self.update_agent_filter()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dataset:\n{str(e)}")
                self.update_status(f"Failed to load dataset: {str(e)}", "error")
    
    def run_assignment(self):
        """Run the ticket assignment algorithm"""
        if not self.dataset:
            messagebox.showwarning("Warning", "Please load a dataset first")
            return
        
        try:
            self.update_status("Running assignment algorithm...", "info")
            self.root.update()
            
            # Run assignment
            self.assignments = self.assignment_system.assign_tickets(self.dataset)
            self.filtered_assignments = self.assignments.copy()
            
            # Update GUI
            self.refresh_assignment_view()
            self.update_assignment_summary()
            self.update_chart()
            
            self.update_status(f"Assignment completed - {len(self.assignments)} tickets assigned", "success")
            
        except Exception as e:
            messagebox.showerror("Error", f"Assignment failed:\n{str(e)}")
            self.update_status(f"Assignment failed: {str(e)}", "error")
    
    def validate_data(self):
        """Run comprehensive data validation"""
        if not self.dataset:
            messagebox.showwarning("Warning", "Please load a dataset first")
            return
        
        self.run_validation()
        self.notebook.select(4)  # Switch to validation tab
    
    def export_results(self):
        """Export assignment results"""
        if not self.assignments:
            messagebox.showwarning("Warning", "No assignments to export. Run assignment first.")
            return
        
        try:
            # Export standard format
            self.assignment_system.generate_output_file(self.assignments)
            
            # Export detailed report
            self.assignment_system.generate_detailed_report(self.assignments)
            
            messagebox.showinfo("Success", "Results exported to:\n- output_result.json\n- detailed_assignment_report.json")
            self.update_status("Results exported successfully", "success")
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed:\n{str(e)}")
    
    def update_status(self, message: str, status_type: str = "info"):
        """Update status message with color coding"""
        self.status_var.set(message)
        
        if status_type == "success":
            self.status_label.configure(style='Success.TLabel')
        elif status_type == "error":
            self.status_label.configure(style='Error.TLabel')
        elif status_type == "warning":
            self.status_label.configure(style='Warning.TLabel')
        else:
            self.status_label.configure(style='TLabel')
    
    def update_statistics(self):
        """Update overview statistics"""
        if not self.dataset:
            return
        
        agents = self.dataset.get('agents', [])
        tickets = self.dataset.get('tickets', [])
        
        # Basic counts
        self.stats_vars['total_tickets'].set(str(len(tickets)))
        self.stats_vars['total_agents'].set(str(len(agents)))
        
        # Available agents
        available = sum(1 for a in agents if a.get('availability_status') == 'Available')
        self.stats_vars['available_agents'].set(str(available))
        
        # Critical tickets (using priority analyzer)
        critical_count = 0
        for ticket in tickets:
            priority = self.priority_analyzer.analyze_priority(
                ticket.get('title', ''), ticket.get('description', '')
            )
            if priority.priority_level == PriorityLevel.CRITICAL:
                critical_count += 1
        
        self.stats_vars['critical_tickets'].set(str(critical_count))
        
        # Average skills per agent
        if agents:
            avg_skills = sum(len(a.get('skills', {})) for a in agents) / len(agents)
            self.stats_vars['avg_skills_per_agent'].set(f"{avg_skills:.1f}")
        
        # Assignment efficiency (if assignments available)
        if self.assignments and agents:
            efficiency = (available / len(agents)) * 100 if agents else 0
            self.stats_vars['assignment_efficiency'].set(f"{efficiency:.1f}%")
    
    def refresh_data_view(self):
        """Refresh the data viewing tab"""
        if not self.dataset:
            return
        
        # Clear existing items
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        data_type = self.data_type_var.get()
        
        if data_type == "agents":
            self.show_agents_data()
        else:
            self.show_tickets_data()
    
    def show_agents_data(self):
        """Display agents data in treeview"""
        agents = self.dataset.get('agents', [])
        
        # Configure columns for agents
        self.data_tree['columns'] = ('Name', 'Experience', 'Availability', 'Current Load', 'Skills Count')
        
        # Configure headings
        self.data_tree.heading('#0', text='Agent ID')
        self.data_tree.heading('Name', text='Name')
        self.data_tree.heading('Experience', text='Experience (years)')
        self.data_tree.heading('Availability', text='Availability')
        self.data_tree.heading('Current Load', text='Current Load')
        self.data_tree.heading('Skills Count', text='Skills Count')
        
        # Configure column widths
        self.data_tree.column('#0', width=100)
        self.data_tree.column('Name', width=150)
        self.data_tree.column('Experience', width=120)
        self.data_tree.column('Availability', width=100)
        self.data_tree.column('Current Load', width=100)
        self.data_tree.column('Skills Count', width=100)
        
        # Filter based on search
        search_term = self.search_var.get().lower()
        
        for agent in agents:
            agent_id = agent.get('agent_id', '')
            name = agent.get('name', '')
            
            # Apply search filter
            if search_term and search_term not in agent_id.lower() and search_term not in name.lower():
                continue
            
            values = (
                name,
                agent.get('experience_level', 0),
                agent.get('availability_status', ''),
                agent.get('current_load', 0),
                len(agent.get('skills', {}))
            )
            
            item = self.data_tree.insert('', 'end', text=agent_id, values=values)
            
            # Add skills as child items
            for skill, level in agent.get('skills', {}).items():
                self.data_tree.insert(item, 'end', text=f"  {skill}", values=('', '', '', '', level))
    
    def show_tickets_data(self):
        """Display tickets data in treeview"""
        tickets = self.dataset.get('tickets', [])
        
        # Configure columns for tickets
        self.data_tree['columns'] = ('Title', 'Priority', 'Priority Score', 'Creation Date')
        
        # Configure headings
        self.data_tree.heading('#0', text='Ticket ID')
        self.data_tree.heading('Title', text='Title')
        self.data_tree.heading('Priority', text='Priority')
        self.data_tree.heading('Priority Score', text='Priority Score')
        self.data_tree.heading('Creation Date', text='Creation Date')
        
        # Configure column widths
        self.data_tree.column('#0', width=120)
        self.data_tree.column('Title', width=300)
        self.data_tree.column('Priority', width=80)
        self.data_tree.column('Priority Score', width=100)
        self.data_tree.column('Creation Date', width=150)
        
        # Filter based on search
        search_term = self.search_var.get().lower()
        
        for ticket in tickets:
            ticket_id = ticket.get('ticket_id', '')
            title = ticket.get('title', '')
            description = ticket.get('description', '')
            
            # Apply search filter
            if search_term and not any(search_term in text.lower() for text in [ticket_id, title, description]):
                continue
            
            # Get priority analysis
            priority_result = self.priority_analyzer.analyze_priority(title, description)
            
            # Format creation date
            timestamp = ticket.get('creation_timestamp', 0)
            try:
                creation_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
            except:
                creation_date = 'Invalid Date'
            
            values = (
                title[:50] + ('...' if len(title) > 50 else ''),
                priority_result.priority_level.name,
                f"{priority_result.priority_score:.1f}",
                creation_date
            )
            
            self.data_tree.insert('', 'end', text=ticket_id, values=values)
    
    def on_search_change(self, *args):
        """Handle search text change"""
        self.refresh_data_view()
    
    def update_agent_filter(self):
        """Update agent filter combobox"""
        if not self.dataset:
            return
        
        agents = self.dataset.get('agents', [])
        agent_options = ["All"] + [f"{a.get('agent_id', '')} - {a.get('name', '')}" for a in agents]
        self.agent_combo['values'] = agent_options
        self.agent_filter_var.set("All")
    
    def filter_assignments(self, event=None):
        """Filter assignments based on selected criteria"""
        if not self.assignments:
            return
        
        priority_filter = self.priority_filter_var.get()
        agent_filter = self.agent_filter_var.get()
        
        # Apply filters
        self.filtered_assignments = []
        
        for assignment in self.assignments:
            # Priority filter
            if priority_filter != "All" and assignment.priority_level != priority_filter:
                continue
            
            # Agent filter
            if agent_filter != "All":
                agent_id = agent_filter.split(' - ')[0] if ' - ' in agent_filter else agent_filter
                if assignment.assigned_agent_id != agent_id:
                    continue
            
            self.filtered_assignments.append(assignment)
        
        self.refresh_assignment_view()
    
    def refresh_assignment_view(self):
        """Refresh assignment results view"""
        # Clear existing items
        for item in self.assignment_tree.get_children():
            self.assignment_tree.delete(item)
        
        if not self.filtered_assignments:
            return
        
        # Sort by priority and score
        sorted_assignments = sorted(self.filtered_assignments, 
                                  key=lambda x: (x.priority_level, -x.priority_score))
        
        for assignment in sorted_assignments:
            # Get agent name
            agent_name = "Unknown"
            if self.dataset:
                for agent in self.dataset.get('agents', []):
                    if agent.get('agent_id') == assignment.assigned_agent_id:
                        agent_name = agent.get('name', 'Unknown')
                        break
            
            values = (
                assignment.priority_level,
                f"{assignment.assigned_agent_id} - {agent_name}",
                f"{assignment.skill_match_score:.3f}",
                f"{assignment.priority_score:.1f}",
                assignment.rationale
            )
            
            item = self.assignment_tree.insert('', 'end', text=assignment.ticket_id, values=values)
            
            # Color code by priority
            if assignment.priority_level == "CRITICAL":
                self.assignment_tree.set(item, 'Priority', "🚨 CRITICAL")
            elif assignment.priority_level == "HIGH":
                self.assignment_tree.set(item, 'Priority', "⚠️ HIGH")
            elif assignment.priority_level == "MEDIUM":
                self.assignment_tree.set(item, 'Priority', "📋 MEDIUM")
            else:
                self.assignment_tree.set(item, 'Priority', "📝 LOW")
    
    def update_assignment_summary(self):
        """Update assignment summary statistics"""
        if not self.assignments:
            return
        
        total = len(self.assignments)
        priority_counts = {}
        agent_counts = {}
        
        for assignment in self.assignments:
            priority_counts[assignment.priority_level] = priority_counts.get(assignment.priority_level, 0) + 1
            agent_counts[assignment.assigned_agent_id] = agent_counts.get(assignment.assigned_agent_id, 0) + 1
        
        summary_text = f"Total Assignments: {total} | "
        summary_text += " | ".join([f"{priority}: {count}" for priority, count in priority_counts.items()])
        summary_text += f" | Max Agent Load: {max(agent_counts.values()) if agent_counts else 0}"
        
        self.assignment_summary_var.set(summary_text)
    
    def update_chart(self):
        """Update visualization chart"""
        if not self.assignments:
            return
        
        # Clear existing chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        chart_type = self.chart_type_var.get()
        
        if chart_type == "priority_distribution":
            self.create_priority_chart(ax)
        elif chart_type == "agent_workload":
            self.create_workload_chart(ax)
        elif chart_type == "skill_scores":
            self.create_skill_scores_chart(ax)
        elif chart_type == "timeline":
            self.create_timeline_chart(ax)
        
        # Embed chart in tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        plt.tight_layout()
    
    def create_priority_chart(self, ax):
        """Create priority distribution pie chart"""
        priority_counts = {}
        for assignment in self.assignments:
            priority_counts[assignment.priority_level] = priority_counts.get(assignment.priority_level, 0) + 1
        
        labels = list(priority_counts.keys())
        sizes = list(priority_counts.values())
        colors = {'CRITICAL': '#ff4444', 'HIGH': '#ff8800', 'MEDIUM': '#ffcc00', 'LOW': '#88cc00'}
        chart_colors = [colors.get(label, '#cccccc') for label in labels]
        
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=chart_colors, startangle=90)
        ax.set_title('Ticket Priority Distribution', fontsize=14, fontweight='bold')
    
    def create_workload_chart(self, ax):
        """Create agent workload bar chart"""
        agent_counts = {}
        agent_names = {}
        
        # Get agent names
        if self.dataset:
            for agent in self.dataset.get('agents', []):
                agent_names[agent.get('agent_id', '')] = agent.get('name', '')
        
        for assignment in self.assignments:
            agent_id = assignment.assigned_agent_id
            agent_counts[agent_id] = agent_counts.get(agent_id, 0) + 1
        
        agents = list(agent_counts.keys())
        counts = list(agent_counts.values())
        
        # Use agent names for labels
        labels = [agent_names.get(agent_id, agent_id) for agent_id in agents]
        
        bars = ax.bar(labels, counts, color='skyblue', edgecolor='darkblue')
        ax.set_title('Agent Workload Distribution', fontsize=14, fontweight='bold')
        ax.set_xlabel('Agents')
        ax.set_ylabel('Number of Assigned Tickets')
        
        # Rotate labels if too many agents
        if len(labels) > 5:
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
    
    def create_skill_scores_chart(self, ax):
        """Create skill match scores histogram"""
        scores = [assignment.skill_match_score for assignment in self.assignments]
        
        ax.hist(scores, bins=20, color='lightgreen', edgecolor='darkgreen', alpha=0.7)
        ax.set_title('Skill Match Score Distribution', fontsize=14, fontweight='bold')
        ax.set_xlabel('Skill Match Score')
        ax.set_ylabel('Number of Assignments')
        
        # Add statistics
        mean_score = sum(scores) / len(scores) if scores else 0
        ax.axvline(mean_score, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_score:.3f}')
        ax.legend()
    
    def create_timeline_chart(self, ax):
        """Create assignment timeline based on priority scores"""
        if not self.dataset:
            return
        
        # Get ticket timestamps and priority scores
        ticket_data = []
        for assignment in self.assignments:
            for ticket in self.dataset.get('tickets', []):
                if ticket.get('ticket_id') == assignment.ticket_id:
                    timestamp = ticket.get('creation_timestamp', 0)
                    try:
                        date = datetime.fromtimestamp(timestamp)
                        ticket_data.append((date, assignment.priority_score, assignment.priority_level))
                    except:
                        continue
                    break
        
        if not ticket_data:
            ax.text(0.5, 0.5, 'No valid timestamp data', ha='center', va='center', transform=ax.transAxes)
            return
        
        # Sort by date
        ticket_data.sort()
        
        dates = [item[0] for item in ticket_data]
        scores = [item[1] for item in ticket_data]
        priorities = [item[2] for item in ticket_data]
        
        # Color code by priority
        colors = {'CRITICAL': 'red', 'HIGH': 'orange', 'MEDIUM': 'yellow', 'LOW': 'green'}
        point_colors = [colors.get(priority, 'gray') for priority in priorities]
        
        ax.scatter(dates, scores, c=point_colors, alpha=0.6, s=50)
        ax.set_title('Tickets by Creation Time and Priority Score', fontsize=14, fontweight='bold')
        ax.set_xlabel('Creation Date')
        ax.set_ylabel('Priority Score')
        
        # Format x-axis
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    
    def run_validation(self):
        """Run comprehensive data validation"""
        if not self.dataset:
            self.validation_text.delete(1.0, tk.END)
            self.validation_text.insert(tk.END, "No dataset loaded for validation.\n", 'error')
            return
        
        # Clear previous results
        self.validation_text.delete(1.0, tk.END)
        
        # Run validation
        validation_result = self.validator.validate_dataset(self.dataset)
        
        # Display results
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.validation_text.insert(tk.END, f"Validation Report - {timestamp}\n", 'info')
        self.validation_text.insert(tk.END, "=" * 60 + "\n\n", 'info')
        
        if validation_result.is_valid:
            self.validation_text.insert(tk.END, "✅ VALIDATION PASSED\n\n", 'success')
        else:
            self.validation_text.insert(tk.END, "❌ VALIDATION FAILED\n\n", 'error')
        
        # Show errors
        if validation_result.errors:
            self.validation_text.insert(tk.END, f"ERRORS ({len(validation_result.errors)}):\n", 'error')
            for i, error in enumerate(validation_result.errors, 1):
                self.validation_text.insert(tk.END, f"{i:2d}. {error}\n", 'error')
            self.validation_text.insert(tk.END, "\n")
        
        # Show warnings
        if validation_result.warnings:
            self.validation_text.insert(tk.END, f"WARNINGS ({len(validation_result.warnings)}):\n", 'warning')
            for i, warning in enumerate(validation_result.warnings, 1):
                self.validation_text.insert(tk.END, f"{i:2d}. {warning}\n", 'warning')
            self.validation_text.insert(tk.END, "\n")
        
        if not validation_result.errors and not validation_result.warnings:
            self.validation_text.insert(tk.END, "No issues found. Dataset is valid.\n", 'success')
        
        # Add summary statistics
        agents = self.dataset.get('agents', [])
        tickets = self.dataset.get('tickets', [])
        
        self.validation_text.insert(tk.END, "\nDATASET SUMMARY:\n", 'info')
        self.validation_text.insert(tk.END, f"- Total Agents: {len(agents)}\n", 'info')
        self.validation_text.insert(tk.END, f"- Total Tickets: {len(tickets)}\n", 'info')
        self.validation_text.insert(tk.END, f"- Available Agents: {sum(1 for a in agents if a.get('availability_status') == 'Available')}\n", 'info')
        
        if agents:
            avg_skills = sum(len(a.get('skills', {})) for a in agents) / len(agents)
            self.validation_text.insert(tk.END, f"- Average Skills per Agent: {avg_skills:.1f}\n", 'info')
        
        # Scroll to top
        self.validation_text.see(1.0)
    
    def export_validation_report(self):
        """Export validation report to file"""
        if not self.dataset:
            messagebox.showwarning("Warning", "No dataset to validate")
            return
        
        try:
            validation_result = self.validator.validate_dataset(self.dataset)
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'is_valid': validation_result.is_valid,
                'errors': validation_result.errors,
                'warnings': validation_result.warnings,
                'summary': {
                    'total_agents': len(self.dataset.get('agents', [])),
                    'total_tickets': len(self.dataset.get('tickets', [])),
                    'error_count': len(validation_result.errors),
                    'warning_count': len(validation_result.warnings)
                }
            }
            
            with open('validation_report.json', 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", "Validation report exported to validation_report.json")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export validation report:\n{str(e)}")


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = TicketAssignmentGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
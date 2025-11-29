import numpy as np
from datetime import datetime

def get_agent_background_color(agent_name: str) -> str:
    """Get background color for agent based on type"""
    color_map = {
        "Planner": "#E3F2FD",
        "Orchestration": "#F3E5F5",
        "RAG": "#FFF9C4",
        "Emotions": "#FFE0B2",
        "Calming": "#FFE0B2",
        "Best Practices": "#E1F5FE",
        "Reflector": "#F8BBD0",
        "Response": "#C8E6C9",
    }
    
    for key, color in color_map.items():
        if key in agent_name:
            return color
    return "#D1C4E9"


def generate_performance_indicator():
    """Generate random performance indicator for demo"""
    return np.random.choice(['🟢', '🟡', '🔴'], p=[0.7, 0.2, 0.1])


def format_timestamp():
    """Format current timestamp"""
    return datetime.now().strftime('%H:%M:%S')
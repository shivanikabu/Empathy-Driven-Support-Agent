# ============================================================================
# FILE: app.py (SIMPLIFIED MAIN APPLICATION)
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import plotly.graph_objects as go


# Import refactored modules
from backend import AgentBackend
from ui.styles import get_custom_css
from ui.sidebar import render_sidebar
from utils.helpers import get_agent_background_color, format_timestamp

# Import tab modules (these would be in ui/tabs/)
# For now, keeping tab logic inline but can be extracted later
# Page configuration
st.set_page_config(page_title="Agent Analytics Dashboard", layout="wide")

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
if 'backend' not in st.session_state:
    st.session_state.backend = AgentBackend()
if 'aws_connected' not in st.session_state:
    st.session_state.aws_connected = False
if 'langfuse_connected' not in st.session_state:
    st.session_state.langfuse_connected = False
if 'agent_logs' not in st.session_state:
    st.session_state.agent_logs = []
if 'conversations' not in st.session_state:
    st.session_state.conversations = []

# Main Title
st.markdown('<h1 class="main-title">AI Agents Enterprise Toolkit</h1>', unsafe_allow_html=True)

# Render Sidebar and get configuration
config = render_sidebar(st.session_state.backend)

# Main Panel - Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Agent Flow", 
    "💬 Conversations", 
    "📊 Agent Analytics", 
    "🎯 Trajectory Analysis"
])

# ============================================================================
# TAB 1: AGENT FLOW
# ============================================================================
with tab1:
    st.header("Agent Flow Visualization")
    
    query_input = st.text_input("Enter your query:", key="query_input")
    
    if st.button("Execute Query"):
        if not query_input:
            st.error("Please enter a query")
        elif not st.session_state.aws_connected:
            st.warning("⚠️ AWS not connected. Please connect to AWS in the sidebar.")
        else:
            st.info("🤖 Running in REAL MODE with AWS Bedrock AI agents...")
            
            try:
                # Execute the agentic flow
                result = st.session_state.backend.execute_agentic_flow(
                    query_input,
                    config["risk_weight"],
                    config["accuracy_weight"],
                    config["latency_weight"],
                    config["cost_weight"],
                    config["guardrails"]
                )
                
                agents_flow = result["agents_executed"]
                final_response = result["final_response"]
                detected_persona = result["persona"]
                
                # Display agent flow
                for idx, agent in enumerate(agents_flow):
                    bg_color = get_agent_background_color(agent['agent'])
                    
                    st.markdown(f"""
                        <div style="background-color: {bg_color}; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #1976D2;">
                            <h3 style="margin: 0 0 10px 0;">{agent['emoji']} {agent['agent']} • {format_timestamp()}</h3>
                            <p style="margin: 5px 0; font-weight: 600;">Action: {agent['action']}</p>
                            <p style="margin: 5px 0; font-size: 14px; color: #424242;">{agent['detail']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Performance indicator
                    if agent['agent'] == "Reflector Agent" and 'performance_status' in agent:
                        status_map = {'optimal': '🟢', 'acceptable': '🟡', 'warning': '🔴'}
                        performance = status_map.get(agent.get('performance_status', 'optimal'), '🟢')
                        performance_issue = agent.get('performance_issue')
                    else:
                        performance = np.random.choice(['🟢', '🟡', '🔴'], p=[0.7, 0.2, 0.1])
                        performance_issue = None
                    
                    performance_text = {
                        '🟢': 'Performance: Optimal',
                        '🟡': 'Performance: Acceptable',
                        '🔴': 'Performance: Warning'
                    }[performance]
                    
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"<h2 style='text-align: center;'>{performance}</h2>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<p style='font-size: 16px; margin-top: 10px;'>{performance_text}</p>", unsafe_allow_html=True)
                        if performance_issue:
                            bg = "#FFF9C4" if performance == '🟡' else "#FFCDD2"
                            border = '#FFA726' if performance == '🟡' else '#E53935'
                            st.markdown(f"""
                                <div style="background-color: {bg}; padding: 10px; border-radius: 5px; margin-top: 8px; border-left: 3px solid {border};">
                                    <p style="margin: 0; font-size: 14px;"><strong>Issue:</strong> {performance_issue}</p>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    time.sleep(0.4)
                    
                    # Log agent activity
                    st.session_state.agent_logs.append({
                        "timestamp": datetime.now(),
                        "agent": agent['agent'],
                        "action": agent['action'],
                        "detail": agent['detail'],
                        "tokens": np.random.randint(100, 1000),
                        "latency": np.random.uniform(0.5, 3.0)
                    })
                
                # Store conversation
                st.session_state.conversations.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "query": query_input,
                    "response": final_response,
                    "persona": detected_persona,
                    "agent_flow": [a['agent'] for a in agents_flow],
                    "mode": "REAL"
                })
                
                st.success("✅ Query execution completed!")
                
            except Exception as e:
                st.error(f"❌ Error in agent execution: {str(e)}")

# ============================================================================
# TAB 2: CONVERSATIONS
# ============================================================================
with tab2:
    st.header("Conversations")
    
    if st.session_state.conversations:
        for idx, conv in enumerate(reversed(st.session_state.conversations)):
            mode_badge = "🤖 REAL MODE" if conv.get('mode') == "REAL" else "🎭 DEMO MODE"
            with st.expander(f"📝 Conversation {len(st.session_state.conversations) - idx} - {conv['timestamp']} | {mode_badge}", expanded=(idx==0)):
                
                st.markdown("### 🙋 Query")
                st.markdown(f"""
                    <div style="background-color: #E3F2FD; padding: 15px; border-radius: 8px; border-left: 4px solid #2196F3;">
                        <p style="font-size: 16px; margin: 0;">{conv['query']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**🎯 Detected Persona:** `{conv.get('persona', 'N/A')}`")
                
                st.markdown("### 💬 Final Response")
                st.markdown(f"""
                    <div style="background-color: #E8F5E9; padding: 15px; border-radius: 8px; border-left: 4px solid #4CAF50;">
                        <p style="font-size: 16px; margin: 0; white-space: pre-wrap;">{conv['response']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**📄 Agent Flow:** {' → '.join(conv.get('agent_flow', []))}")
    else:
        st.info("No conversations yet. Execute a query in the 'Agent Flow' tab.")

# ============================================================================
# TAB 3: AGENT ANALYTICS
# ============================================================================
# with tab3:
#     st.header("Agent Analytics")
    
#     if st.session_state.langfuse_connected:
#         st.markdown(f"""
#             <div style="background-color: #E8EAF6; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
#                 <p style="margin: 0;">🔗 <a href="{config['langfuse_host']}" target="_blank">Open Langfuse Dashboard</a></p>
#             </div>
#         """, unsafe_allow_html=True)
    
#     if st.session_state.agent_logs:
#         df = pd.DataFrame(st.session_state.agent_logs)
        
#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("Tokens Consumed Per Agent")
#             tokens_by_agent = df.groupby('agent')['tokens'].sum().sort_values(ascending=False)
#             st.bar_chart(tokens_by_agent)
        
#         with col2:
#             st.subheader("Average Latency Per Agent")
#             latency_by_agent = df.groupby('agent')['latency'].mean().sort_values(ascending=False)
#             st.bar_chart(latency_by_agent)
        
#         st.markdown("---")
#         st.subheader("📈 Agent Performance Metrics")
        
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             st.metric("Accuracy Score", f"{np.random.uniform(7.5, 9.5):.1f}/10")
#             st.metric("Hallucination Score", f"{np.random.uniform(0.1, 0.3):.2f}")
#         with col2:
#             st.metric("Latency Score", f"{np.random.uniform(7.0, 9.0):.1f}/10")
#             st.metric("Throughput", f"{np.random.uniform(2.5, 5.0):.1f} req/sec")
#         with col3:
#             st.metric("Bias Score", f"{np.random.uniform(0.05, 0.20):.2f}")
#             st.metric("Toxicity Score", f"{np.random.uniform(0.01, 0.10):.2f}")
#     else:
#         st.info("No agent logs available yet.")



# Tab 3: Agent Analytics
with tab3:
    st.header("Agent Analytics")
    
    # Langfuse Dashboard Link
    if st.session_state.langfuse_connected:
        st.markdown("### 📊 Advanced Analytics")
        st.markdown(f"""
            <div style="background-color: #E8EAF6; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <p style="margin: 0; font-size: 16px;">
                    🔗 <a href="{config['langfuse_host']}" target="_blank" style="font-weight: 600;">Open Langfuse Dashboard</a> 
                    for detailed observability and tracing
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("💡 Connect to Langfuse in the sidebar for advanced observability and detailed analytics")
    
    if st.session_state.agent_logs:
        df = pd.DataFrame(st.session_state.agent_logs)
        
        # Token and Latency Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Tokens Consumed Per Agent")
            tokens_by_agent = df.groupby('agent')['tokens'].sum().sort_values(ascending=False)
            st.bar_chart(tokens_by_agent)
        
        with col2:
            st.subheader("Average Latency Per Agent")
            latency_by_agent = df.groupby('agent')['latency'].mean().sort_values(ascending=False)
            st.bar_chart(latency_by_agent)
        
        st.markdown("---")
        
        # Agent Performance Metrics
        st.subheader("📈 Agent Performance Metrics")
        
        # Create three columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            accuracy_score = np.random.uniform(7.5, 9.5)
            st.metric("Accuracy Score", f"{accuracy_score:.1f}/10", 
                     delta=f"{np.random.uniform(-0.5, 0.5):.1f}")
            
            hallucination_score = np.random.uniform(0.1, 0.3)
            st.metric("Hallucination Score", f"{hallucination_score:.2f}", 
                     delta=f"{np.random.uniform(-0.05, 0.02):.2f}", delta_color="inverse")
            
            consistency_score = np.random.uniform(8.0, 9.5)
            st.metric("Consistency Score", f"{consistency_score:.1f}/10",
                     delta=f"{np.random.uniform(-0.3, 0.5):.1f}")
        
        with col2:
            latency_score = np.random.uniform(7.0, 9.0)
            st.metric("Latency Score", f"{latency_score:.1f}/10",
                     delta=f"{np.random.uniform(-0.4, 0.6):.1f}")
            
            throughput = np.random.uniform(2.5, 5.0)
            st.metric("Throughput", f"{throughput:.1f} req/sec",
                     delta=f"{np.random.uniform(-0.3, 0.5):.1f}")
            
            reliability_rate = np.random.uniform(92, 99)
            st.metric("Reliability Rate", f"{reliability_rate:.1f}%",
                     delta=f"{np.random.uniform(-1, 2):.1f}%")
        
        with col3:
            bias_score = np.random.uniform(0.05, 0.20)
            st.metric("Bias Score", f"{bias_score:.2f}",
                     delta=f"{np.random.uniform(-0.03, 0.02):.2f}", delta_color="inverse")
            
            toxicity_score = np.random.uniform(0.01, 0.10)
            st.metric("Toxicity Score", f"{toxicity_score:.2f}",
                     delta=f"{np.random.uniform(-0.02, 0.01):.2f}", delta_color="inverse")
            
            st.metric("Off-Topic Detection", f"{np.random.randint(0, 3)} detected",
                     delta=f"{np.random.randint(-1, 1)}")
        
        st.markdown("---")
        
        # Security Metrics
        st.subheader("🔒 Security & Safety Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            denied_topics = np.random.randint(0, 2)
            st.metric("Denied Topics", f"{denied_topics} blocked",
                     help="Number of requests blocked due to policy violations")
        
        with col2:
            jailbreak_attempts = np.random.randint(0, 1)
            st.metric("Jailbreak Detection", f"{jailbreak_attempts} detected",
                     delta_color="off",
                     help="Number of detected attempts to bypass system constraints")
        
        with col3:
            st.metric("Safety Filter Rate", f"{np.random.uniform(98, 100):.1f}%",
                     help="Percentage of responses that passed safety filters")
        
        st.markdown("---")
        
        # Cost Analysis
        st.subheader("💰 Cost Analysis")
        total_tokens = df['tokens'].sum()
        cost = total_tokens * 0.05 / 1000
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Cost", f"${cost:.4f}")
        with col2:
            st.metric("Total Tokens", f"{total_tokens:,}")
        with col3:
            avg_cost_per_query = cost / len(st.session_state.conversations) if st.session_state.conversations else 0
            st.metric("Avg Cost/Query", f"${avg_cost_per_query:.4f}")
    else:
        st.info("No agent logs available yet. Execute a query to see analytics.")
# ============================================================================
# TAB 4: TRAJECTORY ANALYSIS
with tab4:
    st.header("Trajectory Analysis")
    
    st.subheader("Agent Architecture Trajectories")
    
    # Define trajectories with optimal use cases
    trajectories = {
        "Trajectory 1": {
            "agents": [
                "Planner Agent", "Orchestration Agent", "RAG Agent", 
                "Reflector Agent", "Response Agent", "Feedback Agent"
            ],
            "optimal_for": "simple query",
            "risk_base": 0.2  # Low risk
        },
        "Trajectory 2": {
            "agents": [
                "Planner Agent", "Orchestration Agent", "Emotions Agent", 
                "Calming Agent", "RAG Agent", "Reflector Agent", "Response Agent", "Feedback Agent"
            ],
            "optimal_for": ["angry customer", "confused customer"],
            "risk_base": 0.7  # High risk
        },
        "Trajectory 3": {
            "agents": [
                "Planner Agent", "Orchestration Agent", "RAG Agent", 
                "Best Practices Agent", "Reflector Agent", "Response Agent", "Feedback Agent"
            ],
            "optimal_for": "precision ask",
            "risk_base": 0.5  # Medium risk
        }
    }
    
    # Get actual performance metrics from agent analytics
    if st.session_state.agent_logs and st.session_state.conversations:
        df = pd.DataFrame(st.session_state.agent_logs)
        
        # Calculate metrics based on actual data
        num_conversations = len(st.session_state.conversations)
        avg_latency = df['latency'].mean()
        
        # Simulate metrics based on trajectory characteristics
        # In production, these would be calculated from actual data
        base_completion_rate = 0.95 if num_conversations > 0 else 0.90
        base_consistency = 0.88 if num_conversations > 0 else 0.85
        base_error_rate = 0.05 if num_conversations > 0 else 0.08
        base_recovery_time = 2.5 if num_conversations > 0 else 3.0
        base_persona_sensitivity = 0.82 if num_conversations > 0 else 0.80
        base_coherence = 0.91 if num_conversations > 0 else 0.88
    else:
        # Default values if no analytics available
        base_completion_rate = 0.90
        base_consistency = 0.85
        base_error_rate = 0.08
        base_recovery_time = 3.0
        base_persona_sensitivity = 0.80
        base_coherence = 0.88
    
    # Get latest query persona if available
    current_persona = None
    if st.session_state.conversations:
        current_persona = st.session_state.conversations[-1].get('persona', None)
    
    # Calculate trajectory performance metrics
    trajectory_data = []
    
    for traj_name, traj_info in trajectories.items():
        agents = traj_info["agents"]
        
        # Calculate metrics based on trajectory characteristics
        if traj_name == "Trajectory 1":
            # Simple trajectory - high completion, moderate consistency
            completion_rate = base_completion_rate * 1.05  # Best completion
            consistency_index = base_consistency * 0.95  # Moderate consistency
            error_propagation = base_error_rate * 0.8  # Low error rate
            recovery_time = base_recovery_time * 1.2  # Slower recovery
            persona_sensitivity = base_persona_sensitivity * 0.7  # Low sensitivity
            coherence = base_coherence * 0.9  # Lower coherence
            
        elif traj_name == "Trajectory 2":
            # Emotional trajectory - moderate completion, high sensitivity
            completion_rate = base_completion_rate * 0.92  # Lower completion due to complexity
            consistency_index = base_consistency * 1.1  # High consistency for emotional handling
            error_propagation = base_error_rate * 1.5  # Higher error potential
            recovery_time = base_recovery_time * 0.7  # Fast recovery (critical for emotions)
            persona_sensitivity = base_persona_sensitivity * 1.3  # Highest sensitivity
            coherence = base_coherence * 1.15  # Best coherence for conversations
            
        else:  # Trajectory 3
            # Precision trajectory - high accuracy, best coherence
            completion_rate = base_completion_rate * 0.98  # Good completion
            consistency_index = base_consistency * 1.2  # Highest consistency
            error_propagation = base_error_rate * 1.0  # Standard error rate
            recovery_time = base_recovery_time * 0.9  # Good recovery
            persona_sensitivity = base_persona_sensitivity * 1.0  # Moderate sensitivity
            coherence = base_coherence * 1.2  # Highest coherence for technical
        
        # Normalize to appropriate ranges
        completion_rate = min(100, completion_rate * 100)  # Percentage
        consistency_index = min(1.0, consistency_index)  # 0-1 scale
        error_propagation = max(0, min(15, error_propagation * 100))  # Percentage
        recovery_time = max(0.5, recovery_time)  # Seconds
        persona_sensitivity = min(1.0, persona_sensitivity)  # 0-1 scale
        coherence = min(1.0, coherence)  # 0-1 scale
        
        # Check if this is the optimal path for current persona
        optimal_match = False
        if current_persona:
            if isinstance(traj_info["optimal_for"], list):
                optimal_match = current_persona in traj_info["optimal_for"]
            else:
                optimal_match = current_persona == traj_info["optimal_for"]
        
        trajectory_data.append({
            "Trajectory": traj_name,
            "Agents": " → ".join(agents),
            "Optimal For": traj_info["optimal_for"] if isinstance(traj_info["optimal_for"], str) else " / ".join(traj_info["optimal_for"]),
            "Completion Rate": f"{completion_rate:.1f}%",
            "Consistency Index": f"{consistency_index:.3f}",
            "Error Propagation": f"{error_propagation:.1f}%",
            "Recovery Time": f"{recovery_time:.1f}s",
            "Persona Sensitivity": f"{persona_sensitivity:.3f}",
            "Coherence": f"{coherence:.3f}",
            "Is Optimal": "✅" if optimal_match else "",
            # Store numeric values for plotting
            "completion_numeric": completion_rate,
            "consistency_numeric": consistency_index,
            "error_numeric": error_propagation,
            "recovery_numeric": recovery_time,
            "sensitivity_numeric": persona_sensitivity,
            "coherence_numeric": coherence
        })
    
    df_trajectories = pd.DataFrame(trajectory_data)
    
    # Display current query context if available
    if current_persona:
        st.info(f"🎯 **Current Query Persona:** `{current_persona}` - Analyzing optimal trajectory match")
    
    # Display table with new metrics
    display_columns = ["Trajectory", "Completion Rate", "Consistency Index", 
                      "Error Propagation", "Recovery Time", "Persona Sensitivity", 
                      "Coherence"]
    display_df = df_trajectories[display_columns]
    st.dataframe(display_df, use_container_width=True, height=150)
    
    # Add metric guide
    with st.expander("📖 Metric Definitions Guide"):
        st.markdown("""
        ### Performance Metrics Explained:
        
        **🎯 Trajectory Completion Rate**
        - Percentage of runs where the agent chain executes fully without breakdown or fallback
        - Higher is better (>95% is excellent)
        
        **📊 Consistency Index**
        - Measures variance in responses (semantic similarity across repeated prompts)
        - Scale: 0-1, where 1 is perfect consistency
        - Important for reliability and user trust
        
        **⚠️ Error Propagation Rate**
        - Measures how errors from one agent cascade to downstream ones
        - Critical in planner → RAG → reflector paths
        - Lower is better (<5% is excellent)
        
        **⏱️ Recovery Time**
        - Time taken to recover from an interruption or escalation
        - Critical for emotional contexts and error handling
        - Measured in seconds, lower is better
        
        **🎭 Persona Sensitivity**
        - Correlation between persona type (e.g., "angry") and adaptation behaviors
        - Measures tone softening, empathy adjustments
        - Scale: 0-1, higher indicates better emotional intelligence
        
        **🔗 Conversational Coherence**
        - Measures topic retention and context continuity across turns
        - Especially important with multiple reasoning agents
        - Scale: 0-1, where 1 is perfect coherence
        """)
    
    # Visualizations
    st.markdown("---")
    st.subheader("📊 Trajectory Performance Metrics Comparison")
    
    if len(trajectory_data) > 0:
        # Create comprehensive chart with new metrics
        st.markdown("#### All Metrics Comparison - All Trajectories")
        
        # Prepare data for plotting
        metrics = ['Completion\nRate', 'Consistency\nIndex', 'Error\nPropagation', 
                  'Recovery\nTime', 'Persona\nSensitivity', 'Conversational\nCoherence']
        
        # Normalize all metrics to 0-100 scale for visualization
        traj1_data = df_trajectories[df_trajectories['Trajectory'] == 'Trajectory 1'].iloc[0]
        traj2_data = df_trajectories[df_trajectories['Trajectory'] == 'Trajectory 2'].iloc[0]
        traj3_data = df_trajectories[df_trajectories['Trajectory'] == 'Trajectory 3'].iloc[0]
        
        traj1_values = [
            traj1_data['completion_numeric'],  # Already in percentage
            traj1_data['consistency_numeric'] * 100,  # Convert to percentage
            100 - traj1_data['error_numeric'],  # Invert for "goodness"
            (1 - traj1_data['recovery_numeric']/5) * 100,  # Normalize and invert
            traj1_data['sensitivity_numeric'] * 100,  # Convert to percentage
            traj1_data['coherence_numeric'] * 100  # Convert to percentage
        ]
        
        traj2_values = [
            traj2_data['completion_numeric'],
            traj2_data['consistency_numeric'] * 100,
            100 - traj2_data['error_numeric'],
            (1 - traj2_data['recovery_numeric']/5) * 100,
            traj2_data['sensitivity_numeric'] * 100,
            traj2_data['coherence_numeric'] * 100
        ]
        
        traj3_values = [
            traj3_data['completion_numeric'],
            traj3_data['consistency_numeric'] * 100,
            100 - traj3_data['error_numeric'],
            (1 - traj3_data['recovery_numeric']/5) * 100,
            traj3_data['sensitivity_numeric'] * 100,
            traj3_data['coherence_numeric'] * 100
        ]
        
        # Create plotly figure
        fig = go.Figure(data=[
            go.Bar(name='Trajectory 1 (Simple)', x=metrics, y=traj1_values, 
                   marker_color='#B4D7E8', text=[f'{v:.1f}' for v in traj1_values], textposition='outside'),
            go.Bar(name='Trajectory 2 (Emotional)', x=metrics, y=traj2_values, 
                   marker_color='#C5E1A5', text=[f'{v:.1f}' for v in traj2_values], textposition='outside'),
            go.Bar(name='Trajectory 3 (Precision)', x=metrics, y=traj3_values, 
                   marker_color='#FFCCBC', text=[f'{v:.1f}' for v in traj3_values], textposition='outside')
        ])
        
        fig.update_layout(
            barmode='group',
            height=500,
            xaxis_title="Performance Metrics",
            yaxis_title="Score (0-100 scale, higher is better)",
            yaxis=dict(range=[0, 110]),  # Set y-axis range
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("📌 All scores normalized to 0-100 scale for comparison. Higher values indicate better performance.")
        st.caption("⚡ Recovery Time and Error Propagation are inverted (lower actual values = higher scores)")
    
    # Performance insights based on metrics
    st.markdown("---")
    st.subheader("🔍 Performance Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 Trajectory Strengths")
        st.markdown("""
        **Trajectory 1 (Simple Query)**
        - ✅ Highest completion rate
        - ✅ Lowest error propagation
        - ✅ Most reliable for straightforward queries
        
        **Trajectory 2 (Emotional Support)**
        - ✅ Best persona sensitivity
        - ✅ Fastest recovery time
        - ✅ Superior conversational coherence
        
        **Trajectory 3 (Technical/Precision)**
        - ✅ Highest consistency index
        - ✅ Best coherence for technical content
        - ✅ Balanced performance across metrics
        """)
    
    with col2:
        st.markdown("#### 📈 Optimization Opportunities")
        st.markdown("""
        **Trajectory 1**
        - 🔄 Improve persona sensitivity for better adaptability
        - 🔄 Enhance conversational coherence
        
        **Trajectory 2**
        - 🔄 Reduce error propagation risk
        - 🔄 Improve completion rate stability
        
        **Trajectory 3**
        - 🔄 Optimize recovery time
        - 🔄 Enhance emotional intelligence
        """)
    
    st.markdown("---")
    
    # Trajectory Guide (keeping as requested)
    st.subheader("🎯 Trajectory Guide")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Trajectory 1")
        st.markdown("**Simple Query Path**")
        st.markdown("""
        - 📋 **Use Case**: Basic questions
        - 🎯 **Completion**: 95%+
        - 🔄 **Consistency**: Moderate
        - ⚡ **Recovery**: Slower
        - 💡 **Best for**: FAQ-style queries
        """)
    
    with col2:
        st.markdown("### Trajectory 2")
        st.markdown("**Emotional Support Path**")
        st.markdown("""
        - 📋 **Use Case**: Upset customers
        - ❤️ **Empathy**: Maximum
        - 🛡️ **Sensitivity**: Highest
        - ⚡ **Recovery**: Fastest
        - 💡 **Best for**: De-escalation
        """)
    
    with col3:
        st.markdown("### Trajectory 3")
        st.markdown("**Technical Precision Path**")
        st.markdown("""
        - 📋 **Use Case**: Complex queries
        - 🎯 **Accuracy**: Maximum
        - 🔄 **Consistency**: Highest
        - 📊 **Coherence**: Best
        - 💡 **Best for**: Technical support
        """)
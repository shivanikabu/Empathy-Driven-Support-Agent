import streamlit as st

def render_sidebar(backend):
    """Render the sidebar configuration panel"""
    
    st.sidebar.title("🔧 Configuration")
    
    # AWS Connectivity
    st.sidebar.subheader("AWS API Connectivity")
    aws_access_key = st.sidebar.text_input("AWS Access Key", type="password")
    aws_secret_key = st.sidebar.text_input("AWS Secret Key", type="password")
    aws_region = st.sidebar.text_input("AWS Region", value="us-east-1")
    
    if st.sidebar.button("Connect to AWS"):
        success, message = backend.connect_aws(aws_access_key, aws_secret_key, aws_region)
        if success:
            st.session_state.aws_connected = True
            st.sidebar.success(f"✅ {message}")
        else:
            st.sidebar.error(f"❌ {message}")
    
    # Langfuse Connectivity
    st.sidebar.subheader("Langfuse Connectivity")
    langfuse_public_key = st.sidebar.text_input("Langfuse Public Key", type="password")
    langfuse_secret_key = st.sidebar.text_input("Langfuse Secret Key", type="password")
    langfuse_host = st.sidebar.text_input("Langfuse Host", value="https://cloud.langfuse.com")
    
    if st.sidebar.button("Connect to Langfuse"):
        success, message = backend.connect_langfuse(langfuse_public_key, langfuse_secret_key, langfuse_host)
        if success:
            st.session_state.langfuse_connected = True
            st.sidebar.success(f"✅ {message}")
        else:
            st.sidebar.error(f"❌ {message}")
    
    # Agent Goal Assessment
    st.sidebar.subheader("Agent Goal Assessment")
    st.sidebar.markdown("**Adjust Weights:**")
    risk_weight = st.sidebar.slider("Risk Tolerance", 0.0, 1.0, 0.5, 0.1)
    accuracy_weight = st.sidebar.slider("Accuracy", 0.0, 1.0, 0.8, 0.1)
    latency_weight = st.sidebar.slider("Latency", 0.0, 1.0, 0.6, 0.1)
    cost_weight = st.sidebar.slider("Cost", 0.0, 1.0, 0.4, 0.1)
    
    # Document Upload
    st.sidebar.subheader("Document Upload")
    
    # Database status
    if backend.vector_db is not None:
        try:
            num_docs = backend.vector_db_service.get_document_count()
            if num_docs > 0:
                st.sidebar.info(f"📚 Database: {num_docs} chunks stored")
            else:
                st.sidebar.warning("📚 Database: Empty - upload documents below")
        except:
            st.sidebar.warning("📚 Database: Status unknown")
    else:
        st.sidebar.warning("📚 Database: Not initialized")
    
    uploaded_files = st.sidebar.file_uploader(
        "Upload PDF Documents", 
        accept_multiple_files=True,
        type=['pdf']
    )
    
    # Guardrails
    st.sidebar.subheader("Guardrails")
    guardrails = st.sidebar.text_area(
        "Enter Guardrails (one per line)",
        placeholder="No profanity\nNo PII disclosure\nFactual responses only"
    )
    
    # Process Documents
    if uploaded_files and st.sidebar.button("Process Documents"):
        if not st.session_state.aws_connected:
            st.sidebar.error("❌ Please connect to AWS first")
        else:
            with st.spinner("Processing documents..."):
                success, message = backend.process_documents(uploaded_files)
                if success:
                    st.sidebar.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.sidebar.error(f"❌ {message}")
    
    # Clear database
    if st.sidebar.button("🗑️ Clear Vector Database"):
        if backend.vector_db is not None:
            success, message = backend.clear_vector_db()
            if success:
                st.sidebar.success(f"✅ {message}")
                st.rerun()
            else:
                st.sidebar.error(f"❌ {message}")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Agent Analytics Dashboard v1.0")
    
    return {
        "risk_weight": risk_weight,
        "accuracy_weight": accuracy_weight,
        "latency_weight": latency_weight,
        "cost_weight": cost_weight,
        "guardrails": guardrails,
        "langfuse_host": langfuse_host
    }

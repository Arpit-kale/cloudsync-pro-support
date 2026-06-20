import json
import numpy as np
from src import config
from src.database import embeddings, retrieve_context

# Target personas and their definitions for zero-shot embedding similarity
PERSONAS = {
    "Technical Expert": (
        "A user asking a highly technical question, referencing logs, API schemas, "
        "Bearer headers, OAuth2, 401 Unauthorized codes, 429 rate limits, replication lag metrics, "
        "conflict resolution, regional failovers, database scaling, or technical root-cause procedures."
    ),
    "Frustrated User": (
        "An angry, stressed, or complaining user typing with exclamation marks or ALL CAPS, "
        "expressing extreme frustration about a broken system, unacceptable downtime, "
        "or demanding urgent support and immediate resolution."
    ),
    "Business Executive": (
        "A business executive, manager, or owner asking about billing plans, subscription upgrades, "
        "cancellation policy, payment methods, revenue impact, recovery timeline, operational bottlenecks, "
        "project deadlines, or SLA terms."
    )
}

# Pre-embed persona descriptions for faster classification
print("Pre-embedding persona categories...")
_persona_embeddings = {
    persona: embeddings.embed_query(desc)
    for persona, desc in PERSONAS.items()
}

def detect_persona(user_message: str) -> str:
    """
    Classifies the user message into one of three personas:
    'Technical Expert', 'Frustrated User', or 'Business Executive'.
    Uses zero-shot embedding similarity and keyword rule boosting.
    """
    msg_emb = embeddings.embed_query(user_message)
    best_persona = None
    best_score = -1.0
    
    for persona, emb in _persona_embeddings.items():
        # Cosine similarity
        dot_product = np.dot(msg_emb, emb)
        norm_msg = np.linalg.norm(msg_emb)
        norm_persona = np.linalg.norm(emb)
        similarity = dot_product / (norm_msg * norm_persona) if norm_msg > 0 and norm_persona > 0 else 0.0
        
        # Rule-based boosting for high precision
        boost = 0.0
        msg_lower = user_message.lower()
        
        if persona == "Frustrated User":
            # Boost on uppercase word ratio
            words = [w for w in user_message.split() if w.isalpha()]
            upper_words = [w for w in words if w.isupper()]
            if len(upper_words) >= len(words) * 0.4 and len(words) > 1:
                boost += 0.3
            if "!" in user_message:
                boost += 0.2
            frustrated_words = ["broken", "unacceptable", "terrible", "worst", "fail", "angry", "useless", "disaster", "horrible", "crap", "garbage", "waste"]
            if any(fw in msg_lower for fw in frustrated_words):
                boost += 0.25
                
        elif persona == "Technical Expert":
            tech_words = ["api", "log", "401", "429", "unauthorized", "oauth", "bearer", "header", "latency", "replica", "sync", "database", "timeout", "restoration", "endpoint", "curl", "json", "token", "lag", "port", "ipconfig"]
            if any(tw in msg_lower for tw in tech_words):
                boost += 0.2
                
        elif persona == "Business Executive":
            biz_words = ["revenue", "timeline", "impact", "executive", "business", "contract", "money", "operations", "duration", "eta", "operational", "plan", "cost", "cancel", "refund", "card", "billing", "subscription"]
            if any(bw in msg_lower for bw in biz_words):
                boost += 0.2
                
        score = similarity + boost
        if score > best_score:
            best_score = score
            best_persona = persona
            
    return best_persona

def generate_adaptive_response(query: str, persona: str, chunks: list, avg_score: float) -> str:
    """
    Generates a response tailored to the detected persona using the retrieved support chunks.
    """
    if not chunks:
        if persona == "Technical Expert":
            return "SYSTEM LOGS:\n[ERROR] [RAG_DATABASE] Context retrieval empty.\n[INFO] Resolution directive: Escalate to tier-3 infrastructure engineer."
        elif persona == "Frustrated User":
            return "I am so sorry, but I am having trouble finding the exact steps to solve your issue right now. I know how important this is to your work, and I am transferring you directly to a senior support manager who can help you immediately."
        else: # Business Executive
            return "* **Operational Status**: Unavailable\n* **Business Impact**: High\n* **Action Plan**: System is transferring this thread to an account manager for high-priority support."

    if persona == "Technical Expert":
        response = "### SYSTEM DIAGNOSTIC REPORT\n"
        response += f"**TIMESTAMP**: 2026-06-20T11:41:00Z\n"
        response += f"**RETRIEVAL_SIMILARITY**: {avg_score:.4f}\n\n"
        response += "#### DIAGNOSED ROOT CAUSE & DOCUMENTATION EXTRACTS:\n"
        for chunk in chunks:
            response += f"- {chunk.strip()}\n"
        response += "\n#### RECOMMENDED ACTION SEQUENCE:\n"
        response += "```bash\n"
        if "auth" in query.lower() or "token" in query.lower() or "401" in query:
            response += "# Verify Authorization Header Bearer prefix:\n"
            response += "curl -H \"Authorization: Bearer <TOKEN>\" https://api.cloudsyncpro.com/v1/sync/status\n"
            response += "# Request new access token using refresh token:\n"
            response += "POST /oauth/token?grant_type=refresh_token&refresh_token=<REFRESH_TOKEN>\n"
        elif "rate" in query.lower() or "429" in query:
            response += "# Verify current request limits and Retry-After interval:\n"
            response += "curl -I https://api.cloudsyncpro.com/v1/sync\n"
            response += "# Read response headers: X-RateLimit-Limit, X-RateLimit-Remaining, Retry-After\n"
        elif "storage" in query.lower() or "quota" in query.lower():
            response += "# Run dynamic storage volume extension (zero downtime):\n"
            response += "cloudsync-cli cluster resize --storage +100G --cluster-id db-primary\n"
            response += "# Inspect current table usage:\n"
            response += "SELECT relname, pg_size_pretty(pg_total_relation_size(oid)) FROM pg_class;\n"
        else:
            response += "# Analyze replication lag and network latency:\n"
            response += "cloudsync-cli metrics get replica-lag\n"
            response += "ping replica.cloudsyncpro.internal -c 10\n"
        response += "```\n"
        return response
        
    elif persona == "Frustrated User":
        response = "### We Are On It! Your System Recovery Plan\n\n"
        response += "First and foremost, I am sincerely sorry for the stress and frustration this issue is causing you. I completely understand that having your synchronization system disrupted is unacceptable, and we are going to fix this for you as quickly as possible.\n\n"
        response += "Based on our support guides, we have found the solution. Please follow these simple steps:\n\n"
        
        steps = []
        if "auth" in query.lower() or "token" in query.lower() or "401" in query:
            steps = [
                "Log out of your CloudSync Pro dashboard completely.",
                "Clear your browser's history, cookies, and cache to remove any old token data.",
                "Log back in. A new login token will be generated, which will instantly fix the 401 connection error!"
            ]
        elif "billing" in query.lower() or "card" in query.lower():
            steps = [
                "Open your CloudSync Pro Admin Dashboard.",
                "Go to Settings > Billing and click on Plan details.",
                "Update your credit card details or billing information. The payment system will automatically retry and restore full access!"
            ]
        elif "storage" in query.lower() or "quota" in query.lower():
            steps = [
                "Go to the Admin Console and check your database cluster settings.",
                "Select 'Storage' and drag the slider to increase your capacity by 10% or more.",
                "This will take less than 5 minutes, and your database will immediately resume saving and syncing data!"
            ]
        else:
            steps = [
                "Wait 2 to 3 minutes for our background network failover system to complete.",
                "If you are on Windows, type 'ipconfig /flushdns' in your command prompt to refresh the database route.",
                "The system should automatically resume normal operations. We are keeping a close eye on this!"
            ]
            
        for i, step in enumerate(steps, 1):
            response += f"**Step {i}**: {step}\n"
            
        response += "\nRest assured, if these steps do not resolve the issue, a senior technician is ready to take over. We are here to support you until this is completely resolved."
        return response
        
    else: # Business Executive
        response = "### Executive Operations Summary\n\n"
        response += "Here is the critical performance data and resolution plan regarding your query:\n\n"
        
        status = "Active recovery in progress"
        metric = "99.9% replication availability"
        eta = "2-3 Minutes"
        resolution = "Replication cluster DNS routing is refreshing automatically."
        
        if "auth" in query.lower() or "token" in query.lower() or "401" in query:
            status = "Client credential renewal required"
            metric = "Authentication API SLA at 99.99%"
            eta = "Immediate (following credentials refresh)"
            resolution = "Client session token renewal via OAuth2 endpoint."
        elif "billing" in query.lower() or "card" in query.lower() or "cancel" in query.lower():
            status = "Billing tier update pending"
            metric = "Billing system gateway is fully online"
            eta = "Immediate upon invoice resolution"
            resolution = "Update card details via Admin Console > Billing."
        elif "quota" in query.lower() or "storage" in query.lower():
            status = "Disk limit threshold exceeded"
            metric = "Write-lock active to prevent database corruption"
            eta = "5 Minutes (dynamic volume resize)"
            resolution = "Increase storage tier dynamically in Admin Console > Clusters."
            
        response += f"* **Operational Status**: {status}\n"
        response += f"* **Uptime / SLA Impact**: {metric}\n"
        response += f"* **Estimated Recovery Window (ETA)**: {eta}\n"
        response += f"* **Resolution Action**: {resolution}\n"
        response += "* **Business Impact**: Minimum disruption; backend replica promote algorithms are fully automated and prevent data loss."
        return response

def generate_handoff_summary(persona: str, query: str, metadata_list: list, attempted_steps: list) -> str:
    """
    Generates a structured human handoff JSON string containing diagnostic metrics.
    """
    docs_used = list(set([m.get("source", "unknown") for m in metadata_list]))
    
    # Analyze query to extract a brief bottleneck statement
    issue = "General support inquiry requiring manual review"
    query_lower = query.lower()
    if "auth" in query_lower or "token" in query_lower or "401" in query_lower:
        issue = "OAuth2 token expiration or invalid Bearer authentication header mismatch (401)"
    elif "billing" in query_lower or "card" in query_lower or "cancel" in query_lower:
        issue = "Subscription tier modification, corporate card payment failure, or cancellation request"
    elif "sync" in query_lower or "lag" in query_lower or "latency" in query_lower:
        issue = "Critical replication lag exceeding 10s or network cluster sync timeouts"
    elif "rate" in query_lower or "429" in query_lower:
        issue = "Client exceeding API rate limits resulting in 429 Too Many Requests errors"
    elif "storage" in query_lower or "quota" in query_lower:
        issue = "Cluster storage limit exceeded (write-lock enabled)"
    elif "failover" in query_lower or "dns" in query_lower:
        issue = "Regional failover active, waiting for replica promotion and local DNS cache updates"
        
    recommendation = "Contact customer via primary communication channel. Review database logs for matching error codes."
    if "billing" in query_lower or "cancel" in query_lower or "refund" in query_lower:
        recommendation = "Contact billing operations department immediately. Check payment gateway attempts and billing records."
    elif "sync" in query_lower or "lag" in query_lower:
        recommendation = "Verify destination IOPS limit. Scale cluster performance if write queue bottleneck is detected."
    elif "auth" in query_lower:
        recommendation = "Verify client client_id and API key active state. Help customer refresh Bearer tokens."

    handoff_dict = {
        "persona": persona,
        "issue": issue,
        "documents_used": docs_used,
        "attempted_steps": attempted_steps,
        "recommendation": recommendation
    }
    
    return json.dumps(handoff_dict, indent=2)

def process_chat_message(user_message: str, chat_history: list) -> dict:
    """
    Processes an incoming message through the entire customer support pipeline.
    
    Arguments:
        user_message (str): The current user message.
        chat_history (list): List of dictionaries containing previous turns e.g. [{"role": "user", "content": "..."}]
        
    Returns:
        dict: {
            "persona": str,
            "response": str,
            "escalated": bool,
            "handoff_summary": str or None,
            "retrieved_docs": list_of_metadata_dicts,
            "similarity_score": float
        }
    """
    # 1. Detect user persona
    persona = detect_persona(user_message)
    
    # 2. Retrieve document context
    chunks, metadatas, similarity_score = retrieve_context(user_message, k=3)
    
    # 3. Generate adaptive response
    response_text = generate_adaptive_response(user_message, persona, chunks, similarity_score)
    
    # 4. Check escalation conditions
    escalated = False
    
    # Condition A: Banned keywords
    banned_triggered = [kw for kw in config.BANNED_KEYWORDS if kw in user_message.lower()]
    if banned_triggered:
        escalated = True
        
    # Condition B: Low confidence/similarity score
    if similarity_score < config.CONFIDENCE_THRESHOLD:
        escalated = True
        
    # Condition C: Turn limit exceeded
    # Calculate user turns in history
    user_turns = sum(1 for turn in chat_history if turn.get("role") == "user")
    # Current message is the N-th user turn (user_turns + 1)
    if (user_turns + 1) > config.MAX_TURN_LIMIT:
        escalated = True
        
    # 5. Generate Handoff Summary if escalated
    handoff_summary_json = None
    if escalated:
        # Build attempted steps or references list
        attempted_steps = []
        if len(chunks) > 0:
            attempted_steps.append(f"Retrieved {len(chunks)} support guides containing diagnostic steps.")
        if banned_triggered:
            attempted_steps.append(f"Triggered escalation policy on sensitive keywords: {banned_triggered}.")
        if similarity_score < config.CONFIDENCE_THRESHOLD:
            attempted_steps.append(f"Low confidence search score ({similarity_score:.4f} < {config.CONFIDENCE_THRESHOLD}).")
        if (user_turns + 1) > config.MAX_TURN_LIMIT:
            attempted_steps.append(f"Turn count limit exceeded ({user_turns + 1} > {config.MAX_TURN_LIMIT}).")
            
        handoff_summary_json = generate_handoff_summary(persona, user_message, metadatas, attempted_steps)
        
    return {
        "persona": persona,
        "response": response_text,
        "escalated": escalated,
        "handoff_summary": handoff_summary_json,
        "retrieved_docs": metadatas,
        "retrieved_chunks": chunks,
        "similarity_score": similarity_score
    }

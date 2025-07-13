import os
import logging
from flask import Flask, request, jsonify
from pydantic import PrivateAttr
from crewai import Agent, Task, Crew
from litellm import completion

# ---------- Logging ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- Initialize LLM ----------
try:
    llm_model = os.getenv("LLAMA_MODEL_PATH", "llama2")
    def run_llm(query: str) -> str:
        try:
            response = completion(
                model="ollama/llama2",
                temperature=0.7,
                max_tokens=512,
                top_p=0.95,
                messages=[{"role": "user", "content": query}]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return "Sorry, the AI service is currently unavailable."

except Exception as e:
    logger.exception("=== ERROR DURING LLM INITIALIZATION ===")
    def run_llm(prompt: str) -> str:
        return "Sorry, the AI model failed to load."

# ---------- Define Agents ----------
project_agent = Agent(
    role="Project Manager",
    goal="Provide project updates and timelines.",
    backstory="Handles all project-related inquiries.",
    allow_delegation=False
)

booking_agent = Agent(
    role="Consultant",
    goal="Respond to booking or consultation requests.",
    backstory="Handles bookings and consultation appointments.",
    allow_delegation=False
)

support_agent = Agent(
    role="Support Engineer",
    goal="Resolve technical issues and guide users.",
    backstory="Handles all customer support issues.",
    allow_delegation=False
)

info_agent = Agent(
    role="Information Specialist",
    goal="Explain services offered by the company.",
    backstory="Answers general questions about services.",
    allow_delegation=False
)

billing_agent = Agent(
    role="Billing Department",
    goal="Assist with billing and payment inquiries.",
    backstory="Handles customer billing and payment issues.",
    allow_delegation=False
)

# ---------- Smart Crew ----------
class SmartIVRCrew(Crew):
    _agent_map: dict = PrivateAttr()

    def __init__(self, agents: list):
        super().__init__(agents=agents)
        self._agent_map = {a.role.lower(): a for a in agents}

    def run(self, query: str):
        tasks = []
        try:
            query_lower = query.lower()
            keyword_map = {
                "project": "project manager",
                "status": "project manager",
                "book": "consultant",
                "appointment": "consultant",
                "support": "support engineer",
                "issue": "support engineer",
                "services": "information specialist",
                "offer": "information specialist",
                "billing": "billing department",
                "invoice": "billing department",
                "payment": "billing department",
            }

            matched_roles = {keyword_map[k] for k in keyword_map if k in query_lower}

            if matched_roles:
                for role in matched_roles:
                    agent = self._agent_map.get(role)
                    if agent:
                        tasks.append(Task(
                            agent=agent,
                            input=query,
                            description=f"Handle query related to {role}",
                            expected_output="Helpful and accurate response"
                        ))
            else:
                for agent in self.agents:
                    tasks.append(Task(
                        agent=agent,
                        input=query,
                        description="Handle fallback query",
                        expected_output="Fallback response"
                    ))

            for task in tasks:
                try:
                    return run_llm(query)
                except Exception as e:
                    logger.error(f"Task run failed for {task.agent.role}: {e}")
        except Exception as e:
            logger.exception("Error in SmartIVRCrew run")

        return "Sorry, the AI service is currently unavailable."

# ---------- Instantiate Crew ----------
ivr_crew = SmartIVRCrew(agents=[
    project_agent,
    booking_agent,
    support_agent,
    info_agent,
    billing_agent
])

# ---------- Flask API ----------
app = Flask(__name__)

@app.route('/ivr', methods=['POST'])
def ivr_endpoint():
    try:
        data = request.json
        user_input = data.get('user_input', '').lower()
        response = ivr_crew.run(user_input)
        return jsonify({"response": response})
    except Exception as e:
        logger.exception("IVR endpoint error")
        return jsonify({"error": "Internal server error"}), 500

# ---------- Run ----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)

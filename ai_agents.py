"""
AI Agents for CarbonFootprint application.
------------------------------------------------
This module defines multiple specialized AI agents using CrewAI,
each focusing on specific sustainability-related functions such as
data entry validation, emission reporting, offset suggestions, 
regulation tracking, and emission optimization.

Each agent leverages a large language model (LLM) from Groq,
providing domain-specific intelligence in carbon accounting and ESG.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# -------------------------------------------------------------------
# ✅ Load environment variables securely from the .env file
# -------------------------------------------------------------------
load_dotenv()

# -------------------------------------------------------------------
# ⚠️ RECOMMENDATION: Use env variable names, not hardcoded tokens
# Instead of putting the actual key, load via:
# os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
# -------------------------------------------------------------------
os.environ["GROQ_API_KEY"] = os.getenv("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", "")

# -------------------------------------------------------------------
# ✅ LLM Initialization
# -------------------------------------------------------------------
def get_llm():
    """
    Initialize and return the Groq LLM for all agents.
    
    - Uses the Groq LLaMA 3.3 70B versatile model.
    - Temperature controls creativity vs factuality.
    - Temperature ~0.7 balances reasoning + creativity.

    Returns:
        LLM: Configured Groq language model instance.
    """
    return LLM(
        model="groq/llama-3.3-70b-versatile",
        temperature=0.7
    )


# -------------------------------------------------------------------
# 🌍 CarbonFootprintAgents: Central class that manages all AI agents
# -------------------------------------------------------------------
class CarbonFootprintAgents:
    """
    The CarbonFootprintAgents class defines and manages CrewAI agents
    that perform various sustainability-related intelligence tasks.
    
    Agents include:
        - Data Entry Assistant
        - Report Summary Generator
        - Carbon Offset Advisor
        - Regulation Radar
        - Emission Optimizer
    """
    def __init__(self):
        """Initialize all agents using a shared LLM instance."""
        self.llm = get_llm()
        self._create_agents()  # Setup all agents

    # -------------------------------------------------------------------
    # 🧠 Define all agent personas and goals
    # -------------------------------------------------------------------
    def _create_agents(self):
        """Create and configure all agents with roles, goals, and backstories."""

        # 1️⃣ Data Entry Assistant
        self.data_entry_assistant = Agent(
            llm=self.llm,
            role="Data Entry Assistant",
            goal="Help users classify emissions, map to scopes, and validate data entries",
            backstory=(
                "You are a carbon accounting expert who ensures that user-entered data "
                "is properly categorized under Scope 1, 2, or 3 emissions. You validate "
                "entries and help maintain accuracy across all emission types."
            ),
            allow_delegation=False,
            verbose=False
        )

        # 2️⃣ Report Summary Generator
        self.report_generator = Agent(
            llm=self.llm,
            role="Report Summary Generator",
            goal="Transform emission data into clear, human-readable summaries",
            backstory=(
                "You are a sustainability analyst skilled in transforming raw emissions "
                "data into executive summaries, highlighting key emission sources, "
                "trends, and actionable insights for reporting."
            ),
            allow_delegation=False,
            verbose=False
        )

        # 3️⃣ Carbon Offset Advisor
        self.offset_advisor = Agent(
            llm=self.llm,
            role="Carbon Offset Advisor",
            goal="Recommend verified and region-appropriate carbon offset options",
            backstory=(
                "You are an expert in global carbon offset programs who advises "
                "organizations on verified offset projects that match their industry, "
                "values, and geography. You guide them toward credible and effective offsets."
            ),
            allow_delegation=False,
            verbose=False
        )

        # 4️⃣ Regulation Radar
        self.regulation_radar = Agent(
            llm=self.llm,
            role="Regulation Radar",
            goal="Track and interpret regional compliance and carbon regulations",
            backstory=(
                "You are a regulatory specialist tracking frameworks like the EU CBAM, "
                "Japan GX League, and Indonesia ETS/ETP. You help companies understand "
                "carbon compliance and prepare for upcoming policy shifts."
            ),
            allow_delegation=False,
            verbose=False
        )

        # 5️⃣ Emission Optimizer
        self.emission_optimizer = Agent(
            llm=self.llm,
            role="Emission Optimizer",
            goal="Analyze data and propose actionable emission reduction strategies",
            backstory=(
                "You are a carbon reduction strategist who reviews historical emissions "
                "to find cost-effective, practical reduction opportunities for organizations."
            ),
            allow_delegation=False,
            verbose=False
        )

    # -------------------------------------------------------------------
    # ⚙️ TASK CREATION FUNCTIONS
    # Each method creates a CrewAI Task tailored to an agent’s expertise.
    # -------------------------------------------------------------------
    def create_data_entry_task(self, data_description):
        """Create a data classification and validation task."""
        return Task(
            description=(
                f"Analyze and classify the following emission data: {data_description}\n"
                f"- Determine if it falls under Scope 1, 2, or 3.\n"
                f"- Suggest the most appropriate category.\n"
                f"- Recommend an emission factor if available.\n"
                f"- Validate the data completeness and consistency."
            ),
            expected_output="Detailed emission classification with scope, category, and factor.",
            agent=self.data_entry_assistant
        )

    def create_report_summary_task(self, emissions_data):
        """Create a reporting summary generation task."""
        return Task(
            description=(
                f"Generate an analytical summary of emissions data: {emissions_data}\n"
                f"- Highlight emission trends and key contributors.\n"
                f"- Compare across time periods if applicable.\n"
                f"- Suggest improvement areas."
            ),
            expected_output="Concise summary report with data-driven insights.",
            agent=self.report_generator
        )

    def create_offset_advice_task(self, emissions_total, location, industry):
        """Create a task for recommending carbon offset projects."""
        return Task(
            description=(
                f"Recommend suitable carbon offset options for:\n"
                f"- Emissions: {emissions_total} kgCO2e\n"
                f"- Location: {location}\n"
                f"- Industry: {industry}\n"
                f"Provide verified options with cost, benefits, and project type."
            ),
            expected_output="List of 3–5 verified offset options with cost-benefit analysis.",
            agent=self.offset_advisor
        )

    def create_regulation_check_task(self, location, industry, export_markets):
        """Create a regulation compliance analysis task."""
        return Task(
            description=(
                f"Assess regulatory compliance for:\n"
                f"- Location: {location}\n"
                f"- Industry: {industry}\n"
                f"- Export markets: {export_markets}\n"
                f"Identify active and upcoming carbon regulations, and suggest preparation steps."
            ),
            expected_output="Comprehensive overview of applicable regulations and compliance guidance.",
            agent=self.regulation_radar
        )

    def create_optimization_task(self, emissions_data):
        """Create a task for finding emission reduction opportunities."""
        return Task(
            description=(
                f"Analyze emissions data: {emissions_data}\n"
                f"- Identify top 3–5 emission sources for potential reduction.\n"
                f"- Suggest practical reduction strategies and estimated savings."
            ),
            expected_output="Prioritized emission reduction plan with estimated impact.",
            agent=self.emission_optimizer
        )

    # -------------------------------------------------------------------
    # 🚀 CREW RUNNERS — Executes each agent’s workflow end-to-end
    # -------------------------------------------------------------------
    def run_data_entry_crew(self, data_description):
        """Run the Data Entry Assistant."""
        task = self.create_data_entry_task(data_description)
        crew = Crew(agents=[self.data_entry_assistant], tasks=[task], verbose=False)
        return crew.kickoff()

    def run_report_summary_crew(self, emissions_data):
        """Run the Report Summary Generator."""
        task = self.create_report_summary_task(emissions_data)
        crew = Crew(agents=[self.report_generator], tasks=[task], verbose=False)
        return crew.kickoff()

    def run_offset_advice_crew(self, emissions_total, location, industry):
        """Run the Carbon Offset Advisor."""
        task = self.create_offset_advice_task(emissions_total, location, industry)
        crew = Crew(agents=[self.offset_advisor], tasks=[task], verbose=False)
        return crew.kickoff()

    def run_regulation_check_crew(self, location, industry, export_markets):
        """Run the Regulation Radar."""
        task = self.create_regulation_check_task(location, industry, export_markets)
        crew = Crew(agents=[self.regulation_radar], tasks=[task], verbose=False)
        return crew.kickoff()

    def run_optimization_crew(self, emissions_data):
        """Run the Emission Optimizer."""
        task = self.create_optimization_task(emissions_data)
        crew = Crew(agents=[self.emission_optimizer], tasks=[task], verbose=False)
        return crew.kickoff()

# -------------------------------------------------------------------

# -------------------------------------------------------------------
# 1. 🔐 Never hardcode API keys in the source file. Always load via `.env`.
# 2. 🧩 Add exception handling for network or model errors (try/except in kickoff).
# 3. 📊 Consider caching frequent LLM responses to reduce cost and latency.
# 4. 🌐 Add multilingual support for outputs (integrate with app config language).
# 5. 🧠 For scalability, dynamically register new agents (via config YAML or DB).
# 6. 🧾 Add a "SummaryAgent" to combine results from multiple agents for reporting dashboards.
# 7. 🧰 Future: Integrate with sustainability APIs (Gold Standard, Verra, CDP) for verified offsets.














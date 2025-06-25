# kvp_pdca_tool
Tool zur Verfolgung von Verbesserungsprojekten
A Streamlit-based web application for managing continuous improvement projects using the KVP (Kontinuierlicher Verbesserungsprozess) and PDCA (Plan-Do-Check-Act) methodologies.

📌 Features
✅ Dashboard Overview

Track key metrics (active projects, open tasks, completion rate, savings)

Interactive charts for project status and progress trends

PDCA cycle visualization

✅ Project Management

Create, view, and track improvement projects

Filter by status, priority, and deadline

Track expected vs. actual savings

✅ Task Tracking

Assign tasks with priorities (High/Medium/Low)

Track task status (New, In Progress, Review, Completed)

Associate tasks with PDCA phases

✅ Analytics & Reports

Success rate by category

Savings over time

Project performance metrics

🚀 Installation
Prerequisites
Python 3.8+

pip (Python package manager)

Steps
Clone the repository:

bash
git clone https://github.com/yourusername/kvp-pdca-tool.git
cd kvp-pdca-tool
Set up a virtual environment (recommended):

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
Install dependencies:

bash
pip install -r requirements.txt
Run the app:

bash
streamlit run kvp_pdca_tool.py
The app will open in your browser at http://localhost:8501.

📂 Project Structure
text
kvp-pdca-tool/
├── kvp_pdca_tool.py      # Main application code
├── requirements.txt      # Python dependencies
├── README.md             # Documentation
└── assets/               # (Optional) Screenshots & additional files
📊 Screenshots
Dashboard	Projects	Tasks
https://assets/dashboard.png	https://assets/projects.png	https://assets/tasks.png
🔧 Troubleshooting
Common Issues
❌ "ModuleNotFoundError: No module named 'plotly'"
➡ Run:

bash
pip install plotly
❌ Streamlit not found
➡ Ensure Streamlit is installed:

bash
pip install streamlit
❌ App not updating
➡ Clear cache or restart Streamlit:

bash
streamlit cache clear
📜 License
This project is licensed under the MIT License. See LICENSE for details.

🙏 Acknowledgments
Streamlit for the web framework

Plotly for interactive charts

Bootstrap-inspired styling for a clean UI

🌟 Enjoy using the KVP/PDCA Tool?
⭐ Star the repo if you find it useful!
🐞 Report issues here.

Happy Improving! 🚀

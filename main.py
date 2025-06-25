import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="KVP/PDCA Tool - Kontinuierliche Verbesserung",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
:root {
    --primary-color: #0066cc;
    --secondary-color: #28a745;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --info-color: #17a2b8;
    --light-gray: #f8f9fa;
    --border-color: #dee2e6;
}

[data-testid="stSidebar"] {
    background-color: #f8f9fa;
}

[data-testid="stHeader"] {
    background: linear-gradient(135deg, var(--primary-color), #004499);
    color: white;
}

.card {
    border: none;
    box-shadow: 0 2px 15px rgba(0,0,0,0.08);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 25px rgba(0,0,0,0.12);
}

.kpi-card {
    background: linear-gradient(135deg, #fff, #f8f9fa);
    border-left: 4px solid var(--primary-color);
}

.kpi-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: var(--primary-color);
}

.pdca-phase {
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    transition: all 0.3s ease;
    cursor: pointer;
}

.pdca-plan { background: linear-gradient(135deg, #e3f2fd, #bbdefb); border-left: 5px solid #2196f3; }
.pdca-do { background: linear-gradient(135deg, #e8f5e8, #c8e6c9); border-left: 5px solid #4caf50; }
.pdca-check { background: linear-gradient(135deg, #fff3e0, #ffe0b2); border-left: 5px solid #ff9800; }
.pdca-act { background: linear-gradient(135deg, #fce4ec, #f8bbd9); border-left: 5px solid #e91e63; }

.task-item {
    background: white;
    border-radius: 8px;
    padding: 15px;
    margin: 8px 0;
    border-left: 4px solid #ddd;
    transition: all 0.3s ease;
}

.priority-high { border-left-color: var(--danger-color) !important; }
.priority-medium { border-left-color: var(--warning-color) !important; }
.priority-low { border-left-color: var(--secondary-color) !important; }

.status-badge {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.status-new { background-color: #e3f2fd; color: #1976d2; }
.status-progress { background-color: #fff3e0; color: #f57c00; }
.status-review { background-color: #f3e5f5; color: #7b1fa2; }
.status-completed { background-color: #e8f5e8; color: #388e3c; }

.trend-up { color: var(--secondary-color); }
.trend-down { color: var(--danger-color); }
.trend-stable { color: var(--warning-color); }
</style>
""", unsafe_allow_html=True)

# Sample Data
def initialize_data():
    if 'projects' not in st.session_state:
        st.session_state.projects = [
            {
                "id": 1,
                "name": "Reduktion Ausschussrate Linie 1",
                "category": "Qualität",
                "priority": "high",
                "owner": "Max Mustermann",
                "status": "progress",
                "progress": 65,
                "deadline": "2025-07-15",
                "expectedSavings": 15000,
                "actualSavings": 9750,
                "phase": "do",
                "description": "Reduzierung der Ausschussrate auf Linie 1 durch Prozessoptimierung",
                "created": "2025-05-10"
            },
            {
                "id": 2,
                "name": "Energieeinsparung Produktionshalle",
                "category": "Kosten",
                "priority": "medium",
                "owner": "Erika Musterfrau",
                "status": "review",
                "progress": 45,
                "deadline": "2025-08-30",
                "expectedSavings": 25000,
                "actualSavings": 11250,
                "phase": "check",
                "description": "Reduzierung des Energieverbrauchs durch neue Beleuchtungstechnik",
                "created": "2025-04-15"
            }
        ]
    
    if 'tasks' not in st.session_state:
        st.session_state.tasks = [
            {
                "id": 1,
                "project_id": 1,
                "title": "Datenanalyse Ausschussursachen",
                "description": "Analyse der letzten 3 Monate Ausschussdaten",
                "priority": "high",
                "status": "completed",
                "assignee": "Max Mustermann",
                "due_date": "2025-05-20",
                "phase": "plan",
                "created": "2025-05-10"
            },
            {
                "id": 2,
                "project_id": 1,
                "title": "Maschineneinstellungen optimieren",
                "description": "Optimierung der Parameter für Station 3",
                "priority": "medium",
                "status": "progress",
                "assignee": "Thomas Techniker",
                "due_date": "2025-06-15",
                "phase": "do",
                "created": "2025-05-25"
            }
        ]
    
    if 'comments' not in st.session_state:
        st.session_state.comments = [
            {
                "id": 1,
                "user": "Max Mustermann",
                "text": "Die Datenanalyse zeigt klare Hotspots in Station 3",
                "timestamp": "2025-05-12 14:30",
                "project_id": 1
            },
            {
                "id": 2,
                "user": "Erika Musterfrau",
                "text": "Energieverbrauchsdaten liegen jetzt vor",
                "timestamp": "2025-05-18 09:15",
                "project_id": 2
            }
        ]

# Helper functions
def get_status_badge(status):
    if status == "new":
        return '<span class="status-badge status-new">Neu</span>'
    elif status == "progress":
        return '<span class="status-badge status-progress">In Bearbeitung</span>'
    elif status == "review":
        return '<span class="status-badge status-review">Review</span>'
    else:
        return '<span class="status-badge status-completed">Abgeschlossen</span>'

def get_priority_badge(priority):
    if priority == "high":
        return '<span style="color: var(--danger-color); font-weight: bold;">Hoch</span>'
    elif priority == "medium":
        return '<span style="color: var(--warning-color); font-weight: bold;">Mittel</span>'
    else:
        return '<span style="color: var(--secondary-color); font-weight: bold;">Niedrig</span>'

def get_phase_card(phase, count, progress):
    if phase == "plan":
        return f"""
        <div class="pdca-phase pdca-plan" onclick="alert('PLAN Phase ausgewählt')">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h6><i class="fas fa-lightbulb me-2"></i>PLAN</h6>
                    <p class="mb-0">{count} Aktive Pläne</p>
                </div>
                <div style="text-align: right;">
                    <div class="h4 mb-0">{progress}%</div>
                    <small>Abgeschlossen</small>
                </div>
            </div>
        </div>
        """
    elif phase == "do":
        return f"""
        <div class="pdca-phase pdca-do" onclick="alert('DO Phase ausgewählt')">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h6><i class="fas fa-cogs me-2"></i>DO</h6>
                    <p class="mb-0">{count} In Umsetzung</p>
                </div>
                <div style="text-align: right;">
                    <div class="h4 mb-0">{progress}%</div>
                    <small>Fortschritt</small>
                </div>
            </div>
        </div>
        """
    elif phase == "check":
        return f"""
        <div class="pdca-phase pdca-check" onclick="alert('CHECK Phase ausgewählt')">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h6><i class="fas fa-search me-2"></i>CHECK</h6>
                    <p class="mb-0">{count} In Prüfung</p>
                </div>
                <div style="text-align: right;">
                    <div class="h4 mb-0">{progress}%</div>
                    <small>Geprüft</small>
                </div>
            </div>
        </div>
        """
    else:
        return f"""
        <div class="pdca-phase pdca-act" onclick="alert('ACT Phase ausgewählt')">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h6><i class="fas fa-rocket me-2"></i>ACT</h6>
                    <p class="mb-0">{count} Standardisiert</p>
                </div>
                <div style="text-align: right;">
                    <div class="h4 mb-0">{progress}%</div>
                    <small>Implementiert</small>
                </div>
            </div>
        </div>
        """

# Dashboard Page
def show_dashboard():
    st.title("📊 KVP Dashboard")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="card kpi-card">
            <div style="text-align: center;">
                <div class="kpi-value">24</div>
                <div style="color: #6c757d;">Aktive Projekte</div>
                <div style="display: flex; align-items: center; justify-content: center; margin-top: 10px;">
                    <i class="fas fa-arrow-up" style="color: var(--secondary-color); margin-right: 5px;"></i>
                    <small>+12% vs. Vormonat</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card kpi-card">
            <div style="text-align: center;">
                <div class="kpi-value">156</div>
                <div style="color: #6c757d;">Offene Aufgaben</div>
                <div style="display: flex; align-items: center; justify-content: center; margin-top: 10px;">
                    <i class="fas fa-arrow-down" style="color: var(--danger-color); margin-right: 5px;"></i>
                    <small>-8% vs. Vormonat</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card kpi-card">
            <div style="text-align: center;">
                <div class="kpi-value">78%</div>
                <div style="color: #6c757d;">Abschlussrate</div>
                <div style="display: flex; align-items: center; justify-content: center; margin-top: 10px;">
                    <i class="fas fa-arrow-up" style="color: var(--secondary-color); margin-right: 5px;"></i>
                    <small>+5% vs. Vormonat</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="card kpi-card">
            <div style="text-align: center;">
                <div class="kpi-value">€42k</div>
                <div style="color: #6c757d;">Einsparungen</div>
                <div style="display: flex; align-items: center; justify-content: center; margin-top: 10px;">
                    <i class="fas fa-arrow-up" style="color: var(--secondary-color); margin-right: 5px;"></i>
                    <small>+23% vs. Vormonat</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    st.subheader("Projekt Status Übersicht")
    status_data = pd.DataFrame({
        "Status": ["Neu", "In Bearbeitung", "Review", "Abgeschlossen"],
        "Anzahl": [8, 12, 6, 15]
    })
    fig1 = px.bar(status_data, x="Status", y="Anzahl", color="Status",
                 color_discrete_map={
                     "Neu": "#1976d2",
                     "In Bearbeitung": "#f57c00",
                     "Review": "#7b1fa2",
                     "Abgeschlossen": "#388e3c"
                 })
    st.plotly_chart(fig1, use_container_width=True)
    
    st.subheader("Fortschritt über Zeit")
    progress_data = pd.DataFrame({
        "Monat": ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun"],
        "Fortschritt": [30, 45, 52, 60, 68, 78]
    })
    fig2 = px.line(progress_data, x="Monat", y="Fortschritt", markers=True)
    st.plotly_chart(fig2, use_container_width=True)
    
    # PDCA Cycle
    st.subheader("PDCA Zyklusübersicht")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(get_phase_card("plan", 8, 33), unsafe_allow_html=True)
    with col2:
        st.markdown(get_phase_card("do", 12, 67), unsafe_allow_html=True)
    with col3:
        st.markdown(get_phase_card("check", 6, 45), unsafe_allow_html=True)
    with col4:
        st.markdown(get_phase_card("act", 4, 89), unsafe_allow_html=True)

# Projects Page
def show_projects():
    st.title("📋 Verbesserungsprojekte")
    
    with st.expander("Neues Projekt erstellen", expanded=False):
        with st.form("new_project_form"):
            col1, col2 = st.columns(2)
            with col1:
                project_name = st.text_input("Projektname*")
                project_category = st.selectbox("Kategorie", ["Qualität", "Effizienz", "Kosten", "Sicherheit", "Umwelt"])
                project_priority = st.selectbox("Priorität", ["Hoch", "Mittel", "Niedrig"])
            with col2:
                project_owner = st.text_input("Verantwortlicher")
                project_deadline = st.date_input("Zieltermin")
                expected_savings = st.number_input("Erwartete Einsparung (€)", min_value=0)
            
            problem_description = st.text_area("Problembeschreibung")
            project_goal = st.text_area("Zielstellung")
            
            if st.form_submit_button("Projekt erstellen"):
                new_project = {
                    "id": len(st.session_state.projects) + 1,
                    "name": project_name,
                    "category": project_category,
                    "priority": project_priority.lower(),
                    "owner": project_owner,
                    "status": "new",
                    "progress": 0,
                    "deadline": project_deadline.strftime("%Y-%m-%d"),
                    "expectedSavings": expected_savings,
                    "actualSavings": 0,
                    "phase": "plan",
                    "description": problem_description,
                    "goal": project_goal,
                    "created": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.projects.append(new_project)
                st.success("Projekt erfolgreich erstellt!")
                st.experimental_rerun()
    
    st.subheader("Aktive Projekte")
    for project in st.session_state.projects:
        with st.expander(f"{project['name']} - {project['owner']}", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Kategorie:** {project['category']}")
                st.markdown(f"**Priorität:** {get_priority_badge(project['priority'])}", unsafe_allow_html=True)
                st.markdown(f"**Status:** {get_status_badge(project['status'])}", unsafe_allow_html=True)
                st.markdown(f"**Fortschritt:** {project['progress']}%")
                st.progress(project['progress'] / 100)
            with col2:
                st.markdown(f"**Zieltermin:** {project['deadline']}")
                st.markdown(f"**Erwartete Einsparungen:** €{project['expectedSavings']:,}")
                st.markdown(f"**Realisierte Einsparungen:** €{project['actualSavings']:,}")
            
            st.markdown(f"**Beschreibung:** {project['description']}")
            if 'goal' in project:
                st.markdown(f"**Zielstellung:** {project['goal']}")

# Tasks Page
def show_tasks():
    st.title("✅ Aufgaben & Maßnahmen")
    
    with st.expander("Neue Aufgabe erstellen", expanded=False):
        with st.form("new_task_form"):
            col1, col2 = st.columns(2)
            with col1:
                task_title = st.text_input("Aufgabentitel*")
                task_description = st.text_area("Beschreibung")
                task_priority = st.selectbox("Priorität", ["Hoch", "Mittel", "Niedrig"])
            with col2:
                task_phase = st.selectbox("PDCA Phase", ["Plan", "Do", "Check", "Act"])
                task_assignee = st.text_input("Verantwortlicher")
                task_due_date = st.date_input("Fälligkeitsdatum")
            
            if st.form_submit_button("Aufgabe erstellen"):
                new_task = {
                    "id": len(st.session_state.tasks) + 1,
                    "project_id": 1,  # Default to first project
                    "title": task_title,
                    "description": task_description,
                    "priority": task_priority.lower(),
                    "status": "new",
                    "assignee": task_assignee,
                    "due_date": task_due_date.strftime("%Y-%m-%d"),
                    "phase": task_phase.lower(),
                    "created": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.tasks.append(new_task)
                st.success("Aufgabe erfolgreich erstellt!")
                st.experimental_rerun()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Aufgabenliste")
        for task in st.session_state.tasks:
            priority_class = f"priority-{task['priority']}"
            st.markdown(f"""
            <div class="task-item {priority_class}">
                <div style="display: flex; justify-content: space-between;">
                    <h6>{task['title']}</h6>
                    <div>{get_status_badge(task['status'])}</div>
                </div>
                <p>{task['description']}</p>
                <div style="display: flex; justify-content: space-between; font-size: 0.9em;">
                    <div><strong>Verantwortlich:</strong> {task['assignee']}</div>
                    <div><strong>Fällig:</strong> {task['due_date']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Team Kommentare")
        for comment in st.session_state.comments:
            st.markdown(f"""
            <div class="comment-item">
                <div style="font-weight: bold;">{comment['user']}</div>
                <div style="font-size: 0.9em; color: #6c757d;">{comment['timestamp']}</div>
                <p>{comment['text']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.form("new_comment_form"):
            new_comment = st.text_area("Neuer Kommentar")
            if st.form_submit_button("Kommentar hinzufügen"):
                new_comment_entry = {
                    "id": len(st.session_state.comments) + 1,
                    "user": "Aktueller Benutzer",
                    "text": new_comment,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "project_id": 1  # Default to first project
                }
                st.session_state.comments.append(new_comment_entry)
                st.success("Kommentar hinzugefügt!")
                st.experimental_rerun()

# Analytics Page
def show_analytics():
    st.title("📈 Analytics & Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Erfolgsrate nach Kategorien")
        category_data = pd.DataFrame({
            "Kategorie": ["Qualität", "Effizienz", "Kosten", "Sicherheit", "Umwelt"],
            "Erfolgsrate": [78, 65, 82, 90, 72]
        })
        fig1 = px.bar(category_data, x="Kategorie", y="Erfolgsrate", color="Kategorie")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Zeitlicher Verlauf der Einsparungen")
        savings_data = pd.DataFrame({
            "Monat": ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun"],
            "Einsparungen (€)": [12000, 18000, 22000, 25000, 32000, 42000]
        })
        fig2 = px.line(savings_data, x="Monat", y="Einsparungen (€)", markers=True)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.subheader("Projektmetriken")
    metrics_data = pd.DataFrame({
        "Metrik": ["Durchschn. Projektdauer (Tage)", "Durchschn. Einsparungen pro Projekt (€)", "Durchschn. Aufgaben pro Projekt", "Abschlussquote"],
        "Wert": [45, 12500, 8.5, 78]
    })
    st.dataframe(metrics_data, hide_index=True, use_container_width=True)

# Main App
def main():
    initialize_data()
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("", ["Dashboard", "Projekte", "Aufgaben", "Analytics"])
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Projekte":
        show_projects()
    elif page == "Aufgaben":
        show_tasks()
    elif page == "Analytics":
        show_analytics()
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filter")
    status_filter = st.sidebar.selectbox("Status", ["Alle", "Neu", "In Bearbeitung", "Review", "Abgeschlossen"])
    priority_filter = st.sidebar.selectbox("Priorität", ["Alle", "Hoch", "Mittel", "Niedrig"])
    date_filter = st.sidebar.date_input("Datum")

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import json

# Konfiguration der Seite
st.set_page_config(
    page_title="KVP/PDCA Tool - Kontinuierliche Verbesserung",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS für besseres Styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #fff, #f8f9fa);
        border-left: 4px solid #0066cc;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .pdca-plan { 
        background: linear-gradient(135deg, #e3f2fd, #bbdefb); 
        border-left: 5px solid #2196f3; 
        padding: 1rem; 
        border-radius: 8px; 
        margin: 0.5rem 0;
    }
    .pdca-do { 
        background: linear-gradient(135deg, #e8f5e8, #c8e6c9); 
        border-left: 5px solid #4caf50; 
        padding: 1rem; 
        border-radius: 8px; 
        margin: 0.5rem 0;
    }
    .pdca-check { 
        background: linear-gradient(135deg, #fff3e0, #ffe0b2); 
        border-left: 5px solid #ff9800; 
        padding: 1rem; 
        border-radius: 8px; 
        margin: 0.5rem 0;
    }
    .pdca-act { 
        background: linear-gradient(135deg, #fce4ec, #f8bbd9); 
        border-left: 5px solid #e91e63; 
        padding: 1rem; 
        border-radius: 8px; 
        margin: 0.5rem 0;
    }
    .task-high { border-left: 4px solid #dc3545; padding: 1rem; background: #fff; border-radius: 8px; margin: 0.5rem 0; }
    .task-medium { border-left: 4px solid #ffc107; padding: 1rem; background: #fff; border-radius: 8px; margin: 0.5rem 0; }
    .task-low { border-left: 4px solid #28a745; padding: 1rem; background: #fff; border-radius: 8px; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

# Session State initialisieren
if 'projects' not in st.session_state:
    st.session_state.projects = [
        {
            'id': 1,
            'name': 'Reduktion Ausschussrate Linie 1',
            'category': 'Qualität',
            'priority': 'high',
            'owner': 'Max Mustermann',
            'status': 'progress',
            'progress': 65,
            'deadline': date(2025, 7, 15),
            'expected_savings': 15000,
            'actual_savings': 9750,
            'description': 'Reduzierung der Ausschussrate auf Produktionslinie 1 durch Prozessoptimierung',
            'goal': 'Ausschussrate von 8% auf 3% reduzieren'
        },
        {
            'id': 2,
            'name': 'Energieeffizienz Produktion',
            'category': 'Umwelt',
            'priority': 'medium',
            'owner': 'Anna Schmidt',
            'status': 'review',
            'progress': 85,
            'deadline': date(2025, 8, 30),
            'expected_savings': 25000,
            'actual_savings': 21000,
            'description': 'Optimierung des Energieverbrauchs in der Produktionshalle',
            'goal': 'Energieverbrauch um 20% reduzieren'
        }
    ]

if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {
            'id': 1,
            'title': 'Ursachenanalyse durchführen',
            'description': 'Root Cause Analysis für Ausschussprobleme',
            'priority': 'high',
            'phase': 'plan',
            'assignee': 'Max Mustermann',
            'due_date': date(2025, 7, 10),
            'status': 'progress',
            'project_id': 1
        },
        {
            'id': 2,
            'title': 'Energieverbrauch messen',
            'description': 'Baseline-Messungen für Energieoptimierung',
            'priority': 'medium',
            'phase': 'do',
            'assignee': 'Anna Schmidt',
            'due_date': date(2025, 7, 20),
            'status': 'new',
            'project_id': 2
        }
    ]

if 'comments' not in st.session_state:
    st.session_state.comments = [
        {
            'id': 1,
            'text': 'Erste Messungen zeigen positive Trends',
            'author': 'Max Mustermann',
            'timestamp': datetime.now() - timedelta(hours=2),
            'task_id': 1
        }
    ]

# Sidebar Navigation
st.sidebar.title("🔧 Navigation")
page = st.sidebar.selectbox(
    "Bereich auswählen",
    ["Dashboard", "Projekte", "Aufgaben", "Analytics"]
)

# Sidebar Filters
st.sidebar.subheader("🔍 Filter")
status_filter = st.sidebar.selectbox(
    "Status",
    ["Alle", "Neu", "In Bearbeitung", "Review", "Abgeschlossen"],
    key="status_filter"
)

priority_filter = st.sidebar.selectbox(
    "Priorität",
    ["Alle", "Hoch", "Mittel", "Niedrig"],
    key="priority_filter"
)

date_filter = st.sidebar.date_input(
    "Datum Filter",
    value=None,
    key="date_filter"
)

# Hauptbereich
if page == "Dashboard":
    st.title("📊 KVP Dashboard")
    
    # KPI Metriken
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #0066cc; margin: 0;">24</h3>
            <p style="color: #6c757d; margin: 0;">Aktive Projekte</p>
            <small style="color: #28a745;">📈 +12% vs. Vormonat</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #0066cc; margin: 0;">156</h3>
            <p style="color: #6c757d; margin: 0;">Offene Aufgaben</p>
            <small style="color: #dc3545;">📉 -8% vs. Vormonat</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #0066cc; margin: 0;">78%</h3>
            <p style="color: #6c757d; margin: 0;">Abschlussrate</p>
            <small style="color: #28a745;">📈 +5% vs. Vormonat</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #0066cc; margin: 0;">€42k</h3>
            <p style="color: #6c757d; margin: 0;">Einsparungen</p>
            <small style="color: #28a745;">📈 +23% vs. Vormonat</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Projekt Status Übersicht")
        status_data = {
            'Status': ['Neu', 'In Bearbeitung', 'Review', 'Abgeschlossen'],
            'Anzahl': [8, 12, 6, 18]
        }
        fig = px.bar(status_data, x='Status', y='Anzahl', 
                    color='Status', 
                    color_discrete_map={
                        'Neu': '#17a2b8',
                        'In Bearbeitung': '#ffc107',
                        'Review': '#6f42c1',
                        'Abgeschlossen': '#28a745'
                    })
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Fortschritt über Zeit")
        progress_data = pd.DataFrame({
            'Monat': ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun'],
            'Einsparungen': [15000, 22000, 18000, 35000, 28000, 42000]
        })
        fig = px.line(progress_data, x='Monat', y='Einsparungen', 
                     markers=True, line_shape='spline')
        fig.update_traces(line_color='#0066cc', marker_color='#0066cc')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # PDCA Übersicht
    st.subheader("🔄 PDCA Zyklusübersicht")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="pdca-plan">
            <h4>💡 PLAN</h4>
            <p><strong>8</strong> Aktive Pläne</p>
            <h3>33%</h3>
            <small>Abgeschlossen</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="pdca-do">
            <h4>⚙️ DO</h4>
            <p><strong>12</strong> In Umsetzung</p>
            <h3>67%</h3>
            <small>Fortschritt</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="pdca-check">
            <h4>🔍 CHECK</h4>
            <p><strong>6</strong> In Prüfung</p>
            <h3>45%</h3>
            <small>Geprüft</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="pdca-act">
            <h4>🚀 ACT</h4>
            <p><strong>4</strong> Standardisiert</p>
            <h3>89%</h3>
            <small>Implementiert</small>
        </div>
        """, unsafe_allow_html=True)

elif page == "Projekte":
    st.title("🏗️ Verbesserungsprojekte")
    
    # Neues Projekt Button
    if st.button("➕ Neues Projekt erstellen"):
        st.session_state.show_new_project = True
    
    # Neues Projekt Formular
    if st.session_state.get('show_new_project', False):
        with st.expander("📝 Neues Projekt erstellen", expanded=True):
            with st.form("new_project_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    project_name = st.text_input("Projektname*")
                    project_category = st.selectbox("Kategorie", 
                                                  ["Qualität", "Effizienz", "Kosten", "Sicherheit", "Umwelt"])
                    project_priority = st.selectbox("Priorität", 
                                                   ["high", "medium", "low"],
                                                   format_func=lambda x: {"high": "Hoch", "medium": "Mittel", "low": "Niedrig"}[x])
                
                with col2:
                    project_owner = st.text_input("Verantwortlicher")
                    project_deadline = st.date_input("Zieltermin")
                    expected_savings = st.number_input("Erwartete Einsparung (€)", min_value=0, step=1000)
                
                problem_description = st.text_area("Problembeschreibung")
                project_goal = st.text_area("Zielstellung")
                
                submitted = st.form_submit_button("Projekt erstellen")
                
                if submitted and project_name:
                    new_project = {
                        'id': len(st.session_state.projects) + 1,
                        'name': project_name,
                        'category': project_category,
                        'priority': project_priority,
                        'owner': project_owner,
                        'status': 'new',
                        'progress': 0,
                        'deadline': project_deadline,
                        'expected_savings': expected_savings,
                        'actual_savings': 0,
                        'description': problem_description,
                        'goal': project_goal
                    }
                    st.session_state.projects.append(new_project)
                    st.session_state.show_new_project = False
                    st.success("Projekt erfolgreich erstellt!")
                    st.rerun()
    
    # Projektliste
    for project in st.session_state.projects:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.subheader(f"🎯 {project['name']}")
                st.write(f"**Kategorie:** {project['category']}")
                st.write(f"**Verantwortlicher:** {project['owner']}")
                st.write(f"**Beschreibung:** {project['description']}")
            
            with col2:
                priority_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                st.write(f"**Priorität:** {priority_color[project['priority']]}")
                st.write(f"**Status:** {project['status']}")
                st.write(f"**Fortschritt:** {project['progress']}%")
                st.progress(project['progress'] / 100)
            
            with col3:
                st.write(f"**Zieltermin:** {project['deadline']}")
                st.write(f"**Erwartet:** €{project['expected_savings']:,}")
                st.write(f"**Erreicht:** €{project['actual_savings']:,}")
            
            st.divider()

elif page == "Aufgaben":
    st.title("📋 Aufgaben & Maßnahmen")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Neue Aufgabe Button
        if st.button("➕ Neue Aufgabe erstellen"):
            st.session_state.show_new_task = True
        
        # Neue Aufgabe Formular
        if st.session_state.get('show_new_task', False):
            with st.expander("📝 Neue Aufgabe erstellen", expanded=True):
                with st.form("new_task_form"):
                    task_title = st.text_input("Aufgabentitel*")
                    task_description = st.text_area("Beschreibung")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        task_priority = st.selectbox("Priorität", 
                                                   ["high", "medium", "low"],
                                                   format_func=lambda x: {"high": "Hoch", "medium": "Mittel", "low": "Niedrig"}[x])
                        task_assignee = st.text_input("Verantwortlicher")
                    
                    with col_b:
                        task_phase = st.selectbox("PDCA Phase", ["plan", "do", "check", "act"],
                                                format_func=lambda x: {"plan": "Plan", "do": "Do", "check": "Check", "act": "Act"}[x])
                        task_due_date = st.date_input("Fälligkeitsdatum")
                    
                    submitted = st.form_submit_button("Aufgabe erstellen")
                    
                    if submitted and task_title:
                        new_task = {
                            'id': len(st.session_state.tasks) + 1,
                            'title': task_title,
                            'description': task_description,
                            'priority': task_priority,
                            'phase': task_phase,
                            'assignee': task_assignee,
                            'due_date': task_due_date,
                            'status': 'new',
                            'project_id': 1
                        }
                        st.session_state.tasks.append(new_task)
                        st.session_state.show_new_task = False
                        st.success("Aufgabe erfolgreich erstellt!")
                        st.rerun()
        
        # Aufgabenliste
        st.subheader("📝 Aufgabenliste")
        for task in st.session_state.tasks:
            priority_class = f"task-{task['priority']}"
            
            st.markdown(f"""
            <div class="{priority_class}">
                <h4>{task['title']}</h4>
                <p><strong>Beschreibung:</strong> {task['description']}</p>
                <p><strong>Verantwortlicher:</strong> {task['assignee']} | 
                   <strong>Phase:</strong> {task['phase'].upper()} | 
                   <strong>Fällig:</strong> {task['due_date']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("💬 Team Kommentare")
        
        # Kommentare anzeigen
        for comment in st.session_state.comments:
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin: 10px 0; border-left: 3px solid #17a2b8;">
                <p style="margin: 0;"><strong>{comment['author']}</strong></p>
                <p style="margin: 5px 0;">{comment['text']}</p>
                <small style="color: #6c757d;">{comment['timestamp'].strftime('%d.%m.%Y %H:%M')}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Neuer Kommentar
        new_comment = st.text_area("Kommentar hinzufügen...", key="new_comment")
        if st.button("💬 Kommentar hinzufügen") and new_comment:
            comment = {
                'id': len(st.session_state.comments) + 1,
                'text': new_comment,
                'author': 'Aktueller Benutzer',
                'timestamp': datetime.now(),
                'task_id': 1
            }
            st.session_state.comments.append(comment)
            st.rerun()

elif page == "Analytics":
    st.title("📈 Analytics & Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Erfolgsrate nach Kategorien")
        category_data = {
            'Kategorie': ['Qualität', 'Effizienz', 'Kosten', 'Sicherheit', 'Umwelt'],
            'Erfolgsrate': [85, 72, 91, 68, 79]
        }
        fig = px.bar(category_data, x='Kategorie', y='Erfolgsrate',
                    color='Erfolgsrate', color_continuous_scale='Blues')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Einsparungen über Zeit")
        savings_data = pd.DataFrame({
            'Monat': pd.date_range('2025-01-01', periods=6, freq='M'),
            'Einsparungen': [15000, 22000, 18000, 35000, 28000, 42000],
            'Ziel': [20000, 20000, 20000, 30000, 30000, 40000]
        })
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=savings_data['Monat'], y=savings_data['Einsparungen'],
                                mode='lines+markers', name='Tatsächlich', line_color='#0066cc'))
        fig.add_trace(go.Scatter(x=savings_data['Monat'], y=savings_data['Ziel'],
                                mode='lines+markers', name='Ziel', line_color='#28a745'))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailanalyse
    st.subheader("📋 Detailanalyse")
    
    # Projektstatistiken
    projects_df = pd.DataFrame(st.session_state.projects)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Durchschnittlicher Fortschritt", f"{projects_df['progress'].mean():.1f}%")
    
    with col2:
        st.metric("Gesamte erwartete Einsparungen", f"€{projects_df['expected_savings'].sum():,}")
    
    with col3:
        st.metric("Gesamte erzielte Einsparungen", f"€{projects_df['actual_savings'].sum():,}")
    
    # Projekttabelle
    st.subheader("📋 Projektübersicht")
    st.dataframe(
        projects_df[['name', 'category', 'priority', 'status', 'progress', 'expected_savings', 'actual_savings']],
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown("*KVP/PDCA Tool - Kontinuierliche Verbesserung für Ihr Unternehmen*")

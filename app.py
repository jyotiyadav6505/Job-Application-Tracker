import streamlit as st
import pandas as pd

from database import (
    create_database,
    add_application,
    get_applications,
    get_status_counts,
    update_application,
    delete_application,
    get_dashboard_metrics
)


# ==================================================
# DATABASE SETUP
# ==================================================

create_database()


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Job Application Tracker",
    page_icon="💼",
    layout="wide"
)


# ==================================================
# CUSTOM STYLING
# ==================================================

st.markdown("""
<style>

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        font-size: 18px;
        color: #b0b0b0;
        margin-bottom: 25px;
    }

    /* Dashboard metric cards */
    div[data-testid="stMetric"] {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #374151;
    }

    div[data-testid="stMetricLabel"] {
        color: #d1d5db !important;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Download button */
    .stDownloadButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Expander headers */
    .streamlit-expanderHeader {
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">💼 Job Application Tracker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Track and manage your job and internship applications in one place.'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

st.sidebar.header("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Add Application",
        "Applications"
    ]
)


# ==================================================
# DASHBOARD
# ==================================================

if page == "Dashboard":

    st.header("📊 Dashboard")

    (
        total,
        interviews,
        offers,
        rejected,
        interview_rate,
        success_rate
    ) = get_dashboard_metrics()

    # Main statistics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Applications",
        total
    )

    col2.metric(
        "Interviews",
        interviews
    )

    col3.metric(
        "Offers",
        offers
    )

    col4.metric(
        "Rejected",
        rejected
    )

    st.divider()

    # Performance rates
    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🎯 Interview Rate",
            f"{interview_rate:.1f}%"
        )

    with col2:

        st.metric(
            "🏆 Offer Rate",
            f"{success_rate:.1f}%"
        )

    st.divider()

    # Status chart
    st.subheader("📊 Application Status")

    status_data = get_status_counts()

    if status_data:

        statuses = [
            item[0]
            for item in status_data
        ]

        counts = [
            item[1]
            for item in status_data
        ]

        chart_data = {
            "Status": statuses,
            "Applications": counts
        }

        st.bar_chart(
            chart_data,
            x="Status",
            y="Applications"
        )

    else:

        st.info(
            "No applications available yet. "
            "Add your first application!"
        )


# ==================================================
# ADD APPLICATION
# ==================================================

elif page == "Add Application":

    st.header("➕ Add Job Application")

    company = st.text_input(
        "Company Name",
        placeholder="e.g. Google"
    )

    role = st.text_input(
        "Job Role",
        placeholder="e.g. Software Engineer Intern"
    )

    location = st.text_input(
        "Location",
        placeholder="e.g. Bangalore / Remote"
    )

    application_date = st.date_input(
        "Application Date"
    )

    job_link = st.text_input(
        "Job Link",
        placeholder="https://..."
    )

    status = st.selectbox(
        "Application Status",
        [
            "Applied",
            "Under Review",
            "Interview",
            "Rejected",
            "Offer"
        ]
    )

    interview_date = st.date_input(
        "Interview Date",
        value=None
    )

    notes = st.text_area(
        "Notes",
        placeholder="Add any notes about this application..."
    )

    st.divider()

    if st.button(
        "💾 Save Application"
    ):

        if not company.strip():

            st.error(
                "Company Name is required."
            )

        elif not role.strip():

            st.error(
                "Job Role is required."
            )

        else:

            add_application(
                company,
                role,
                location,
                application_date,
                job_link,
                status,
                interview_date,
                notes
            )

            st.success(
                "Application saved successfully!"
            )


# ==================================================
# APPLICATIONS
# ==================================================

elif page == "Applications":

    st.header("📋 My Applications")

    applications = get_applications()

    if not applications:

        st.info(
            "No applications found. "
            "Add your first application!"
        )

    else:

        # ------------------------------------------
        # CSV EXPORT
        # ------------------------------------------

        columns = [
            "ID",
            "Company",
            "Role",
            "Location",
            "Application Date",
            "Job Link",
            "Status",
            "Interview Date",
            "Notes"
        ]

        df = pd.DataFrame(
            applications,
            columns=columns
        )

        csv_data = df.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Download Applications CSV",
            data=csv_data,
            file_name="job_applications.csv",
            mime="text/csv"
        )

        st.divider()

        # ------------------------------------------
        # SEARCH AND FILTER
        # ------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            search = st.text_input(
                "🔍 Search",
                placeholder="Search company or job role..."
            )

        with col2:

            status_filter = st.selectbox(
                "📌 Filter by Status",
                [
                    "All",
                    "Applied",
                    "Under Review",
                    "Interview",
                    "Rejected",
                    "Offer"
                ]
            )

        # ------------------------------------------
        # FILTER APPLICATIONS
        # ------------------------------------------

        filtered_applications = []

        for application in applications:

            (
                app_id,
                company,
                role,
                location,
                application_date,
                job_link,
                status,
                interview_date,
                notes
            ) = application

            search_match = (
                search.lower() in company.lower()
                or search.lower() in role.lower()
            )

            status_match = (
                status_filter == "All"
                or status == status_filter
            )

            if search_match and status_match:

                filtered_applications.append(
                    application
                )

        st.write(
            f"Showing {len(filtered_applications)} "
            f"application(s)"
        )

        # ------------------------------------------
        # DISPLAY APPLICATIONS
        # ------------------------------------------

        if not filtered_applications:

            st.warning(
                "No applications match your search/filter."
            )

        else:

            for application in filtered_applications:

                (
                    app_id,
                    company,
                    role,
                    location,
                    application_date,
                    job_link,
                    status,
                    interview_date,
                    notes
                ) = application

                with st.expander(
                    f"{company} — {role}"
                ):

                    # Application details
                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"**Location:** {location}"
                        )

                        st.write(
                            f"**Application Date:** "
                            f"{application_date}"
                        )

                        st.write(
                            f"**Status:** {status}"
                        )

                    with col2:

                        st.write(
                            f"**Interview Date:** "
                            f"{interview_date}"
                        )

                        if job_link:

                            st.write(
                                f"**Job Link:** {job_link}"
                            )

                    if notes:

                        st.write(
                            f"**Notes:** {notes}"
                        )

                    st.divider()

                    # ----------------------------------
                    # EDIT AND DELETE
                    # ----------------------------------

                    edit_col, delete_col = st.columns(2)

                    with edit_col:

                        if st.button(
                            "✏️ Edit",
                            key=f"edit_{app_id}"
                        ):

                            st.session_state[
                                f"editing_{app_id}"
                            ] = True

                    with delete_col:

                        if st.button(
                            "🗑️ Delete",
                            key=f"delete_{app_id}"
                        ):

                            delete_application(
                                app_id
                            )

                            st.success(
                                "Application deleted successfully!"
                            )

                            st.rerun()

                    # ----------------------------------
                    # EDIT FORM
                    # ----------------------------------

                    if st.session_state.get(
                        f"editing_{app_id}",
                        False
                    ):

                        st.subheader(
                            "✏️ Edit Application"
                        )

                        edit_company = st.text_input(
                            "Company Name",
                            value=company,
                            key=f"company_{app_id}"
                        )

                        edit_role = st.text_input(
                            "Job Role",
                            value=role,
                            key=f"role_{app_id}"
                        )

                        edit_location = st.text_input(
                            "Location",
                            value=location or "",
                            key=f"location_{app_id}"
                        )

                        edit_date = st.text_input(
                            "Application Date",
                            value=application_date or "",
                            key=f"date_{app_id}"
                        )

                        edit_link = st.text_input(
                            "Job Link",
                            value=job_link or "",
                            key=f"link_{app_id}"
                        )

                        status_options = [
                            "Applied",
                            "Under Review",
                            "Interview",
                            "Rejected",
                            "Offer"
                        ]

                        if status in status_options:

                            status_index = (
                                status_options.index(status)
                            )

                        else:

                            status_index = 0

                        edit_status = st.selectbox(
                            "Application Status",
                            status_options,
                            index=status_index,
                            key=f"status_{app_id}"
                        )

                        edit_interview = st.text_input(
                            "Interview Date",
                            value=interview_date or "",
                            key=f"interview_{app_id}"
                        )

                        edit_notes = st.text_area(
                            "Notes",
                            value=notes or "",
                            key=f"notes_{app_id}"
                        )

                        if st.button(
                            "💾 Save Changes",
                            key=f"save_{app_id}"
                        ):

                            update_application(
                                app_id,
                                edit_company,
                                edit_role,
                                edit_location,
                                edit_date,
                                edit_link,
                                edit_status,
                                edit_interview,
                                edit_notes
                            )

                            st.session_state[
                                f"editing_{app_id}"
                            ] = False

                            st.success(
                                "Application updated successfully!"
                            )

                            st.rerun()
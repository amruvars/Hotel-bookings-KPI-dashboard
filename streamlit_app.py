import streamlit as st

from snowflake.snowpark.context import get_active_session


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Hotel Booking Dashboard",
    page_icon="🏨",
    layout="wide"
)


# =========================================================
# SNOWFLAKE SESSION
# =========================================================

session = get_active_session()


# =========================================================
# TITLE
# =========================================================

st.title("🏨 Hotel Booking Dashboard")
st.write("Hotel Booking Analysis & Revenue Dashboard")


# =========================================================
# LOAD BOOKING DATA
# =========================================================

booking_query = """
SELECT *
FROM HOTEL_DB.PUBLIC.GOLD_BOOKING_CLEAN
"""

df = session.sql(booking_query).to_pandas()


# =========================================================
# CHECK DATA
# =========================================================

if df.empty:

    st.warning("No booking data found.")

else:

    # =====================================================
    # KPI CALCULATIONS
    # =====================================================

    total_bookings = len(df)

    total_revenue = df["TOTAL_AMOUNT"].sum()

    average_booking = df["TOTAL_AMOUNT"].mean()

    total_guests = df["NUM_GUESTS"].sum()


    # =====================================================
    # KPI CARDS
    # =====================================================

    st.subheader("📌 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Bookings",
        f"{total_bookings:,}"
    )

    col2.metric(
        "Total Revenue",
        f"${total_revenue:,.2f}"
    )

    col3.metric(
        "Average Booking",
        f"${average_booking:,.2f}"
    )

    col4.metric(
        "Total Guests",
        f"{total_guests:,}"
    )


    # =====================================================
    # DAILY BOOKING TREND
    # =====================================================

    st.subheader("📈 Daily Booking Trend")

    daily_query = """
    SELECT DATE, TOTAL_BOOKING
    FROM HOTEL_DB.PUBLIC.GOLD_AGG_DAILY_BOOKINGS
    ORDER BY DATE
    """

    daily_df = session.sql(daily_query).to_pandas()

    if not daily_df.empty:

        st.line_chart(
            daily_df.set_index("DATE")["TOTAL_BOOKING"]
        )

    else:

        st.warning("No daily booking data available.")


    # =====================================================
    # REVENUE BY HOTEL CITY
    # =====================================================

    st.subheader("💰 Revenue by Hotel City")

    city_query = """
    SELECT HOTEL_CITY, TOTAL_REVENUE
    FROM HOTEL_DB.PUBLIC.GOLD_AGG_HOTEL_CITY_SALES
    ORDER BY TOTAL_REVENUE DESC
    """

    city_df = session.sql(city_query).to_pandas()

    if not city_df.empty:

        st.bar_chart(
            city_df.set_index("HOTEL_CITY")["TOTAL_REVENUE"]
        )

    else:

        st.warning("No hotel city revenue data available.")


    # =====================================================
    # BOOKING STATUS
    # =====================================================

    st.subheader("📊 Booking Status Distribution")

    status_query = """
    SELECT
        BOOKING_STATUS,
        COUNT(*) AS BOOKINGS
    FROM HOTEL_DB.PUBLIC.GOLD_BOOKING_CLEAN
    GROUP BY BOOKING_STATUS
    ORDER BY BOOKINGS DESC
    """

    status_df = session.sql(status_query).to_pandas()

    if not status_df.empty:

        st.bar_chart(
            status_df.set_index("BOOKING_STATUS")["BOOKINGS"]
        )


    # =====================================================
    # ROOM TYPE
    # =====================================================

    st.subheader("🛏️ Bookings by Room Type")

    room_query = """
    SELECT
        ROOM_TYPE,
        COUNT(*) AS BOOKINGS
    FROM HOTEL_DB.PUBLIC.GOLD_BOOKING_CLEAN
    GROUP BY ROOM_TYPE
    ORDER BY BOOKINGS DESC
    """

    room_df = session.sql(room_query).to_pandas()

    if not room_df.empty:

        st.bar_chart(
            room_df.set_index("ROOM_TYPE")["BOOKINGS"]
        )


    # =====================================================
    # REVENUE BY BOOKING STATUS
    # =====================================================

    st.subheader("💵 Revenue by Booking Status")

    revenue_status_query = """
    SELECT
        BOOKING_STATUS,
        SUM(TOTAL_AMOUNT) AS TOTAL_REVENUE
    FROM HOTEL_DB.PUBLIC.GOLD_BOOKING_CLEAN
    GROUP BY BOOKING_STATUS
    ORDER BY TOTAL_REVENUE DESC
    """

    revenue_status_df = session.sql(
        revenue_status_query
    ).to_pandas()

    if not revenue_status_df.empty:

        st.bar_chart(
            revenue_status_df.set_index(
                "BOOKING_STATUS"
            )["TOTAL_REVENUE"]
        )


    # =====================================================
    # GUESTS BY ROOM TYPE
    # =====================================================

    st.subheader("👥 Guests by Room Type")

    guests_query = """
    SELECT
        ROOM_TYPE,
        SUM(NUM_GUESTS) AS TOTAL_GUESTS
    FROM HOTEL_DB.PUBLIC.GOLD_BOOKING_CLEAN
    GROUP BY ROOM_TYPE
    ORDER BY TOTAL_GUESTS DESC
    """

    guests_df = session.sql(
        guests_query
    ).to_pandas()

    if not guests_df.empty:

        st.bar_chart(
            guests_df.set_index("ROOM_TYPE")["TOTAL_GUESTS"]
        )


    # =====================================================
    # CITY SUMMARY
    # =====================================================

    st.subheader("📋 Revenue by Hotel City")

    st.dataframe(
        city_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # BOOKING STATUS SUMMARY
    # =====================================================

    st.subheader("📋 Booking Status Summary")

    st.dataframe(
        status_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # ROOM SUMMARY
    # =====================================================

    st.subheader("📋 Room Type Summary")

    st.dataframe(
        room_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # COMPLETE BOOKING DATA
    # =====================================================

    st.subheader("📋 Hotel Booking Data")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown("---")

    st.caption(
        "Hotel Booking Dashboard | Snowflake Streamlit"
    )
import streamlit as st
from CoolProp.CoolProp import PropsSI
import pandas as pd


def check_inlet():
    """
    Check if the inlet is superheated steam
    """
    t_sat = PropsSI("T", "P", P, "Q", 1, FLUID)
    if T > t_sat:
        return True
    else:
        return False


def calculate_inlet():
    inlet_data = pd.DataFrame(data={"Property": ["T", "P", "Q"], "Value": [T, P, 1]})
    return inlet_data


with st.sidebar:

    st.write("## Turbine model parameters")
    FLUID = st.selectbox(
        "Select Fluid",
        [
            "Water",
            "R134a",
            "R410A",
            "R22",
            "R290",
            "R600a",
            "R744",
        ],
    )
    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input(
            "Inlet pressure [Pa]",
            value=101325.0,
            max_value=PropsSI("PCRIT", FLUID),
            min_value=PropsSI("PMIN", FLUID),
            step=1000.0,
            format="%.0f",
        )
    with col2:
        T = st.number_input(
            "Inlet temperature [K]",
            value=300.0,
            max_value=PropsSI("Tcrit", FLUID),
            min_value=PropsSI("Tmin", FLUID),
            step=0.1,
            format="%.1f",
        )


if check_inlet():
    inlet_data = calculate_inlet()
    st.success("Inlet is superheated steam")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Inlet Properties")
        st.table(calculate_inlet())
    with col2:
        st.write("### Outlet Properties")
else:
    st.error("Inlet is not superheated steam")
    st.stop()

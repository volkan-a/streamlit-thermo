"""
Streamlit implementation of expansion valve modeling
User can select the outlet vapor quality and the inlet conditions
Then model will calculate the outlet pressure using bisection method
"""
import streamlit as st
from CoolProp.CoolProp import PropsSI
from PIL import Image


def calculate(p_out: float) -> float:
    """
    Calculate the outlet vapor quality of the fluid according to given outlet pressure
    """
    try:
        h_out = PropsSI("H", PROP1, VALUE1, PROP2, VALUE2, FLUID)
        x_actual = PropsSI("Q", "P", p_out, "H", h_out, FLUID)
        return x_actual - x_out
    except ValueError:
        st.error("Value error")
        return 0.0


def bisection(iter_max=20, tol=1e-6):
    """
    Bisection method to find the outlet pressure
    """
    p_l = PropsSI("PMIN", FLUID)
    p_u = PropsSI("P", PROP1, VALUE1, PROP2, VALUE2, FLUID)

    x_m = 100
    i = 0
    while abs(x_m) > tol:
        i += 1
        p_m = 0.5 * (p_l + p_u)
        x_m = calculate(p_m)
        x_l = calculate(p_l)
        if x_m * x_l > 0.0:
            p_l = p_m
        else:
            p_u = p_m
        if i > iter_max:
            st.error(
                "Maximum number of iterations reached\nTry to change the inlet conditions"
            )
            st.stop()
    return (p_m, x_m)


with st.sidebar:
    st.write("### Valve outlet vapor fraction")
    valve_image = Image.open("./Images/expansion_valve.png")
    st.image(valve_image, use_column_width=True)
    col1, col2 = st.columns(2)
    with col1:
        FLUID = st.selectbox(
            "Fluid",
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
    with col2:
        property_pair = st.selectbox("Property pair", ["TP", "TQ", "PQ"])

    if property_pair == "TP":
        PROP1 = "T"
        PROP2 = "P"
        LABEL1 = "Temperature [K]"
        LABEL2 = "Pressure [Pa]"
        VALUE1 = 300.0
        VALUE2 = 101325.0
    elif property_pair == "TQ":
        PROP1 = "T"
        PROP2 = "Q"
        LABEL1 = "Temperature [K]"
        LABEL2 = "Vapor fraction [-]"
        VALUE1 = 300.0
        VALUE2 = 0.0000
    elif property_pair == "PQ":
        PROP1 = "P"
        PROP2 = "Q"
        LABEL1 = "Pressure [Pa]"
        LABEL2 = "Vapor fraction [-]"
        VALUE1 = 101325.0
        VALUE2 = 0.0000
    col1, col2 = st.columns(2)
    with col1:
        VALUE1 = st.number_input(label=LABEL1, value=VALUE1, max_value=1e6, step=1.0)
    with col2:
        VALUE2 = st.number_input(LABEL2, VALUE2)
    x_out = st.number_input(
        "Outlet vapor fraction", value=0.5, min_value=0.0, max_value=1.0, step=0.01
    )
    calculate_button = st.button("Calculate")


POUT, err = bisection()
PIN = PropsSI("P", PROP1, VALUE1, PROP2, VALUE2, FLUID)
TIN = PropsSI("T", PROP1, VALUE1, PROP2, VALUE2, FLUID)
SIN = PropsSI("S", PROP1, VALUE1, PROP2, VALUE2, FLUID)
TOUT = PropsSI("T", "P", POUT, "Q", x_out, FLUID)
SOUT = PropsSI("S", "P", POUT, "Q", x_out, FLUID)

deltaP = POUT - PIN
deltaT = TOUT - TIN
deltaS = SOUT - SIN
st.write("### Valve output stream properties")
st.metric(
    label="Pressure",
    value=f"{POUT/1000:.1f} kPa",
    delta=f"{deltaP/1000:.1f} kPa",
)
st.metric(
    label="Temperature",
    value=f"{TOUT:.1f} K",
    delta=f"{deltaT:.1f} K",
)
st.metric(
    label="Specific entropy",
    value=f"{SOUT:.1f} kJ/kg/K",
    delta=f"{deltaS:.1f} kJ/kg/K",
)

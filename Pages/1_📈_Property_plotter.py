"""
Plots ts and ph diagrams for select fluid
"""
import streamlit as st
from CoolProp.CoolProp import PropsSI
from bokeh.plotting import figure


def ts_plotter(fluid: str, n_max=1000) -> tuple[list[float], list[float]]:
    """
    Return entropy and temperature of a given fluid in order to plot ts diagram
    """
    print(fluid)
    t_min = PropsSI("TMIN", fluid)
    t_max = PropsSI("TCRIT", fluid)
    t_list = []
    s_list = []
    for i in range(n_max):
        t_cur = t_min + i * (t_max - t_min) / n_max
        s_cur = PropsSI("S", "T", t_cur, "Q", 0, fluid)
        t_list.append(t_cur - 273.15)
        s_list.append(s_cur / 1000)
    for i in range(n_max):
        t_cur = t_max - i * (t_max - t_min) / n_max
        s_cur = PropsSI("S", "T", t_cur, "Q", 1, fluid)
        t_list.append(t_cur - 273.15)
        s_list.append(s_cur / 1000)
    return (s_list, t_list)


def ph_plotter(fluid: str, n_max=1000) -> tuple[list[float], list[float]]:
    """
    Return enthalpy and pressure of a given fluid in order to plot ph diagram
    """
    print(fluid)
    p_min = PropsSI("PMIN", fluid)
    p_max = PropsSI("PCRIT", fluid)
    p_list = []
    h_list = []
    for i in range(n_max):
        p_cur = p_min + i * (p_max - p_min) / n_max
        try:
            h_cur = PropsSI("H", "P", p_cur, "Q", 0, fluid)
        except ValueError:
            continue
        p_list.append(p_cur / 1000)
        h_list.append(h_cur / 1000)
    for i in range(n_max):
        p_cur = p_max - i * (p_max - p_min) / n_max
        try:
            h_cur = PropsSI("H", "P", p_cur, "Q", 1, fluid)
        except ValueError:
            continue
        p_list.append(p_cur / 1000)
        h_list.append(h_cur / 1000)
    return (h_list, p_list)


st.write("# Property plotter")
# Get the input parameters
FLUID = st.selectbox(
    "Select a fluid",
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
PROPERTY_PAIR = st.radio("Select a property pair", ["TS", "PH"])
SLIST, TLIST = ts_plotter(FLUID)
HLIST, PLIST = ph_plotter(FLUID)
if PROPERTY_PAIR == "TS":
    p = figure(
        title=f"TS diagram of {FLUID}",
        x_axis_label="Entropy (kJ/kgK)",
        y_axis_label="Temperature (°C)",
        height=400,
        width=300,
    )
    p.varea(x=SLIST, y1=TLIST, y2=TLIST[0], color="orange", alpha=0.3)
    p.line(SLIST, TLIST, line_width=2, color="orange")
elif PROPERTY_PAIR == "PH":
    p = figure(
        title=f"PH diagram of {FLUID}",
        x_axis_label="Enthalpy (kJ/kg)",
        y_axis_label="Pressure (kPa)",
        height=400,
        width=300,
    )
    p.varea(
        x=HLIST,
        y1=PLIST,
        y2=PLIST[0],
        color="blue",
        alpha=0.3,
    )
    p.line(HLIST, PLIST, line_width=2, color="blue")
with st.container():
    p.title_location = "above"
    st.bokeh_chart(p, use_container_width=True)

import streamlit as st
from CoolProp.CoolProp import PropsSI
from bokeh.plotting import figure

# a function that plot ts diagram of a given fluid
def ts_plotter(fluid: str, N=1000) -> tuple[list[float], list[float]]:
    """
    Return entropy and temperature of a given fluid in order to plot ts diagram
    """
    t_min = PropsSI("TMIN", fluid)
    t_max = PropsSI("TCRIT", fluid)
    t_list = []
    s_list = []
    for i in range(N):
        t_cur = t_min + i * (t_max - t_min) / N
        s_cur = PropsSI("S", "T", t_cur, "Q", 0, fluid)
        t_list.append(t_cur - 273.15)
        s_list.append(s_cur / 1000)
    for i in range(N):
        t_cur = t_max - i * (t_max - t_min) / N
        s_cur = PropsSI("S", "T", t_cur, "Q", 1, fluid)
        t_list.append(t_cur - 273.15)
        s_list.append(s_cur / 1000)
    return (s_list, t_list)


st.title("TS diagram plotter")
# Get the input parameters
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
SLIST, TLIST = ts_plotter(FLUID)
p = figure(
    title=f"TS diagram of {FLUID}",
    x_axis_label="Entropy (kJ/kgK)",
    y_axis_label="Temperature (°C)",
    height=400,
    width=300,
)
p.varea(x=SLIST, y1=TLIST, y2=TLIST[0], color="orange", alpha=0.3)
p.title_location = "below"
p.line(SLIST, TLIST, line_width=2, color="orange")
with st.container():
    st.bokeh_chart(p, use_container_width=True)

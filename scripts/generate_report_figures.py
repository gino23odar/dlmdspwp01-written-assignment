
from pathlib import Path
import sqlite3

import pandas as pd

from bokeh.io import save
from bokeh.layouts import column
from bokeh.models import Range1d
from bokeh.plotting import figure
from bokeh.resources import INLINE

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = ROOT / "output"
OUTPUT.mkdir(parents=True, exist_ok=True)

# read the input datasets
training = pd.read_csv(DATA / "train.csv")
ideal = pd.read_csv(DATA / "ideal.csv")

# read actual results
db_path = OUTPUT / "assignment.db"
with sqlite3.connect(db_path) as connection:
    mapped = pd.read_sql_query(
        "SELECT x, y, delta_y, ideal_func FROM test_results",
        connection,
    )

assert len(mapped) == 34, (
    f"Expected 34 mapped observations, got {len(mapped)}"
)

# ---------------------------------------------------
# FIGURE 1: Training y1 versus selected ideal y13
# ---------------------------------------------------

comparison = training[["x", "y1"]].merge(
    ideal[["x", "y13"]],
    on="x",
    validate="one_to_one",
).sort_values("x")

comparison["residual"] = (
    comparison["y1"] - comparison["y13"]
)

p1 = figure(
    title="Training function y1 and selected ideal y13",
    width=850,
    height=340,
    x_axis_label="x",
    y_axis_label="y",
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

p1.line(
    comparison["x"],
    comparison["y1"],
    color="navy",
    line_width=2,
    legend_label="Training y1",
)

p1.line(
    comparison["x"],
    comparison["y13"],
    color="forestgreen",
    line_width=2,
    line_dash="dashed",
    legend_label="Ideal y13",
)

p1.legend.location = "top_left"

p1_residual = figure(
    title="Training residual: y1 - y13",
    width=850,
    height=230,
    x_range=p1.x_range,
    x_axis_label="x",
    y_axis_label="Residual",
)

p1_residual.scatter(
    comparison["x"],
    comparison["residual"],
    size=4,
    alpha=0.7,
    color="navy",
)

p1_residual.line(
    comparison["x"],
    [0] * len(comparison),
    color="gray",
    line_dash="dashed",
)

save(
    column(p1, p1_residual),
    filename=str(OUTPUT / "report_figure1.html"),
    resources=INLINE,
    title="Figure 1 - Training and ideal function",
)

# ---------------------------------------------------
# FIGURE 2: Accepted observations mapped to y24
# ---------------------------------------------------

assigned = mapped[mapped["ideal_func"] == 24].copy()

assigned = assigned.merge(
    ideal[["x", "y24"]],
    on="x",
    how="left",
    validate="many_to_one",
)

assert not assigned["y24"].isna().any()
assert len(assigned) == 9
assert (
    (assigned["y"] - assigned["y24"]).abs()
    .sub(assigned["delta_y"]).abs().max() < 1e-5
)

# verified threshold for selected ideal y24.
threshold = 0.705693

p2 = figure(
    title="Ideal y24 and its accepted test observations",
    width=850,
    height=340,
    x_axis_label="x",
    y_axis_label="y",
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

p2.line(
    ideal["x"],
    ideal["y24"],
    color="forestgreen",
    line_width=2,
    legend_label="Ideal y24",
)

# actual observed y-values, not fitted
p2.scatter(
    assigned["x"],
    assigned["y"],
    color="red",
    size=10,
    legend_label="Accepted observations",
)

# connect observations to their fitted ideal vals
p2.segment(
    x0=assigned["x"],
    y0=assigned["y"],
    x1=assigned["x"],
    y1=assigned["y24"],
    line_color="black",
    line_width=2,
    line_dash="dotted",
)

p2.legend.location = "top_left"

p2_deviation = figure(
    title="Absolute deviations of accepted y24 observations",
    width=850,
    height=230,
    x_range=p2.x_range,
    y_range=Range1d(0, threshold * 1.15),
    x_axis_label="x",
    y_axis_label="Absolute deviation",
)

p2_deviation.scatter(
    assigned["x"],
    assigned["delta_y"],
    size=9,
    color="red",
    legend_label="Mapped-point deviation",
)

p2_deviation.line(
    [float(ideal["x"].min()), float(ideal["x"].max())],
    [threshold, threshold],
    color="gray",
    line_width=2,
    line_dash="dashed",
    legend_label="Acceptance threshold",
)

p2_deviation.legend.location = "top_left"

save(
    column(p2, p2_deviation),
    filename=str(OUTPUT / "report_figure2.html"),
    resources=INLINE,
    title="Figure 2 - Mapped points and deviations",
)

print("Created report_figure1.html")
print("Created report_figure2.html")

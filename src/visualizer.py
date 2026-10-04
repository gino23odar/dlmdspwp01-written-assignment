import pandas as pd

from pathlib import Path
from bokeh.layouts import column
from bokeh.plotting import (
    figure,
    output_file,
    save,
)

from src.selector import SelectionResult

class AssignmentVisualizer:
    def __init__(self, output_path: str | Path ) -> None:
        # initialize visualizer with output path for HTML file
        self.output_path = Path(output_path)

    def create(
            self,
            training_data: pd.DataFrame,
            ideal_data: pd.DataFrame,
            test_data: pd.DataFrame,
            mapped_data: pd.DataFrame,
            selections: list[SelectionResult],
    ) -> Path:
        # plot the training and ideal functions, highlighting the selected ideal functions

        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        ideal_indexed = (ideal_data.set_index("x"))

        plots = []

        for selection in selections:

            ideal_num = int(selection.ideal_func.removeprefix("y"))
            assigned = mapped_data[mapped_data["ideal_func"] == ideal_num]

            plot = figure(
                title=(
                    f"{selection.training_func} and {selection.ideal_func}"
                ),
                x_axis_label="x",
                y_axis_label="y",
                width=800,
                height=400,
            )

            plot.line(
                training_data["x"],
                training_data[selection.training_func],
                legend_label="Training Func",
                line_color="blue",
                line_width=2,
            )

            plot.line(
                ideal_data["x"],
                ideal_data[selection.ideal_func],
                legend_label="Ideal Func",
                line_color="green",
                line_width=2,
                line_dash="dashed",
            )

            plot.scatter(
                test_data["x"],
                test_data["y"],
                legend_label="Test Points",
                size=6,
                alpha=0.5,
                color="orange",
            )

            if not assigned.empty:

                ideal_y_vals = [
                    float(ideal_indexed.at[float(x_val), selection.ideal_func])
                    for x_val in assigned["x"]
                ]

                plot.scatter(
                    assigned["x"],
                    ideal_y_vals,
                    legend_label="Assigned Points",
                    size=8,
                    alpha=0.8,
                    color="red",
                )

                plot.segment(
                    x0=assigned["x"],
                    y0=assigned["y"],
                    x1=assigned["x"],
                    y1=ideal_y_vals,
                    legend_label="Deviation",
                    line_color="black",
                    line_dash="dotted",
                    alpha=0.7,
                )

            plot.legend.click_policy = "hide"

            plots.append(plot)

        output_file(self.output_path)
        save(column(*plots))

        return self.output_path
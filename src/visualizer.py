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

    def create(self, training_data: pd.DataFrame, ideal_data: pd.DataFrame, selections: list[SelectionResult]) -> Path:
        # plot the training and ideal functions, highlighting the selected ideal functions

        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        plots = []

        for selection in selections:
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

            plot.legend.click_policy = "hide"

            plots.append(plot)

        output_file(self.output_path)
        save(column(*plots))

        return self.output_path
# Copyright (c) 2023 Purvish Jajal
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import argparse
import time

import plotext as plt
from rich.ansi import AnsiDecoder
from rich.console import Group
from rich.jupyter import JupyterMixin
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

from picoboard import PicoParser


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-path", type=str, required=True, dest="log_path")
    parser.add_argument("--names", nargs="+", required=True, dest="names")
    # By default there is a 2.5 second refresh rate for the graph.
    parser.add_argument("--refresh-rate", dest="refresh_rate", default=2.5)
    args = parser.parse_args()
    return args


def data_generator(data_dict):
    data_dict = {name: val for name, val in data_dict.items() if len(val) > 0}
    for name, data in data_dict.items():
        data = list(map(lambda x: float(x["message"]), data))
        yield name, data


def create_plot(width, height, filtered_data):
    plt.clear_figure()
    for name, data in data_generator(filtered_data):
        plt.plot(data, label=name, marker="hd")
    plt.plot_size(width, height)
    return plt.build()


class plotextMixin(JupyterMixin):
    def __init__(
        self,
        filtered_data,
    ):
        self.decoder = AnsiDecoder()
        self.filtered_data = filtered_data

    def __rich_console__(self, console, options):
        self.width = options.max_width or console.width
        self.height = options.height or console.height
        canvas = create_plot(self.width, self.height, self.filtered_data)
        self.rich_canvas = Group(*self.decoder.decode(canvas))
        yield self.rich_canvas


def setup_layout():
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=1),
        Layout(name="main", ratio=1),
    )

    header = layout["header"]
    title = "picoboard :: use ctrl-c to exit."
    header.update(Text(title,style="bold cornflower_blue on black", justify="full"))

    main_layout = layout["main"]
    return layout, header, main_layout


def picoboard_cli():
    args = parse_args()
    pparser = PicoParser(args.log_path)
    filtered_data = pparser.filtered_log(args.names)

    layout, header, main_layout = setup_layout()
    main_layout.update(Panel(plotextMixin(filtered_data)))

    try:
        with Live(layout) as live:
            while True:
                time.sleep(args.refresh_rate)
                filtered_data = pparser.filtered_log(args.names)
                main_layout.update(Panel(plotextMixin(filtered_data)))
                live.refresh()
    except KeyboardInterrupt:
        rprint(Text("exiting picoboard.",style="bold red3 on black", justify="full"))

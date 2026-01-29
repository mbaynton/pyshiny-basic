from shiny import App, render, ui
import os
import pwd
from rpy2.robjects import r
from rpy2.robjects.packages import importr

rb64 = importr("base64enc")
import rpy2.robjects as robjects

app_ui = ui.page_fluid(
    ui.input_slider("n", "N slider", 0, 100, 20),
    ui.output_text_verbatim("txt"),
    ui.div(f"Linux user running user code: {pwd.getpwuid(os.getuid()).pw_name}"),
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        pi = robjects.r['pi']
        return f"n*3 is going to be {r[input.n() * 3]}, btw pi is {pi}"


app = App(app_ui, server)

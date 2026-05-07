from shiny import App, render, ui
import os
import pwd
import jwt

app_ui = ui.page_fluid(
    ui.input_slider("n", "N slider", 0, 100, 20),
    ui.output_text_verbatim("txt"),
    ui.div(f"Linux user running user code: {pwd.getpwuid(os.getuid()).pw_name}"),
    ui.output_text_verbatim("user_id"),
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"n*2 is going to be {input.n() * 2}"

    @output
    @render.text
    def user_id():
        token = session.http_conn.headers.get("posit-connect-user-session-token")
        if not token:
            return "No user session token present."
        try:
            claims = jwt.decode(token, options={"verify_signature": False})
            return f"User ID (sub): {claims.get('sub', '(sub claim not found)')}"
        except Exception as e:
            return f"Failed to decode token: {e}"


app = App(app_ui, server)

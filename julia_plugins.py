import sublime
import sublime_plugin

# TODO:
# add keybind to open source-code when you for example do "@which norm(x)"
# add GKS QtTerm back-end view below the terminal view :)
# add keybind to comment out piece of code

class WhichJuliaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        code = selected_or_code_line(self.view)

        if code:
            wrapped_code = f"@which({code})"
            send_terminus_command(wrapped_code, clear = False, center = False)

class HelpJuliaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        code = selected_or_code_line(self.view)

        if code:
            wrapped_code = f"?{code}"
            send_terminus_command(wrapped_code, clear = False, center = False)

class MethodsJuliaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        code = selected_or_code_line(self.view)

        if code:
            wrapped_code = f"methods({code})"
            send_terminus_command(wrapped_code, clear = False, center = False)

class TypeofJuliaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        code = selected_or_code_line(self.view)

        if code:
            wrapped_code = f"typeof({code})"
            send_terminus_command(wrapped_code, clear = False, center = False)

class ClearJuliaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        send_terminus_command("", enter = False)

class InstantiateJuliaCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        code = "using Pkg; Pkg.instantiate()"
        send_terminus_command(code)

def selected_or_code_line(view):
    # Check if there's a valid view
    if view is None:
        return ""

    sel = view.sel()

    # If there's no selection, get the entire line where the cursor is
    if len(sel) == 1 and sel[0].empty():
        line_region = view.line(sel[0])   
        return view.substr(line_region) 

    # Return the selected text (even if it's multi-line)
    return view.substr(sel[0]) if sel else ""

def find_terminus_sheet():
    for win in sublime.windows():
        for sheet in win.sheets():
            name = sheet.view().name()
            if name == "Login Shell" or name.startswith("Julia"):
                return sheet
    return None

def send_terminus_command(
    command,
    clear=True,
    center=True,
    enter=True,
):
    # Find terminus window
    terminal_sheet = find_terminus_sheet()
    if terminal_sheet is None:
        return
    window = terminal_sheet.window()
    view = terminal_sheet.view()
    _, col = view.rowcol(view.size()) #cursor position

    # Ammend command with various keyboard shortcuts
    full_command = "".join([
        "\x7F" * col if clear else "",  # Bad hack
        "\x0C" if center else "",  # Command + l
        command,
        "\n" if enter else "",
    ])
    window.run_command("terminus_send_string", {"string": full_command})


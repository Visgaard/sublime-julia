# Configuring Julia to work with Sublime Text 4

Lots of inspiration taken from [@PetrKryslUCSD](https://www.github.com/PetrKryslUCSD) and their configuring of Sublime Text 3 with Julia. I have made it for Sublime Text 4 and included my own plugins inspired from [@3b1b](https://github.com/3b1b/videos/tree/master/sublime_custom_commands).

## Rationale
There are many advantages of using Julia compared to other languages, many of them are listed here: [Julia Docs](https://docs.julialang.org/).

## How to get started

### Downloading Julia
Follow the instructions [here](https://julialang.org/downloads/). I personally opened a `cmd` and ran `winget install julia -s msstore`.

When it has finished, I can open `cmd` and call `julia` which should open a Julia REPL (read-eval-print loop). If you want to know where the bin directory is located, you can go to `cmd`, type `julia` to open the REPL and type `Sys.BINDIR`. Mine is located here: `"C:\\Users\\Rvisg\\.julia\\juliaup\\julia-1.11.1+0.x64.w64.mingw32\\bin"`.

Conveniently, when installing through microsoft store, [juliaup](https://github.com/JuliaLang/juliaup) is also installed to keep track of new Julia releases. Julia has also been added to the environment variables of your PC (for me, that's `C:\Users\Rvisg\AppData\Local\Microsoft\WindowsApps`, wherein `juliaup`, `julia` and a `JuliaComputingInc` folder is located), which is why we can open the REPL print like we did above. Further information on juliaup can be found in the link. 

You can now essentially begin using the Julia Programming Language with this interactive REPL and have all the fun you want :-) But we're interested in setting up a workflow with our favorite text editor and possibly dabbling in multiple projects at a time. Unlike Matlab, for Julia and other programming languages such as Python, you need to be more aware about which "environment" you are working in. In Matlab, when a friend or colleague sends a script or a function to you, you crank open Matlab and run it directly without having to install anything, provided that you use the same or a newer version of Matlab. We cannot necessarily do that in Julia. 

### Julia's Package Manager, Pkg
Pkg is designed around “environments”: independent sets of packages that can be local to an individual project or shared and selected by name. The exact set of packages and versions in an environment is captured in a `manifest` and `project` file, which can be tracked in a version control tool for improved reproducibility. 

With a Julia REPL open, type in `]` to enter the Pkg REPL. You can go back to the Julia REPL by clicking `Ctrl+D` or `backspace`. You should see something similar to this

`(@v1.11) pkg>`

The first part in parenthesis tells us which `environment` is active. Each environment may have totally different packages and versions. The active environment is what will be modified with Pkg commands. When you start a new project, you may wish to keep a seperate environment for that project. We can do this with the `activate` command followed by the name of the new environment. 

```
(@v1.11) pkg> activate MyJuliaProject
```

The Pkg prompt is now updated to reflect which environment we are working in

`(MyJuliaProject) pkg>`

#### Returning to a project
When you come back to your project after a summer hiatus, you don't need to go through the hassle of opening julia, entering the Pkg REPL and activating the environment as we did above. You can do this directly when you open Julia in the directory where the `manifest` and `project` file is.

```
julia --project=.
```

Check that the environment is active by going to the Pkg REPL `]`.

#### Using someone else's project
Suppose someone sends you a repo URL: `https://github.com/JuliaLang/Example.jl.git`. You simply `git clone` the project down and `cd` into the directory. Then `activate` and `instantiate` it

```
(@v1.10) pkg> activate Example.jl
Activating project at `~/Example.jl`

(Example) pkg> instantiate
  No Changes to `~/Example.jl/Project.toml`
  No Changes to `~/Example.jl/Manifest.toml`
``` 

The `instantiate` commands resolves the environment and installs anything missing. 

## Using Sublime Text 4 with Julia

In the following we describe how to set up the editor from scratch. Download
the editor from the website [https://www.sublimetext.com/](https://www.sublimetext.com/). 

### Installing Package Control
The first thing you would want to do is install the package **Package Control**.
Use the menu item **Tools/Command Palette** (`ctrl+shift+P`), type `install`, and an item **Install Package Control** will show up. Click this one. The **Package Control** will allow us to install other packages for Sublime Text that we need for a good workflow with Julia.

#### Packages to install
Julia: Bring up the **Command Palette**, and type **Package Control: Install Package** and select it. In the new window type `Julia`. A button named **Julia** (with the subtitle "Julia syntax highlighting for Sublime Text 4"; refer to [https://github.com/JuliaEditorSupport/Julia-sublime](https://github.com/JuliaEditorSupport/Julia-sublime)) will come up highlighted. Click on it, and the package will be installed. At this point one should be able to open a Julia source file and get it highlighted based upon the syntax of Julia.

Terminus: Install the terminal emulation package **Terminus** (https://github.com/randy3k/Terminus). This will allow us to have a terminal inside Sublime Text.

SendCode: Install the package to enable communication between a source window (like a Julia file) and the terminal, **SendCode** (https://github.com/randy3k/SendCode).

Origami: Install the package to allow for some post-window hooks that come in handy for a smoother workflow. **Origami** (https://github.com/SublimeText/Origami).

### Minimal Customization
In order to open up a Julia REPL in our text-editor, we are going to create a Build File. Go to **Tools/Build System/New Build System...**. Remove the content therein and paste below (again, thanks to [@PetrKryslUCSD](https://discourse.julialang.org/t/build-system-for-sublime-text-running-julia-in-terminus/95362)).

```
{ // This build system simply opens a new interactive Julia REPL 
    "title": "Julia REPL",
    "target": "terminus_open",
    "auto_close": false,
    "shell_cmd": "julia --project=.", 
    "cwd": "${file_path:${folder}}",
    "selector": "source.julia",   
    "post_window_hooks": [ 
       ["carry_file_to_pane", {"direction": "right"}], // Origami command
        ["focus_group", {"group": 0}] // focus on file instead of terminal
    ],
    "file_regex": "(?:[@](?:\\s\\S[\\w.]*[^@])??|in expression starting at)\\s(\\S+[.]jl):([0-9]+)"
}
```
When you save the file, it should automatically start in `~\Data\Packages\User` where you can save it with any name, for example `Julia-REPL.sublime-build`. The extension is important, so it's recognized as a build file. 

Normally, Sublime Text's Build System is used to actually build or compile files and run them. We're using it to open up an interactive Julia REPL. The `shell_cmd: "julia --project=."` tells the terminal to open julia and activate the environment if there is any present. You can just remove the `--project=.` if you just want to open the julia REPL. We can only call julia in the terminal if julia is actually on the path. That's why we downloaded `juliaup`. In addition, we tell terminal to set the working directory as the path of the .jl file you currently have open. Lastly, the `post_window_hooks` makes the terminal open in a second pane and re-focuses the .jl source file. In this way we can open a Julia REPL in the environment where our .jl is in, and start coding right away without having to use the mouse. You should be able to test this new build with the short-cut `ctrl+b` or go to **Tools/Build/** and you can choose `Julia-REPL.sublime-build`.

Now that we have our julia REPL, we have to make sure SendCode targets our Terminus terminal when we are using Julia, such that we can send commands to the terminal. Select **Preferences/Package Settings/SendCode/Settings** and in the SendCode.sublime-settings file, paste below in. The SendCode (Windows).sublime-settings window on the left are the default settings for SendCode.

```
{
    "prog": "terminus",

    "julia" : {
        "prog": "terminus",
        "bracketed_paste_mode": false
    }
}
```

In order to send code to the terminal from our .jl file, we need to add some keybinds. Go to **Preferences/Key Bindings** and in the right pane add below

```
[
    // Access to code evaluation. A current line,
    // or a selection is passed to the terminal for evaluation
    // (the command belongs to the SendCode package).
    {
        "keys": ["ctrl+keypad_enter"], 
        "command": "send_code",
        "context": [
            { 
                "key": "selector", 
                "operator": "equal", 
                "operand": "source.julia" 
            }
        ]
    },

    // Include Julia file to run entire thing
    {
        "keys": ["ctrl+shift+b"],
        "command": "send_code",
        "args": {
            "code": "include(\"$file_name\")"
        },
        "context": [
            { 
            "key": "selector", 
            "operator": "equal", 
            "operand": "source.julia" 
            }
        ]
    },

    // To make the copy and paste keys work in the Terminus window
    // (otherwise they are ctrl+shift+c, ctrl+shift+v)
    { 
        "keys": ["ctrl+c"], 
        "command": "terminus_copy",
        "context": [
            { "key": "terminus_view" },
            { "key": "terminus_view.natural_keyboard" },
            { 
                "key": "selection_empty", 
                "operator": "equal", 
                "operand": false, 
                "match_all": true 
            }
        ]
    },
    { 
        "keys": ["ctrl+v"], 
        "command": "terminus_paste",
        "context": [
            { "key": "terminus_view" },
            { "key": "terminus_view.natural_keyboard" }
        ]
    },

    // Making Julia understand alt+left and alt+right
    { 
        "keys": ["alt+left"], 
        "command": "terminus_keypress", 
        "args": {
            "key": "b", "alt": true
        }, 
        "context": [
            {
                "key": "terminus_view"
            }
        ] 
    },
    { 
        "keys": ["alt+right"], 
        "command": "terminus_keypress", 
        "args": {
            "key": "f", 
            "alt": true
        }, 
        "context": [
            {
                "key": "terminus_view"
            }
        ] 
    },
]

```

Now we can send code-lines from our .jl file directly to the julia REPL with the command `ctrl+keypad_enter` either by selecting code or hovering on a code line. We can also include the entire .jl file with the command `ctrl+shift+b` to run everything.

### Extras
If you can code in python, you can create custom plugins that allow you to do all sorts of things with Sublime Text. [@3b1b](https://github.com/3b1b/videos/tree/master/sublime_custom_commands) uses it when he creates videos with Manim. I have created my own julia commands that help my workflow. You need to create a .py file in the `Data\Packages\User` directory called `julia_plugins.py` for example. This is the place to put all your custom commands. Here is a list of mine:

```
import sublime
import sublime_plugin

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


```

And I have attached keybinds to each command in the **Preferences/Key Bindings** file:

```
[
    // Close all terminals
    { 
        "keys": ["alt+q"], 
        "command": "terminus_close_all", 
    },

    // Only close currently focused terminal
    { 
        "keys": ["alt+shift+q"], 
        "command": "terminus_close", 
        "context": [
            { 
                "key": "terminus_view" // Only for focused terminal
            } 
        ],
    },

    // Display help information
    {
        "keys": ["ctrl+h"], 
        "command": "help_julia",
        "context": [
            { 
            "key": "selector", 
            "operator": "equal", 
            "operand": "source.julia" 
            }
        ]
    },

    // Display which method
    {
        "keys": ["ctrl+w"],
        "command": "which_julia",
        "context": [
            {
            "key": "selector", 
            "operator": "equal", 
            "operand": "source.julia" 
            }
        ]
    },

    // Display all methods
    {
        "keys": ["ctrl+m"],
        "command": "methods_julia",
        "context": [
            {
            "key": "selector", 
            "operator": "equal", 
            "operand": "source.julia" 
            }
        ]
    },

    // Instantiate Project
    {
        "keys": ["ctrl+i"],
        "command": "instantiate_julia",
        "context": [
            {
            "key": "selector", 
            "operator": "equal", 
            "operand": "source.julia" 
            }
        ]
    },

    // Clear Julia REPL
    {
        "keys": ["ctrl+q"],
        "command": "clear_julia",
        "context": [
            {
            "key": "selector", 
            "operator": "equal", 
            "operand": "source.julia" 
            }
        ]
    }
]

```

Which means I can do the following quickly:

**Reset terminal by closing all and opening one again**: `alt+q` -> `ctrl+b`. Of course due to the way we set up the build system, julia will automatically activate the same environment.

**After cloning a julia project from github, activate the environment and instantiate the project**: `ctrl+b` -> `ctrl+i`

**Clear Julia REPL**: `ctrl+q`

**Check which method is being called for my code**: Highlight code -> `ctrl+m`

**Check method that would be called of function**: Highlight code -> `ctrl+w`

**Get help/documentation for anything**: Highlight code -> `ctrl+h`

## Final Remarks
Of course, you don't have to go through these steps everytime you need to setup the workflow for a new device. Just download the portable sublime text from the .zip file and get coding. :-)

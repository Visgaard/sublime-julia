# Configuring Julia to work with Sublime Text 4

## Rationale
There are many advantages of using Julia compared to other languages, many of then are listed here: [Julia Docs](https://docs.julialang.org/).

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

### Using Sublime Text 4 with Julia

In the following we describe how to set up the editor from scratch. Download
the editor from the website [https://www.sublimetext.com/](https://www.sublimetext.com/). 

#### Installing Package Control
The first thing you would want to do is install the package **Package Control**.
Use the menu item **Tools/Command Palette** (`ctrl+shift+P`), type `install`, and an item **Install Package Control** will show up. Click this one. The **Package Control** will allow us to install other packages for Sublime Text that we need for a good workflow with Julia.

##### Packages to install
==Julia== : Bring up the **Command Palette**, and type **Package Control: Install Package** and select it. In the new window type `Julia`. A button named **Julia** (with the subtitle "Julia syntax highlighting for Sublime Text 4"; refer to [https://github.com/JuliaEditorSupport/Julia-sublime](https://github.com/JuliaEditorSupport/Julia-sublime)) will come up highlighted. Click on it, and the package will be installed. At this point one should be able to open a Julia source file and get it highlighted based upon the syntax of Julia.

==Terminus== : Install the terminal emulation package **Terminus** (https://github.com/randy3k/Terminus). This will allow us to have a terminal inside Sublime Text.

==SendCode== : Install the package to enable communication between a source window (like a Julia file) and the terminal, **SendCode** (https://github.com/randy3k/SendCode).






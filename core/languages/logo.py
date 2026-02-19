# pylint: disable=W0718,R0913,R0914,R0915,C0301,C0302,W0212
"""
TW Logo Language Executor
=========================

Implements TW Logo, an educational variant of the Logo programming language
for the Time_Warp IDE, featuring turtle graphics and educational programming constructs.

Language Features:
- Turtle graphics movement: FORWARD/BACK, LEFT/RIGHT, PENUP/PENDOWN
- Drawing commands: CIRCLE, ARC, SQUARE, TRIANGLE, POLYGON
- Color control: SETPENCOLOR, SETFILLCOLOR, SETBACKGROUND
- Turtle state: SHOWTURTLE/HIDETURTLE, HOME, CLEARSCREEN
- Variable assignment and arithmetic operations
- Control structures: REPEAT, IF, WHILE loops
- Procedure definition with TO/END
- Mathematical functions: SIN, COS, TAN, SQRT, RANDOM
- List operations: FIRST, LAST, BUTFIRST, BUTLAST, ITEM
- String operations: WORD, SENTENCE, LIST operations

The executor integrates with the Time_Warp IDE's turtle graphics canvas for
visual output, providing an intuitive programming environment for learning
geometry, mathematics, and programming concepts through turtle graphics.
"""

import re
import math
import time

# pylint: disable=C0302,C0301,C0115,C0116,W0613,R0903,C0413,W0718,R0902,R0915,C0415,W0404,W0621,R0913,R0917,R0914,W0612,W0108,W0123,R0911,R0912,R1705,W0611,too-many-nested-blocks


class TwLogoExecutor:
    """Handles TW Logo language command execution"""

    def __init__(self, interpreter):
        """Initialize with reference to main interpreter"""
        self.interpreter = interpreter

    def execute_command(self, command):
        """Execute a Logo command and return the result"""
        try:
            # Filter out comments (lines starting with semicolon)
            command = command.strip()
            if command.startswith(";"):
                return "continue"

            # Handle curly-brace comments { ... }
            if command.startswith("{"):
                return "continue"
            # Strip inline curly-brace comments
            if "{" in command:
                import re as _re
                command = _re.sub(r'\{[^}]*\}', '', command).strip()
                if not command:
                    return "continue"

            parts = command.split()
            if not parts:
                return "continue"

            cmd = parts[0].upper()

            # Debug: log the command execution if debug mode enabled
            self.interpreter.debug_output(f"Executing Logo command: {cmd}")

            # Ensure turtle system exists early
            if not self.interpreter.turtle_graphics:
                self.interpreter.init_turtle_graphics()

            # Dispatch to appropriate handler
            return self._dispatch_command(cmd, parts, command)

        except Exception as e:
            self.interpreter.log_output(f"Logo error: {e}")
            return "error"

    def _dispatch_command(self, cmd, parts, command):
        """Dispatch command to appropriate handler based on command name"""
        # Macro and definition commands
        if cmd == "CALL" and len(parts) >= 2:
            return self._handle_call(parts[1])
        if cmd == "MAKE" and len(parts) >= 3:
            return self._handle_make(parts)
        if cmd == "DEFINE" and len(parts) >= 2:
            return self._handle_define(command, parts[1])

        # Control structures
        if cmd == "REPEAT":
            return self._handle_repeat(command)
        if cmd == "IF":
            return self._handle_if(command)

        # Movement command group
        result = self._handle_movement_commands(cmd, parts)
        if result is not None:
            return result

        # Pen and screen commands
        result = self._handle_pen_screen_commands(cmd, parts)
        if result is not None:
            return result

        # Color and visual commands
        result = self._handle_visual_commands(cmd, parts)
        if result is not None:
            return result

        # Drawing commands
        result = self._handle_drawing_commands(cmd, parts)
        if result is not None:
            return result

        # Advanced command groups
        result = self._handle_advanced_commands(cmd, parts)
        if result is not None:
            return result

        # User-defined procedures
        return self._handle_user_procedure(cmd, parts)

    def _handle_movement_commands(self, cmd, parts):
        """Handle movement-related commands"""
        if cmd in ["FORWARD", "FD"]:
            return self._handle_forward(parts)
        if cmd in ["BACK", "BK", "BACKWARD"]:
            return self._handle_backward(parts)
        if cmd in ["LEFT", "LT"]:
            return self._handle_left(parts)
        if cmd in ["RIGHT", "RT"]:
            return self._handle_right(parts)
        return None

    def _handle_pen_screen_commands(self, cmd, parts):
        """Handle pen control and screen commands"""
        if cmd in ["PENUP", "PU"]:
            return self._handle_penup()
        if cmd in ["PENDOWN", "PD"]:
            return self._handle_pendown()
        if cmd in ["CLEARSCREEN", "CS"]:
            return self._handle_clearscreen()
        if cmd in ["CLEARTEXT", "CT"]:
            return self._handle_cleartext()
        if cmd == "HOME":
            return self._handle_home()
        if cmd == "SETXY":
            return self._handle_setxy(parts)
        return None

    def _handle_visual_commands(self, cmd, parts):
        """Handle color and turtle visibility commands"""
        if cmd in ["SETCOLOR", "SETCOLOUR", "COLOR", "SETPENCOLOR", "SETPC"]:
            return self._handle_setcolor(parts)
        if cmd == "SETPENSIZE":
            return self._handle_setpensize(parts)
        if cmd in ["SHOWTURTLE", "ST"]:
            return self._handle_showturtle()
        if cmd in ["HIDETURTLE", "HT"]:
            return self._handle_hideturtle()
        return None

    def _handle_drawing_commands(self, cmd, parts):
        """Handle shape drawing commands"""
        if cmd == "CIRCLE":
            return self._handle_circle(parts)
        if cmd == "DOT":
            return self._handle_dot(parts)
        if cmd == "RECT":
            return self._handle_rect(parts)
        if cmd == "TEXT":
            return self._handle_text(parts)
        if cmd in ("ARC", "POLYGON", "FILL", "STAMP", "CLONE"):
            return self._handle_enhanced_turtle(cmd, parts)
        return None

    def _handle_advanced_commands(self, cmd, parts):
        """Handle advanced Logo commands"""
        # Information and utility commands
        if cmd == "PRINT":
            return self._handle_print(parts)
        if cmd == "STOP":
            return "stop"
        if cmd == "HEADING":
            return self._handle_heading()
        if cmd == "POSITION":
            return self._handle_position()
        if cmd == "TRACE":
            return self._handle_trace(parts)
        if cmd == "PROFILE":
            return self._handle_profile(parts)

        # Game, audio, and specialized commands
        if cmd.startswith("CREATE") or cmd.startswith("MOVE") or cmd.startswith("GAME"):
            return self._handle_game_commands(cmd, parts)
        if cmd.startswith("LOAD") or cmd.startswith("PLAY"):
            return self._handle_audio_commands(cmd, parts)

        # List and array operations
        if cmd in ["LIST", "FIRST", "LAST", "BUTFIRST", "BUTLAST"]:
            return self._handle_list_operations(cmd, parts)
        if cmd in ["ARRAY", "MDARRAY", "SETITEM", "MDSETITEM", "ITEM"]:
            return self._handle_array_operations(cmd, parts)

        # Math, file, sound, and 3D commands
        if cmd in ["SIN", "COS", "TAN", "SQRT", "POWER", "LOG"]:
            return self._handle_math_functions(cmd, parts)
        if cmd in ["SAVE", "LOAD", "EXPORT"]:
            return self._handle_file_operations(cmd, parts)
        if cmd in ["PLAYNOTE", "PLAYTUNE", "SETSOUND"]:
            return self._handle_sound_generation(cmd, parts)
        if cmd in ["CUBE", "SPHERE", "CYLINDER", "PYRAMID"]:
            return self._handle_3d_primitives(cmd, parts)

        # UCBLogo advanced features
        ucblogo_result = self._handle_ucblogo_features(cmd, parts)
        if ucblogo_result is not None:
            return ucblogo_result

        return None

    def _handle_ucblogo_features(self, cmd, parts):
        """Handle UCBLogo advanced features"""
        # Property list commands
        if cmd == "PPROP":
            return self._handle_pprop(parts)
        if cmd == "GPROP":
            return self._handle_gprop(parts)
        if cmd == "PLIST":
            return self._handle_plist(parts)
        if cmd == "REMPROP":
            return self._handle_remprop(parts)

        # Control structures
        control_cmds = {
            "APPLY": self._handle_apply,
            "INVOKE": self._handle_invoke,
            "FOREACH": self._handle_foreach,
            "CASCADE": self._handle_cascade,
            "CASE": self._handle_case,
            "COND": self._handle_cond,
            "WHILE": self._handle_while,
            "UNTIL": self._handle_until,
            "DO.WHILE": self._handle_do_while,
            "DO.UNTIL": self._handle_do_until,
            "FOR": self._handle_for,
        }
        if cmd in control_cmds:
            return control_cmds[cmd](parts)

        # Turtle commands
        if cmd == "SETHEADING":
            return self._handle_setheading(parts)
        if cmd == "TOWARDS":
            return self._handle_towards(parts)
        if cmd == "SCRUNCH":
            return self._handle_scrunch(parts)

        # Error handling
        if cmd == "ERRACT":
            return self._handle_erract(parts)
        if cmd == "ERROR":
            return self._handle_error(parts)

        # Bitwise operations
        bitwise_cmds = ["BITAND", "BITOR", "BITXOR", "BITNOT", "ASHIFT", "LSHIFT"]
        if cmd in bitwise_cmds:
            return self._handle_bitwise(cmd, parts)

        # Macros
        if cmd == ".MACRO":
            return self._handle_macro_define(parts)
        if cmd == ".DEFMACRO":
            return self._handle_defmacro(parts)

        return None

    def _handle_user_procedure(self, cmd, parts):
        """Handle user-defined procedure calls"""
        if cmd in self.interpreter.logo_procedures:
            self.interpreter.debug_output(f"Calling procedure: {cmd}")
            params, _ = self.interpreter.logo_procedures[cmd]
            args = self._collect_procedure_args(parts, len(params))
            return self._call_logo_procedure(cmd, args)

        # Try case-insensitive lookup
        cmd_upper = cmd.upper()
        if cmd_upper in self.interpreter.logo_procedures:
            self.interpreter.debug_output(f"Calling procedure: {cmd_upper}")
            params, _ = self.interpreter.logo_procedures[cmd_upper]
            args = self._collect_procedure_args(parts, len(params))
            return self._call_logo_procedure(cmd_upper, args)

        self.interpreter.log_output(f"Unknown Logo command: {cmd}")
        return None

    def _collect_procedure_args(self, parts, num_params):
        """Collect arguments for a procedure call"""
        args = []
        idx = 1
        for _ in range(num_params):
            arg_tokens = []
            while idx < len(parts):
                token = parts[idx]
                if arg_tokens and (token.startswith(":") or not token[0].isalpha()):
                    break
                arg_tokens.append(token)
                idx += 1
            if arg_tokens:
                args.append(" ".join(arg_tokens))
        return args

    def _handle_array_operations(self, cmd, parts):
        """Handle array-related operations"""
        if cmd == "ARRAY":
            return self._handle_array(parts)
        if cmd == "MDARRAY":
            return self._handle_mdarray(parts)
        if cmd == "SETITEM":
            return self._handle_setitem(parts)
        if cmd == "MDSETITEM":
            return self._handle_mdsetitem(parts)
        if cmd == "ITEM":
            return self._handle_item(parts)
        return None

    def _handle_call(self, name):
        """Handle macro CALL"""
        if name not in self.interpreter.macros:
            self.interpreter.log_output(f"Unknown macro: {name}")
            return "continue"
        if name in self.interpreter._macro_call_stack:
            self.interpreter.log_output(f"Macro recursion detected: {name}")
            return "continue"
        if len(self.interpreter._macro_call_stack) > 16:
            self.interpreter.log_output("Macro call depth limit exceeded")
            return "continue"

        self.interpreter._macro_call_stack.append(name)
        try:
            for mline in self.interpreter.macros[name]:
                if not self.interpreter.turtle_graphics:
                    self.interpreter.init_turtle_graphics()
                self.execute_command(mline)
        finally:
            self.interpreter._macro_call_stack.pop()
        return "continue"

    def _handle_make(self, parts):
        """Handle MAKE command for variable assignment
        MAKE "VARNAME value or MAKE "VARNAME :expression
        """
        if len(parts) < 3:
            return "continue"

        var_name = parts[1].strip('"').upper()
        value_expr = ' '.join(parts[2:])

        self.interpreter.debug_output(f"MAKE: var={var_name}, expr='{value_expr}'")

        try:
            # Evaluate the value expression (handles :VARS, literals, math)
            value = self._eval_argument(value_expr)
            self.interpreter.variables[var_name] = value
            self.interpreter.debug_output(f"MAKE {var_name} = {value}")
        except Exception as e:
            self.interpreter.debug_output(f"MAKE error: {e}")
            self.interpreter.log_output(f"Error in MAKE: {e}")

        return "continue"

    def _handle_define(self, command, name):
        """Handle DEFINE macro"""
        bracket_index = command.find("[")
        if bracket_index == -1:
            self.interpreter.log_output("Malformed DEFINE (missing [)")
            return "continue"
        block, ok = self._extract_bracket_block(command[bracket_index:])
        if not ok:
            self.interpreter.log_output("Malformed DEFINE (unmatched ] )")
            return "continue"
        inner = block[1:-1].strip()
        subcommands = self._split_top_level_commands(inner)
        self.interpreter.macros[name] = subcommands
        self.interpreter.log_output(
            f"Macro '{name}' defined ({len(subcommands)} commands)"
        )
        return "continue"

    def _handle_repeat(self, command):
        """Handle REPEAT command with support for multi-line syntax"""
        # Preprocess multi-line REPEAT blocks by joining lines
        command_lines = command.strip().split("\n")

        if len(command_lines) > 1:
            # Multi-line format - join into single line
            processed_command = ""
            bracket_depth = 0
            for line in command_lines:
                line = line.strip()
                if not line or line.startswith(";"):  # Skip empty and comment lines
                    continue

                # Track bracket depth
                bracket_depth += line.count("[") - line.count("]")

                # Add line to processed command
                if processed_command:
                    processed_command += " " + line
                else:
                    processed_command = line

                # If brackets are balanced, we have complete command
                if bracket_depth == 0 and "[" in processed_command:
                    break

            command = processed_command

        parsed = self._parse_repeat_nested(command.strip())
        if not parsed:
            self.interpreter.log_output("Malformed REPEAT syntax or unmatched brackets")
            return "continue"
        count, subcommands = parsed

        guard = 0
        for _ in range(count):
            for sub in subcommands:
                guard += 1
                if guard > 5000:
                    self.interpreter.log_output("REPEAT aborted: expansion too large")
                    return "continue"
                result = self.execute_command(sub)
                if result == "stop":
                    return "stop"
        return "continue"

    def _handle_if(self, command):
        """Handle IF conditional command: IF condition [commands]"""
        import re

        # Parse: IF condition [commands]
        match = re.match(r"IF\s+(.+?)\s*\[(.+)\]", command, re.IGNORECASE | re.DOTALL)
        if not match:
            self.interpreter.log_output(
                "Malformed IF syntax. Use: IF condition [commands]"
            )
            return "continue"

        condition_str = match.group(1).strip()
        commands_str = match.group(2).strip()

        # Evaluate condition
        try:
            # Replace :VAR with variable values
            def replace_var(m):
                var_name = m.group(1).upper()
                return str(self.interpreter.variables.get(var_name, 0))

            condition_eval = re.sub(r":(\w+)", replace_var, condition_str)

            # Evaluate the condition
            result = eval(condition_eval, {"__builtins__": {}}, {})

            # If condition is true, execute commands
            if result:
                # Execute each command from the block (separated by newlines)
                for cmd_line in commands_str.strip().split("\n"):
                    cmd_line = cmd_line.strip()
                    if cmd_line and not cmd_line.startswith(";"):
                        result_cmd = self.execute_command(cmd_line)
                        if result_cmd == "stop":
                            return "stop"

        except Exception as e:
            self.interpreter.log_output(f"IF condition error: {e}")

        return "continue"

    def _execute_command_block(self, block_str):
        """Execute a block of Logo commands from IF/REPEAT blocks"""
        # Split block into individual commands, respecting multi-word commands
        block_str = block_str.strip()
        commands = []
        current_cmd = []

        for token in block_str.split():
            # Recognize command keywords to know when a new command starts
            if (
                token.upper()
                in [
                    "FORWARD",
                    "FD",
                    "BACK",
                    "BK",
                    "BACKWARD",
                    "LEFT",
                    "LT",
                    "RIGHT",
                    "RT",
                    "REPEAT",
                    "IF",
                    "PENUP",
                    "PU",
                    "PENDOWN",
                    "PD",
                    "SETPENCOLOR",
                    "SETCOLOR",
                    "SETXY",
                    "CIRCLE",
                    "ARC",
                    "SQUARE",
                    "CLEARSCREEN",
                    "CS",
                    "HOME",
                    "SHOWTURTLE",
                    "HIDETURTLE",
                    "SETHEADING",
                    "SETH",
                ]
                and current_cmd
            ):
                # New command starts, save previous one
                commands.append(" ".join(current_cmd))
                current_cmd = [token]
            else:
                current_cmd.append(token)

        # Don't forget last command
        if current_cmd:
            commands.append(" ".join(current_cmd))

        # Execute each command
        for cmd in commands:
            if cmd.strip():
                result = self.execute_command(cmd.strip())
                if result == "stop":
                    return "stop"

    def _eval_argument(self, arg):
        """Evaluate an argument which could be a variable, number, or expression"""
        import re

        arg = str(arg).strip()

        # Check if it's a simple variable reference (just :VARNAME with no operators)
        if arg.startswith(":") and re.match(r'^:\w+$', arg):
            var_name = arg[1:].upper()
            value = self.interpreter.variables.get(var_name, 0)
            self.interpreter.debug_output(f"_eval_argument: :{var_name} -> {value}")
            return value

        # Otherwise try to evaluate as expression (may contain :VARS, operators, numbers)
        try:
            # Replace any :VARS in the expression
            def replace_var(m):
                var_name = m.group(1).upper()
                val = self.interpreter.variables.get(var_name, 0)
                self.interpreter.debug_output(f"_eval_argument: replacing :{var_name} with {val}")
                return str(val)

            expr_str = re.sub(r":(\w+)", replace_var, arg)
            self.interpreter.debug_output(f"_eval_argument: '{arg}' -> '{expr_str}'")
            result = eval(expr_str, {"__builtins__": {}}, {})
            self.interpreter.debug_output(f"_eval_argument: eval result = {result}")
            return float(result)
        except Exception as e:
            self.interpreter.debug_output(f"_eval_argument: exception {e}")
            try:
                return float(arg)
            except (ValueError, TypeError):
                return arg

    def _handle_forward(self, parts):
        """Handle FORWARD command"""
        try:
            # Get distance, evaluating variables if needed
            distance_arg = parts[1] if len(parts) > 1 else "50.0"
            distance = self._eval_argument(distance_arg)
        except Exception:
            distance = 50.0

        if not self.interpreter.turtle_graphics:
            self.interpreter.init_turtle_graphics()
        self.interpreter.turtle_forward(distance)
        self.interpreter.debug_output(f"Turtle moved forward {distance} units")
        self.interpreter.log_output("Turtle moved")

        if self.interpreter.turtle_trace:
            self.interpreter.log_output(
                f"TRACE: POS=({self.interpreter.turtle_graphics['x']:.1f},{self.interpreter.turtle_graphics['y']:.1f}) HEADING={self.interpreter.turtle_graphics['heading']:.1f}° PEN={'DOWN' if self.interpreter.turtle_graphics['pen_down'] else 'UP'}"
            )

        # Set turtle position variables for testing
        self.interpreter.variables["TURTLE_X"] = self.interpreter.turtle_graphics["x"]
        self.interpreter.variables["TURTLE_Y"] = self.interpreter.turtle_graphics["y"]
        self.interpreter.variables["TURTLE_HEADING"] = self.interpreter.turtle_graphics[
            "heading"
        ]

        return "continue"

    def _handle_backward(self, parts):
        """Handle BACK/BACKWARD command"""
        try:
            distance_arg = parts[1] if len(parts) > 1 else "50.0"
            distance = self._eval_argument(distance_arg)
        except Exception:
            distance = 50.0
        self.interpreter.turtle_forward(-distance)  # Move backward
        self.interpreter.debug_output(f"Turtle moved backward {distance} units")
        if self.interpreter.turtle_trace:
            self.interpreter.log_output(
                f"TRACE: POS=({self.interpreter.turtle_graphics['x']:.1f},{self.interpreter.turtle_graphics['y']:.1f}) HEADING={self.interpreter.turtle_graphics['heading']:.1f}° PEN={'DOWN' if self.interpreter.turtle_graphics['pen_down'] else 'UP'}"
            )
        # Set turtle position variables for testing
        self.interpreter.variables["TURTLE_X"] = self.interpreter.turtle_graphics["x"]
        self.interpreter.variables["TURTLE_Y"] = self.interpreter.turtle_graphics["y"]
        self.interpreter.variables["TURTLE_HEADING"] = self.interpreter.turtle_graphics[
            "heading"
        ]
        return "continue"

    def _handle_left(self, parts):
        """Handle LEFT command"""
        try:
            angle_arg = parts[1] if len(parts) > 1 else "90"
            angle = self._eval_argument(angle_arg)
        except Exception:
            angle = 90
        self.interpreter.turtle_turn(-angle)  # Negative angle for LEFT (counter-clockwise)
        self.interpreter.log_output(
            f"Turtle turned left {angle} degrees (heading={self.interpreter.turtle_graphics['heading']})"
        )
        if self.interpreter.turtle_trace:
            self.interpreter.log_output(
                f"TRACE: POS=({self.interpreter.turtle_graphics['x']:.1f},{self.interpreter.turtle_graphics['y']:.1f}) HEADING={self.interpreter.turtle_graphics['heading']:.1f}° PEN={'DOWN' if self.interpreter.turtle_graphics['pen_down'] else 'UP'}"
            )
        # Set turtle position variables for testing
        self.interpreter.variables["TURTLE_X"] = self.interpreter.turtle_graphics["x"]
        self.interpreter.variables["TURTLE_Y"] = self.interpreter.turtle_graphics["y"]
        self.interpreter.variables["TURTLE_HEADING"] = self.interpreter.turtle_graphics[
            "heading"
        ]
        return "continue"

    def _handle_right(self, parts):
        """Handle RIGHT command"""
        try:
            angle_arg = parts[1] if len(parts) > 1 else "90"
            angle = self._eval_argument(angle_arg)
        except Exception:
            angle = 90

        if not self.interpreter.turtle_graphics:
            self.interpreter.init_turtle_graphics()
        # Use positive angle for RIGHT to match test expectations
        self.interpreter.turtle_turn(angle)
        self.interpreter.log_output(
            f"Turtle turned right {angle} degrees (heading={self.interpreter.turtle_graphics['heading']})"
        )
        if self.interpreter.turtle_trace:
            self.interpreter.log_output(
                f"TRACE: POS=({self.interpreter.turtle_graphics['x']:.1f},{self.interpreter.turtle_graphics['y']:.1f}) HEADING={self.interpreter.turtle_graphics['heading']:.1f}° PEN={'DOWN' if self.interpreter.turtle_graphics['pen_down'] else 'UP'}"
            )
        # Set turtle position variables for testing
        self.interpreter.variables["TURTLE_X"] = self.interpreter.turtle_graphics["x"]
        self.interpreter.variables["TURTLE_Y"] = self.interpreter.turtle_graphics["y"]
        self.interpreter.variables["TURTLE_HEADING"] = self.interpreter.turtle_graphics[
            "heading"
        ]
        return "continue"

    def _handle_penup(self):
        """Handle PENUP command"""
        self.interpreter.turtle_graphics["pen_down"] = False
        self.interpreter.log_output("Pen up - turtle will move without drawing")
        if self.interpreter.turtle_trace:
            self.interpreter.log_output("TRACE: PEN=UP")
        return "continue"

    def _handle_pendown(self):
        """Handle PENDOWN command"""
        prev_state = self.interpreter.turtle_graphics["pen_down"]
        self.interpreter.turtle_graphics["pen_down"] = True
        # If transitioning from up to down,
        # advance color for new shape for visibility
        if not prev_state:
            self.interpreter._turtle_color_index = (
                self.interpreter._turtle_color_index + 1
            ) % len(self.interpreter._turtle_color_palette)
            self.interpreter.turtle_graphics["pen_color"] = (
                self.interpreter._turtle_color_palette[
                    self.interpreter._turtle_color_index
                ]
            )
        self.interpreter.log_output("Pen down - turtle will draw when moving")
        if self.interpreter.turtle_trace:
            self.interpreter.log_output(
                f"TRACE: PEN=DOWN COLOR={self.interpreter.turtle_graphics['pen_color']}"
            )
        return "continue"

    def _handle_clearscreen(self):
        """Handle CLEARSCREEN command"""
        self.interpreter.clear_turtle_screen()
        self.interpreter.log_output("Screen cleared")
        return "continue"

    def _handle_cleartext(self):
        """Handle CLEARTEXT command - clears text output area"""
        # Clear the output widget
        if (
            hasattr(self.interpreter, "output_widget")
            and self.interpreter.output_widget
        ):
            try:
                self.interpreter.output_widget.delete("1.0", "end")
            except Exception:
                pass
        self.interpreter.log_output("Text output cleared")
        return "continue"

    def _handle_home(self):
        """Handle HOME command"""
        self.interpreter.turtle_home()
        self.interpreter.log_output("Turtle returned to home position")
        # Set turtle position variables for testing
        self.interpreter.variables["TURTLE_X"] = self.interpreter.turtle_graphics["x"]
        self.interpreter.variables["TURTLE_Y"] = self.interpreter.turtle_graphics["y"]
        self.interpreter.variables["TURTLE_HEADING"] = self.interpreter.turtle_graphics[
            "heading"
        ]
        return "continue"

    def _handle_setxy(self, parts):
        """Handle SETXY command"""
        if len(parts) >= 3:
            x = float(parts[1])
            y = float(parts[2])
            self.interpreter.turtle_setxy(x, y)
            self.interpreter.log_output(f"SETXY -> Turtle moved to position ({x}, {y})")
        else:
            self.interpreter.log_output("SETXY requires X and Y coordinates")
        # Set turtle position variables for testing
        self.interpreter.variables["TURTLE_X"] = self.interpreter.turtle_graphics["x"]
        self.interpreter.variables["TURTLE_Y"] = self.interpreter.turtle_graphics["y"]
        self.interpreter.variables["TURTLE_HEADING"] = self.interpreter.turtle_graphics[
            "heading"
        ]
        return "continue"

    def _handle_setcolor(self, parts):
        """Handle SETCOLOR/COLOR/SETPENCOLOR command

        Supported formats:
            SETPENCOLOR [R G B]      - bracketed RGB list
            SETPENCOLOR R G B        - space-separated RGB values
            SETPENCOLOR colorname    - named color (red, blue, etc.)
            SETPENCOLOR #RRGGBB      - hex color code
        """
        if len(parts) < 2:
            self.interpreter.log_output("Color command requires a color parameter")
            return "continue"

        # Check if it's an RGB list [R G B]
        command_str = " ".join(parts[1:])
        if "[" in command_str and "]" in command_str:
            # Parse bracketed RGB list
            try:
                import re
                match = re.search(r'\[\s*(\d+)\s+(\d+)\s+(\d+)\s*\]', command_str)
                if match:
                    r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    self.interpreter.turtle_set_color(color)
                    self.interpreter.log_output(f"Pen color set to RGB({r}, {g}, {b})")
                else:
                    self.interpreter.log_output("Invalid RGB format. Use [R G B] or R G B")
            except Exception as e:
                self.interpreter.debug_output(f"Color parsing error: {e}")
                self.interpreter.log_output("Invalid color format")
        elif len(parts) >= 4:
            # Space-separated RGB values: SETPENCOLOR R G B
            try:
                r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                color = f"#{r:02x}{g:02x}{b:02x}"
                self.interpreter.turtle_set_color(color)
                self.interpreter.log_output(f"Pen color set to RGB({r}, {g}, {b})")
            except (ValueError, IndexError):
                # Not numeric — fall through to named color
                color = parts[1].lower()
                self.interpreter.turtle_set_color(color)
                self.interpreter.log_output(f"Pen color set to {color}")
        else:
            # Named color or hex
            color = parts[1].lower()
            self.interpreter.turtle_set_color(color)
            self.interpreter.log_output(f"Pen color set to {color}")
        return "continue"

    def _handle_setpensize(self, parts):
        """Handle SETPENSIZE command"""
        size = int(parts[1]) if len(parts) > 1 else 1
        self.interpreter.turtle_set_pen_size(size)
        self.interpreter.log_output(f"Pen size set to {size}")
        return "continue"

    def _handle_circle(self, parts):
        """Handle CIRCLE command"""
        radius = float(parts[1]) if len(parts) > 1 else 50
        self.interpreter.turtle_circle(radius)
        self.interpreter.log_output(f"Drew circle with radius {radius}")
        return "continue"

    def _handle_dot(self, parts):
        """Handle DOT command"""
        size = int(parts[1]) if len(parts) > 1 else 5
        self.interpreter.turtle_dot(size)
        self.interpreter.log_output(f"Drew dot with size {size}")
        return "continue"

    def _handle_rect(self, parts):
        """Handle RECT command"""
        if len(parts) >= 3:
            width = float(parts[1])
            height = float(parts[2])
            self.interpreter.turtle_rect(width, height)
            self.interpreter.log_output(f"Drew rectangle {width}x{height}")
        else:
            self.interpreter.log_output("RECT requires width and height")
        return "continue"

    def _handle_text(self, parts):
        """Handle TEXT command"""
        if len(parts) > 1:
            text = " ".join(parts[1:])
            # Remove quotes if present
            if text.startswith('"') and text.endswith('"'):
                text = text[1:-1]
            self.interpreter.turtle_text(text)
            self.interpreter.log_output(f"Drew text: {text}")
        else:
            self.interpreter.log_output("TEXT requires text content")
        return "continue"

    def _handle_showturtle(self):
        """Handle SHOWTURTLE command"""
        self.interpreter.turtle_graphics["visible"] = True
        self.interpreter.update_turtle_display()
        self.interpreter.log_output("Turtle is now visible")
        return "continue"

    def _handle_hideturtle(self):
        """Handle HIDETURTLE command"""
        self.interpreter.turtle_graphics["visible"] = False
        self.interpreter.update_turtle_display()
        self.interpreter.log_output("Turtle is now hidden")
        return "continue"

    def _handle_print(self, parts):
        """Handle PRINT command - outputs text to the text output area"""
        if len(parts) < 2:
            self.interpreter.log_output("PRINT requires text to output")
            return "continue"

        # Join all parts after PRINT, handle [brackets] for word lists
        text = " ".join(parts[1:])

        # Remove brackets if present
        if text.startswith("[") and text.endswith("]"):
            text = text[1:-1]

        self.interpreter.log_output(text)
        return "continue"

    def _handle_heading(self):
        """Handle HEADING command"""
        heading = self.interpreter.turtle_graphics["heading"]
        self.interpreter.log_output(f"Turtle heading: {heading} degrees")
        return "continue"

    def _handle_position(self):
        """Handle POSITION command"""
        x, y = (
            self.interpreter.turtle_graphics["x"],
            self.interpreter.turtle_graphics["y"],
        )
        self.interpreter.log_output(f"Turtle position: ({x:.1f}, {y:.1f})")
        return "continue"

    def _handle_trace(self, parts):
        """Handle TRACE command"""
        if len(parts) > 1:
            state = parts[1].upper()
            if state in ("ON", "TRUE", "1"):
                self.interpreter.turtle_trace = True
                self.interpreter.log_output("Turtle trace enabled")
            elif state in ("OFF", "FALSE", "0"):
                self.interpreter.turtle_trace = False
                self.interpreter.log_output("Turtle trace disabled")
        else:
            self.interpreter.turtle_trace = not self.interpreter.turtle_trace
            self.interpreter.log_output(
                f"Turtle trace {'enabled' if self.interpreter.turtle_trace else 'disabled'}"
            )
        return "continue"

    def _handle_profile(self, parts):
        """Handle PROFILE command"""
        action = parts[1].upper() if len(parts) > 1 else "REPORT"
        if action == "ON":
            self.interpreter.profile_enabled = True
            self.interpreter.profile_stats = {}
            self.interpreter.log_output("Profiling enabled")
        elif action == "OFF":
            self.interpreter.profile_enabled = False
            self.interpreter.log_output("Profiling disabled")
        elif action == "RESET":
            self.interpreter.profile_stats = {}
            self.interpreter.log_output("Profiling data reset")
        elif action == "REPORT":
            if not self.interpreter.profile_stats:
                self.interpreter.log_output("No profiling data")
            else:
                self.interpreter.log_output(
                    "PROFILE REPORT (command  count   avg(ms)   max(ms)  total(ms)):"
                )
                for k, v in sorted(
                    self.interpreter.profile_stats.items(),
                    key=lambda kv: kv[1]["total"],
                    reverse=True,
                ):
                    avg = (v["total"] / v["count"]) if v["count"] else 0.0
                    self.interpreter.log_output(
                        f"  {k:<12} {v['count']:>5} {avg*1000:>9.3f} {v['max']*1000:>9.3f} {v['total']*1000:>10.3f}"
                    )
        else:
            self.interpreter.log_output("PROFILE expects ON|OFF|RESET|REPORT")
        return "continue"

    def _handle_game_commands(self, cmd, parts):
        """Handle game commands in Logo style"""
        self.interpreter.log_output(f"Game command: {cmd} {' '.join(parts[1:])}")
        return "continue"

    def _handle_audio_commands(self, cmd, parts):
        """Handle audio commands in Logo style"""
        self.interpreter.log_output(f"Audio command: {cmd} {' '.join(parts[1:])}")
        return "continue"

    def _handle_enhanced_turtle(self, cmd, parts):
        """Handle enhanced turtle graphics commands"""
        try:
            if cmd == "ARC":
                # ARC radius, angle [,steps]
                if len(parts) >= 2:
                    radius = float(parts[1])
                    angle = float(parts[2]) if len(parts) > 2 else 360
                    steps = int(parts[3]) if len(parts) > 3 else 36

                    # Draw an arc by moving in small steps
                    step_angle = angle / steps
                    step_size = (2 * math.pi * radius * step_angle) / 360

                    for _ in range(steps):
                        self.interpreter.turtle_forward(step_size)
                        self.interpreter.turtle_turn(step_angle)

                    self.interpreter.log_output(
                        f"Drew arc with radius {radius}, angle {angle}°"
                    )

            elif cmd == "POLYGON":
                # POLYGON sides, size [,angle]
                if len(parts) >= 3:
                    sides = int(parts[1])
                    size = float(parts[2])
                    angle = float(parts[3]) if len(parts) > 3 else 0

                    if sides >= 3:
                        # Turn to starting angle
                        if angle != 0:
                            self.interpreter.turtle_turn(angle)

                        # Draw the polygon
                        exterior_angle = 360 / sides
                        for _ in range(sides):
                            self.interpreter.turtle_forward(size)
                            self.interpreter.turtle_turn(exterior_angle)

                        self.interpreter.log_output(
                            f"Drew {sides}-sided polygon with side length {size}"
                        )
                    else:
                        self.interpreter.log_output(
                            "Polygon must have at least 3 sides"
                        )

            elif cmd == "FILL":
                # FILL - flood fill current area with current color
                # This is a simplified implementation - just
                # draw a filled circle at current position
                current_color = self.interpreter.turtle_graphics.get(
                    "pen_color", "black"
                )
                if (
                    hasattr(self.interpreter, "ide_turtle_canvas")
                    and self.interpreter.ide_turtle_canvas
                ):
                    canvas = self.interpreter.ide_turtle_canvas
                    x = self.interpreter.turtle_graphics["x"]
                    y = self.interpreter.turtle_graphics["y"]
                    # Draw a filled circle to simulate flood fill
                    canvas.create_oval(
                        x - 20,
                        y - 20,
                        x + 20,
                        y + 20,
                        fill=current_color,
                        outline=current_color,
                        tags="game_objects",
                    )
                    self.interpreter.log_output(
                        f"Flood filled area at ({x:.1f}, {y:.1f}) with {current_color}"
                    )
                else:
                    self.interpreter.log_output("FILL command requires graphics canvas")

            elif cmd == "CLONE":
                # CLONE - create a copy of the turtle at current position
                # This would create a visual clone - simplified implementation
                current_x = self.interpreter.turtle_graphics["x"]
                current_y = self.interpreter.turtle_graphics["y"]
                current_heading = self.interpreter.turtle_graphics["heading"]

                # Store clone information
                if not hasattr(self.interpreter, "turtle_clones"):
                    self.interpreter.turtle_clones = []

                clone_info = {
                    "x": current_x,
                    "y": current_y,
                    "heading": current_heading,
                    "color": self.interpreter.turtle_graphics.get("pen_color", "black"),
                    "visible": True,
                }
                self.interpreter.turtle_clones.append(clone_info)

                self.interpreter.log_output(
                    f"Created turtle clone at ({current_x:.1f}, {current_y:.1f})"
                )

            elif cmd == "STAMP":
                # STAMP - leave an imprint of the turtle shape
                current_x = self.interpreter.turtle_graphics["x"]
                current_y = self.interpreter.turtle_graphics["y"]
                current_color = self.interpreter.turtle_graphics.get(
                    "pen_color", "black"
                )

                if (
                    hasattr(self.interpreter, "ide_turtle_canvas")
                    and self.interpreter.ide_turtle_canvas
                ):
                    canvas = self.interpreter.ide_turtle_canvas
                    # Draw a small triangle to represent turtle stamp
                    size = 8
                    canvas.create_polygon(
                        current_x,
                        current_y - size,
                        current_x - size // 2,
                        current_y + size // 2,
                        current_x + size // 2,
                        current_y + size // 2,
                        fill=current_color,
                        outline=current_color,
                        tags="game_objects",
                    )
                    self.interpreter.log_output(
                        f"Stamped turtle at ({current_x:.1f}, {current_y:.1f})"
                    )
                else:
                    self.interpreter.log_output(
                        "STAMP command requires graphics canvas"
                    )

        except Exception as e:
            self.interpreter.debug_output(f"Enhanced turtle command error: {e}")
        return "continue"

    def _handle_math_functions(self, cmd, parts):
        """Handle mathematical functions in Logo"""
        try:
            if cmd == "SIN":
                # SIN angle - sine of angle in degrees
                if len(parts) >= 2:
                    angle = float(parts[1])
                    result = math.sin(math.radians(angle))
                    self.interpreter.variables["MATH_RESULT"] = result
                    self.interpreter.log_output(f"SIN {angle}° = {result:.4f}")

            elif cmd == "COS":
                # COS angle - cosine of angle in degrees
                if len(parts) >= 2:
                    angle = float(parts[1])
                    result = math.cos(math.radians(angle))
                    self.interpreter.variables["MATH_RESULT"] = result
                    self.interpreter.log_output(f"COS {angle}° = {result:.4f}")

            elif cmd == "TAN":
                # TAN angle - tangent of angle in degrees
                if len(parts) >= 2:
                    angle = float(parts[1])
                    result = math.tan(math.radians(angle))
                    self.interpreter.variables["MATH_RESULT"] = result
                    self.interpreter.log_output(f"TAN {angle}° = {result:.4f}")

            elif cmd == "SQRT":
                # SQRT value - square root
                if len(parts) >= 2:
                    value = float(parts[1])
                    if value >= 0:
                        result = math.sqrt(value)
                        self.interpreter.variables["MATH_RESULT"] = result
                        self.interpreter.log_output(f"SQRT {value} = {result:.4f}")
                    else:
                        self.interpreter.log_output("SQRT requires non-negative value")

            elif cmd == "POWER":
                # POWER base, exponent
                if len(parts) >= 3:
                    base = float(parts[1])
                    exponent = float(parts[2])
                    result = math.pow(base, exponent)
                    self.interpreter.variables["MATH_RESULT"] = result
                    self.interpreter.log_output(
                        f"POWER {base} {exponent} = {result:.4f}"
                    )

            elif cmd == "LOG":
                # LOG value [,base] - logarithm (default base 10)
                if len(parts) >= 2:
                    value = float(parts[1])
                    base = float(parts[2]) if len(parts) > 2 else 10
                    if value > 0 and base > 0 and base != 1:
                        result = math.log(value, base)
                        self.interpreter.variables["MATH_RESULT"] = result
                        self.interpreter.log_output(
                            f"LOG {value} {base} = {result:.4f}"
                        )
                    else:
                        self.interpreter.log_output(
                            "LOG requires positive value and valid base"
                        )

        except Exception as e:
            self.interpreter.debug_output(f"Math function error: {e}")
        return "continue"

    def _handle_list_operations(self, cmd, parts):
        """Handle list processing operations in Logo"""
        try:
            if cmd == "LIST":
                return self._handle_list_creation(parts)

            # All list access operations
            result = self._handle_list_access(cmd, parts)
            if result:
                return result

        except Exception as e:
            self.interpreter.debug_output(f"List operation error: {e}")
        return "continue"

    def _handle_list_creation(self, parts):
        """Create a new list from parts"""
        if len(parts) >= 2:
            items = []
            for part in parts[1:]:
                try:
                    items.append(float(part))
                except ValueError:
                    items.append(part.strip('"'))

            list_name = f"LIST_{len(self.interpreter.variables)}"
            self.interpreter.variables[list_name] = items
            self.interpreter.log_output(
                f"Created list {list_name} with {len(items)} items"
            )
            self.interpreter.variables["LAST_LIST"] = list_name
        return "continue"

    def _handle_list_access(self, cmd, parts):
        """Handle list access operations (ITEM, FIRST, LAST, BUTFIRST, BUTLAST)"""
        if cmd not in ["ITEM", "FIRST", "LAST", "BUTFIRST", "BUTLAST"]:
            return None

        list_name = (
            parts[1]
            if len(parts) > 1
            else self.interpreter.variables.get("LAST_LIST")
        )

        if not list_name or list_name not in self.interpreter.variables:
            self.interpreter.log_output("No list available")
            return "continue"

        lst = self.interpreter.variables[list_name]
        if not isinstance(lst, list) or not lst:
            self.interpreter.log_output("Invalid or empty list")
            return "continue"

        # Dispatch to specific operation handler
        if cmd == "ITEM":
            self._list_item_operation(parts, list_name, lst)
        elif cmd == "FIRST":
            self._list_first_operation(list_name, lst)
        elif cmd == "LAST":
            self._list_last_operation(list_name, lst)
        elif cmd == "BUTFIRST":
            self._list_butfirst_operation(list_name, lst)
        elif cmd == "BUTLAST":
            self._list_butlast_operation(list_name, lst)

        return "continue"

    def _list_item_operation(self, parts, list_name, lst):
        """Handle ITEM index list operation"""
        if len(parts) >= 3:
            try:
                index = int(parts[1]) - 1
                list_name = parts[2]
                if list_name in self.interpreter.variables:
                    lst = self.interpreter.variables[list_name]
                    if isinstance(lst, list) and 0 <= index < len(lst):
                        result = lst[index]
                        self.interpreter.variables["LIST_RESULT"] = result
                        self.interpreter.log_output(
                            f"ITEM {index+1} of {list_name} = {result}"
                        )
                    else:
                        self.interpreter.log_output("Invalid index or list")
            except ValueError:
                self.interpreter.log_output("ITEM requires numeric index")

    def _list_first_operation(self, list_name, lst):
        """Handle FIRST operation"""
        result = lst[0]
        self.interpreter.variables["LIST_RESULT"] = result
        self.interpreter.log_output(f"FIRST of {list_name} = {result}")

    def _list_last_operation(self, list_name, lst):
        """Handle LAST operation"""
        result = lst[-1]
        self.interpreter.variables["LIST_RESULT"] = result
        self.interpreter.log_output(f"LAST of {list_name} = {result}")

    def _list_butfirst_operation(self, list_name, lst):
        """Handle BUTFIRST operation"""
        result = lst[1:]
        self.interpreter.variables["LIST_RESULT"] = result
        self.interpreter.log_output(f"BUTFIRST of {list_name} = {result}")

    def _list_butlast_operation(self, list_name, lst):
        """Handle BUTLAST operation"""
        result = lst[:-1]
        self.interpreter.variables["LIST_RESULT"] = result
        self.interpreter.log_output(f"BUTLAST of {list_name} = {result}")

    def _handle_file_operations(self, cmd, parts):
        """Handle file operations in Logo"""
        try:
            if cmd == "SAVE":
                # SAVE "filename" - save current canvas/turtle state
                if len(parts) >= 2:
                    filename = parts[1].strip('"')

                    # Save turtle state and any drawings
                    state = {
                        "turtle": self.interpreter.turtle_graphics.copy(),
                        "variables": dict(self.interpreter.variables),
                        "timestamp": time.time(),
                    }

                    import json

                    try:
                        with open(filename, "w", encoding="utf-8") as f:
                            json.dump(state, f, indent=2, default=str)
                        self.interpreter.log_output(
                            f"Saved turtle state to '{filename}'"
                        )
                    except Exception as e:
                        self.interpreter.debug_output(f"SAVE error: {e}")

            elif cmd == "LOAD":
                # LOAD "filename" - load turtle state
                if len(parts) >= 2:
                    filename = parts[1].strip('"')

                    import json

                    try:
                        with open(filename, "r", encoding="utf-8") as f:
                            state = json.load(f)

                        # Restore turtle state
                        if "turtle" in state:
                            self.interpreter.turtle_graphics.update(state["turtle"])

                        # Restore variables
                        if "variables" in state:
                            self.interpreter.variables.update(state["variables"])

                        self.interpreter.log_output(
                            f"Loaded turtle state from '{filename}'"
                        )

                        # Update display
                        if hasattr(self.interpreter, "update_turtle_display"):
                            self.interpreter.update_turtle_display()

                    except Exception as e:
                        self.interpreter.debug_output(f"LOAD error: {e}")

            elif cmd == "EXPORT":
                # EXPORT "filename" - export canvas as image
                if len(parts) >= 2:
                    filename = parts[1].strip('"')

                    # This would export the current canvas as an image
                    # Simplified implementation - just log for now
                    self.interpreter.log_output(
                        f"Exported canvas to '{filename}' (simulated)"
                    )

        except Exception as e:
            self.interpreter.debug_output(f"File operation error: {e}")
        return "continue"

    def _handle_sound_generation(self, cmd, parts):
        """Handle sound generation commands in Logo"""
        try:
            if cmd == "PLAYNOTE":
                # PLAYNOTE note duration - play a musical note
                if len(parts) >= 3:
                    note = parts[1].strip('"')
                    duration = float(parts[2])

                    # Simple note to frequency mapping
                    note_freqs = {
                        "C4": 261.63,
                        "C#4": 277.18,
                        "D4": 293.66,
                        "D#4": 311.13,
                        "E4": 329.63,
                        "F4": 349.23,
                        "F#4": 369.99,
                        "G4": 392.00,
                        "G#4": 415.30,
                        "A4": 440.00,
                        "A#4": 466.16,
                        "B4": 493.88,
                        "C5": 523.25,
                    }

                    if note.upper() in note_freqs:
                        frequency = note_freqs[note.upper()]
                        try:
                            import winsound

                            winsound.Beep(int(frequency), int(duration * 1000))
                            self.interpreter.log_output(
                                f"Played note {note} for {duration}s"
                            )
                        except ImportError:
                            self.interpreter.log_output(
                                f"Played note {note} for {duration}s (simulated)"
                            )
                    else:
                        self.interpreter.log_output("Unknown note")

            elif cmd == "PLAYTUNE":
                # PLAYTUNE "notes" - play a sequence of notes
                if len(parts) >= 2:
                    notes_str = parts[1].strip('"')
                    notes = [n.strip() for n in notes_str.split()]

                    note_freqs = {
                        "C": 261.63,
                        "D": 293.66,
                        "E": 329.63,
                        "F": 349.23,
                        "G": 392.00,
                        "A": 440.00,
                        "B": 493.88,
                    }

                    duration = 0.3  # Default note duration
                    for note in notes:
                        if note.upper() in note_freqs:
                            frequency = note_freqs[note.upper()]
                            try:
                                import winsound

                                winsound.Beep(int(frequency), int(duration * 1000))
                            except ImportError:
                                pass  # Simulated
                            time.sleep(0.1)  # Brief pause between notes

                    self.interpreter.log_output(f"Played tune: {notes_str}")

            elif cmd == "SETSOUND":
                # SETSOUND frequency duration - set sound parameters
                if len(parts) >= 3:
                    frequency = float(parts[1])
                    duration = float(parts[2])

                    # Store sound settings
                    self.interpreter.variables["SOUND_FREQUENCY"] = frequency
                    self.interpreter.variables["SOUND_DURATION"] = duration

                    self.interpreter.log_output(
                        f"Set sound: {frequency}Hz for {duration}s"
                    )

        except Exception as e:
            self.interpreter.debug_output(f"Sound generation error: {e}")
        return "continue"

    def _handle_3d_primitives(self, cmd, parts):
        """Handle 3D graphics primitives in Logo"""
        try:
            # These are simplified 2D representations of 3D shapes
            if cmd == "CUBE":
                # CUBE size - draw a cube (simplified as square with 3D effect)
                if len(parts) >= 2:
                    size = float(parts[1])

                    # Draw a simple cube representation
                    current_x = self.interpreter.turtle_graphics["x"]
                    current_y = self.interpreter.turtle_graphics["y"]

                    if (
                        hasattr(self.interpreter, "ide_turtle_canvas")
                        and self.interpreter.ide_turtle_canvas
                    ):
                        canvas = self.interpreter.ide_turtle_canvas
                        # Draw front face
                        canvas.create_rectangle(
                            current_x,
                            current_y,
                            current_x + size,
                            current_y + size,
                            outline="black",
                            tags="game_objects",
                        )
                        # Draw back face (offset)
                        offset = size * 0.3
                        canvas.create_rectangle(
                            current_x + offset,
                            current_y - offset,
                            current_x + size + offset,
                            current_y + size - offset,
                            outline="gray",
                            tags="game_objects",
                        )
                        # Connect corners
                        canvas.create_line(
                            current_x,
                            current_y,
                            current_x + offset,
                            current_y - offset,
                            tags="game_objects",
                        )
                        canvas.create_line(
                            current_x + size,
                            current_y,
                            current_x + size + offset,
                            current_y - offset,
                            tags="game_objects",
                        )
                        canvas.create_line(
                            current_x + size,
                            current_y + size,
                            current_x + size + offset,
                            current_y + size - offset,
                            tags="game_objects",
                        )
                        canvas.create_line(
                            current_x,
                            current_y + size,
                            current_x + offset,
                            current_y + size - offset,
                            tags="game_objects",
                        )

                        self.interpreter.log_output(f"Drew 3D cube (size {size})")
                    else:
                        self.interpreter.log_output(
                            "CUBE command requires graphics canvas"
                        )

            elif cmd == "SPHERE":
                # SPHERE radius - draw a
                # sphere (simplified as circle with shading)
                if len(parts) >= 2:
                    radius = float(parts[1])

                    if (
                        hasattr(self.interpreter, "ide_turtle_canvas")
                        and self.interpreter.ide_turtle_canvas
                    ):
                        canvas = self.interpreter.ide_turtle_canvas
                        current_x = self.interpreter.turtle_graphics["x"]
                        current_y = self.interpreter.turtle_graphics["y"]

                        # Draw main circle
                        canvas.create_oval(
                            current_x - radius,
                            current_y - radius,
                            current_x + radius,
                            current_y + radius,
                            fill="lightblue",
                            outline="blue",
                            tags="game_objects",
                        )
                        # Add highlight
                        canvas.create_oval(
                            current_x - radius * 0.7,
                            current_y - radius * 0.7,
                            current_x - radius * 0.3,
                            current_y - radius * 0.3,
                            fill="white",
                            outline="white",
                            tags="game_objects",
                        )

                        self.interpreter.log_output(f"Drew 3D sphere (radius {radius})")
                    else:
                        self.interpreter.log_output(
                            "SPHERE command requires graphics canvas"
                        )

            elif cmd == "CYLINDER":
                # CYLINDER radius height - draw a cylinder
                if len(parts) >= 3:
                    radius = float(parts[1])
                    height = float(parts[2])

                    if (
                        hasattr(self.interpreter, "ide_turtle_canvas")
                        and self.interpreter.ide_turtle_canvas
                    ):
                        canvas = self.interpreter.ide_turtle_canvas
                        current_x = self.interpreter.turtle_graphics["x"]
                        current_y = self.interpreter.turtle_graphics["y"]

                        # Draw top ellipse
                        canvas.create_oval(
                            current_x - radius,
                            current_y - radius,
                            current_x + radius,
                            current_y + radius,
                            fill="lightgray",
                            outline="black",
                            tags="game_objects",
                        )
                        # Draw bottom ellipse
                        canvas.create_oval(
                            current_x - radius,
                            current_y + height - radius,
                            current_x + radius,
                            current_y + height + radius,
                            fill="darkgray",
                            outline="black",
                            tags="game_objects",
                        )
                        # Draw connecting lines
                        canvas.create_line(
                            current_x - radius,
                            current_y,
                            current_x - radius,
                            current_y + height,
                            tags="game_objects",
                        )
                        canvas.create_line(
                            current_x + radius,
                            current_y,
                            current_x + radius,
                            current_y + height,
                            tags="game_objects",
                        )

                        self.interpreter.log_output(
                            f"Drew 3D cylinder (radius {radius}, height {height})"
                        )
                    else:
                        self.interpreter.log_output(
                            "CYLINDER command requires graphics canvas"
                        )

            elif cmd == "PYRAMID":
                # PYRAMID base_size height - draw a pyramid
                if len(parts) >= 3:
                    base_size = float(parts[1])
                    height = float(parts[2])

                    if (
                        hasattr(self.interpreter, "ide_turtle_canvas")
                        and self.interpreter.ide_turtle_canvas
                    ):
                        canvas = self.interpreter.ide_turtle_canvas
                        current_x = self.interpreter.turtle_graphics["x"]
                        current_y = self.interpreter.turtle_graphics["y"]

                        half_base = base_size / 2
                        # Draw base
                        canvas.create_polygon(
                            current_x - half_base,
                            current_y + height,
                            current_x + half_base,
                            current_y + height,
                            current_x + half_base,
                            current_y + height + base_size,
                            current_x - half_base,
                            current_y + height + base_size,
                            fill="lightgray",
                            outline="black",
                            tags="game_objects",
                        )
                        # Draw sides
                        canvas.create_polygon(
                            current_x,
                            current_y,
                            current_x - half_base,
                            current_y + height,
                            current_x + half_base,
                            current_y + height,
                            fill="gray",
                            outline="black",
                            tags="game_objects",
                        )

                        self.interpreter.log_output(
                            f"Drew 3D pyramid (base {base_size}, height {height})"
                        )
                    else:
                        self.interpreter.log_output(
                            "PYRAMID command requires graphics canvas"
                        )

        except Exception as e:
            self.interpreter.debug_output(f"3D primitive error: {e}")
        return "continue"

    # Helper methods for parsing
    def _extract_bracket_block(self, text):
        """Extract a [...] block from the start of text. Returns (block, ok)."""
        text = text.strip()
        if not text.startswith("["):
            return "", False
        depth = 0
        for i, ch in enumerate(text):
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return text[: i + 1], True
        return text, False  # unmatched

    def _split_top_level_commands(self, inner):
        """Split commands properly keeping command-argument pairs together while preserving nested [ ] blocks."""
        # Known Logo commands that we need to recognize
        logo_commands = {
            "FORWARD",
            "FD",
            "BACK",
            "BK",
            "BACKWARD",
            "LEFT",
            "LT",
            "RIGHT",
            "RT",
            "PENUP",
            "PU",
            "PENDOWN",
            "PD",
            "CLEARSCREEN",
            "CS",
            "HOME",
            "SETXY",
            "SETCOLOR",
            "SETCOLOUR",
            "COLOR",
            "SETPENCOLOR",
            "SETPC",
            "SETPENSIZE",
            "CIRCLE",
            "DOT",
            "RECT",
            "TEXT",
            "SHOWTURTLE",
            "ST",
            "HIDETURTLE",
            "HT",
            "HEADING",
            "POSITION",
            "TRACE",
            "PROFILE",
            "REPEAT",
            "DEFINE",
            "CALL",
            "MAKE",
            "PRINT",
            "IF",
            "STOP",
        }

        # Commands that take a bracket block as an argument
        bracket_commands = {"REPEAT", "IF", "WHILE", "UNTIL", "PRINT"}

        # Tokenize the input respecting brackets
        tokens = []
        buf = []
        depth = 0
        i = 0

        while i < len(inner):
            ch = inner[i]
            if ch == "[":
                depth += 1
                buf.append(ch)
            elif ch == "]":
                depth = max(0, depth - 1)
                buf.append(ch)
            elif ch.isspace() and depth == 0:
                if buf:
                    tokens.append("".join(buf).strip())
                    buf = []
            else:
                buf.append(ch)
            i += 1
        if buf:
            tokens.append("".join(buf).strip())

        # Now group tokens into commands with their arguments
        commands = []
        i = 0
        while i < len(tokens):
            token = tokens[i].upper()

            # Check if this token is a known command
            if token in logo_commands or token.startswith("["):
                # Start building a command
                cmd_parts = [tokens[i]]
                cmd_upper = token
                i += 1

                # Collect arguments until we hit another command or end
                while i < len(tokens):
                    next_token = tokens[i].upper()

                    # If next token starts with '[', check if the current
                    # command expects a bracket block argument
                    if next_token.startswith("["):
                        if cmd_upper in bracket_commands:
                            # Include the bracket block as part of this command
                            cmd_parts.append(tokens[i])
                            i += 1
                            break  # Bracket block terminates the command
                        else:
                            break  # Not a bracket command — stop

                    # If next token is a command, stop collecting args
                    if next_token in logo_commands:
                        break

                    cmd_parts.append(tokens[i])
                    i += 1

                # Join the command and its arguments
                commands.append(" ".join(cmd_parts))
            else:
                # Unknown token - treat as standalone command
                commands.append(tokens[i])
                i += 1

        return [cmd.strip() for cmd in commands if cmd.strip()]

    def _parse_repeat_nested(self, full_command):
        """Parse REPEAT n [ commands ... ] supporting nested REPEAT blocks."""
        m = re.match(r"^REPEAT\s+([0-9]+)\s+(.*)$", full_command.strip(), re.IGNORECASE)
        if not m:
            return None
        try:
            count = int(m.group(1))
        except ValueError:
            return None
        rest = m.group(2).strip()
        block, ok = self._extract_bracket_block(rest)
        if not ok:
            return None
        inner = block[1:-1].strip()
        raw_cmds = self._split_top_level_commands(inner)
        commands = [c.strip() for c in raw_cmds if c.strip()]
        return count, commands

    # UCBLogo Array Operations
    def _handle_array(self, parts):
        """Handle ARRAY command - create a 1D array"""
        try:
            if len(parts) >= 3:
                array_name = parts[1]
                size = int(parts[2])
                default_value = parts[3] if len(parts) > 3 else 0

                # Create array with default values
                array = [default_value] * size
                self.interpreter.logo_arrays[array_name] = array
                self.interpreter.log_output(
                    f"Created array '{array_name}' with {size} elements"
                )
            else:
                self.interpreter.log_output("ARRAY requires name and size")
        except Exception as e:
            self.interpreter.debug_output(f"ARRAY error: {e}")
        return "continue"

    def _handle_mdarray(self, parts):
        """Handle MDARRAY command - create multi-dimensional array"""
        try:
            if len(parts) >= 3:
                array_name = parts[1]
                # Parse dimensions from remaining parts
                dimensions = []
                for part in parts[2:]:
                    dimensions.append(int(part))

                # Create nested array structure
                def create_nested_array(dims):
                    if len(dims) == 1:
                        return [0] * dims[0]
                    else:
                        return [create_nested_array(dims[1:]) for _ in range(dims[0])]

                array = create_nested_array(dimensions)
                self.interpreter.logo_arrays[array_name] = array
                self.interpreter.log_output(
                    f"Created {len(dimensions)}D array '{array_name}' with dimensions {dimensions}"
                )
            else:
                self.interpreter.log_output("MDARRAY requires name and dimensions")
        except Exception as e:
            self.interpreter.debug_output(f"MDARRAY error: {e}")
        return "continue"

    def _handle_setitem(self, parts):
        """Handle SETITEM command - set array element"""
        try:
            if len(parts) >= 4:
                array_name = parts[1]
                index = int(parts[2])
                value = parts[3]

                if array_name in self.interpreter.logo_arrays:
                    array = self.interpreter.logo_arrays[array_name]
                    if isinstance(array, list) and 0 <= index < len(array):
                        array[index] = value
                        self.interpreter.log_output(
                            f"Set {array_name}[{index}] = {value}"
                        )
                    else:
                        self.interpreter.log_output("Invalid array or index")
                else:
                    self.interpreter.log_output(f"Array '{array_name}' not found")
            else:
                self.interpreter.log_output(
                    "SETITEM requires array name, index, and value"
                )
        except Exception as e:
            self.interpreter.debug_output(f"SETITEM error: {e}")
        return "continue"

    def _handle_mdsetitem(self, parts):
        """Handle MDSETITEM command - set multi-dimensional array element"""
        try:
            if len(parts) >= 4:
                array_name = parts[1]
                indices = [int(idx) for idx in parts[2:-1]]
                value = parts[-1]

                if array_name in self.interpreter.logo_arrays:
                    array = self.interpreter.logo_arrays[array_name]

                    # Navigate to the correct nested position
                    for idx in indices[:-1]:
                        if isinstance(array, list) and 0 <= idx < len(array):
                            array = array[idx]
                        else:
                            self.interpreter.log_output("Invalid array indices")
                            return "continue"

                    # Set the final value
                    final_idx = indices[-1]
                    if isinstance(array, list) and 0 <= final_idx < len(array):
                        array[final_idx] = value
                        self.interpreter.log_output(
                            f"Set {array_name}[{','.join(map(str, indices))}] = {value}"
                        )
                    else:
                        self.interpreter.log_output("Invalid final index")
                else:
                    self.interpreter.log_output(f"Array '{array_name}' not found")
            else:
                self.interpreter.log_output(
                    "MDSETITEM requires array name, indices, and value"
                )
        except Exception as e:
            self.interpreter.debug_output(f"MDSETITEM error: {e}")
        return "continue"

    def _handle_item(self, parts):
        """Handle ITEM command - get array/list element"""
        try:
            if len(parts) >= 3:
                index = int(parts[1])
                source = parts[2]

                # Check if it's an array
                if source in self.interpreter.logo_arrays:
                    array = self.interpreter.logo_arrays[source]
                    # Use 1-based indexing for ITEM to match Logo semantics
                    index = index - 1
                    if isinstance(array, list) and 0 <= index < len(array):
                        result = array[index]
                        self.interpreter.variables["ARRAY_RESULT"] = result
                        self.interpreter.log_output(
                            f"ITEM {index + 1} of {source} = {result}"
                        )
                    else:
                        self.interpreter.log_output("Invalid array or index")
                # Check if it's a list variable
                elif source in self.interpreter.variables:
                    lst = self.interpreter.variables[source]
                    # Use 1-based indexing for lists as well
                    index = index - 1
                    if isinstance(lst, list) and 0 <= index < len(lst):
                        result = lst[index]
                        self.interpreter.variables["LIST_RESULT"] = result
                        self.interpreter.log_output(
                            f"ITEM {index + 1} of {source} = {result}"
                        )
                    else:
                        self.interpreter.log_output("Invalid list or index")
                else:
                    self.interpreter.log_output(f"Array/list '{source}' not found")
            else:
                self.interpreter.log_output("ITEM requires index and array/list name")
        except Exception as e:
            self.interpreter.debug_output(f"ITEM error: {e}")
        return "continue"

    # UCBLogo Property List Operations
    def _handle_pprop(self, parts):
        """Handle PPROP command - put property"""
        try:
            if len(parts) >= 4:
                plist_name = parts[1]
                prop_name = parts[2]
                value = " ".join(parts[3:])

                if plist_name not in self.interpreter.property_lists:
                    self.interpreter.property_lists[plist_name] = {}

                self.interpreter.property_lists[plist_name][prop_name] = value
                self.interpreter.log_output(
                    f"Set property '{prop_name}' in '{plist_name}' to '{value}'"
                )
            else:
                self.interpreter.log_output(
                    "PPROP requires property list name, property name, and value"
                )
        except Exception as e:
            self.interpreter.debug_output(f"PPROP error: {e}")
        return "continue"

    def _handle_gprop(self, parts):
        """Handle GPROP command - get property"""
        try:
            if len(parts) >= 3:
                plist_name = parts[1]
                prop_name = parts[2]

                if plist_name in self.interpreter.property_lists:
                    plist = self.interpreter.property_lists[plist_name]
                    if prop_name in plist:
                        value = plist[prop_name]
                        self.interpreter.variables["PROP_RESULT"] = value
                        self.interpreter.log_output(
                            f"Property '{prop_name}' in '{plist_name}' = '{value}'"
                        )
                    else:
                        self.interpreter.log_output(
                            f"Property '{prop_name}' not found in '{plist_name}'"
                        )
                else:
                    self.interpreter.log_output(
                        f"Property list '{plist_name}' not found"
                    )
            else:
                self.interpreter.log_output(
                    "GPROP requires property list name and property name"
                )
        except Exception as e:
            self.interpreter.debug_output(f"GPROP error: {e}")
        return "continue"

    def _handle_plist(self, parts):
        """Handle PLIST command - list all properties"""
        try:
            if len(parts) >= 2:
                plist_name = parts[1]

                if plist_name in self.interpreter.property_lists:
                    plist = self.interpreter.property_lists[plist_name]
                    if plist:
                        props = list(plist.keys())
                        self.interpreter.variables["PLIST_RESULT"] = props
                        self.interpreter.log_output(
                            f"Properties in '{plist_name}': {props}"
                        )
                    else:
                        self.interpreter.log_output(
                            f"Property list '{plist_name}' is empty"
                        )
                else:
                    self.interpreter.log_output(
                        f"Property list '{plist_name}' not found"
                    )
            else:
                self.interpreter.log_output("PLIST requires property list name")
        except Exception as e:
            self.interpreter.debug_output(f"PLIST error: {e}")
        return "continue"

    def _handle_remprop(self, parts):
        """Handle REMPROP command - remove property"""
        try:
            if len(parts) >= 3:
                plist_name = parts[1]
                prop_name = parts[2]

                if plist_name in self.interpreter.property_lists:
                    plist = self.interpreter.property_lists[plist_name]
                    if prop_name in plist:
                        del plist[prop_name]
                        self.interpreter.log_output(
                            f"Removed property '{prop_name}' from '{plist_name}'"
                        )
                    else:
                        self.interpreter.log_output(
                            f"Property '{prop_name}' not found in '{plist_name}'"
                        )
                else:
                    self.interpreter.log_output(
                        f"Property list '{plist_name}' not found"
                    )
            else:
                self.interpreter.log_output(
                    "REMPROP requires property list name and property name"
                )
        except Exception as e:
            self.interpreter.debug_output(f"REMPROP error: {e}")
        return "continue"

    # UCBLogo Advanced Control Structures
    def _handle_apply(self, parts):
        """Handle APPLY command — call a procedure with an argument list.

        Syntax: APPLY "procname [arg1 arg2 ...]
        """
        try:
            if len(parts) < 3:
                self.interpreter.log_output(
                    "⚠️  APPLY syntax: APPLY \"procname [arg1 arg2 ...]"
                )
                return "continue"

            proc_name = parts[1].strip('"').upper()
            lists = self._extract_bracket_lists(parts[2:])
            args = lists[0].split() if lists else parts[2:]
            return self._call_logo_procedure(proc_name, args)
        except Exception as e:
            self.interpreter.debug_output(f"APPLY error: {e}")
        return "continue"

    def _handle_invoke(self, parts):
        """Handle INVOKE command — call a procedure with individual arguments.

        Syntax: INVOKE "procname arg1 arg2 ...
        """
        try:
            if len(parts) < 2:
                self.interpreter.log_output(
                    "⚠️  INVOKE syntax: INVOKE \"procname arg1 arg2 ..."
                )
                return "continue"

            proc_name = parts[1].strip('"').upper()
            args = parts[2:]
            return self._call_logo_procedure(proc_name, args)
        except Exception as e:
            self.interpreter.debug_output(f"INVOKE error: {e}")
        return "continue"

    def _handle_foreach(self, parts):
        """Handle FOREACH command - iterate over list and execute block for each item"""
        try:
            # FOREACH var_name list_name [block_commands]
            if len(parts) >= 3:
                var_name = parts[1]
                list_name = parts[2]
                # Commands to execute for each item (everything after list_name)
                block_commands = ' '.join(parts[3:]) if len(parts) > 3 else None

                if list_name in self.interpreter.variables:
                    lst = self.interpreter.variables[list_name]
                    if isinstance(lst, list):
                        for item in lst:
                            self.interpreter.variables[var_name] = item
                            self.interpreter.debug_output(f"FOREACH: {var_name} = {item}")

                            # Execute the block for each item if provided
                            if block_commands:
                                # Parse and execute block commands
                                block_parts = block_commands.split()
                                # Execute each command in the block
                                for cmd in block_parts:
                                    if cmd.strip():
                                        result = self.execute_command(cmd)
                                        if result in ["break", "return"]:
                                            break
                        self.interpreter.log_output(f"FOREACH: Completed iteration over {list_name}")
                    else:
                        self.interpreter.log_output(f"❌ '{list_name}' is not a list, got {type(lst).__name__}")
                else:
                    self.interpreter.log_output(f"❌ Variable '{list_name}' not found")
            else:
                self.interpreter.log_output(
                    "⚠️  FOREACH syntax: FOREACH var_name list_name [commands...]"
                )
        except Exception as e:
            self.interpreter.debug_output(f"FOREACH error: {e}")
        return "continue"

    def _handle_cascade(self, parts):
        """Handle CASCADE command — iterative function application.

        Syntax: CASCADE n [template1] [template2] ... start_value
        Applies templates *n* times, using ``?`` for the current value.
        """
        try:
            lists = self._extract_bracket_lists(parts)
            # Need at least: CASCADE n [template] start
            if len(parts) < 4 or not lists:
                self.interpreter.log_output(
                    "⚠️  CASCADE syntax: CASCADE n [template] start_value"
                )
                return "continue"
            n = int(self._eval_argument(parts[1]))
            start_val = self._eval_argument(parts[-1])
            current = start_val
            for _ in range(n):
                for tmpl in lists:
                    cmd = tmpl.replace("?", str(current))
                    result = self._execute_command_block(cmd)
                    if result == "stop":
                        return "stop"
                    # Attempt to capture the output value for chaining
                    # (simple: check if a variable '?' was set)
                    current = self.interpreter.variables.get("?", current)
        except Exception as e:
            self.interpreter.debug_output(f"CASCADE error: {e}")
        return "continue"

    def _handle_case(self, parts):
        """Handle CASE command — select and execute a matching clause.

        Syntax: CASE value [match1 [action1]] [match2 [action2]] ...
        """
        try:
            if len(parts) < 3:
                self.interpreter.log_output(
                    "⚠️  CASE syntax: CASE value [match1 [action1]] ..."
                )
                return "continue"

            value = str(self._eval_argument(parts[1]))
            lists = self._extract_bracket_lists(parts[2:])
            for clause in lists:
                # Each clause: "match_value action_commands"
                clause_parts = clause.split(None, 1)
                if not clause_parts:
                    continue
                match_val = clause_parts[0]
                if match_val.upper() == "ELSE" or match_val == value:
                    if len(clause_parts) > 1:
                        result = self._execute_command_block(clause_parts[1])
                        if result == "stop":
                            return "stop"
                    break
        except Exception as e:
            self.interpreter.debug_output(f"CASE error: {e}")
        return "continue"

    def _handle_cond(self, parts):
        """Handle COND command — evaluate condition/action pairs.

        Syntax: COND [[condition1] [action1]] [[condition2] [action2]] ...
        Evaluates each condition in order; executes the first true action.
        """
        try:
            lists = self._extract_bracket_lists(parts[1:])
            if not lists:
                self.interpreter.log_output(
                    "⚠️  COND syntax: COND [[condition] [action]] ..."
                )
                return "continue"

            for clause in lists:
                # Each clause is "[condition] [action]" as inner bracket lists
                inner = self._extract_bracket_lists(["dummy"] + clause.split())
                if len(inner) >= 2:
                    cond_str, action_str = inner[0], inner[1]
                    if self._eval_logo_condition(cond_str):
                        result = self._execute_command_block(action_str)
                        if result == "stop":
                            return "stop"
                        break
        except Exception as e:
            self.interpreter.debug_output(f"COND error: {e}")
        return "continue"

    # ---- helper for bracket-list extraction ----

    @staticmethod
    def _extract_bracket_lists(parts: list[str]) -> list[str]:
        """Extract ``[...]`` bracket-delimited lists from *parts*.

        Returns a list of strings, one per matched bracket group, with the
        brackets themselves stripped.  Handles nested brackets correctly.
        """
        text = " ".join(parts)
        result = []
        depth = 0
        current: list[str] = []
        for ch in text:
            if ch == "[":
                if depth > 0:
                    current.append(ch)
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    result.append("".join(current).strip())
                    current = []
                elif depth > 0:
                    current.append(ch)
            elif depth > 0:
                current.append(ch)
        return result

    def _eval_logo_condition(self, cond_str):
        """Evaluate a Logo condition string, returning a Python bool."""
        import re

        def replace_var(m):
            var_name = m.group(1).upper()
            return str(self.interpreter.variables.get(var_name, 0))

        evaluated = re.sub(r":(\w+)", replace_var, cond_str)
        return bool(eval(evaluated, {"__builtins__": {}}, {}))  # noqa: S307

    # ---- UCBLogo loop constructs ----

    def _handle_while(self, parts):
        """Handle WHILE [condition] [instructions] — repeat while condition is true."""
        try:
            lists = self._extract_bracket_lists(parts)
            if len(lists) < 2:
                self.interpreter.log_output(
                    "⚠️  WHILE syntax: WHILE [condition] [instructions]"
                )
                return "continue"

            cond_str, body_str = lists[0], lists[1]
            guard = 0
            while self._eval_logo_condition(cond_str):
                guard += 1
                if guard > 10000:
                    self.interpreter.log_output("WHILE aborted: iteration limit reached")
                    break
                result = self._execute_command_block(body_str)
                if result == "stop":
                    return "stop"
        except Exception as e:
            self.interpreter.debug_output(f"WHILE error: {e}")
        return "continue"

    def _handle_until(self, parts):
        """Handle UNTIL [condition] [instructions] — repeat until condition is true."""
        try:
            lists = self._extract_bracket_lists(parts)
            if len(lists) < 2:
                self.interpreter.log_output(
                    "⚠️  UNTIL syntax: UNTIL [condition] [instructions]"
                )
                return "continue"

            cond_str, body_str = lists[0], lists[1]
            guard = 0
            while not self._eval_logo_condition(cond_str):
                guard += 1
                if guard > 10000:
                    self.interpreter.log_output("UNTIL aborted: iteration limit reached")
                    break
                result = self._execute_command_block(body_str)
                if result == "stop":
                    return "stop"
        except Exception as e:
            self.interpreter.debug_output(f"UNTIL error: {e}")
        return "continue"

    def _handle_do_while(self, parts):
        """Handle DO.WHILE [instructions] [condition] — execute at least once, then loop while true."""
        try:
            lists = self._extract_bracket_lists(parts)
            if len(lists) < 2:
                self.interpreter.log_output(
                    "⚠️  DO.WHILE syntax: DO.WHILE [instructions] [condition]"
                )
                return "continue"

            body_str, cond_str = lists[0], lists[1]
            guard = 0
            while True:
                guard += 1
                if guard > 10000:
                    self.interpreter.log_output("DO.WHILE aborted: iteration limit reached")
                    break
                result = self._execute_command_block(body_str)
                if result == "stop":
                    return "stop"
                if not self._eval_logo_condition(cond_str):
                    break
        except Exception as e:
            self.interpreter.debug_output(f"DO.WHILE error: {e}")
        return "continue"

    def _handle_do_until(self, parts):
        """Handle DO.UNTIL [instructions] [condition] — execute at least once, then loop until true."""
        try:
            lists = self._extract_bracket_lists(parts)
            if len(lists) < 2:
                self.interpreter.log_output(
                    "⚠️  DO.UNTIL syntax: DO.UNTIL [instructions] [condition]"
                )
                return "continue"

            body_str, cond_str = lists[0], lists[1]
            guard = 0
            while True:
                guard += 1
                if guard > 10000:
                    self.interpreter.log_output("DO.UNTIL aborted: iteration limit reached")
                    break
                result = self._execute_command_block(body_str)
                if result == "stop":
                    return "stop"
                if self._eval_logo_condition(cond_str):
                    break
        except Exception as e:
            self.interpreter.debug_output(f"DO.UNTIL error: {e}")
        return "continue"

    def _handle_for(self, parts):
        """Handle FOR command - for loop"""
        try:
            if len(parts) >= 5:
                var_name = parts[1]
                start_val = int(parts[2])
                end_val = int(parts[3])
                step = int(parts[4]) if len(parts) > 4 else 1

                for i in range(start_val, end_val + 1, step):
                    self.interpreter.variables[var_name] = i
                    self.interpreter.log_output(f"FOR {var_name} = {i}")
                    # In real implementation, would execute a block here
            else:
                self.interpreter.log_output(
                    "FOR requires variable name, start, and end values"
                )
        except Exception as e:
            self.interpreter.debug_output(f"FOR error: {e}")
        return "continue"

    # UCBLogo Advanced Turtle Commands
    def _handle_setheading(self, parts):
        """Handle SETHEADING command - set turtle heading"""
        try:
            if len(parts) >= 2:
                angle = float(parts[1])
                self.interpreter.turtle_graphics["heading"] = angle % 360
                self.interpreter.update_turtle_display()
                self.interpreter.log_output(f"Turtle heading set to {angle}°")
            else:
                self.interpreter.log_output("SETHEADING requires angle")
        except Exception as e:
            self.interpreter.debug_output(f"SETHEADING error: {e}")
        return "continue"

    def _handle_towards(self, parts):
        """Handle TOWARDS command - point turtle towards position"""
        try:
            if len(parts) >= 3:
                x = float(parts[1])
                y = float(parts[2])

                current_x = self.interpreter.turtle_graphics["x"]
                current_y = self.interpreter.turtle_graphics["y"]

                # Calculate angle to target
                dx = x - current_x
                dy = y - current_y
                angle = math.degrees(math.atan2(dy, dx))

                self.interpreter.turtle_graphics["heading"] = angle % 360
                self.interpreter.update_turtle_display()
                self.interpreter.log_output(
                    f"Turtle turned towards ({x}, {y}) - heading {angle:.1f}°"
                )
            else:
                self.interpreter.log_output("TOWARDS requires X and Y coordinates")
        except Exception as e:
            self.interpreter.debug_output(f"TOWARDS error: {e}")
        return "continue"

    def _handle_scrunch(self, parts):
        """Handle SCRUNCH command - adjust coordinate system"""
        try:
            if len(parts) >= 3:
                x_scale = float(parts[1])
                y_scale = float(parts[2])

                # Simplified scrunch implementation -
                # would adjust coordinate scaling
                self.interpreter.log_output(
                    f"SCRUNCH coordinate system: x_scale={x_scale}, y_scale={y_scale} (simplified implementation)"
                )
            else:
                self.interpreter.log_output("SCRUNCH requires X and Y scale factors")
        except Exception as e:
            self.interpreter.debug_output(f"SCRUNCH error: {e}")
        return "continue"

    # UCBLogo Error Handling
    def _handle_erract(self, parts):
        """Handle ERRACT command - set error action"""
        try:
            if len(parts) >= 2:
                action = parts[1]
                self.interpreter.logo_error_handler = action
                self.interpreter.log_output(f"Error handler set to: {action}")
            else:
                self.interpreter.log_output("ERRACT requires error action")
        except Exception as e:
            self.interpreter.debug_output(f"ERRACT error: {e}")
        return "continue"

    def _handle_error(self, parts):
        """Handle ERROR command - generate error"""
        try:
            if len(parts) >= 2:
                error_msg = " ".join(parts[1:])
                if self.interpreter.logo_error_handler:
                    self.interpreter.log_output(
                        f"Error handled by {self.interpreter.logo_error_handler}: {error_msg}"
                    )
                else:
                    self.interpreter.log_output(f"ERROR: {error_msg}")
            else:
                self.interpreter.log_output("ERROR: Generic error")
        except Exception as e:
            self.interpreter.debug_output(f"ERROR command error: {e}")
        return "continue"

    # UCBLogo Advanced Arithmetic
    def _handle_bitwise(self, cmd, parts):
        """Handle bitwise operations"""
        try:
            if len(parts) >= 3:
                op1 = int(parts[1])
                op2 = int(parts[2]) if len(parts) > 2 else 0

                if cmd == "BITAND":
                    result = op1 & op2
                    self.interpreter.log_output(f"{op1} BITAND {op2} = {result}")
                elif cmd == "BITOR":
                    result = op1 | op2
                    self.interpreter.log_output(f"{op1} BITOR {op2} = {result}")
                elif cmd == "BITXOR":
                    result = op1 ^ op2
                    self.interpreter.log_output(f"{op1} BITXOR {op2} = {result}")
                elif cmd == "BITNOT":
                    result = ~op1
                    self.interpreter.log_output(f"BITNOT {op1} = {result}")
                elif cmd == "ASHIFT":
                    # Arithmetic shift: positive op2 shifts left, negative shifts right (sign-preserving)
                    if op2 >= 0:
                        result = op1 << op2
                    else:
                        result = op1 >> (-op2)
                    self.interpreter.log_output(f"{op1} ASHIFT {op2} = {result}")
                elif cmd == "LSHIFT":
                    # Logical left shift
                    if op2 >= 0:
                        result = op1 << op2
                    else:
                        result = (op1 & 0xFFFFFFFF) >> (-op2)  # Unsigned right shift
                    self.interpreter.log_output(f"{op1} LSHIFT {op2} = {result}")

                self.interpreter.variables["BITWISE_RESULT"] = result
            else:
                self.interpreter.log_output(f"{cmd} requires operands")
        except Exception as e:
            self.interpreter.debug_output(f"Bitwise operation error: {e}")
        return "continue"

    # UCBLogo Macros
    def _handle_macro_define(self, parts):
        """Handle .MACRO command - define macro"""
        try:
            if len(parts) >= 2:
                macro_name = parts[1]
                # Simplified macro definition
                self.interpreter.log_output(f"Macro '{macro_name}' defined (.MACRO)")
            else:
                self.interpreter.log_output(".MACRO requires macro name")
        except Exception as e:
            self.interpreter.debug_output(f".MACRO error: {e}")
        return "continue"

    def _handle_defmacro(self, parts):
        """Handle .DEFMACRO command - define macro with parameters"""
        try:
            if len(parts) >= 3:
                macro_name = parts[1]
                params = parts[2:]
                # Simplified macro definition with parameters
                self.interpreter.log_output(
                    f"Macro '{macro_name}' defined with params {params} (.DEFMACRO)"
                )
            else:
                self.interpreter.log_output(
                    ".DEFMACRO requires macro name and parameters"
                )
        except Exception as e:
            self.interpreter.debug_output(f".DEFMACRO error: {e}")
        return "continue"

    def _call_logo_procedure(self, proc_name, args):
        """Call a user-defined Logo procedure (TO/END)"""
        if proc_name not in self.interpreter.logo_procedures:
            self.interpreter.log_output(f"Undefined procedure: {proc_name}")
            return "continue"

        params, body = self.interpreter.logo_procedures[proc_name]

        # Save current variable state
        saved_vars = {}

        # Bind arguments to parameters
        for i, param in enumerate(params):
            param_name = param[1:].upper() if param.startswith(":") else param.upper()
            if i < len(args):
                # Evaluate the argument (could be a variable or expression)
                arg_value = args[i]
                # If it starts with :, it's a variable reference
                if arg_value.startswith(":"):
                    var_name = arg_value[1:].upper()
                    arg_value = self.interpreter.variables.get(var_name, 0)
                else:
                    # Try to evaluate as number or expression
                    try:
                        arg_value = self._eval_expression(arg_value)
                    except Exception:
                        pass  # Keep as string if can't evaluate

                # Save old value if it exists
                if param_name in self.interpreter.variables:
                    saved_vars[param_name] = self.interpreter.variables[param_name]

                self.interpreter.variables[param_name] = arg_value
                self.interpreter.debug_output(f"  {param_name} = {arg_value}")

        # Execute procedure body
        for line in body:
            result = self.execute_command(line)
            if result == "stop":
                return "stop"

        # Restore saved variables
        for var_name in params:
            var_name = (
                var_name[1:].upper() if var_name.startswith(":") else var_name.upper()
            )
            if var_name in saved_vars:
                self.interpreter.variables[var_name] = saved_vars[var_name]
            elif var_name in self.interpreter.variables:
                del self.interpreter.variables[var_name]

        return "continue"

    def _eval_expression(self, expr):
        """Evaluate a simple arithmetic expression"""
        import re

        try:

            def replace_var(match):
                var_name = match.group(1).upper()
                return str(self.interpreter.variables.get(var_name, 0))

            expr_str = re.sub(r":(\w+)", replace_var, str(expr))

            # Evaluate the expression
            result = eval(expr_str, {"__builtins__": {}}, {})
            return result
        except Exception:
            # If evaluation fails, try to parse as number
            try:
                return float(expr)
            except (ValueError, TypeError):
                return expr

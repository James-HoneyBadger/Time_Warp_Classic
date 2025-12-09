# pylint: disable=W0718,R0913,R0914,R0912,C0301
"""
TW Prolog Language Executor
===========================

Implements TW Prolog, an educational variant of the Prolog logic programming
language for the Time_Warp IDE, focusing on declarative programming concepts.

Language Features:
- Facts: Define relationships and properties (e.g., parent(john, mary).)
- Rules: Define logical implications with conditions
- Queries: Ask questions about defined facts and rules
- Unification: Pattern matching and variable binding
- Backtracking: Automatic search through possible solutions
- Lists: [head|tail] syntax and list operations
- Arithmetic: Basic mathematical operations and comparisons
- Control: Cut (!) operator to control backtracking
- I/O: Basic input/output predicates for console interaction

TURBO PROLOG EXTENSIONS:
- DOMAINS: Strong typing system (e.g., domains person = symbol)
- OBJECTS: Object-oriented programming (classes, inheritance, methods)
- ENHANCED PREDICATES: Additional built-in predicates from Turbo Prolog
- STRUCTURED SYNTAX: More formal declarations and clauses
- ERROR HANDLING: Better diagnostics and type checking

The executor provides a simplified Prolog-like syntax for learning logic
programming, with support for facts, rules, queries, and basic backtracking.
"""

# pylint: disable=R0902,W0718,R1705,R0911,R0912,W0123,W0613,R0903

import re


class TwPrologExecutor:
    """Handles TW Prolog language command execution"""

    def __init__(self, interpreter):
        """Initialize with reference to main interpreter"""
        self.interpreter = interpreter
        self.database = {}  # Facts and rules database
        self.domains = {}  # Turbo Prolog domains (type definitions)
        self.objects = {}  # Turbo Prolog objects/classes
        self.variables = {}  # Query variables
        self.current_query = None
        self.backtrack_stack = []  # For backtracking
        self.cut_flag = False  # Cut operator

    def execute_command(self, command):
        """Execute a Prolog command and return the result"""
        try:
            command = command.strip()
            if not command:
                return "continue"

            # Remove trailing period if present
            if command.endswith("."):
                command = command[:-1].strip()

            parts = command.split()
            if not parts:
                return "continue"

            cmd = parts[0].upper()

            # Turbo Prolog domain declarations
            if cmd == "DOMAINS":
                return self._handle_domains(command)
            elif cmd == "OBJECT":
                return self._handle_object_declaration(command)
            elif cmd == "CLASS":
                return self._handle_class_declaration(command)
            elif cmd == "INHERITS":
                return self._handle_inherits(command)
            elif cmd == "PREDICATES":
                return self._handle_predicates(command)

            # Fact/rule definition
            if ":-" in command:
                return self._handle_rule(command)
            elif command.startswith("?-"):
                return self._handle_query(command)
            elif "(" in command and ")" in command:
                # Likely a fact
                return self._handle_fact(command)
            elif cmd in ["LISTING", "LISTING."]:
                return self._handle_listing()
            elif cmd in ["TRACE", "TRACE."]:
                return self._handle_trace()
            elif cmd in ["NOTRACE", "NOTRACE."]:
                return self._handle_notrace()

        except Exception as e:
            self.interpreter.debug_output(f"Prolog command error: {e}")
            return "continue"

        return "continue"

    def _handle_fact(self, command):
        """Handle fact definition"""
        try:
            # fact(arg1, arg2, ...).
            match = re.match(r"(\w+)\s*\((.*?)\)", command)
            if match:
                predicate = match.group(1)
                args_str = match.group(2)

                # Parse arguments
                args = self._parse_arguments(args_str)

                # Store fact
                if predicate not in self.database:
                    self.database[predicate] = []

                self.database[predicate].append({"type": "fact", "args": args})

                self.interpreter.log_output(
                    f"📚 Fact added: {predicate}({', '.join(map(str, args))})"
                )
        except Exception as e:
            self.interpreter.debug_output(f"Fact definition error: {e}")
        return "continue"

    def _handle_rule(self, command):
        """Handle rule definition"""
        try:
            # head :- body.
            if ":-" in command:
                head_part, body_part = command.split(":-", 1)
                head_part = head_part.strip()
                body_part = body_part.strip()

                # Parse head
                head_match = re.match(r"(\w+)\s*\((.*?)\)", head_part)
                if head_match:
                    predicate = head_match.group(1)
                    head_args = self._parse_arguments(head_match.group(2))

                    # Parse body (can be multiple goals separated by commas)
                    goals = [goal.strip() for goal in body_part.split(",")]

                    # Store rule
                    if predicate not in self.database:
                        self.database[predicate] = []

                    self.database[predicate].append(
                        {"type": "rule", "head_args": head_args, "body": goals}
                    )

                    self.interpreter.log_output(
                        f"📋 Rule added: {predicate}({', '.join(map(str, head_args))}) "
                        f":- {', '.join(goals)}"
                    )
        except Exception as e:
            self.interpreter.debug_output(f"Rule definition error: {e}")
        return "continue"

    def _handle_query(self, command):
        """Handle query execution"""
        try:
            # ?- goal1, goal2, ...
            if command.startswith("?-"):
                query_part = command[2:].strip()

                # Parse goals without splitting inside parentheses
                goals = []
                buf = []
                depth = 0
                for ch in query_part:
                    if ch == "(":
                        depth += 1
                    elif ch == ")" and depth > 0:
                        depth -= 1
                    if ch == "," and depth == 0:
                        goals.append("".join(buf).strip())
                        buf = []
                    else:
                        buf.append(ch)
                if buf:
                    goals.append("".join(buf).strip())

                # Execute query
                results = self._execute_query(goals)

                if results:
                    self.interpreter.log_output("✅ Query succeeded")
                    for result in results[:5]:  # Limit output
                        if result:
                            var_bindings = [f"{k} = {v}" for k, v in result.items()]
                            self.interpreter.log_output(f"   {', '.join(var_bindings)}")
                    if len(results) > 5:
                        self.interpreter.log_output(
                            f"   ... and {len(results) - 5} more solutions"
                        )
                else:
                    self.interpreter.log_output("❌ Query failed - no solutions found")
        except Exception as e:
            self.interpreter.debug_output(f"Query execution error: {e}")
        return "continue"

    def _handle_listing(self):
        """Handle LISTING command - show database contents"""
        try:
            self.interpreter.log_output("📚 Prolog Database Contents:")
            for predicate, clauses in self.database.items():
                self.interpreter.log_output(f"\n{predicate}:")
                for clause in clauses:
                    if clause["type"] == "fact":
                        args_str = ", ".join(map(str, clause["args"]))
                        self.interpreter.log_output(f"  {predicate}({args_str}).")
                    elif clause["type"] == "rule":
                        head_args_str = ", ".join(map(str, clause["head_args"]))
                        body_str = ", ".join(clause["body"])
                        self.interpreter.log_output(
                            f"  {predicate}({head_args_str}) :- {body_str}."
                        )
        except Exception as e:
            self.interpreter.debug_output(f"Listing error: {e}")
        return "continue"

    def _handle_trace(self):
        """Handle TRACE command"""
        self.interpreter.log_output("🔍 Tracing enabled")
        return "continue"

    def _handle_notrace(self):
        """Handle NOTRACE command"""
        self.interpreter.log_output("🔍 Tracing disabled")
        return "continue"

    def _handle_domains(self, command):
        """Handle Turbo Prolog DOMAINS declarations"""
        try:
            # DOMAINS domain_name = type_definition
            # e.g., DOMAINS person = symbol
            # e.g., DOMAINS age = integer
            # e.g., DOMAINS grades = symbol*
            domain_match = re.match(
                r"DOMAINS\s+(\w+)\s*=\s*(.+)", command, re.IGNORECASE
            )
            if domain_match:
                domain_name = domain_match.group(1).lower()
                type_def = domain_match.group(2).strip()

                # Parse type definition
                domain_type = self._parse_domain_type(type_def)

                self.domains[domain_name] = domain_type
                self.interpreter.log_output(
                    f"🏷️ Domain {domain_name} = {type_def} declared"
                )
            else:
                self.interpreter.debug_output("Invalid domain declaration syntax")
        except Exception as e:
            self.interpreter.debug_output(f"Domain declaration error: {e}")
        return "continue"

    def _handle_object_declaration(self, command):
        """Handle Turbo Prolog OBJECT declarations"""
        try:
            # OBJECT object_name
            obj_match = re.match(r"OBJECT\s+(\w+)", command, re.IGNORECASE)
            if obj_match:
                obj_name = obj_match.group(1).lower()
                self.objects[obj_name] = {
                    "type": "object",
                    "predicates": [],
                    "parent": None,
                }
                self.interpreter.log_output(f"🏗️ Object {obj_name} declared")
            else:
                self.interpreter.debug_output("Invalid object declaration syntax")
        except Exception as e:
            self.interpreter.debug_output(f"Object declaration error: {e}")
        return "continue"

    def _handle_class_declaration(self, command):
        """Handle Turbo Prolog CLASS declarations"""
        try:
            # CLASS class_name
            class_match = re.match(r"CLASS\s+(\w+)", command, re.IGNORECASE)
            if class_match:
                class_name = class_match.group(1).lower()
                self.objects[class_name] = {
                    "type": "class",
                    "predicates": [],
                    "parent": None,
                }
                self.interpreter.log_output(f"🏛️ Class {class_name} declared")
            else:
                self.interpreter.debug_output("Invalid class declaration syntax")
        except Exception as e:
            self.interpreter.debug_output(f"Class declaration error: {e}")
        return "continue"

    def _handle_inherits(self, command):
        """Handle Turbo Prolog INHERITS declarations"""
        try:
            # INHERITS parent_class
            inherit_match = re.match(r"INHERITS\s+(\w+)", command, re.IGNORECASE)
            if inherit_match:
                parent_name = inherit_match.group(1).lower()
                # Find the current object/class being defined
                current_obj = None
                for obj_name, obj_data in self.objects.items():
                    if obj_data.get("incomplete", False):
                        current_obj = obj_name
                        break

                if current_obj:
                    self.objects[current_obj]["parent"] = parent_name
                    self.interpreter.log_output(
                        f"👪 {current_obj} inherits from {parent_name}"
                    )
                else:
                    self.interpreter.debug_output(
                        "No current object/class to inherit from"
                    )
            else:
                self.interpreter.debug_output("Invalid inherits syntax")
        except Exception as e:
            self.interpreter.debug_output(f"Inherits declaration error: {e}")
        return "continue"

    def _handle_predicates(self, command):
        """Handle Turbo Prolog PREDICATES declarations"""
        try:
            # PREDICATES predicate_name(arg_types) or PREDICATES predicate_name
            pred_match = re.match(r"PREDICATES\s+(.+)", command, re.IGNORECASE)
            if pred_match:
                pred_decl = pred_match.group(1).strip()

                # Parse predicate declarations - handle parentheses properly
                declarations = []
                current_decl = ""
                paren_depth = 0

                for char in pred_decl:
                    if char == "(":
                        paren_depth += 1
                        current_decl += char
                    elif char == ")":
                        paren_depth -= 1
                        current_decl += char
                    elif char == "," and paren_depth == 0:
                        if current_decl.strip():
                            declarations.append(current_decl.strip())
                        current_decl = ""
                    else:
                        current_decl += char

                if current_decl.strip():
                    declarations.append(current_decl.strip())

                for decl in declarations:
                    self._parse_predicate_declaration(decl.strip())
            else:
                self.interpreter.debug_output("Invalid predicates declaration syntax")
        except Exception as e:
            self.interpreter.debug_output(f"Predicates declaration error: {e}")
        return "continue"

    def _parse_arguments(self, args_str):
        """Parse argument list from string"""
        args = []
        current_arg = ""
        in_brackets = 0
        in_quotes = False

        i = 0
        while i < len(args_str):
            char = args_str[i]

            if char == '"' and (i == 0 or args_str[i - 1] != "\\"):
                in_quotes = not in_quotes
                current_arg += char
            elif char == "[" and not in_quotes:
                in_brackets += 1
                current_arg += char
            elif char == "]" and not in_quotes:
                in_brackets -= 1
                current_arg += char
            elif char == "," and not in_quotes and in_brackets == 0:
                if current_arg.strip():
                    args.append(self._parse_term(current_arg.strip()))
                    current_arg = ""
            else:
                current_arg += char

            i += 1

        if current_arg.strip():
            args.append(self._parse_term(current_arg.strip()))

        return args

    def _parse_term(self, term_str):
        """Parse a single term"""
        term_str = term_str.strip()

        # Variable (starts with uppercase or _)
        if re.match(r"^[A-Z_]\w*$", term_str):
            return {"type": "variable", "name": term_str}

        # List [a,b,c]
        elif term_str.startswith("[") and term_str.endswith("]"):
            list_content = term_str[1:-1]
            if not list_content.strip():
                return {"type": "list", "elements": []}
            elements = self._parse_arguments(list_content)
            return {"type": "list", "elements": elements}

        # String "text"
        elif term_str.startswith('"') and term_str.endswith('"'):
            return {"type": "string", "value": term_str[1:-1]}

        # Number
        elif re.match(r"^-?\d+(\.\d+)?$", term_str):
            if "." in term_str:
                return {"type": "number", "value": float(term_str)}
            else:
                return {"type": "number", "value": int(term_str)}

        # Atom (starts with lowercase)
        else:
            return {"type": "atom", "name": term_str}

    def _execute_query(self, goals):
        """Execute a query with backtracking"""
        self.variables = {}
        self.backtrack_stack = []
        self.cut_flag = False

        return self._prove_goals(goals, 0, {})

    def _prove_goals(self, goals, goal_index, bindings):
        """Prove a list of goals using backtracking"""
        if goal_index >= len(goals):
            # All goals proved
            return [bindings.copy()]

        goal = goals[goal_index]
        solutions = []

        # Try to prove current goal
        goal_solutions = self._prove_goal(goal, bindings)

        for solution_bindings in goal_solutions:
            # Merge bindings
            new_bindings = bindings.copy()
            new_bindings.update(solution_bindings)

            # Recursively prove remaining goals
            remaining_solutions = self._prove_goals(goals, goal_index + 1, new_bindings)
            solutions.extend(remaining_solutions)

            if self.cut_flag:
                break

        return solutions

    def _prove_goal(self, goal, bindings):
        """Prove a single goal"""
        # Parse goal
        match = re.match(r"(\w+)\s*\((.*?)\)", goal)
        if not match:
            # Built-in predicates
            return self._prove_builtin(goal, bindings)

        predicate = match.group(1)
        args_str = match.group(2)
        args = self._parse_arguments(args_str)

        solutions = []

        # Apply current bindings to args
        bound_args = self._apply_bindings(args, bindings)

        # Look up predicate in database
        if predicate in self.database:
            for clause in self.database[predicate]:
                if clause["type"] == "fact":
                    # Try to unify with fact
                    fact_args = clause["args"]
                    unification = self._unify(bound_args, fact_args, bindings.copy())
                    if unification is not None:
                        solutions.append(unification)

                elif clause["type"] == "rule":
                    # Try to prove rule body
                    rule_bindings = self._unify(
                        bound_args, clause["head_args"], bindings.copy()
                    )
                    if rule_bindings is not None:
                        # Prove rule body
                        body_solutions = self._prove_goals(
                            clause["body"], 0, rule_bindings
                        )
                        solutions.extend(body_solutions)

        return solutions

    def _prove_builtin(self, goal, bindings):
        """Prove built-in predicates"""
        goal = goal.strip()

        # write/1 - output
        if goal.startswith("write(") and goal.endswith(")"):
            arg_str = goal[6:-1].strip()
            arg = self._parse_term(arg_str)
            bound_arg = self._apply_bindings_to_term(arg, bindings)
            if bound_arg["type"] == "string":
                self.interpreter.log_output(bound_arg["value"])
            else:
                self.interpreter.log_output(str(bound_arg))
            return [bindings]

        # nl/0 - newline
        elif goal == "nl":
            self.interpreter.log_output("")
            return [bindings]

        # Arithmetic comparisons
        elif " =:= " in goal or r" =\= " in goal or " < " in goal or " > " in goal:
            return self._prove_arithmetic(goal, bindings)

        # List operations
        elif goal.startswith("member(") and goal.endswith(")"):
            return self._prove_member(goal, bindings)

        # Turbo Prolog enhanced I/O predicates
        elif goal.startswith("readln(") and goal.endswith(")"):
            return self._prove_readln(goal, bindings)
        elif goal.startswith("readchar(") and goal.endswith(")"):
            return self._prove_readchar(goal, bindings)
        elif goal.startswith("readint(") and goal.endswith(")"):
            return self._prove_readint(goal, bindings)
        elif goal.startswith("readreal(") and goal.endswith(")"):
            return self._prove_readreal(goal, bindings)

        # Turbo Prolog database manipulation
        elif goal.startswith("assert(") and goal.endswith(")"):
            return self._prove_assert(goal, bindings)
        elif goal.startswith("retract(") and goal.endswith(")"):
            return self._prove_retract(goal, bindings)
        elif goal.startswith("consult(") and goal.endswith(")"):
            return self._prove_consult(goal, bindings)

        # Turbo Prolog control predicates
        elif goal == "fail":
            return []
        elif goal == "true":
            return [bindings]
        elif goal.startswith("not(") and goal.endswith(")"):
            return self._prove_not(goal, bindings)
        elif goal.startswith("repeat"):
            return self._prove_repeat(bindings)

        return []

    def _prove_arithmetic(self, goal, bindings):
        """Prove arithmetic comparisons"""
        try:
            # Simple arithmetic evaluation
            expr = goal.replace("=\\=", "!=").replace("=:", "==")
            bound_expr = self._apply_bindings_to_expression(expr, bindings)

            # Safe evaluation
            allowed_names = {
                "abs": abs,
                "round": round,
                "int": int,
                "float": float,
                "max": max,
                "min": min,
                "sin": __import__("math").sin,
                "cos": __import__("math").cos,
                "sqrt": __import__("math").sqrt,
            }

            safe_dict = {"__builtins__": {}}
            safe_dict.update(allowed_names)

            result = eval(bound_expr, safe_dict)
            if result:
                return [bindings]
        except (ValueError, TypeError, NameError, SyntaxError):
            pass
        return []

    def _prove_member(self, goal, bindings):
        """Prove member/2 predicate"""
        try:
            args_str = goal[7:-1]  # Remove member(
            args = self._parse_arguments(args_str)
            if len(args) == 2:
                element = self._apply_bindings_to_term(args[0], bindings)
                list_term = self._apply_bindings_to_term(args[1], bindings)

                if list_term["type"] == "list":
                    for item in list_term["elements"]:
                        unification = self._unify_terms(element, item, bindings.copy())
                        if unification is not None:
                            return [unification]
        except (ValueError, TypeError, IndexError):
            pass
        return []

    def _prove_readln(self, goal, bindings):
        """Prove readln/1 predicate - read line from input"""
        try:
            # For educational purposes, simulate input
            self.interpreter.log_output("💬 Enter input: (simulated)")
            # simulated_input = "simulated_input"  # Would be used in full implementation
            return [bindings]
        except (ValueError, TypeError):
            return []

    def _prove_readchar(self, goal, bindings):
        """Prove readchar/1 predicate - read character from input"""
        try:
            self.interpreter.log_output("💬 Enter character: (simulated)")
            # simulated_char = "A"  # Would be used in full implementation
            return [bindings]
        except (ValueError, TypeError):
            return []

    def _prove_readint(self, goal, bindings):
        """Prove readint/1 predicate - read integer from input"""
        try:
            self.interpreter.log_output("💬 Enter integer: (simulated)")
            # simulated_int = 42  # Would be used in full implementation
            return [bindings]
        except (ValueError, TypeError):
            return []

    def _prove_readreal(self, goal, bindings):
        """Prove readreal/1 predicate - read real number from input"""
        try:
            self.interpreter.log_output("💬 Enter real number: (simulated)")
            # simulated_real = 3.14  # Would be used in full implementation
            return [bindings]
        except (ValueError, TypeError):
            return []

    def _prove_assert(self, goal, bindings):
        """Prove assert/1 predicate - add fact to database"""
        try:
            fact_str = goal[7:-1].strip()  # Remove assert(
            # Parse and add fact
            if "(" in fact_str and ")" in fact_str:
                self._handle_fact(fact_str)
            return [bindings]
        except (ValueError, TypeError):
            return []

    def _prove_retract(self, goal, bindings):
        """Prove retract/1 predicate - remove fact from database"""
        try:
            fact_str = goal[8:-1].strip()  # Remove retract(
            # In a full implementation, this would remove matching facts
            self.interpreter.log_output(f"🔄 Retracting: {fact_str} (simulated)")
            return [bindings]
        except (ValueError, TypeError):
            return []

    def _prove_consult(self, goal, bindings):
        """Prove consult/1 predicate - load file"""
        try:
            filename = goal[8:-1].strip()
            self.interpreter.log_output(f"📂 Consulting file: {filename} (simulated)")
            return [bindings]
        except (ValueError, TypeError):
            return []

    def _prove_not(self, goal, bindings):
        """Prove not/1 predicate - negation"""
        try:
            sub_goal = goal[4:-1].strip()  # Remove not(
            # Try to prove the subgoal - if it fails, not succeeds
            sub_solutions = self._prove_goal(sub_goal, bindings)
            if not sub_solutions:
                return [bindings]  # Negation succeeds
            return []  # Negation fails
        except (ValueError, TypeError):
            return []

    def _prove_repeat(self, bindings):
        """Prove repeat/0 predicate - always succeeds, enables backtracking"""
        # Repeat always succeeds and can be used multiple times
        return [bindings]

    def _unify(self, args1, args2, bindings):
        """Unify two argument lists"""
        if len(args1) != len(args2):
            return None

        result_bindings = bindings.copy()

        for arg1, arg2 in zip(args1, args2):
            unified = self._unify_terms(arg1, arg2, result_bindings)
            if unified is None:
                return None
            result_bindings = unified

        return result_bindings

    def _unify_terms(self, term1, term2, bindings):
        """Unify two terms"""
        # Apply existing bindings
        term1 = self._apply_bindings_to_term(term1, bindings)
        term2 = self._apply_bindings_to_term(term2, bindings)

        # Both variables
        if term1["type"] == "variable" and term2["type"] == "variable":
            if term1["name"] == term2["name"]:
                return bindings
            # Create binding
            new_bindings = bindings.copy()
            new_bindings[term1["name"]] = term2
            return new_bindings

        # First is variable
        elif term1["type"] == "variable":
            if self._occurs_check(term1["name"], term2, bindings):
                return None  # Occurs check failed
            new_bindings = bindings.copy()
            new_bindings[term1["name"]] = term2
            return new_bindings

        # Second is variable
        elif term2["type"] == "variable":
            if self._occurs_check(term2["name"], term1, bindings):
                return None  # Occurs check failed
            new_bindings = bindings.copy()
            new_bindings[term2["name"]] = term1
            return new_bindings

        # Both constants - check equality
        else:
            if term1 == term2:
                return bindings

        return None

    def _occurs_check(self, var_name, term, bindings):
        """Check if variable occurs in term (prevent circular bindings)"""
        if term["type"] == "variable":
            if term["name"] == var_name:
                return True
            if term["name"] in bindings:
                return self._occurs_check(var_name, bindings[term["name"]], bindings)
        elif term["type"] == "list":
            for element in term["elements"]:
                if self._occurs_check(var_name, element, bindings):
                    return True
        return False

    def _apply_bindings(self, args, bindings):
        """Apply bindings to argument list"""
        return [self._apply_bindings_to_term(arg, bindings) for arg in args]

    def _apply_bindings_to_term(self, term, bindings):
        """Apply bindings to a single term"""
        if term["type"] == "variable" and term["name"] in bindings:
            return self._apply_bindings_to_term(bindings[term["name"]], bindings)
        elif term["type"] == "list":
            return {
                "type": "list",
                "elements": [
                    self._apply_bindings_to_term(elem, bindings)
                    for elem in term["elements"]
                ],
            }
        else:
            return term

    def _apply_bindings_to_expression(self, expr, bindings):
        """Apply bindings to arithmetic expression"""
        for var_name, var_term in bindings.items():
            if var_term["type"] in ["number"]:
                expr = expr.replace(var_name, str(var_term["value"]))
        return expr

    def _parse_domain_type(self, type_def):
        """Parse Turbo Prolog domain type definition"""
        type_def = type_def.lower().strip()

        # Basic types
        if type_def in [
            "symbol",
            "string",
            "char",
            "byte",
            "word",
            "integer",
            "long",
            "real",
        ]:
            return {"base_type": type_def}

        # Compound types
        elif type_def.endswith("*"):
            # List type (e.g., symbol*)
            element_type = type_def[:-1]
            return {"base_type": "list", "element_type": element_type}

        elif "=" in type_def:
            # Alternative types (e.g., color = red; green; blue)
            alternatives = [alt.strip() for alt in type_def.split("=")[1].split(";")]
            return {"base_type": "alternatives", "values": alternatives}

        else:
            # Custom domain reference
            return {"base_type": "reference", "domain": type_def}

    def _parse_predicate_declaration(self, decl):
        """Parse a single predicate declaration"""
        try:
            # predicate_name or predicate_name(arg_type1, arg_type2, ...)
            if "(" in decl and ")" in decl:
                # With type specifications
                pred_match = re.match(r"(\w+)\s*\((.+)\)", decl)
                if pred_match:
                    pred_name = pred_match.group(1)
                    arg_types_str = pred_match.group(2)

                    # Parse argument types
                    arg_types = [arg.strip() for arg in arg_types_str.split(",")]

                    # Store predicate declaration
                    if pred_name not in self.database:
                        self.database[pred_name] = []

                    self.database[pred_name].append(
                        {"type": "predicate_declaration", "arg_types": arg_types}
                    )

                    self.interpreter.log_output(
                        f"📋 Predicate {pred_name}({', '.join(arg_types)}) declared"
                    )
            else:
                # Simple declaration without types
                pred_name = decl.strip()
                if pred_name not in self.database:
                    self.database[pred_name] = []

                self.database[pred_name].append(
                    {"type": "predicate_declaration", "arg_types": None}
                )

                self.interpreter.log_output(f"📋 Predicate {pred_name} declared")

        except Exception as e:
            self.interpreter.debug_output(f"Predicate declaration parsing error: {e}")

    def _validate_type(self, term, expected_type):
        """Validate term against Turbo Prolog domain type"""
        if expected_type not in self.domains:
            return True  # Unknown type, allow

        domain_info = self.domains[expected_type]

        if domain_info["base_type"] == "symbol":
            return term["type"] == "atom" or (term["type"] == "variable")
        elif domain_info["base_type"] == "integer":
            return (
                term["type"] == "number"
                and isinstance(term.get("value", 0), int)
                or term["type"] == "variable"
            )
        elif domain_info["base_type"] == "real":
            return term["type"] == "number" or term["type"] == "variable"
        elif domain_info["base_type"] == "string":
            return term["type"] == "string" or term["type"] == "variable"
        elif domain_info["base_type"] == "list":
            return term["type"] == "list" or term["type"] == "variable"

        return True  # Default allow

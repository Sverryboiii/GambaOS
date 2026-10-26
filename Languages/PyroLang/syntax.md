# Syntax
PyroLang has a very weird syntax.
You could associate it with an esoteric language, but it is used for real programming throughout GambaOS.

GET: Puts a builtin function in the global functions.<br>
[GET {builtin function name}]<br>
GETF: Get and run an external file.<br>
[GETF {path/to/external/file.pr}] (modules/ gets a builtin module)<br>
SET: Set a variable.<br>
[SET {variable name} {value}]<br>
if: An run 1 line of code if the expression is true.<br>
[if [{expression}] _{evaluation}_] (Important: This may only be in 1 line!)<br>
func: Create a function.<br>
[func {name} [{parameters split by ';'}] {] (Close on another line using '}')
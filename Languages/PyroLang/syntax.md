# Syntax
PyroLang has a very weird syntax.
You could associate it with an esoteric language, but it is used for real programming throughout GambaOS.

Some quick rules essential rules:<br>
\- Whenever you see a space in the `syntax` parts, assume this space is mandatory.<br>
\- Every operation made with the standard keywords must have a newline.<br>
\- Indentation is not necessary.<br>

#### GET: Puts a builtin function in the global functions.<br>
`[GET {builtin function name}]`<br>
Example:<br>
`GET add`<br>
`// This gets the add method to add 2 or more values`
<br>
<br>
#### GETF: Get and run an external file.<br>
`[GETF {path/to/external/file.pr}]` (modules/ gets a builtin module)<br>
Example:<br>
`GETF modules/io.pr`<br>
`// Gets all the builtin Input/Output methods.`
<br>
<br>
#### SET: Set a variable.<br>
`[SET {variable name} {value}]`<br>
Example:
`SET x "5"+`<br>
`// Sets 'x' to the integer 5.`
<br>
<br>
#### if: An run 1 line of code if the expression is true.<br>
`[if [{expression}] _{evaluation}_ _{else evaluation}_]` (Important: This may only be in 1 line!)<br>
Example:<br>
`if [x="5"+] _out ("X = 5!"!)_
_out ("X != 5!"!)_`<br>
`// Says "X = 5!" if x is 5 else "X != 5!".`
<br>
<br>
#### func: Create a function.<br>
`[func {name} [{parameter1};{parameter2}] {]` (Close on another line using '}')<br>
Example:<br>
`func greet [text] {`<br>
`// Create a function called 'greet' which accepts 1 argument`
<br>
<br>
#### return: Return a value.<br>
[return {value}]
Example:<br>
`return "False"B`<br>
`// Return False.`
<br>
### Functions
Functions are called by their name,
Therefore a functions can NOT have any keyword as name.<br>
If a keyword is used as a function name,
the function itself will not be possible to reach again.<br>
Syntax: `{function name} ({argument1};{argument2})`

## Data types
Boolean:<br>
\- Can be True or False.<br>
\- Syntax: `"{Value}"B`

Integer:<br>
\- Can be any whole number.<br>
\- Syntax: `"{value}"+`

Float:<br>
\- Can be any numeric value.<br>
\- Syntax: `"{value}"-`

String:<br>
\- Can be any Unicode character.<br>
\- Syntax: `"{value}"!`
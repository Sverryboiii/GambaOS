# Scopes
Scopes are very weird in PyroLang.<br>
Here is everything you need to know.<br>

#### Functions
Every function does have a scope, but that scope isn't what you'd think.<br>
The scopes of functions can only be used for the parameters of the functions.<br>
Every variable defined inside the function gets defined in the global variable scope.<br>

Functions themselves are not saved in the global variable scope.<br>
They are stored in a separate global functions scope.

#### Modules / External files.
Modules and external files are treated the same for everything.<br>
They both have their own variable scopes,
but they don't have their own functions scope.<br>
This means that functions are global across all files.

#### Alternative:
Although variables have different scopes across files.<br>
You can still change the global scope from any file using the builtin `up_g` method.<br>
`up_g` stands for update globals.

### All in short:
 - Functions are global across all files.
 - Variables are global across the whole file except if the variable is a parameter.
 - Parameters have their own scope.
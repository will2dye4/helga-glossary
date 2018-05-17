# helga-glossary
A helga command to define and look up terms. Usage:

```
helga glossary [(add|define) <term> <definition>|(find|lookup) <term>|(delete|remove) <term>|random]
```

Without any arguments `helga glossary` will return a randomly selected term from the glossary of terms
that have been previously defined. Each subcommand acts as follows:

* `(add|define) <term> <definition>`

  Add a new term to the glossary. If the term consists of multiple words, it must be quoted. For example,
  to add the term "helga bot" to the glossary, use `helga glossary add "helga bot" a really cool chatbot`.
  The definition may also optionally be quoted.

* `(find|lookup) <term>`

  Retrieve the definition of a term from the glossary. As long as the term does not conflict with the name
  of a subcommand, a term may also be looked up without the find/lookup subcommand, as in `helga glossary <term>`.

* `(delete|remove) <term>`

  Remove a term from the glossary.
  
* `random`

  Retrieve a randomly selected term from the glossary.
  
**NOTE:** This plugin requires database access.

# Using the Judge Verdict Effect
In addition to the usual dialogue text boxes, *Objection* allows you to recreate
the dramatic "Guilty" and "Not Guilty" screens that appear at the end of
*Ace Attorney* cases. In fact, you can make the verdict be any text you want!

The process for setting this up correctly is a bit complex, so hopefully this
document will help you understand how to go about it.

## Basic steps
Displaying verdict text consists of three major steps:
1. Set the text and text color you want to display
2. Make the text actually show up
3. Clear the text once you're done

In this document, I'll go over each of these steps. We'll have the Judge's
verdict be "Really Cool", in white letters with a black border (like "Not Guilty"
from the original gmaes).

### Initializing the verdict text
This step is easy: just issue the single command `verdict set "Really Cool" white`.

As a Python `DialogueAction` object:
```py
DialogueAction("verdict set \"Really Cool\" white", 0)
```

As a command in a written script:
```
[verdict set "Really Cool" white]
```
If you wanted the text to be black with a white border (i.e., styled like "Guilty"
from the original games), then you'd simply change `white` to `black`.

### Making the verdict text appear
This is the hardest step, although it's not too bad. When the text is initialized
as shown above, it doesn't appear on screen. To make each individual character
appear, we have to issue the command `verdict show <i>`, where `<i>` is the 
zero-based index of the character from the verdict text to show. In our example,
the verdict text is "Really Cool", so:
* `verdict show 0` would make "R" appear
* `verdict show 1` would make "e" appear
* `verdict show 2` would make "a" appear
* `verdict show 3` would make "l" appear

and so on.


### Clearing the verdict text
To make the text disappear, simply issue the command `verdict clear`.

As a Python `DialogueAction` object:
```py
DialogueAction("verdict clear", 0)
```

As a command in a written script:
```
[verdict clear]
```
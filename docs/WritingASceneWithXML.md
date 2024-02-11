# Writing a Scene with XML

Using *Objection*, you can easily write *Ace Attorney* courtroom scenes as XML
files, then export them to video clips! In the `examples` folder, the XML file
`test_script.xml` and Python script `example_xml.py` demonstrate how to
structure an *Objection* XML script. Here, I'll go over its structure.

Much like with the other *Objection* formats, a script (or conversation) is broken up into
multiple *pages*, which are defined with the `<page>` tag.
Inside each page is a sequence of commands and text.

```xml
<conversation>
    <page>
        <sprite position="judge" src="assets/characters/judge/judge-normal-talk.gif"/>
        <nametag text="Judge"/>
        <cut position="judge"/>
        <showbox/>
        <evidence action="clear"/>
    </page>
    <page>
        <startblip gender="male"/>
        Court is now in session for the
        <br/>
        trial of<sp/><font color="red">Larry Butz</font>.
        <sprite position="judge" src="assets/characters/judge/judge-normal-idle.gif"/>
        <stopblip/>
        <showarrow/>
        <wait duration="2"/>
    </page>
</conversation>
```

Here we have two pages. In the first page, we run the following commands
in sequence:

1. `<sprite ...>` sets the character sprite in the judge position to the judge
talking animation.
2. `<nametag text="Judge">` sets the text in the dialogue box name tag to
"Judge" (since it's the Judge speaking).
3. `<cut position="judge">` cuts the camera to the judge's position, so we can
see him.
4. `<showbox />` makes the dialogue box show up.
5. `<evidence action="clear"/>` removes the evidence box. (There wasn't any
evidence to begin with, so this doesn't actually make a difference in this
case. But it's usually nice to add anyways, just in case there's a possibility
evidence was added earlier.)

These commands run sequentially, but there is no delay between them, so they
are effectively instantaneous.

In the second page, we do the following:

1. `<startblip gender="male">` starts making the speaking sounds for a male character (since the judge is male).
2. Text not part of a tag shows up as if the character is speaking.
3. `<br/>` adds a line break. If we didn't add this, the judge's text would
go off the right-hand side of the screen.
4. The judge's words continue with "trial of".
5. `<sp/>` adds a single space between "of" and the upcoming word "Larry".
6. `<font color="red">` colors any text inside to be red. So in this case,
"Larry Butz" shows up as red text. The closing tag `</font>` stops the
red coloring.
7. The period ending the judge's sentence appears, uncolored.
8. `<sprite ...>` once again sets the judge's sprite. This time, since he's
done talking, we set it to an idle sprite.
9. `<stopblip/>` stops the speaking sounds.
10. `<showarrow/>` makes the "next dialogue" triangle show up in the corner
of the dialogue box.
11. `<wait duration="2"/>` makes the "game" wait for two seconds before
continuing to execute commands (or, in this case since this the last command
for the box, continuing to the next page).

All commands in [Dialogue Action Commands](DialogueActionCommands.md) should
be usable with the XML format. If you run into any problems, please let us know
so we can look further into it!
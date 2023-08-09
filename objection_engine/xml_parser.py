import xml.sax
from .parse_tags import (
    BaseDialogueItem,
    DialoguePage,
    DialogueTextChunk,
    DialogueAction,
    DialogueTextLineBreak
)

class Handler(xml.sax.ContentHandler):
    pages: list[DialoguePage] = []
    __current_page_contents: list[BaseDialogueItem] | None = None
    __color_stack: list[str] = []
    def __init__(self) -> None:
        self.pages = []
        self.__color_stack = []
        
    def startElement(self, name: str, attrs: xml.sax.xmlreader.AttributesImpl):
        attrs_dict = {n: attrs.getValue(n) for n in attrs.getNames()}
        if name == 'page':
            if self.__current_page_contents is None:
                self.__current_page_contents = []
            else:
                raise Exception("Pages cannot be nested")
        elif name == 'br':
            self.__current_page_contents.append(DialogueTextLineBreak())
        elif name == 'startblip':
            gender = attrs_dict.get('gender', 'male')
            self.__current_page_contents.append(DialogueAction(f"startblip {gender}", 0))
        elif name == 'stopblip':
            self.__current_page_contents.append(DialogueAction(f"stopblip", 0))
        elif name == 'sprite':
            position = attrs_dict.get('position')
            if position is None:
                raise Exception("`<sprite/>` tag needs `position` attribute")
            
            src = attrs_dict.get('src')
            if src is None:
                raise Exception("`<sprite/>` tag needs `src` attribute")
            
            self.__current_page_contents.append(DialogueAction(f"sprite {position} {src}", 0))
        elif name == 'wait':
            duration = attrs_dict.get('duration')
            if duration is None:
                raise Exception("`<wait/>` tag needs `duration` attribute")
            
            self.__current_page_contents.append(DialogueAction(f"wait {duration}", 0))
        elif name == 'bubble':
            type = attrs_dict.get('type', 'objection')
            character = attrs_dict.get('character', 'None')
            self.__current_page_contents.append(DialogueAction(f"bubble {type} {character}", 0))
            
        elif name == 'showarrow':
            self.__current_page_contents.append(DialogueAction("showarrow", 0))

        elif name == 'hidearrow':
            self.__current_page_contents.append(DialogueAction("hidearrow", 0))

        elif name == 'showbox':
            self.__current_page_contents.append(DialogueAction("showbox", 0))

        elif name == 'hidebox':
            self.__current_page_contents.append(DialogueAction("hidebox", 0))

        elif name == 'nametag':
            name_text = attrs_dict.get('text')
            if name_text is None:
                raise Exception("`<nametag/>` tag needs `text` attribute")
            
            self.__current_page_contents.append(DialogueAction(f"nametag {name_text}", 0))

        elif name == 'evidence':
            action = attrs_dict.get('action')
            if action is None:
                raise Exception("`<evidence/>` tag needs `action` attribute")
            
            if action == 'clear':
                self.__current_page_contents.append(DialogueAction(f"evidence clear", 0))
            else:
                src = attrs_dict.get('src')
                if src is None:
                    raise Exception("`<evidence/>` tag needs `src` attribute")
                
                self.__current_page_contents.append(DialogueAction(f"evidence {action} {src}", 0))

        elif name == 'sound':
            src = attrs_dict.get('src')
            if src is None:
                raise Exception("`<sound/>` tag needs `src` attribute")
            
            self.__current_page_contents.append(DialogueAction(f"sound {src}", 0))

        elif name == 'shake':
            magnitude_str = attrs_dict.get('magnitude')
            if magnitude_str is None:
                raise Exception("`<shake/>` tag needs `magnitude` attribute")
            
            duration_str = attrs_dict.get('duration')
            if duration_str is None:
                raise Exception("`<shake/>` tag needs `duration` attribute")
            
            self.__current_page_contents.append(DialogueAction(f"shake {magnitude_str} {duration_str}", 0))

        elif name == 'flash':
            duration_str = attrs_dict.get('duration')
            if duration_str is None:
                raise Exception("`<flash/>` tag needs `duration` attribute")
            
            self.__current_page_contents.append(DialogueAction(f"flash {duration_str}", 0))

        elif name == 'music':
            action = attrs_dict.get('action')
            if action is None:
                raise Exception("`<music/>` tag needs `action` attribute")
            if action not in ['start', 'stop']:
                raise Exception("`<music/>` tag's `action` attribute must be `\"start\"` or `\"stop\"`")
            
            if action == 'start':
                src = attrs_dict.get('src')
                if src is None:
                    raise Exception("`<music/>` tag needs `src` attribute")
                
                self.__current_page_contents.append(DialogueAction(f"music start {src}", 0))
            elif action == 'stop':
                self.__current_page_contents.append(DialogueAction(f"music stop", 0))

        elif name in ['cut', 'pan', 'show', 'hide']:
            position = attrs_dict.get('position')
            if position is None:
                raise Exception(f"`<{name}/>` tag needs `position` attribute")
            
            self.__current_page_contents.append(DialogueAction(f"{name} {position}", 0))

        elif name == 'verdict':
            action = attrs_dict.get('action')
            if action is None:
                raise Exception("`<verdict/>` tag needs `action` attribute")
            if action == 'set':
                new_text = attrs_dict.get('text')
                if new_text is None:
                    raise Exception("`<verdict action=\"set\"/>` tag needs `text` attribute")
                color = attrs_dict.get('color')
                if color is None:
                    raise Exception("`<verdict action=\"set\"/>` tag needs `color` attribute")
                self.__current_page_contents.append(DialogueAction(f"verdict set \"{new_text}\" {color}", 0))
            elif action == 'show':
                index = attrs_dict.get('index')
                if index is None:
                    raise Exception("`<verdict action=\"show\"/>` tag needs `index` attribute")
                self.__current_page_contents.append(DialogueAction(f"verdict show {index}", 0))
            elif action == 'clear':
                self.__current_page_contents.append(DialogueAction("verdict clear", 0))
            else:
                raise Exception("`<verdict/>` tag's `action` attribute must be `\"set\"`, `\"show\"`, or `\"clear\"`")
        
        elif name == 'font':
            color = attrs_dict.get('color')
            self.__color_stack.append(color)

    def endElement(self, name: str):
        if name == 'page':
            if isinstance(self.__current_page_contents, list):
                self.pages.append(DialoguePage(self.__current_page_contents))
                self.__current_page_contents = None
            elif self.__current_page_contents is None:
                raise Exception("Page must be started before it can end")
            
        elif name == 'font':
            self.__color_stack.pop()

    
    def characters(self, content: str):
        content = content.strip()
        if len(content) == 0:
            return
        content = content.replace('&nbsp;', ' ')
        tags = []
        if len(self.__color_stack) > 0:
            tags.append(self.__color_stack[-1])
        self.__current_page_contents.append(DialogueTextChunk(content, tags))
    
    def startDocument(self):
        self.pages = []
        self.__color_stack = []
        self.__current_page_contents = None
    
    def endDocument(self):
        return super().endDocument()
    

def parse_script(source_script: str) -> list[DialoguePage]:
    h = Handler()
    xml.sax.parse(source_script, h)
    return h.pages
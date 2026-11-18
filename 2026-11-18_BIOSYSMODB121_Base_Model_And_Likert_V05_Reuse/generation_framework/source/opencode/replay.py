"""Independent raw Responses SSE replay. No import of the live parser."""
import json, re

def replay(raw):
    frames=re.split(r'\r?\n\r?\n',raw.decode('utf-8'))
    delta=[]; final=None; terminal=None
    for frame in frames[:-1]:
        data=[]
        for line in frame.splitlines():
            if line.startswith('data:'):data.append(line[5:].removeprefix(' '))
        if not data:continue
        text='\n'.join(data)
        if text=='[DONE]':continue
        event=json.loads(text)
        if event.get('type')=='response.output_text.delta':delta.append(event['delta'])
        if event.get('type') in ('response.completed','response.failed','response.incomplete'):
            final=event.get('response',{}); terminal=event['type']
    final=final or {}; output=[]
    for item in final.get('output',[]):
        if item.get('type')=='message':
            for content in item.get('content',[]):
                if content.get('type')=='output_text':output.append(content['text'])
    return {'visible_answer':''.join(output) or ''.join(delta),'usage':final.get('usage'),'terminal':terminal}

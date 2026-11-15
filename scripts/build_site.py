#!/usr/bin/env python3
"""Compile a self-contained HTML research dashboard from versioned JSON files."""
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]

def js_json(path):
    x=json.loads(path.read_text(encoding='utf-8'))
    # Prevent data from closing the JSON script element; preserve unicode symbols.
    return json.dumps(x,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')

def build():
    template=(ROOT/'site.template.html').read_text(encoding='utf-8')
    bindings={
       '__TARGETS_JSON__':ROOT/'data/targets.json',
       '__LITERATURE_JSON__':ROOT/'data/literature.json',
       '__REFERENCES_JSON__':ROOT/'data/curated_references.json',
    }
    for name,file in bindings.items():
        assert template.count(name)==1, 'missing or duplicate placeholder: '+name
        template=template.replace(name,js_json(file))
    out=ROOT/'docs/index.html';out.parent.mkdir(exist_ok=True)
    out.write_text(template,encoding='utf-8')
    (ROOT/'docs/.nojekyll').touch()
    print('Built',out, 'bytes=',out.stat().st_size)

if __name__=='__main__':build()

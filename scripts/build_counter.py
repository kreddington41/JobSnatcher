#!/usr/bin/env python3
"""Build the in-page keyword counter for JobSnatcher.

Usage:
    python3 scripts/build_counter.py references/keywords/<set>.json > counter.js

The output is one self-contained JavaScript expression. Run it on a job
posting page (for example with a browser automation tool's "run JavaScript"
action). It returns a compact string:

    <word_count>|<theme_index>:<count>,<theme_index>:<count>,...|<top phrases>

Theme indexes refer to the order of "themes" in the JSON file, so
aggregate.py can turn the results into a ranked report.
"""
import json
import sys

STOPWORDS = (
    "the a an and or of to in for with on at by from as is are be our we you your will this that it its into "
    "across their they who what how about all can more not have has using use including work help well new such "
    "other through role team teams company job apply experience strong ability"
).split()


def build(keyword_file: str) -> str:
    data = json.load(open(keyword_file, encoding="utf-8"))
    patterns = [t["pattern"] for t in data["themes"]]
    return (
        "(async()=>{"
        "await new Promise(r=>setTimeout(r,1800));"
        "let t=document.body.innerText;"
        # LinkedIn job pages: keep only the job description, if the person pasted one there
        "if(location.host.includes('linkedin')){let i=t.indexOf('About the job');"
        "let j=t.indexOf('About the company',i);t=i>0?t.slice(i,j>0?j:i+9000):''}"
        "t=t.toLowerCase();"
        f"const R={json.dumps(patterns)};"
        f"const S=new Set({json.dumps(STOPWORDS)});"
        "let h=R.map((r,i)=>{let m=t.match(new RegExp('\\\\b(?:'+r+')','g'));"
        "return m?i+':'+m.length:null}).filter(x=>x).join(',');"
        "let w=t.replace(/[^a-z0-9\\-\\s]/g,' ').split(/\\s+/).filter(x=>x.length>2&&!S.has(x));"
        "let c={};for(let i=0;i<w.length-1;i++){let b=w[i]+' '+w[i+1];c[b]=(c[b]||0)+1}"
        "let top=Object.entries(c).filter(e=>e[1]>1).sort((a,b)=>b[1]-a[1]).slice(0,10)"
        ".map(e=>e[0]).join(';');"
        "return w.length+'|'+h+'|'+top})()"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(build(sys.argv[1]))

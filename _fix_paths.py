import sys,os,re
sys.stdout.reconfigure(encoding='utf-8')
base=r'https://github.com/error-wtf/ssz-qubits'
# Replacements: longest first to avoid partial matches
REPS=[
    (r'ssz-qubits/paper_final/figures  # https://github.com/error-wtf/ssz-qubits', 'ssz-qubits/paper_final/figures  # https://github.com/error-wtf/ssz-qubits'),
    (r'ssz-qubits/paper_final  # https://github.com/error-wtf/ssz-qubits', 'ssz-qubits/paper_final  # https://github.com/error-wtf/ssz-qubits'),
    (r'https://github.com/error-wtf/ssz-qubits/tree/main/outputs/', 'https://github.com/error-wtf/ssz-qubits/tree/main/outputs/'),
    (r'https://github.com/error-wtf/ssz-qubits/', 'https://github.com/error-wtf/ssz-qubits/'),
    (r'https://github.com/error-wtf/ssz-qubits', 'https://github.com/error-wtf/ssz-qubits'),
    (r'https://github.com/error-wtf/ssz-metric-pure/blob/main/src/ssz_core/segment_density.py', 'https://github.com/error-wtf/ssz-metric-pure/blob/main/src/ssz_core/segment_density.py'),
    (r'https://github.com/error-wtf/ssz-metric-pure', 'https://github.com/error-wtf/ssz-metric-pure'),
    (r'https://github.com/error-wtf/Segmented-Spacetime-Mass-Projection-Unified-Results', 'https://github.com/error-wtf/Segmented-Spacetime-Mass-Projection-Unified-Results'),
    (r'https://github.com/error-wtf/segmented-energy', 'https://github.com/error-wtf/segmented-energy'),
    (r'SSZ_QUBIT_PAPERS', 'SSZ_QUBIT_PAPERS'),
    (r"SSZ_QUBIT_PAPERS", 'SSZ_QUBIT_PAPERS'),
]
# For .py files, handle raw strings differently
PY_REPS=[
    (r"os.path.join(SCRIPT_DIR, '..', 'QUBITS')  # was SSZ_QUBIT_PAPERS", "os.path.join(SCRIPT_DIR, '..', 'QUBITS')  # was E:\\clone\\SSZ_QUBIT_PAPERS"),
]
total=0
for root,dirs,files in os.walk(base):
    dirs[:]=[d for d in dirs if d!='.git']
    for f in files:
        if not f.endswith(('.md','.py','.txt')): continue
        fp=os.path.join(root,f)
        with open(fp,encoding='utf-8',errors='replace') as fh:
            txt=fh.read()
        orig=txt
        if f.endswith('.py'):
            for old,new in PY_REPS:
                txt=txt.replace(old,new)
        for old,new in REPS:
            txt=txt.replace(old,new)
        if txt!=orig:
            with open(fp,'w',encoding='utf-8') as fh:
                fh.write(txt)
            rel=os.path.relpath(fp,base)
            c=sum(1 for a,b in zip(orig,txt) if a!=b)
            print(f'  {rel}')
            total+=1
print(f'Total: {total} files fixed')
# verify
rem=0
for root,dirs,files in os.walk(base):
    dirs[:]=[d for d in dirs if d!='.git']
    for f in files:
        if not f.endswith(('.md','.py','.txt')): continue
        fp=os.path.join(root,f)
        with open(fp,encoding='utf-8',errors='replace') as fh:
            txt=fh.read()
        c=txt.count('E:\\clone')
        if c>0:
            rel=os.path.relpath(fp,base)
            print(f'  REMAINING: {rel} ({c})')
            rem+=c
print(f'Remaining E:\\clone: {rem}')

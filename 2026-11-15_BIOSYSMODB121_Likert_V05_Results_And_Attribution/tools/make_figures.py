"""Generate shareable figures exclusively from the released tables."""
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def read(name):
    with(ROOT/'data'/name).open()as f:return list(csv.DictReader(f,delimiter='\t'))


def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from matplotlib.colors import TwoSlopeNorm
    import numpy as np
    out=ROOT/'figures';out.mkdir(exist_ok=True)
    try:fontpath=font_manager.findfont('Times New Roman',fallback_to_default=False);family='Times New Roman'
    except ValueError:fontpath=font_manager.findfont('DejaVu Serif',fallback_to_default=False);family='DejaVu Serif'
    plt.rcParams.update({'font.family':family,'font.size':10,'pdf.fonttype':42})
    change=read('FOUR_MODEL_DIMENSION_CHANGE_28.tsv')
    models=['Kimi','GLM','Qwen','DeepSeek'];dims=['D1','D2','D3a','D3b','D4','D5','D6']
    vals=np.array([[float(next(x['mean_delta']for x in change if x['model_display']==m and x['dimension']==d))for d in dims]for m in models])
    limit=max(1,float(np.abs(vals).max()))
    fig,ax=plt.subplots(figsize=(9.4,4.0))
    im=ax.imshow(vals,cmap='RdBu',norm=TwoSlopeNorm(vmin=-limit,vcenter=0,vmax=limit),aspect='auto')
    ax.set_xticks(range(7),dims);ax.set_yticks(range(4),models)
    for i in range(4):
        for j in range(7):
            ax.text(j,i,f'{vals[i,j]:+.2f}',ha='center',va='center',color='white'if abs(vals[i,j])>.55*limit else'black')
    ax.set_title('V0.5 minus V0.4: mean dimension score change')
    fig.colorbar(im,ax=ax,label='Score change (1–10 dimension scale)')
    fig.text(.5,.025,'480 paired answers / 120 cases; two reference cases corrected; AI ratings; human validity pending',ha='center',fontsize=8)
    fig.tight_layout(rect=(0,.06,1,1))
    for ext in ['png','pdf']:fig.savefig(out/f'v04_v05_dimension_change.{ext}',dpi=180,bbox_inches='tight')
    plt.close(fig)
    scores=read('LIKERT_V05_SCORES_726.tsv')
    models=['GLM','DeepSeek','Kimi','Qwen','Grok','GPT5.6']
    scored=[];missing=[];interrupted=[]
    for m in models:
        g=[x for x in scores if x['model_display']==m]
        scored.append(sum(x['likert_status']=='COMPARABLE'for x in g))
        interrupted.append(sum(x['likert_status']!='COMPARABLE'and x['case_id']=='BIOPATH150_145'for x in g))
        missing.append(121-scored[-1]-interrupted[-1])
    fig,ax=plt.subplots(figsize=(9.4,4))
    ax.barh(models,scored,label='Scored',color='#315c87')
    ax.barh(models,missing,left=scored,label='No usable original answer',color='#a7abb1')
    left=[a+b for a,b in zip(scored,missing)]
    ax.barh(models,interrupted,left=left,label='Scoring stream interrupted',color='#e3a247')
    for i,n in enumerate(scored):ax.text(2,i,f'{n}/121',va='center',ha='left',color='white')
    ax.set_xlim(0,124);ax.set_xlabel('Original question positions (121 per model)')
    ax.set_title('Scoring coverage: 723/726 positions; common scope = 118 cases')
    ax.invert_yaxis();ax.legend(loc='upper center',bbox_to_anchor=(.5,-.19),ncol=3,fontsize=8)
    fig.tight_layout()
    for ext in ['png','pdf']:fig.savefig(out/f'scoring_coverage.{ext}',dpi=180,bbox_inches='tight')
    plt.close(fig)
    (out/'FIGURE_METADATA.json').write_text(json.dumps(dict(font_family=family,font_file_name=Path(fontpath).name,
        matplotlib_version=matplotlib.__version__,numpy_version=np.__version__,
        requested_font='Times New Roman',requested_font_available=family=='Times New Roman',
        fallback_disclosed=True,data_source='released TSV only',new_model_calls=0),indent=2)+'\n')
    print(json.dumps(dict(figures=4,font_family=family,new_calls=0)))


if __name__=='__main__':main()

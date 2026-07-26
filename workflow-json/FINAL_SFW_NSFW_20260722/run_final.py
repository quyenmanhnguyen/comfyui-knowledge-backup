import csv,json,subprocess,time,urllib.request,uuid
from pathlib import Path
ROOT=Path(r'C:\AI');DIR=ROOT/r'workflows\FINAL_SFW_NSFW_20260722';PY=ROOT/r'python_embeded\python.exe';CTL=ROOT/r'workflows\BENCH_CONTROLLED_20260719\bench_matrix.py';SERVER='http://127.0.0.1:8188';SEED=7229001
REAL_SFW='Premium editorial fashion photograph, one clearly adult Vietnamese woman age 25, youthful soft oval face, natural warm brown eyes, long glossy dark hair, graceful three-quarter full-body portrait walking beside a rain-washed modern gallery at blue hour, tailored black silk blazer over an ivory satin midi dress, both complete hands visible and separated, bright diffused key light with clean white bounce fill, luminous healthy neutral-warm skin, fine pores, peach fuzz, subtle natural blush, realistic hair and silk, restrained teal and warm gold reflections, 85mm lens, shallow depth of field, sophisticated clean composition, no text'
REAL_NUDE='Fine-art studio photograph, one clearly adult Vietnamese woman age 29, solo, completely nude nonsexual full-body figure study, relaxed standing contrapposto, both complete hands visible and separated at her sides, both feet fully visible, youthful soft oval face, natural adult anatomy and balanced proportions, long dark hair, bright diffused north-window key light with white bounce fill, evenly exposed luminous neutral-warm skin, fine pores, peach fuzz and subtle tonal variation, 85mm lens, seamless warm-grey background, restrained museum photography, no props, no clothing, no text'
RNEG='child, teen, underage, elderly, gaunt, grey skin, orange skin, dark face, underexposed, waxy, plastic, airbrushed, deformed hands, extra fingers, fused fingers, missing fingers, extra limbs, malformed feet, duplicate, text, logo, watermark, worst quality, low quality'
AN_SFW='masterwork, masterpiece, best quality, detailed, high detail, very aesthetic, depth of field, dynamic angle, adult, aged up, 1girl, solo, clearly adult woman age 25, beautiful soft oval face, natural warm brown eyes, long dark brown hair, elegant ivory silk blouse and fitted black midi skirt, graceful three-quarter full-body fashion portrait walking through a bright botanical conservatory, both complete hands visible and separated, soft golden daylight, clean warm skin shading, detailed hair and fabric, balanced composition'
AN_NUDE='masterwork, masterpiece, best quality, detailed, high detail, very aesthetic, adult, aged up, 1girl, solo, clearly adult woman age 27, completely nude, tasteful nonsexual full-body fine-art figure study, relaxed standing contrapposto, both complete hands visible and separated at her sides, both feet visible, natural mature proportions, soft oval face, warm brown eyes, long dark hair, bright diffused studio daylight, warm grey seamless background, clean subtle skin shading'
ANEG='lowres, worst quality, low quality, bad anatomy, bad hands, extra fingers, fused fingers, missing fingers, extra limbs, malformed feet, clothing, dress, towel, censored, jpeg artifacts, signature, watermark, text, logo, child, teen, loli, young-looking'
def req(path,payload=None,timeout=30):
 data=json.dumps(payload).encode() if payload is not None else None;q=urllib.request.Request(SERVER+path,data=data,headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(q,timeout=timeout) as r:raw=r.read();return json.loads(raw) if raw else {}
def stop():subprocess.run([str(PY),str(CTL),'stop'],check=False,stdout=subprocess.DEVNULL)
def start():subprocess.run([str(PY),str(CTL),'start','--mode','pytorch'],check=True,stdout=subprocess.DEVNULL)
def zflow(tag,model,steps):
 return {'1':{'class_type':'UNETLoader','inputs':{'unet_name':model,'weight_dtype':'default'}},'2':{'class_type':'CLIPLoader','inputs':{'clip_name':'qwen_3_4b.safetensors','type':'lumina2','device':'cpu'}},'3':{'class_type':'VAELoader','inputs':{'vae_name':'ae.safetensors'}},'4':{'class_type':'CLIPTextEncode','inputs':{'clip':['2',0],'text':REAL_SFW}},'5':{'class_type':'ConditioningZeroOut','inputs':{'conditioning':['4',0]}},'6':{'class_type':'EmptyLatentImage','inputs':{'width':576,'height':800,'batch_size':1}},'7':{'class_type':'ModelSamplingAuraFlow','inputs':{'model':['1',0],'shift':3}},'8':{'class_type':'KSampler','inputs':{'model':['7',0],'positive':['4',0],'negative':['5',0],'latent_image':['6',0],'seed':SEED,'steps':steps,'cfg':1,'sampler_name':'res_2s','scheduler':'beta57','denoise':1}},'9':{'class_type':'VAEDecode','inputs':{'samples':['8',0],'vae':['3',0]}},'10':{'class_type':'SaveImage','inputs':{'images':['9',0],'filename_prefix':'FINAL-'+tag}}}
def xlflow(tag,ckpt,steps,cfg,sampler,sched,w,h,lora=None,strength=0,real=False):
 p={'1':{'class_type':'CheckpointLoaderSimple','inputs':{'ckpt_name':ckpt}},'2':{'class_type':'CLIPTextEncode','inputs':{'clip':['1',1],'text':REAL_SFW if real else AN_SFW}},'3':{'class_type':'CLIPTextEncode','inputs':{'clip':['1',1],'text':RNEG if real else ANEG}},'4':{'class_type':'EmptyLatentImage','inputs':{'width':w,'height':h,'batch_size':1}},'6':{'class_type':'KSampler','inputs':{'model':['1',0],'positive':['2',0],'negative':['3',0],'latent_image':['4',0],'seed':SEED,'steps':steps,'cfg':cfg,'sampler_name':sampler,'scheduler':sched,'denoise':1}},'7':{'class_type':'VAEDecode','inputs':{'samples':['6',0],'vae':['1',2]}},'8':{'class_type':'SaveImage','inputs':{'images':['7',0],'filename_prefix':'FINAL-'+tag}}}
 if not real:
  p['10']={'class_type':'CLIPSetLastLayer','inputs':{'clip':['1',1],'stop_at_clip_layer':-2}};p['2']['inputs']['clip']=['10',0];p['3']['inputs']['clip']=['10',0]
 if lora:
  p['9']={'class_type':'LoraLoader','inputs':{'model':['1',0],'clip':['1',1],'lora_name':lora,'strength_model':strength,'strength_clip':strength}};p['6']['inputs']['model']=['9',0];p['10']['inputs']['clip']=['9',1]
 return p
def anima(tag,extra=None,strength=.6):
 p={'1':{'class_type':'UNETLoader','inputs':{'unet_name':'animayume_v10.safetensors' if not extra else 'anima_baseV10.safetensors','weight_dtype':'default'}},'2':{'class_type':'LoraLoaderModelOnly','inputs':{'model':['1',0],'lora_name':'anima-turbo-lora-v0.2.safetensors','strength_model':1}},'5':{'class_type':'CLIPLoader','inputs':{'clip_name':'qwen_3_06b_base.safetensors','type':'stable_diffusion','device':'default'}},'6':{'class_type':'VAELoader','inputs':{'vae_name':'qwen_image_vae.safetensors'}},'7':{'class_type':'CLIPTextEncode','inputs':{'clip':['5',0],'text':AN_SFW}},'8':{'class_type':'EmptyLatentImage','inputs':{'width':768,'height':1024,'batch_size':1}},'9':{'class_type':'RandomNoise','inputs':{'noise_seed':SEED}},'10':{'class_type':'BasicGuider','inputs':{'model':['2',0],'conditioning':['7',0]}},'11':{'class_type':'SamplerSPEED','inputs':{'base_sampler':'er_sde','transform':'dct','mode':'delta_optimal','model_preset':'flux','scales':'0.5,1.0','delta':.01,'manual_sigmas':'0.85','spectrum_A':203.615097,'spectrum_beta':1.915461,'seed':SEED}},'12':{'class_type':'BasicScheduler','inputs':{'model':['2',0],'scheduler':'simple','steps':16,'denoise':1}},'13':{'class_type':'SamplerCustomAdvanced','inputs':{'noise':['9',0],'guider':['10',0],'sampler':['11',0],'sigmas':['12',0],'latent_image':['8',0]}},'14':{'class_type':'VAEDecode','inputs':{'samples':['13',0],'vae':['6',0]}},'15':{'class_type':'SaveImage','inputs':{'images':['14',0],'filename_prefix':'FINAL-'+tag}}}
 if extra:p['3']={'class_type':'LoraLoaderModelOnly','inputs':{'model':['2',0],'lora_name':extra,'strength_model':strength}};p['10']['inputs']['model']=['3',0];p['12']['inputs']['model']=['3',0]
 return p
CASES=[('Z01_BEYOND',zflow('Z01','china_community\\beyondREALITY_V30_CIVITAI_BF16.safetensors',12),'z'),('Z02_MOODY',zflow('Z02','moodyProMix_zitV13.safetensors',12),'z'),('Z03_DIVING',zflow('Z03','divingZImageTurbo_v70Fp16.safetensors',10),'z'),('R04_INTO',xlflow('R04','intorealismUltra_sdxlV1NoLightning.safetensors',35,4.5,'dpmpp_sde','karras',896,1152,real=True),'real'),('A05_RIMIX',xlflow('A05','aMixIllustrious_aMix.safetensors',30,7,'euler_ancestral','normal',768,1152,'rimixxO2.safetensors',.65),'anime'),('A06_FAB',xlflow('A06','fabricatedXL_v70.safetensors',28,6,'euler_ancestral','normal',768,1152),'anime'),('N07_YUME',anima('N07'),'anima'),('N08_NIJI',anima('N08','Niji_semi_realism_v5.safetensors',.6),'anima')]
def run(tag,p):
 (DIR/f'{tag}.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8');t=time.time()
 try:
  q=req('/prompt',{'prompt':p,'client_id':str(uuid.uuid4())})
  if q.get('node_errors'):return 'node_error',0,'',json.dumps(q['node_errors'])[:700]
  pid=q['prompt_id']
  while time.time()-t<240:
   e=req('/history/'+pid,timeout=10).get(pid)
   if e and e.get('status',{}).get('completed'):
    fs=[im['filename'] for o in e.get('outputs',{}).values() for im in o.get('images',[])];return 'ok',round(time.time()-t,1),fs[0] if fs else '',''
   if e and e.get('status',{}).get('status_str')=='error':return 'error',round(time.time()-t,1),'',json.dumps(e['status'])[:700]
   time.sleep(2)
  try:req('/interrupt',{},5)
  except:pass
  return 'timeout',240,'','limit'
 except Exception as e:return 'exception',round(time.time()-t,1),'',repr(e)
def main():
 DIR.mkdir(parents=True,exist_ok=True);rows=[]
 for i,(name,base,fam) in enumerate(CASES):
  stop();start()
  for mode in ('SFW','NSFW'):
   p=json.loads(json.dumps(base));isn=mode=='NSFW'
   if fam=='z':p['4']['inputs']['text']=REAL_NUDE if isn else REAL_SFW;p['8']['inputs']['seed']=SEED+i*10+isn
   elif fam=='real':p['2']['inputs']['text']=REAL_NUDE if isn else REAL_SFW;p['6']['inputs']['seed']=SEED+i*10+isn
   elif fam=='anime':p['2']['inputs']['text']=AN_NUDE if isn else AN_SFW;p['6']['inputs']['seed']=SEED+i*10+isn
   else:p['7']['inputs']['text']=AN_NUDE if isn else AN_SFW;p['9']['inputs']['noise_seed']=SEED+i*10+isn;p['11']['inputs']['seed']=SEED+i*10+isn
   save=next(k for k,v in p.items() if v['class_type']=='SaveImage');p[save]['inputs']['filename_prefix']=f'FINAL-{name}-{mode}'
   st,sec,img,note=run(f'{name}_{mode}',p);row={'workflow':name,'family':fam,'mode':mode,'state':st,'elapsed_s':sec,'image':img,'note':note};rows.append(row);print(row,flush=True)
   with (DIR/'results.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=row.keys());w.writeheader();w.writerows(rows)
 stop()
if __name__=='__main__':main()

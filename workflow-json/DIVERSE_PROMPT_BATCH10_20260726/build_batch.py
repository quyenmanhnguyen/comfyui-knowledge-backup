import json
from pathlib import Path

ROOT = Path(r"C:\AI\workflows\DIVERSE_PROMPT_BATCH10_20260726")
ROOT.mkdir(parents=True, exist_ok=True)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def set_pos(g, text):
    for node in g.values():
        if isinstance(node, dict) and node.get("class_type") == "CLIPTextEncode":
            old = str(node.get("inputs", {}).get("text", "")).lower()
            if "lowres" not in old and "worst quality" not in old:
                node["inputs"]["text"] = text
                return


def set_neg(g, add):
    for node in g.values():
        if isinstance(node, dict) and node.get("class_type") == "CLIPTextEncode":
            old = str(node.get("inputs", {}).get("text", ""))
            if "lowres" in old.lower() or "worst quality" in old.lower():
                node["inputs"]["text"] = old + ", " + add
                return


def set_seed_prefix(g, seed, prefix):
    for node in g.values():
        if not isinstance(node, dict):
            continue
        inp = node.get("inputs", {})
        if node.get("class_type") == "KSampler":
            inp["seed"] = seed
        if node.get("class_type") == "RandomNoise":
            inp["noise_seed"] = seed
        if node.get("class_type") == "SaveImage":
            inp["filename_prefix"] = prefix


def save(prefix, src, text, seed, neg_extra):
    g = load(src)
    set_pos(g, text)
    set_neg(g, neg_extra)
    set_seed_prefix(g, seed, prefix)
    p = ROOT / f"{prefix}.json"
    p.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    print(p)


NEG_PHOTO = "child, teen, loli, young-looking, old face, grey skin, muddy skin, oily blur, waxy skin, plastic skin, smeared skin, bad eyes, crossed eyes, malformed face, bad hands, fused fingers, extra fingers, extra hands, disembodied hands, pov hands, fake text, watermark"
NEG_ANIME = "child, teen, loli, young-looking, lowres, bad anatomy, bad hands, extra hands, pov hands, disembodied hands, malformed eyes, dead eyes, waxy skin, muddy color, oil painting smear, fake text, watermark"

Z_MOODY = r"C:\AI\workflows\ZIMAGE_FINAL10_MAIN_20260725\MAIN_ZIMAGE_MOODY_RES2S.json"
Z_DIVING = r"C:\AI\workflows\ZIMAGE_FINAL10_MAIN_20260725\01_Z1_DIVING_RES2S_SFW.json"
Z_BEYOND = r"C:\AI\workflows\ZIMAGE_FINAL10_MAIN_20260725\03_Z2_BEYOND_RES2S_SFW.json"
INTO = r"C:\AI\workflows\HISTORICAL_WINNER_RECOVERY_20260722\SDXL_INTO_AUTHOR.json"
REALVIS = r"C:\AI\workflows\HISTORICAL_WINNER_RECOVERY_20260722\SDXL_REALVIS_SDE.json"
RIMIX = r"C:\AI\workflows\TELEGRAM_PHOTO_DIRECTION_20260726\TG_SDXL_RIMIX065_WINDOW_CINEMATIC.json"
ONEOBS = r"C:\AI\workflows\TG_CIVITAI_ADV_CINEMATIC_20260724\S4_ONEOBSESSION_CINEMATIC_NSFW.json"
ANIMA = r"C:\AI\workflows\TELEGRAM_PHOTO_DIRECTION_20260726\TG_ANIMA_RIMIX_ALPHA_LAYERED_CINEMATIC.json"
HASSAKU = r"C:\AI\workflows\STYLE_EXPANSION_CIVITAI_TG_20260724\B4_HASSAKU_V34.json"

photo_prompts = [
    ("DP10-01_Z_MOODY_HIGHKEY_WHITE", Z_MOODY, 72629101,
     "High-key premium beauty photograph, one clearly adult Vietnamese woman age 30, bright white daylight studio, clean cream backdrop, standing three-quarter from head to mid-thigh, fresh soft oval face, natural brown eyes, small confident smile, long glossy black hair, healthy full curvy figure, open ivory satin blouse and fitted white skirt, both hands visible: left hand lightly touches her waist, right hand holds the blouse cuff, separated fingers, crisp eyelashes and hair strands, luminous neutral-warm skin with fine pores and peach fuzz, white bounce fill, 85mm lens, shallow depth, no blue cast"),
    ("DP10-02_Z_MOODY_STREET_FLASH", Z_MOODY, 72629102,
     "Editorial street fashion photograph after rain, one clearly adult East Asian woman age 31, walking toward camera on a clean wet shopping street, black tailored blazer over ivory silk dress, youthful bright face, clear eyes, glossy moving hair, full soft body proportions, both hands visible and relaxed at her sides, fingers separated, bright storefront fill, soft on-camera fashion flash, natural skin pores, crisp jacket and silk texture, 70mm lens, background bokeh, clean saturated but not dark"),
    ("DP10-03_Z_DIVING_MORNING_WINDOW", Z_DIVING, 72629103,
     "Natural bright morning window portrait, one clearly adult Vietnamese woman age 29, seated sideways on a wooden chair in a minimal white room, soft fresh face, clear brown eyes, gentle direct expression, black hair tucked behind one ear, white linen shirt draped loosely and cream skirt, full healthy figure, left hand on chair back, right hand resting on knee, exact two hands visible, fine pores, peach fuzz, subtle blush, realistic linen wrinkles, airy sunlight, 85mm lens"),
    ("DP10-04_Z_BEYOND_CLEAN_STUDIO", Z_BEYOND, 72629104,
     "Clean studio editorial photograph, one clearly adult Southeast Asian woman age 32, standing against pale warm grey seamless paper, soft youthful mature face, direct calm gaze, long dark hair with natural flyaways, healthy fuller hips and soft waist, minimal ivory silk wrap dress, left hand at hip, right hand holding the wrap edge, both hands fully visible, crisp skin pores and tonal variation, bright softbox key, white reflector fill, 85mm lens, natural anatomy and material texture"),
    ("DP10-05_SDXL_INTO_BRIGHT_PORTRAIT", INTO, 72629105,
     "Premium bright editorial photograph of one clearly adult Vietnamese woman age 30 in a sunlit white apartment, head-to-thigh portrait, soft oval youthful face, natural brown eyes, relaxed confident smile, long black hair, healthy full curvy proportions, ivory satin blouse open at collar and fitted cream skirt, left hand resting on window frame, right hand holding a pearl necklace, separated natural fingers, luminous neutral-warm skin with visible fine pores, peach fuzz, subtle blush, crisp fabric, 85mm lens, clean background"),
    ("DP10-06_SDXL_REALVIS_SKIN", REALVIS, 72629106,
     "Natural high-resolution beauty photograph, one clearly adult East Asian woman age 31, seated near a large white window in a modern studio, fresh youthful mature face, clear eyes, soft smile, black hair in loose waves, healthy fuller figure, white silk robe loosely tied, left hand on lap, right hand on window sill, exact two hands visible, realistic skin pores, soft peach fuzz, subtle tonal variation, bright diffused daylight, 70mm lens, clean composition"),
]

anime_prompts = [
    ("DP10-07_RIMIX_DAYLIGHT_CHARM", RIMIX, 72629107,
     "masterwork, masterpiece, best quality, detailed, high detail, very aesthetic, adult woman age 29, bright semi-real anime glamour portrait, soft oval face, brown eyes, warm confident smile, long black hair with airy strands, voluptuous soft-curvy figure, ivory satin blouse and cream skirt, sunlit white apartment, pearl earrings, left hand at waist, right hand touching hair, separated fingers, luminous skin, crisp hair and fabric, clean daylight, shallow depth of field"),
    ("DP10-08_ONEOBS_PINK_STUDIO", ONEOBS, 72629108,
     "masterwork, masterpiece, best quality, detailed, high detail, very aesthetic, adult woman age 29, expressive semi-real anime close portrait, glossy black hair with bangs, brown emotional eyes, soft confident gaze, very full soft-curvy figure, pale blush-pink studio lounge, ivory silk wrap, pearl choker, warm key light, white bounce fill, her left hand on sofa cushion, her right hand resting on her thigh, separated fingers, crisp hair highlights, clean luminous skin, elegant mood"),
    ("DP10-09_ANIMA_RIMIX_GOLD_WINDOW", ANIMA, 72629109,
     "masterpiece, best quality, very aesthetic, detailed cinematic anime illustration, adult woman age 30, warm golden daylight window scene, soft oval face, brown eyes, gentle confident smile, long black hair flowing over shoulder, voluptuous soft-curvy figure, ivory silk dress, pearl earrings, standing near a white curtain, left hand holding curtain edge, right hand resting on waist, separated fingers, clean bright skin, rich hair detail, elegant cinematic depth"),
    ("DP10-10_HASSAKU_CLEAN_ANIME", HASSAKU, 72629110,
     "masterpiece, best quality, very aesthetic, adult woman age 29, clean bright anime fashion portrait, soft pretty mature face, brown eyes, long black hair, healthy curvy body, white blouse and black pencil skirt, standing in a sunny modern boutique, left hand holding handbag strap, right hand relaxed at side, separated fingers, glossy hair, clean skin, crisp fabric, warm daylight, shallow depth of field"),
]

for prefix, src, seed, text in photo_prompts:
    save(prefix, src, text, seed, NEG_PHOTO)
for prefix, src, seed, text in anime_prompts:
    save(prefix, src, text, seed, NEG_ANIME)

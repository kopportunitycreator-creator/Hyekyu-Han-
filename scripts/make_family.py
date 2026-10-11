import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"expected {count} of {old!r}, found {n}")
    s = s.replace(old, new)

# ---- HTML ----
rep("<title>해린이네 식탁</title>", "<title>우리 집 식탁</title>")
rep("""      <h1>해린이네 식탁</h1>
      <div class="family">
        <span class="chip">엄마 · 아빠</span>
        <span class="chip kid">해린 48개월</span>
        <span class="chip">계성유치원 · 메이플베어 월·수</span>
      </div>""", """      <h1>우리 집 식탁</h1>
      <div class="family" id="familyChips"></div>""")
rep("한 달에 한 번, 계성유치원 식단표와 메이플베어 간식표를", "한 달에 한 번, 유치원·어린이집 식단표와 방과후 수업 간식표(있으면)를")
rep('<label for="lunchText">계성유치원 식단표', '<label for="lunchText"><span class="kName">유치원</span> 식단표')
rep('<label for="mbText">메이플베어 간식표 <span class="hint">월·수</span></label>', '<label for="mbText"><span class="xName">방과후 수업</span> 간식표 <span class="hint" id="xDaysHint">있는 경우만</span></label>')
rep('aria-selected="false">우리 집 취향</button>', 'aria-selected="false">우리 가족·취향</button>')
rep("""    <h2>우리 집 취향</h2>
    <p class="muted small">입력하면 바로 저장되고, 식단을 짤 때마다 반영돼요.</p>
    <div class="prefs-grid">
""", """    <h2>우리 가족·취향</h2>
    <p class="muted small">입력하면 바로 저장되고, 식단을 짤 때마다 반영돼요. 여기 적은 내용은 내 계정에만 저장되고 링크를 받은 다른 사람에게는 보이지 않아요.</p>
    <div class="prefs-grid">
      <div class="card">
        <span class="who">우리 가족</span>
        <div class="field"><label for="adults">어른 수</label><div style="display:flex;align-items:center;gap:8px"><input type="number" id="adults" min="1" max="8" step="1" placeholder="2"> <span>명</span></div></div>
        <div class="field"><label for="kids">아이 이름·나이 <span class="hint">여러 명이면 쉼표로</span></label><input type="text" id="kids" placeholder="예) 서윤 5살, 도윤 20개월"></div>
        <div class="field"><label for="kinderName">유치원·어린이집 이름</label><input type="text" id="kinderName" placeholder="예) 햇살유치원"></div>
      </div>
      <div class="card">
        <span class="who">방과후 수업 간식</span>
        <p class="muted small">유치원 끝나고 간식을 주는 수업이 있으면 적어주세요. 그 요일엔 집 간식을 빼고, 그 간식과도 겹치지 않게 짜요.</p>
        <div class="field"><label for="extraName">수업 이름</label><input type="text" id="extraName" placeholder="예) 영어 놀이반 (없으면 비워두세요)"></div>
        <div class="field"><span class="lab">간식 주는 요일</span>
          <div class="summary" id="extraDaysBox"></div>
        </div>
      </div>
""")
rep('<span class="who">해린</span>', '<span class="who kLabel">아이</span>')
rep('<span class="who">남편</span>', '<span class="who">배우자</span>')
s = s.replace("haerinLikes", "kidLikes").replace("haerinDislikes", "kidDislikes")

# ---- JS: storage (private per account) ----
rep('localStorage.getItem("hr:" + k)', 'localStorage.getItem("ft:" + k)')
rep('localStorage.setItem("hr:" + k, JSON.stringify(v))', 'localStorage.setItem("ft:" + k, JSON.stringify(v))')
rep('localStorage.setItem("hr:tab", t)', 'localStorage.setItem("ft:tab", t)')
rep('localStorage.getItem("hr:tab")', 'localStorage.getItem("ft:tab")')
rep("  let db = null;\n", "  let db = null, uid = null;\n  // 각자 계정의 비공개 공간(data/users/<id>)에 저장: 같은 링크를 여러 집이 써도 섞이지 않음\n  const dbPath = (p) => `data/users/${uid}/${p.replace(\"/\", \"_\")}`;\n")
rep("db.doc(path)", "db.doc(dbPath(path))", 3)
rep('    [db, sample] = await Promise.all([use("db"), use("sample")]);',
    '    let user;\n    [db, sample, user] = await Promise.all([use("db"), use("sample"), use("user")]);\n    uid = user ? await user.id().catch(() => null) : null;\n    if (!uid) db = null;')

# ---- JS: family settings ----
rep('const PREF_IDS = ["kidLikes",', 'const PREF_IDS = ["adults", "kids", "kinderName", "extraName", "kidLikes",')
rep("""    PREF_IDS.forEach((k) => { const n = $(k); if (document.activeElement !== n) n.value = settings[k] ?? ""; });
""", """    PREF_IDS.forEach((k) => { const n = $(k); if (document.activeElement !== n) n.value = settings[k] ?? ""; });
    DAYS.slice(0, 5).forEach((_, i) => { const c = $("xd" + i); if (c) c.checked = extraDays().includes(i); });
    applyFamilyLabels();
""")
rep("""  const cookMin = () => Number(settings.cookMin) || 30;
""", """  const cookMin = () => Number(settings.cookMin) || 30;
  const adults = () => Number(settings.adults) || 2;
  const kidsText = () => settings.kids || "";
  const kName = () => settings.kinderName || "유치원";
  const xName = () => settings.extraName || "방과후 수업";
  const extraDays = () => (settings.extraName && Array.isArray(settings.extraDays) ? settings.extraDays : []);
  const xDaysLabel = () => extraDays().map((i) => DAYS[i]).join("·");
  const familyShort = () => `어른 ${adults()} + ${kidsText() || "아이"}`;
  const servesRule = () => `한 끼에 어른 ${adults()}명 + 아이(${kidsText() || "나이 정보 없음"}). 아이 몫은 나이에 맞게 어른의 약 0.3~0.7배로 잡아 한 끼 총량을 정하고, 재료가 남지 않게 딱 맞게.`;
  function applyFamilyLabels() {
    const chips = $("familyChips"); chips.replaceChildren();
    chips.append(el("span", "chip", `어른 ${adults()}`));
    if (kidsText()) chips.append(el("span", "chip kid", kidsText()));
    chips.append(el("span", "chip", kName() + (settings.extraName ? ` · ${xName()} ${xDaysLabel()}` : "")));
    document.querySelectorAll(".kName").forEach((n) => (n.textContent = kName()));
    document.querySelectorAll(".xName").forEach((n) => (n.textContent = xName()));
    document.querySelectorAll(".kLabel").forEach((n) => (n.textContent = (kidsText().split(/[ ,]/)[0]) || "아이"));
    $("xDaysHint").textContent = xDaysLabel() || "있는 경우만";
  }
  // 방과후 간식 요일 체크박스
  DAYS.slice(0, 5).forEach((d, i) => {
    const lab = el("label", "chip"); const c = el("input"); c.type = "checkbox"; c.id = "xd" + i;
    c.onchange = async () => {
      const days = DAYS.slice(0, 5).map((_, j) => j).filter((j) => $("xd" + j).checked);
      settings = { ...settings, extraDays: days };
      try { await store.set("settings/family", settings); $("prefsSaved").textContent = "저장됨"; } catch { $("prefsSaved").textContent = "저장하지 못했어요."; }
      setTimeout(() => ($("prefsSaved").textContent = ""), 2000);
      applyFamilyLabels(); renderWeekTab(); renderMonth();
    };
    lab.append(c, " " + d); $("extraDaysBox").append(lab);
  });
""")
rep('if (meal === "snack") return [1, 3, 4].includes(i);  // 화·목·금 (월·수는 메이플베어 간식)',
    'if (meal === "snack") return i <= 4 && !extraDays().includes(i);  // 평일 중 방과후 간식이 없는 날')

# ---- JS: labels ----
rep('`어른 2 + 해린 1 (약 2.5인분)${r.min', '`${familyShort()}${r.min')
rep('"해린이 몫 · " + r.kidTip', '"아이 몫 · " + r.kidTip')
rep('`[${p.menu}] 어른 2 + 해린 1`', '`[${p.menu}] ${familyShort()}`')
rep('"해린이 몫: " + r.kidTip', '"아이 몫: " + r.kidTip')
rep('line("메이플베어", k.mb)', 'line(xName(), k.mb)')
rep('["날짜", "유치원 점심", "유치원 간식", "메이플베어 간식"]', '["날짜", `${kName()} 점심`, `${kName()} 간식`, `${xName()} 간식`]')
rep('if (f === "mb" && w !== 0 && w !== 2 && !r[f])', 'if (f === "mb" && !extraDays().includes(w) && !r[f])')

# ---- JS: prompts ----
rep("번은 계성유치원 식단표야.`", "번은 ${kName()} 식단표야.`")
rep("번은 메이플베어(월·수 수업) 간식표야.`", "번은 ${xName()}(${xDaysLabel() || \"방과후 수업\"}) 간식표야.`")
rep("[계성유치원 식단표 (글)]", "[${kName()} 식단표 (글)]")
rep("[메이플베어 간식표 (글)]", "[${xName()} 간식표 (글)]")
rep('- lunch: 계성유치원 점심 메뉴를', '- lunch: ${kName()} 점심 메뉴를')
rep('- snack: 계성유치원 오전·오후 간식', '- snack: ${kName()} 오전·오후 간식')
rep('- mb: 메이플베어 간식. 보통 월·수에만 있어.', '- mb: ${xName()} 간식. ${xDaysLabel() ? `보통 ${xDaysLabel()}에만 있어.` : "따로 받은 간식표가 있을 때만."}')
rep('"[가족] 엄마, 아빠, 해린(48개월·만 4세). 셋이 같이 먹는 메뉴로 짜되 해린이 몫은 싱겁고 맵지 않게. 어른 몫에 양념을 더하면 되는 경우 tip에 적어줘.",',
    '`[가족] 어른 ${adults()}명, 아이: ${kidsText() || "(정보 없음)"}. 다 같이 먹는 메뉴로 짜되 아이 몫은 나이에 맞게 싱겁고 맵지 않게. 어른 몫에 양념을 더하면 되는 경우 tip에 적어줘.`,')
rep("`[분량 기준] ${SERVES}`", "`[분량 기준] ${servesRule()}`")
rep("[해린이가 좋아하는 음식·특성]", "[아이가 좋아하는 음식·특성]")
rep("[해린이가 안 먹는 음식]", "[아이가 안 먹는 음식]")
rep("[남편이 좋아하는 음식·특성]", "[배우자가 좋아하는 음식·특성]")
rep("[남편이 안 먹는 음식]", "[배우자가 안 먹는 음식]")
rep("[엄마가 좋아하는 음식]", "[요리하는 사람(나)이 좋아하는 음식]")
s = re.sub(r'  const SERVES = "[^\n]*";\n', "", s)
rep("  const SHOP_RULES = `장보기 목록은 아래 '만들 끼니'에 필요한 것만, 어른 2명 + 48개월 아이 1명(한 끼 약 2.5인분) 기준 분량을 끼니별로 합산해서,",
    "  const shopRules = () => `장보기 목록은 아래 '만들 끼니'에 필요한 것만, 이 분량 기준(${servesRule()})으로 끼니별로 합산해서,")
s = s.replace("${SHOP_RULES}", "${shopRules()}")
s = s.replace("${SERVES}", "${servesRule()}")
rep('${k.mb ? ` / 메이플베어 간식: ${k.mb}` : ""}', '${k.mb ? ` / ${xName()} 간식: ${k.mb}` : ""}')
rep("1. 해린이는 유치원에서 먹은 것과", "1. 아이는 유치원에서 먹은 것과")
rep("유치원 점심·간식·메이플베어 간식과", "유치원 점심·간식·방과후 간식과")
rep("해린이와 남편이 좋아하는 것을", "아이와 배우자가 좋아하는 것을")
rep("- kidTip: 해린이(48개월) 몫을", "- kidTip: 아이 몫(나이 참고)을")
rep("/ 메이플베어 ${k.mb", "/ ${xName()} ${k.mb")
rep("해린이는 유치원에서 먹은 것과 주재료", "아이는 유치원에서 먹은 것과 주재료")

rep("""    setTimeout(() => (msg.textContent = ""), 2000);
    renderSummary();
  }));""", """    setTimeout(() => (msg.textContent = ""), 2000);
    applyFamilyLabels(); renderWeekTab();
  }));""")

# ---- first-run banner ----
rep("""    const b = $("banners"); b.replaceChildren();
""", """    const b = $("banners"); b.replaceChildren();
    if (booted && !settings.kids) {
      const s0 = el("div", "banner example"); s0.append(el("span", null, "처음이시면 '우리 가족·취향' 탭에서 가족 구성과 유치원 이름부터 적어주세요."));
      const go = el("button", "ghost", "가족 정보 적기"); go.onclick = () => showTab("prefs"); s0.append(go); b.append(s0);
    }
""")
rep('"claude.ai에 로그인한 상태로 열어야 가족이 함께 쓰는 식단과 장보기 체크가 보여요. 지금은 이 기기에만 저장돼요."',
    '"claude.ai에 로그인한 상태로 열어야 내 식단이 계정에 저장돼요. 지금은 이 기기에만 저장돼요."')

left = [m for m in re.findall(r"해린|계성|메이플|남편|48개월|SHOP_RULES|SERVES\b", s)]
if left: sys.exit(f"leftovers: {set(left)}")
open(dst, "w", encoding="utf-8").write(s)
print("ok")

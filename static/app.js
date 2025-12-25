let activeTab = "upload";
let uploadedFile = null;

const $ = (id) => document.getElementById(id);

function setStatus(kind, text){
  const dot = $("dot");
  dot.classList.remove("good","bad");
  if (kind === "good") dot.classList.add("good");
  if (kind === "bad") dot.classList.add("bad");
  $("status").textContent = text;
}

function logLine(s){
  const box = $("log");
  box.value = (box.value ? box.value + "\n" : "") + s;
  box.scrollTop = box.scrollHeight;
}

function switchTab(tab){
  activeTab = tab;
  document.querySelectorAll(".tab").forEach(t => t.classList.toggle("active", t.dataset.tab === tab));
  ["upload","url","paste"].forEach(x => {
    $("panel-"+x).style.display = (x === tab) ? "block" : "none";
  });
}

async function processNow(){
  setStatus("warn","Processing…");
  $("btnProcess").disabled = true;
  $("btnDownload").style.pointerEvents = "none";
  $("btnDownload").style.opacity = ".6";
  $("btnDownload").href = "#";
  $("total").textContent = "0";
  $("log").value = "";

  const payload = new FormData();

  payload.append("check_mode", $("checkMode").value);
  payload.append("clash_mode", $("clashMode").value);
  payload.append("only_active", $("onlyActive").checked ? "1" : "0");
  payload.append("top_n", $("topN").value || "0");
  payload.append("countries", $("countries").value || "");
  payload.append("flap_rounds", $("flapRounds").value || "2");

  if (activeTab === "upload"){
    if (!uploadedFile){
      setStatus("bad","No file");
      $("btnProcess").disabled = false;
      logLine("Select a file first.");
      return;
    }
    payload.append("input_type","file");
    payload.append("file", uploadedFile);
  } else if (activeTab === "url"){
    const url = $("urlInput").value.trim();
    if (!url){
      setStatus("bad","No URL");
      $("btnProcess").disabled = false;
      logLine("Paste a URL first.");
      return;
    }
    payload.append("input_type","url");
    payload.append("url", url);
  } else {
    const text = $("textInput").value;
    if (!text.trim()){
      setStatus("bad","No text");
      $("btnProcess").disabled = false;
      logLine("Paste text first.");
      return;
    }
    payload.append("input_type","text");
    payload.append("text", text);
  }

  try{
    const res = await fetch("/api/process", { method:"POST", body: payload });
    const text = await res.text();

    let data;
    try { data = JSON.parse(text); }
    catch {
      console.error("Non-JSON response:", text.slice(0,300));
      throw new Error("Server returned non-JSON. Check Flask console.");
    }

    if (!res.ok){
      throw new Error(data.error || "Failed");
    }

    $("total").textContent = String(data.total || 0);
    logLine("Success ✅");
    logLine("Active proxies exported: " + (data.total || 0));

    const dl = data.download;
    if (dl){
      $("btnDownload").href = dl;
      $("btnDownload").style.pointerEvents = "auto";
      $("btnDownload").style.opacity = "1";
      logLine("Download ready: " + dl);
    }

    setStatus("good","Done");
  }catch(e){
    setStatus("bad","Error");
    logLine("Error: " + (e.message || e));
  }finally{
    $("btnProcess").disabled = false;
  }
}

function resetUI(){
  uploadedFile = null;
  $("fileName").textContent = "";
  $("urlInput").value = "";
  $("textInput").value = "";
  $("log").value = "";
  $("total").textContent = "0";
  $("btnDownload").href = "#";
  $("btnDownload").style.pointerEvents = "none";
  $("btnDownload").style.opacity = ".6";
  setStatus("warn","Idle");
}

function setup(){
  document.querySelectorAll(".tab").forEach(t => t.addEventListener("click", () => switchTab(t.dataset.tab)));

  const dz = $("dropZone");
  const fi = $("fileInput");

  dz.addEventListener("click", () => fi.click());
  dz.addEventListener("dragover", (e) => { e.preventDefault(); dz.style.borderColor = "rgba(124,92,255,.7)"; });
  dz.addEventListener("dragleave", () => { dz.style.borderColor = "rgba(255,255,255,.22)"; });
  dz.addEventListener("drop", (e) => {
    e.preventDefault();
    dz.style.borderColor = "rgba(255,255,255,.22)";
    const f = e.dataTransfer.files?.[0];
    if (f){
      uploadedFile = f;
      $("fileName").textContent = `${f.name} (${Math.round(f.size/1024)} KB)`;
      setStatus("warn","Ready");
    }
  });
  fi.addEventListener("change", () => {
    const f = fi.files?.[0];
    if (f){
      uploadedFile = f;
      $("fileName").textContent = `${f.name} (${Math.round(f.size/1024)} KB)`;
      setStatus("warn","Ready");
    }
  });

  $("btnProcess").addEventListener("click", processNow);
  $("btnClear").addEventListener("click", resetUI);

  resetUI();
  switchTab("upload");
}

setup();

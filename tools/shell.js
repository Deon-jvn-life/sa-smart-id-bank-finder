(function(){
  var el=document.getElementById("search-data");
  var input=document.getElementById("q");
  var box=document.getElementById("search-results");
  if(!el||!input||!box) return;
  var pages=[];
  try { pages=JSON.parse(el.textContent); } catch(e){ return; }
  function esc(s){
    return String(s).replace(/[&<>"']/g, function(c){
      return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c];
    });
  }
  function activeWords(q){
    var t=String(q||"").trim().toLowerCase();
    if(t.length<2) return [];
    return t.split(/\s+/).filter(function(w){ return w; });
  }
  function match(blob, ws){
    if(!ws.length) return true;
    blob=String(blob).toLowerCase();
    for(var i=0;i<ws.length;i++) if(blob.indexOf(ws[i])<0) return false;
    return true;
  }
  function filterIndex(q){
    var root=document.getElementById("page-index");
    if(!root) return;
    var ws=activeWords(q);
    var items=root.querySelectorAll("li");
    var shown=0;
    for(var i=0;i<items.length;i++){
      var li=items[i];
      var blob=li.textContent+" "+(li.getAttribute("data-keywords")||"");
      var ok=match(blob, ws);
      li.hidden=!ok;
      if(ok) shown++;
    }
    var sections=root.querySelectorAll("section");
    for(var s=0;s<sections.length;s++){
      var sec=sections[s];
      var lis=sec.querySelectorAll("li");
      var any=false;
      for(var k=0;k<lis.length;k++) if(!lis[k].hidden) any=true;
      sec.hidden=!any;
    }
    var status=document.getElementById("index-status");
    if(status){
      if(!ws.length) status.textContent="Showing every page.";
      else if(!shown) status.textContent="No page matches. Try a different word, or clear the search.";
      else status.textContent="Showing "+shown+" of "+items.length+" pages.";
    }
  }
  function show(q){
    var ws=activeWords(q);
    if(!ws.length){
      box.hidden=true;
      box.innerHTML="";
    } else {
      var hits=[];
      for(var i=0;i<pages.length;i++){
        var p=pages[i];
        var blob=p.t+" "+p.s+" "+p.g+" "+(p.k||"");
        if(match(blob, ws)) hits.push(p);
        if(hits.length===8) break;
      }
      if(!hits.length){
        box.innerHTML="<p class=\"search-empty\">No matching page. Open the <a href=\"/find/\">full page list</a>.</p>";
      } else {
        var html="<ul>";
        for(var j=0;j<hits.length;j++){
          var hit=hits[j];
          html+="<li><a href=\""+esc(hit.u)+"\"><strong>"+esc(hit.t)+"</strong><span>"+esc(hit.s)+"</span></a></li>";
        }
        html+="</ul>";
        box.innerHTML=html;
      }
      box.hidden=false;
    }
    filterIndex(q);
  }
  input.addEventListener("input", function(){ show(input.value); });
  input.addEventListener("keydown", function(e){
    if(e.key==="Escape"){ box.hidden=true; box.innerHTML=""; }
  });
  document.addEventListener("click", function(e){
    if(!box.contains(e.target) && e.target!==input){ box.hidden=true; }
  });
  var initial="";
  try { initial=new URLSearchParams(window.location.search).get("q")||""; } catch(err){ initial=""; }
  if(initial){ input.value=initial; show(initial); }
  else filterIndex("");
  var sums=document.querySelectorAll(".grp > summary");
  for(var n=0;n<sums.length;n++){
    sums[n].addEventListener("click", function(){
      var parent=this.parentNode;
      var open=document.querySelectorAll(".grp[open]");
      for(var i=0;i<open.length;i++) if(open[i]!==parent) open[i].removeAttribute("open");
    });
  }
})();
(function(){
  var header=document.getElementById("site-header");
  var slot=document.getElementById("head-slot");
  var toggle=document.querySelector(".search-toggle");
  var search=document.getElementById("site-search");
  var nav=document.getElementById("site-nav");
  if(!header||!slot) return;
  function closeGroups(){
    var open=document.querySelectorAll(".grp[open]");
    for(var i=0;i<open.length;i++) open[i].removeAttribute("open");
  }
  function wide(){
    return window.matchMedia("(min-width:960px)").matches;
  }
  function setSpace(){
    var h=header.offsetHeight;
    document.documentElement.style.setProperty("--header-space", h+"px");
    document.documentElement.style.setProperty("--scroll-pad", (h+16)+"px");
    slot.style.height=h+"px";
  }
  function setSearchOpen(open){
    if(!search||!toggle) return;
    if(wide()) open=false;
    search.classList.toggle("is-open", !!open);
    toggle.setAttribute("aria-expanded", open?"true":"false");
    if(open){
      closeGroups();
      var input=document.getElementById("q");
      if(input) input.focus();
    }
  }
  function updateHint(){
    if(!nav) return;
    var more=nav.scrollWidth>nav.clientWidth+8;
    var atEnd=nav.scrollLeft+nav.clientWidth>=nav.scrollWidth-8;
    var atStart=nav.scrollLeft<=8;
    document.body.classList.toggle("nav-more-right", !!(more && !atEnd));
    document.body.classList.toggle("nav-more-left", !!(more && !atStart));
  }
  function revealCurrent(){
    if(!nav) return;
    var cur=nav.querySelector(".grp.has-current");
    if(!cur || nav.scrollWidth<=nav.clientWidth+8){ updateHint(); return; }
    var left=cur.offsetLeft-(nav.clientWidth-cur.offsetWidth)/2;
    nav.scrollLeft=left<0?0:left;
    updateHint();
  }
  function coverEdge(){
    return header.getBoundingClientRect().height+16;
  }
  function revealTarget(el){
    if(!el||!el.getBoundingClientRect) return;
    var edge=coverEdge();
    var r=el.getBoundingClientRect();
    if(r.top>=edge-1) return;
    var y=(window.scrollY||0)+r.top-edge;
    window.scrollTo(0, y<0?0:y);
  }
  function revealHash(){
    if(!location.hash||location.hash.length<2) return;
    var id="";
    try { id=decodeURIComponent(location.hash.slice(1)); } catch(err){ id=location.hash.slice(1); }
    var el=document.getElementById(id);
    if(el) revealTarget(el);
  }
  if(toggle){
    toggle.addEventListener("click", function(){
      var open=toggle.getAttribute("aria-expanded")==="true";
      setSearchOpen(!open);
    });
  }
  document.addEventListener("keydown", function(e){
    if(e.key!=="Escape") return;
    setSearchOpen(false);
    closeGroups();
    var box=document.getElementById("search-results");
    if(box){ box.hidden=true; box.innerHTML=""; }
  });
  document.addEventListener("click", function(e){
    var t=e.target;
    var link=t&&t.closest?t.closest("a[href]"):null;
    if(link){
      var href=link.getAttribute("href")||"";
      if(href.indexOf("#")>=0) setTimeout(revealHash, 0);
    }
    if(header.contains(t)) return;
    setSearchOpen(false);
    closeGroups();
  });
  if(nav){
    nav.addEventListener("scroll", updateHint, {passive:true});
    var topicSums=nav.querySelectorAll(".grp>summary");
    for(var s=0;s<topicSums.length;s++){
      topicSums[s].addEventListener("click", function(){ setSearchOpen(false); });
    }
  }
  document.addEventListener("focusin", function(e){
    var t=e.target;
    if(!t) return;
    if(nav && nav.contains(t) && nav.scrollWidth>nav.clientWidth+8 && t.closest){
      var grp=t.closest(".grp");
      if(grp){
        var pad=16;
        var left=grp.offsetLeft-pad;
        var right=grp.offsetLeft+grp.offsetWidth+pad;
        if(left<nav.scrollLeft) nav.scrollLeft=Math.max(0,left);
        else if(right>nav.scrollLeft+nav.clientWidth) nav.scrollLeft=right-nav.clientWidth;
        updateHint();
      }
    }
    if(header.contains(t)||(t.classList&&t.classList.contains("skip"))) return;
    revealTarget(t);
  });
  window.addEventListener("hashchange", function(){ setTimeout(revealHash, 0); });
  window.addEventListener("resize", function(){
    setSearchOpen(false);
    setSpace();
    updateHint();
  });
  setSpace();
  revealCurrent();
  revealHash();
})();
(function(){
  function esc(s){
    return String(s).replace(/[&<>"']/g, function(c){
      return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c];
    });
  }
  var cards=document.querySelectorAll(".branch-card");
  var bank=document.getElementById("bank-filter");
  var text=document.getElementById("branch-filter");
  var count=document.getElementById("branch-count");
  function applyFilter(){
    if(!cards.length || (!bank && !text)) return;
    var b=bank?bank.value:"";
    var q=(text&&text.value?text.value:"").trim().toLowerCase();
    var shown=0;
    for(var i=0;i<cards.length;i++){
      var el=cards[i];
      var blob=(el.getAttribute("data-text")||el.textContent||"").toLowerCase();
      var ok=true;
      if(b && el.getAttribute("data-bank")!==b) ok=false;
      if(ok && q && blob.indexOf(q)<0) ok=false;
      el.hidden=!ok;
      if(ok) shown++;
    }
    var groups=document.querySelectorAll(".branch-group");
    for(var g=0;g<groups.length;g++){
      var vis=groups[g].querySelectorAll(".branch-card:not([hidden])");
      groups[g].hidden=vis.length===0;
    }
    if(count){
      if(!b && !q) count.textContent="Showing all "+cards.length+" branches.";
      else count.textContent="Showing "+shown+" of "+cards.length+" branches.";
    }
  }
  if(bank) bank.addEventListener("change", applyFilter);
  if(text) text.addEventListener("input", applyFilter);
  applyFilter();
  var locBtn=document.getElementById("use-location");
  var locStatus=document.getElementById("location-status");
  var locList=document.getElementById("nearest-list");
  var locData=document.getElementById("nearest-data");
  if(!locBtn||!locStatus||!locList||!locData) return;
  var places=[];
  try { places=JSON.parse(locData.textContent)||[]; } catch(e){ places=[]; }
  function dist(lat1,lon1,lat2,lon2){
    var R=6371, p=Math.PI/180;
    var dLat=(lat2-lat1)*p, dLon=(lon2-lon1)*p;
    var x=Math.sin(dLat/2)*Math.sin(dLat/2)+Math.cos(lat1*p)*Math.cos(lat2*p)*Math.sin(dLon/2)*Math.sin(dLon/2);
    return 2*R*Math.asin(Math.min(1,Math.sqrt(x)));
  }
  locBtn.addEventListener("click", function(){
    locStatus.textContent="Asking this browser for a location. The coordinates stay on this page.";
    if(!navigator.geolocation){
      locStatus.textContent="This browser cannot share a location. Pick a bank, a province, or a city.";
      return;
    }
    navigator.geolocation.getCurrentPosition(function(pos){
      var lat=pos.coords.latitude, lon=pos.coords.longitude;
      var ranked=[];
      for(var i=0;i<places.length;i++){
        var place=places[i];
        if(typeof place.lat!=="number"||typeof place.lon!=="number") continue;
        ranked.push({p:place, km:dist(lat, lon, place.lat, place.lon)});
      }
      ranked.sort(function(a,b){ return a.km-b.km; });
      ranked=ranked.slice(0,5);
      if(!ranked.length){
        locStatus.textContent="No placed branches to compare. Pick a city or a province.";
        locList.innerHTML="";
        return;
      }
      locStatus.textContent="Five nearest branches this guide could place on a map. Distance is a straight line. A city page lists every branch, including ones without a pin.";
      var html="";
      for(var n=0;n<ranked.length;n++){
        var item=ranked[n].p;
        var km=ranked[n].km<10?ranked[n].km.toFixed(1):String(Math.round(ranked[n].km));
        html+='<li class="branch-card"><p class="bc-kicker">'+esc(item.bank)+'</p><p class="bc-name">'+esc(item.name)+'</p><p class="bc-where">'+esc(item.city)+', about '+esc(km)+' km</p><p class="bc-go"><a href="'+esc(item.directions)+'" target="_blank" rel="noopener">Get directions<span class="vh"> (opens in a new tab)</span></a></p></li>';
      }
      locList.innerHTML=html;
    }, function(){
      locStatus.textContent="Location was not shared. Pick a bank, a province, or a city.";
    }, {enableHighAccuracy:false, timeout:12000, maximumAge:300000});
  });
})();

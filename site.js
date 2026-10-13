(function(){
var nav=document.getElementById('nav'),mb=document.getElementById('menu');
if(mb)mb.addEventListener('click',function(){var o=nav.classList.toggle('open');mb.setAttribute('aria-expanded',o)});

/* Vimeo click-to-play */
[].forEach.call(document.querySelectorAll('.player[data-vimeo]'),function(p){
  p.querySelector('button').addEventListener('click',function(){
    var f=document.createElement('iframe');
    f.src='https://player.vimeo.com/video/'+p.dataset.vimeo+'?autoplay=1';
    f.allow='autoplay; fullscreen; picture-in-picture';f.allowFullscreen=true;f.title=p.dataset.title;
    p.innerHTML='';p.appendChild(f);
  });
});

/* Forms: posted to Formspree as JSON. Replace YOUR_..._FORM_ID in the HTML action with the real ID. */
[].forEach.call(document.querySelectorAll('form[data-form]'),function(f){
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var out=f.querySelector('output'),btn=f.querySelector('button[type=submit]');
    if(/YOUR_/.test(f.action)){out.textContent='This form is not connected yet. Please write to baron@globalharlem.com.';return}
    btn.disabled=true;out.textContent='Sending...';
    fetch(f.action,{method:'POST',body:new FormData(f),headers:{'Accept':'application/json'}})
      .then(function(r){if(r.ok){f.reset();out.textContent='Thank you. We will be in touch.'}else{out.textContent='Something went wrong. Please write to baron@globalharlem.com.'}})
      .catch(function(){out.textContent='Something went wrong. Please write to baron@globalharlem.com.'})
      .then(function(){btn.disabled=false});
  });
});

/* Trust Audit iframe: grow to fit the tool */
window.addEventListener('message',function(e){
  if(e.origin!==location.origin||!e.data||e.data.type!=='gh-height')return;
  var fr=document.getElementById('toolframe');if(fr)fr.style.height=Math.ceil(e.data.h)+'px';
});
})();

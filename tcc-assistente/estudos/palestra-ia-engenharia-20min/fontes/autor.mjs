import {slides} from './conteudo.mjs';
export function build(presentation){
 const W=1280,H=720,ink='#102C3A',teal='#087E8B',paper='#F6F5EF';
 function text(s,name,value,x,y,w,h,size=30,color=ink,bold=false){const t=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=value;t.text.style={typeface:'Aptos',fontSize:size,color,bold,wrap:true};return t;}
 const total=slides.reduce((n,s)=>n+s.minutes,0);if(total!==20)throw Error('Duracao diferente de 20 minutos: '+total);
 for(const [i,d] of slides.entries()){
  const s=presentation.slides.add();s.background.fill=d.kind==='cover'||d.kind==='metric'?ink:paper;const dark=d.kind==='cover'||d.kind==='metric',fg=dark?'#FFFFFF':ink;
  if(d.kind==='cover'){
   text(s,'titulo',d.title,72,155,1110,215,76,'#FFFFFF',true);
   text(s,'subtitulo',d.subtitle,76,405,1100,145,34,'#BCD5DB');
   text(s,'contexto','Estudo de caso do TCC',76,625,1000,40,24,'#81D4CD');
  }else{
   text(s,'titulo',d.title,72,46,1135,80,48,fg,true);
   if(d.kind==='image'){
    s.images.add({path:d.image,alt:d.caption,position:{left:72,top:144,width:1136,height:476},fit:'contain'});
    text(s,'legenda',d.caption,72,640,1136,52,26,teal,true);
   }else if(d.kind==='statement'){
    text(s,'mensagem',d.lead,72,178,1136,185,57,ink,true);
    text(s,'apoio',d.body,76,424,1100,180,31,teal);
   }else if(d.kind==='columns'){
    text(s,'coluna-cad-titulo',d.leftTitle,72,183,540,62,38,teal,true);
    text(s,'coluna-bim-titulo',d.rightTitle,666,183,540,62,38,teal,true);
    text(s,'coluna-cad',d.left,72,272,530,270,31,ink);
    text(s,'coluna-bim',d.right,666,272,540,270,31,ink);
    text(s,'nota',d.bottom,72,621,1136,66,26,teal,true);
   }else if(d.kind==='roles'){
    for(const [j,[label,body]] of d.rows.entries()){text(s,'rotulo-'+j,label,72,177+j*94,280,68,30,teal,true);text(s,'explicacao-'+j,body,380,177+j*94,815,76,29,ink);}
    text(s,'nota',d.bottom,72,624,1136,64,25,teal,true);
   }else if(d.kind==='prompt'){
    text(s,'pedido',d.lead,72,166,1135,92,45,teal,true);
    text(s,'entradas',d.body,76,286,1115,270,36,ink);
    text(s,'limite',d.bottom,72,627,1136,60,26,teal,true);
   }else if(d.kind==='metric'){
    text(s,'tempo-api',d.metric,72,159,700,162,126,'#81D4CD',true);
    text(s,'escopo-tempo',d.label,78,338,1120,66,36,'#FFFFFF',true);
    text(s,'exclusoes',d.body,78,454,1120,114,30,'#BCD5DB');
    text(s,'nota',d.bottom,78,626,1120,64,26,'#81D4CD',true);
   }
  }
  s.speakerNotes.text=`Tempo sugerido: ${d.minutes.toLocaleString('pt-BR')} minuto(s).\n\n${d.notes}`;
 }
 return{slides:slides.length,plannedMinutes:total,size:{width:W,height:H},fontPolicy:{basis:'design',families:['Aptos']}};
}

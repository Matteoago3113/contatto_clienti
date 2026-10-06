'use strict';
const fs=require('node:fs');
const path=require('node:path');
function validate(catalog){
 if(!Array.isArray(catalog)||!catalog.length||catalog.length>5000)throw new Error('Il catalogo deve contenere da 1 a 5000 messaggi.');
 const ids=new Set();
 for(const t of catalog){
  for(const key of ['id','brand','category','channel','stage','title','body','subject','source','sourceLabel'])if(typeof t[key]!=='string'||t[key].length>200000)throw new Error('Formato messaggio non valido.');
  if(!t.id.trim()||!t.category.trim()||!t.title.trim()||!t.body.trim()||!t.sourceLabel.trim())throw new Error('Compila titolo, ambito e testo.');
  if(ids.has(t.id))throw new Error('Identificativo messaggio duplicato.');ids.add(t.id);
  if(!['Sitointerattivo','Abracadabra'].includes(t.brand)||!['email','whatsapp','entrambi'].includes(t.channel)||!['primo','secondo','terzo','servizi'].includes(t.stage))throw new Error('Progetto, canale o fase non validi.');
 }
 return catalog;
}
function load(file,fallback){
 try{return{catalog:validate(JSON.parse(fs.readFileSync(file,'utf8'))),error:''};}
 catch(e){if(e.code==='ENOENT')return{catalog:fallback,error:''};return{catalog:fallback,error:'Il catalogo salvato non è leggibile. Uso i modelli originali. Il file precedente sarà conservato se salvi nuove modifiche.'};}
}
function save(file,catalog){
 validate(catalog);fs.mkdirSync(path.dirname(file),{recursive:true});
 const temporary=file+'.tmp';fs.writeFileSync(temporary,JSON.stringify(catalog,null,2),'utf8');
 if(fs.existsSync(file))fs.copyFileSync(file,file+'.backup');
 fs.renameSync(temporary,file);return true;
}
module.exports={validate,load,save};

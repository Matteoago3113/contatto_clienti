'use strict';
const {app,BrowserWindow,ipcMain,shell,dialog}=require('electron');
const path=require('node:path');
const fs=require('node:fs');
const store=require('./catalog-store.cjs');
let window;
app.setName('Contatto');
if(!app.requestSingleInstanceLock()){app.quit();}else{
 app.on('second-instance',()=>{if(window){if(window.isMinimized())window.restore();window.focus();}});
 app.whenReady().then(()=>{
  const file=path.join(app.getPath('userData'),'messaggi.json');
  const fallback=JSON.parse(fs.readFileSync(path.join(__dirname,'catalog.json'),'utf8'));
  ipcMain.handle('catalog:load',()=>store.load(file,fallback));
  ipcMain.handle('catalog:save',(_event,catalog)=>{try{store.save(file,catalog);return{ok:true};}catch(e){return{ok:false,error:e.message};}});
  ipcMain.handle('catalog:export',async(_event,catalog)=>{store.validate(catalog);const result=await dialog.showSaveDialog(window,{title:'Salva backup messaggi',defaultPath:'Contatto-messaggi.json',filters:[{name:'Catalogo messaggi',extensions:['json']}]});if(result.canceled)return false;fs.writeFileSync(result.filePath,JSON.stringify(catalog,null,2),'utf8');return true;});
  window=new BrowserWindow({width:1080,height:900,minWidth:640,minHeight:600,title:'Contatto',backgroundColor:'#f6f8f3',autoHideMenuBar:true,webPreferences:{preload:path.join(__dirname,'preload.cjs'),contextIsolation:true,nodeIntegration:false,sandbox:true}});
  window.webContents.setWindowOpenHandler(({url})=>{if(/^https?:\/\//.test(url))shell.openExternal(url);return{action:'deny'};});
  window.webContents.on('will-navigate',(event,url)=>{if(!url.startsWith('file:'))event.preventDefault();});
  window.loadFile(path.join(__dirname,'Contatto.html'));
 });
 app.on('window-all-closed',()=>app.quit());
}

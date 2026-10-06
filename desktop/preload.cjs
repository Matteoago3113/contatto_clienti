'use strict';
const {contextBridge,ipcRenderer}=require('electron');
contextBridge.exposeInMainWorld('contattoDesktop',{
 loadCatalog:()=>ipcRenderer.invoke('catalog:load'),
 saveCatalog:catalog=>ipcRenderer.invoke('catalog:save',catalog),
 exportCatalog:catalog=>ipcRenderer.invoke('catalog:export',catalog)
});

(()=>{"use strict";var e,t={7199:(e,t,r)=>{var i=r(9465);class o extends i.y{chooserModalClass=ImageChooserModal;initHTMLElements(e){super.initHTMLElements(e),this.previewImage=this.chooserElement.querySelector("[data-chooser-image]")}getStateFromHTML(){const e=super.getStateFromHTML();return e&&(e.preview={url:this.previewImage.getAttribute("src"),width:this.previewImage.getAttribute("width"),height:this.previewImage.getAttribute("height")}),e}renderState(e){super.renderState(e),this.previewImage.setAttribute("src",e.preview.url),this.previewImage.setAttribute("width",e.preview.width)}}class a extends i._{widgetClass=o;chooserModalClass=ImageChooserModal}window.telepath.register("wagtail.images.widgets.ImageChooser",a)},1669:e=>{e.exports=jQuery}},r={};function i(e){var o=r[e];if(void 0!==o)return o.exports;var a=r[e]={exports:{}};return t[e](a,a.exports,i),a.exports}i.m=t,e=[],i.O=(t,r,o,a)=>{if(!r){var s=1/0;for(u=0;u<e.length;u++){for(var[r,o,a]=e[u],n=!0,l=0;l<r.length;l++)(!1&a||s>=a)&&Object.keys(i.O).every((e=>i.O[e](r[l])))?r.splice(l--,1):(n=!1,a<s&&(s=a));if(n){e.splice(u--,1);var h=o();void 0!==h&&(t=h)}}return t}a=a||0;for(var u=e.length;u>0&&e[u-1][2]>a;u--)e[u]=e[u-1];e[u]=[r,o,a]},i.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return i.d(t,{a:t}),t},i.d=(e,t)=>{for(var r in t)i.o(t,r)&&!i.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},i.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),i.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),i.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.j=246,(()=>{var e={246:0};i.O.j=t=>0===e[t];var t=(t,r)=>{var o,a,[s,n,l]=r,h=0;if(s.some((t=>0!==e[t]))){for(o in n)i.o(n,o)&&(i.m[o]=n[o]);if(l)var u=l(i)}for(t&&t(r);h<s.length;h++)a=s[h],i.o(e,a)&&e[a]&&e[a][0](),e[a]=0;return i.O(u)},r=globalThis.webpackChunkwagtail=globalThis.webpackChunkwagtail||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))})();var o=i.O(void 0,[321],(()=>i(7199)));o=i.O(o)})();
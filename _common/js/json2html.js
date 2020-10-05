/**
 * The simplest "JSON->HTML" templater with multilanguage support
 * Author: Leonid Arefev
 * Started: 11-05-2013
 * GitHub: https://github.com/wtf-develop/JSONtemplate
 * Web: https://wtf-dev.ru/
 */
var $jscomp={scope:{},checkStringArgs:function(c,v,m){if(null==c)throw new TypeError("The 'this' value for String.prototype."+m+" must not be null or undefined");if(v instanceof RegExp)throw new TypeError("First argument to String.prototype."+m+" must not be a regular expression");return c+""}};
$jscomp.defineProperty="function"==typeof Object.defineProperties?Object.defineProperty:function(c,v,m){if(m.get||m.set)throw new TypeError("ES3 does not support getters and setters.");c!=Array.prototype&&c!=Object.prototype&&(c[v]=m.value)};$jscomp.getGlobal=function(c){return"undefined"!=typeof window&&window===c?c:"undefined"!=typeof global&&null!=global?global:c};$jscomp.global=$jscomp.getGlobal(this);
$jscomp.polyfill=function(c,v,m,x){if(v){m=$jscomp.global;c=c.split(".");for(x=0;x<c.length-1;x++){var n=c[x];n in m||(m[n]={});m=m[n]}c=c[c.length-1];x=m[c];v=v(x);v!=x&&null!=v&&$jscomp.defineProperty(m,c,{configurable:!0,writable:!0,value:v})}};
$jscomp.polyfill("String.prototype.endsWith",function(c){return c?c:function(c,m){var v=$jscomp.checkStringArgs(this,c,"endsWith");c+="";void 0===m&&(m=v.length);for(var n=Math.max(0,Math.min(m|0,v.length)),e=c.length;0<e&&0<n;)if(v[--n]!=c[--e])return!1;return 0>=e}},"es6-impl","es3");
$jscomp.polyfill("String.prototype.startsWith",function(c){return c?c:function(c,m){var v=$jscomp.checkStringArgs(this,c,"startsWith");c+="";for(var n=v.length,e=c.length,r=Math.max(0,Math.min(m|0,v.length)),y=0;y<e&&r<n;)if(v[r++]!=c[y++])return!1;return y>=e}},"es6-impl","es3");$jscomp.polyfill("Number.isFinite",function(c){return c?c:function(c){return"number"!==typeof c?!1:!isNaN(c)&&Infinity!==c&&-Infinity!==c}},"es6-impl","es3");
$jscomp.polyfill("Number.isInteger",function(c){return c?c:function(c){return Number.isFinite(c)?c===Math.floor(c):!1}},"es6-impl","es3");$jscomp.SYMBOL_PREFIX="jscomp_symbol_";$jscomp.initSymbol=function(){$jscomp.initSymbol=function(){};$jscomp.global.Symbol||($jscomp.global.Symbol=$jscomp.Symbol)};$jscomp.symbolCounter_=0;$jscomp.Symbol=function(c){return $jscomp.SYMBOL_PREFIX+(c||"")+$jscomp.symbolCounter_++};
$jscomp.initSymbolIterator=function(){$jscomp.initSymbol();var c=$jscomp.global.Symbol.iterator;c||(c=$jscomp.global.Symbol.iterator=$jscomp.global.Symbol("iterator"));"function"!=typeof Array.prototype[c]&&$jscomp.defineProperty(Array.prototype,c,{configurable:!0,writable:!0,value:function(){return $jscomp.arrayIterator(this)}});$jscomp.initSymbolIterator=function(){}};$jscomp.arrayIterator=function(c){var v=0;return $jscomp.iteratorPrototype(function(){return v<c.length?{done:!1,value:c[v++]}:{done:!0}})};
$jscomp.iteratorPrototype=function(c){$jscomp.initSymbolIterator();c={next:c};c[$jscomp.global.Symbol.iterator]=function(){return this};return c};$jscomp.array=$jscomp.array||{};$jscomp.iteratorFromArray=function(c,v){$jscomp.initSymbolIterator();c instanceof String&&(c+="");var m=0,x={next:function(){if(m<c.length){var n=m++;return{value:v(n,c[n]),done:!1}}x.next=function(){return{done:!0,value:void 0}};return x.next()}};x[Symbol.iterator]=function(){return x};return x};
$jscomp.polyfill("Array.prototype.keys",function(c){return c?c:function(){return $jscomp.iteratorFromArray(this,function(c){return c})}},"es6-impl","es3");
if(void 0===jth||void 0===json2html)var json2html=function(){function c(a,b,c){c="undefined"==typeof c?!1:c;if(void 0===b||null==b||0==b.length)return!1;var h,d;for(d in a){h=a[d];if(h==b)return!0;if(c){var f=h.indexOf("*");if(0==f){if(b.endsWith(h.substr(1)))return!0}else if(f==h.length-1&&b.startsWith(h.substr(0,h.length-1)))return!0}}return!1}function v(a,b,c){if(void 0===b)return G&&alert("Json2Html: CRITICAL error. Varialble name is undefined. Check your loop templates"),console.log("Json2Html: CRITICAL error. Varialble name is undefined. Check your loop templates"),
"";b=r(b);var h,d=b.split(".");for(h=0;h<d.length;h++)if(d[h]=m(r(d[h])),"this"!=d[h]){if("vardump"==d[h])return J(a);if("length"==d[h]&&Array.isArray(a))return a.length;if("random"==d[h])return Math.floor(1E5*Math.random()+1);if("instance_id"==d[h])return c;if(void 0!==a&&null!==a&&void 0!==a[d[h]])a=a[d[h]];else{G&&-1==I.indexOf(d[h])&&(I=I+d[h]+" in ("+b+")\n");a="";break}}if(void 0===a||null===a)a="";return a}function m(a){if(null===a)return"";if("string"!=typeof a||3>a.length)return a;'"'==a.charAt(0)&&
'"'==a.charAt(a.length-1)&&(a=a.substr(1,a.length-2));"'"==a.charAt(0)&&"'"==a.charAt(a.length-1)&&(a=a.substr(1,a.length-2));"`"==a.charAt(0)&&"`"==a.charAt(a.length-1)&&(a=a.substr(1,a.length-2));return a}function x(a,b){function c(a){d=a;d=e("if=`","",d);d=e("`","",d);d=r(d);return 1>d.length?!1:!0}function h(a){if(1>d.length)return!0;a={obj:a,func:function(){return!!eval("function __hey(obj){return ("+d+");}; __hey(this.obj);")}};try{return a.func()}catch(Y){y("debug error in filter!\n"+d+"\n"+
Y.name)}return!1}var d="",f=K,O=T;T++;b=r(m(b));var k=-1,F="",g="";G&&0==L&&(I="");if(15<L)return y("stack overflow in parser detect"),"";if(void 0===f[b])return y("template "+b+" is UNDEFINED"),"";L++;var f=f[b],q=0,p=0,w,t,l,u,C=t=-1,n="",E="",D=-1;w=-1;for(p=q=0;-1!=f.indexOf(z[0],q);)if(q=f.indexOf(z[0],q),p=f.indexOf(z[1],q+z[0].length),D=C=t=-1,E=n="",w=-1,g=l=k="",-1!=p&&155>p-q&&0<p-q){u=p=f.substr(q+z[0].length,p-(q+z[0].length));g="";-1!=p.indexOf(",")&&(g=p.split(","),u=g[0],void 0!==g[1]&&
0==g[1].indexOf("hash32")?(D=1,g=""):void 0!==g[1]&&-1!=g[1].indexOf("replace=")?(-1!=g[1].indexOf("`with`")&&(g[1]=g[1].split("`with`"),n=g[1][0],E=g[1][1],n=e("replace=","",n),n=e("`","",n),E=e("replace=","",E),E=e("`","",E),C=0<n.length?n.length:-1),g=""):void 0!==g[1]&&-1!=g[1].indexOf("crop=")?(t=parseInt(m(e("crop=","",g[1]))),1>t&&(t=-1),g=""):void 0!==g[1]&&-1!=g[1].indexOf("ift=`")?(w=1,l=k="",-1!=g[1].indexOf("`then`")?(g[1]=g[1].split("`then`"),k=g[1][1],l=k.split("`else`")):(then_n=void 0,
l=g[1].split("`else`")),void 0===l[1]?l=void 0:(k=l[0],l=l[1]),g[1]=e("ift=","",g[1][0]),g[1]=r(e("`","",g[1])),void 0!==l&&(l=r(e("`","",l))),void 0!==k&&(k=r(e("`","",k)))):void 0===g[1]||-1==g[1].indexOf("ifc=`")&&-1==g[1].indexOf("if=`")?void 0!==g[1]&&-1!=g[1].indexOf("ifb=`")?(w=3,l=k="",-1!=g[1].indexOf("`then`")?(g[1]=g[1].split("`then`"),k=g[1][1],l=k.split("`else`")):(then_n=void 0,l=g[1].split("`else`")),void 0===l[1]?l=void 0:(k=l[0],l=l[1]),g[1]=e("ifb=","",g[1][0]),g[1]=r(e("`","",g[1])),
void 0!==l&&(l=r(e("`","",l))),void 0!==k&&(k=r(e("`","",k)))):g="":(w=2,l=k="",-1!=g[1].indexOf("`then`")?(g[1]=g[1].split("`then`"),k=g[1][1],l=k.split("`else`")):(then_n=void 0,l=g[1].split("`else`")),void 0===l[1]?l=void 0:(k=l[0],l=l[1]),-1!=g[1][0].indexOf("ifc=")?g[1]=e("ifc=","",g[1][0]):g[1]=e("if=","",g[1][0]),g[1]=r(e("`","",g[1])),void 0!==l&&(l=r(e("`","",l))),void 0!==k&&(k=r(e("`","",k)))));u=v(a,u,O);if(0<D)u=Z(u);else if(0<C)u=e(n,E,u);else if(0<t)u.length>t&&(u=u.substr(0,t)+"...");
else if((1==w||2==w)&&void 0!==g[1]){t=g[1].toString().toUpperCase();g=!1;if(-1!=t.indexOf("||"))for(t=t.split("||"),C=C=0;C<t.length&&(g||!(g=u.toString().toUpperCase()==t[C]));C++);else g=u.toString().toUpperCase()==t;g?void 0!==k&&""!=k?u=1==w?x(a,k):r(m(k)):void 0!==k&&(u=""):void 0!==l&&""!=l?u=1==w?x(a,l):r(m(l)):void 0!==l&&(u="")}else if(3==w&&void 0!==g[1]){g=g[1].toString();t=0;C=!0;n=parseInt(u);if(isNaN(n))C=!1;else for(t=0;t<g.length;t++)if(C&&(E=g.charAt(t),"1"==E||"0"==E))if(0!=(n>>
t)%2){if("0"==E){C=!1;break}}else if("1"==E){C=!1;break}C?void 0!==k&&""!=k?u=1==w?x(a,k):r(m(k)):void 0!==k&&(u=""):void 0!==l&&""!=l?u=1==w?x(a,l):r(m(l)):void 0!==l&&(u="")}f=e(z[0]+p+z[1],u+"",f)}else y("too long or short Value[*..*] in "+b+" on "+f.substr(q,p-q)),q+=1;p=q=0;for(g="";-1!=f.indexOf(A[0],q);)if(w=k=t=-1,q=f.indexOf(A[0],q),p=f.indexOf(A[1],q+A[0].length),g="",c(g),l="",-1!=p&&195>p-q&&0<p-q){w=f.substr(q+A[0].length,p-(q+A[0].length));u=w.split(",");l="";p=2;g="";for(p=2;p<u.length;p++)g=
u[p],-1!=g.indexOf("if=`")?c(g):-1!=g.indexOf("limit=`")?(k=parseInt(e("limit=","",e("`","",g))),1>k&&(k=-1)):-1!=g.indexOf("default=`")&&(F=e("default=","",e("`","",g)));g=a;p=u[0];g=v(a,m(p),O);t=0;C=g.length-1;0>C&&(l=l+F+"",y("No data in this array! "+p));p=0;n=g.length;for(p in g){n--;if(0<k&&t>=k)break;h(g[p])&&("object"==typeof g[p]&&(g[p].json2html_counter=t+"",g[p].json2html_key=p+"",0==t&&(g[p].json2html_first="1"),t==C&&(g[p].json2html_last="1"),0==(t+1)%2?g[p].json2html_even="1":g[p].json2html_odd=
"1"),l+=x(g[p],u[1]),t++)}f=e(A[0]+w+A[1],l,f)}else y("too long or short Foreach[!..!] in "+b+" on "+f.substr(q,p-q)),q+=1;for(p=q=0;-1!=f.indexOf(B[0],q);)w=t=-1,q=f.indexOf(B[0],q),p=f.indexOf(B[1],q+B[0].length),F=a,-1!=p&&95>p-q&&0<p-q?(p=w=f.substr(q+B[0].length,p-(q+B[0].length)),-1!=w.indexOf(",")&&(w=w.split(",",2),k=w[1],w=w[0],F=v(F,k,O)),f=e(B[0]+p+B[1],x(F,w),f)):(y("too long or short template{{..}} in "+b+" on "+f.substr(q,p-q)),q+=1);L--;G&&""!=I&&0==L&&(I="");return r(f)}function n(a){a=
Array.prototype.slice.call(a.getElementsByTagName("script"));for(var b=0;b<a.length;b++){if(""!=a[b].src){var c=document.getElementsByTagName("head")[0],h=r(a[b].src),d=e(".","_",e(":","_",e("/","_",h)));if(!document.getElementById(d)){var f=document.createElement("script");f.src=h;f.id=d;c.appendChild(f)}}else eval(a[b].innerHTML);a[b].parentElement.removeChild(a[b])}}function e(a,b,c){return void 0===c?c:c.split(a).join(b)}function r(a){return void 0===a||null===a?"":1>a.length?"":a.trim()}function y(a){G&&
console.log("Json2Html: "+a)}function J(a,b){var c="undefined"==typeof b?1:b,h="";c||(c=0);for(var d="",f=0;f<c+1;f++)d+="    ";if("object"==typeof a)for(var e in a)f=a[e],"object"==typeof f?(h+=d+"'"+e+"' :\n",h+=J(f,c+1)):h+=d+"'"+e+"' => \""+f+'"\n';else h="===>"+a+"<===("+typeof a+")";return h}function N(a,b,c,h){h="undefined"==typeof h?500:h;G&&y("Network: "+b+"\n"+J(c));a(JSON.parse('{"error":{"state":true,"title":"Network error","message":"'+e("'","",e('"',"",b))+'","code":'+h+"}}"))}function P(a,
b,c,h,d){var f={mode:"same-origin",cache:"no-cache",credentials:"same-origin",redirect:"follow"},e="JSON"==r(b).toUpperCase();"POST"==r(a).toUpperCase()?(f.method="POST",f.body=JSON.stringify(h),f.headers={"Content-Type":"application/json",Accept:e?"application/json":"text/html"}):(f.method="GET",f.headers={Accept:e?"application/json":"text/html"});fetch(c,f).then(function(a){if(!a.ok)throw Error(a.statusText);return e?a.json():a.text()}).then(function(a){d(a)})["catch"](function(a){e?N(d,a.message,
a):(G&&y(textStatus+"\n"+J(errorThrown)),alert('json2html: "'+c+'" '+a.message))})}function Q(a,b,c,h,d){var f=new XMLHttpRequest;f.withCredentials=!0;var e="JSON"==r(b).toUpperCase();a="POST"==r(a).toUpperCase();f.onload=function(a){if(4==f.readyState)if(200==f.status)if(a=f.responseText,e)try{d(JSON.parse(a))}catch(F){N(d,F.name,F,f.status)}else d(a);else N(d,"Wrong status "+f.status,{error:"XMLHttpRequest",status:f.status},f.status)};f.onerror=function(a){N(d,f.statusText,a,f.status)};f.open(a?
"POST":"GET",c,!0);a?(f.setRequestHeader("Content-Type","application/json"),f.setRequestHeader("Accept",e?"application/json":"text/html"),f.send(JSON.stringify(h))):(f.setRequestHeader("Accept",e?"application/json":"text/html"),f.send())}function aa(a,b,c){void 0===b?y("Undefined URL in templates array"):(H++,"fetch"in window?P("get","text",b,null,function(h){U(h,a,c,b)}):Q("get","text",b,null,function(h){U(h,a,c,b)}))}function U(a,b,c,h){h=h.substring(h.lastIndexOf("/")+1);h=r(h.substring(0,h.lastIndexOf(".")));
if(a.match(/^\s*?NextTemplateName:\s*?\S{1,100}\s*?$/m)){y("File with templates detected: "+h);a=a.split("NextTemplateName:");var d;for(d=0;d<a.length;d++){var f=a[d].indexOf("\n"),e;if(0<d){if(0>f||100<f){y("Strange template loaded from file "+h+'. All templates should be starter with line "NextTemplateName: name_of_template"');y(a[d]);continue}e=r(a[d].substring(0,f));f=r(a[d].substring(f+1))}else{f=r(a[d]);if(0==f.length){y('thete is nothing in first "'+h+'" of the content '+d);continue}e=h}0==
f.length?y("thete is nothing in one of the content "+d):(0==e.length&&(y("thete is no title in one of the templates "+d),e=h),b[e]=f,y("Loaded template "+e+" from file "+h))}}else b[h]=a,y("Loaded file "+h);H--;0==H&&c()}function V(a){var b={};a=a.querySelectorAll("input, select, textarea");for(var c=0;c<a.length;++c){var h=a[c],d=h.name;if(d){var f=h.value;"INPUT"==h.tagName.toUpperCase()&&"CHECKBOX"==h.type.toUpperCase()&&(h.checked||(f+="__false"));var m=b,k=d;if(/\[.*?\]/.test(k)){var n=k.split("[")[0],
d=k.match(/\[.*?\]/g),h=d.length,k=-1!=k.indexOf("[]");void 0===m[n]&&(m[n]=1==h&&k?[]:{});n=m[n];for(m=0;m<h;m++){var g=e("[","",e("]","",d[m]));m==h-1?""==g?Array.isArray(n)&&n.push(f):n[g]=f:(void 0===n[g]&&(n[g]=m==h-2&&k?[]:{}),n=n[g])}}else void 0===m[k]&&(m[k]=f)}}return b}function W(){if(!(1>H))return!1;var a=K,b;for(b in a)a[b]=e(z[0].charAt(0)+" "+z[0].charAt(1),z[0],a[b]),a[b]=e(A[0].charAt(0)+" "+A[0].charAt(1),A[0],a[b]),a[b]=e(B[0].charAt(0)+" "+B[0].charAt(1),B[0],a[b]),a[b]=e(z[1].charAt(0)+
" "+z[1].charAt(1),z[1],a[b]),a[b]=e(A[1].charAt(0)+" "+A[1].charAt(1),A[1],a[b]),a[b]=e(B[1].charAt(0)+" "+B[1].charAt(1),B[1],a[b]),a[b]=e(z[0]+"  ",z[0],a[b]),a[b]=e(z[0]+" ",z[0],a[b]),a[b]=e(A[0]+"  ",A[0],a[b]),a[b]=e(A[0]+" ",A[0],a[b]),a[b]=e(B[0]+"  ",B[0],a[b]),a[b]=e(B[0]+" ",B[0],a[b]),a[b]=e("  "+z[1],z[1],a[b]),a[b]=e(" "+z[1],z[1],a[b]),a[b]=e("  "+A[1],A[1],a[b]),a[b]=e(" "+A[1],A[1],a[b]),a[b]=e("  "+B[1],B[1],a[b]),a[b]=e(" "+B[1],B[1],a[b]),a[b]=e("` then `","`then`",a[b]),a[b]=
e("` then","`then",a[b]),a[b]=e("then `","then`",a[b]),a[b]=e("` else `","`else`",a[b]),a[b]=e("` else","`else",a[b]),a[b]=e("else `","else`",a[b]),a[b]=e("if = `","if=`",a[b]),a[b]=e("if= `","if=`",a[b]),a[b]=e("if =`","if=`",a[b]);R(K);X()}function Z(a){var b=ba,c,h,d,f;c=a.length&3;h=a.length-c;d=b;for(b=0;b<h;)f=a.charCodeAt(b)&255|(a.charCodeAt(++b)&255)<<8|(a.charCodeAt(++b)&255)<<16|(a.charCodeAt(++b)&255)<<24,++b,f=3432918353*(f&65535)+((3432918353*(f>>>16)&65535)<<16)&4294967295,f=f<<15|
f>>>17,f=461845907*(f&65535)+((461845907*(f>>>16)&65535)<<16)&4294967295,d^=f,d=d<<13|d>>>19,d=5*(d&65535)+((5*(d>>>16)&65535)<<16)&4294967295,d=(d&65535)+27492+(((d>>>16)+58964&65535)<<16);f=0;switch(c){case 3:f^=(a.charCodeAt(b+2)&255)<<16;case 2:f^=(a.charCodeAt(b+1)&255)<<8;case 1:f^=a.charCodeAt(b)&255,f=3432918353*(f&65535)+((3432918353*(f>>>16)&65535)<<16)&4294967295,f=f<<15|f>>>17,d^=461845907*(f&65535)+((461845907*(f>>>16)&65535)<<16)&4294967295}d^=a.length;d^=d>>>16;d=2246822507*(d&65535)+
((2246822507*(d>>>16)&65535)<<16)&4294967295;d^=d>>>13;d=3266489909*(d&65535)+((3266489909*(d>>>16)&65535)<<16)&4294967295;return(d^d>>>16)>>>0}function R(a,b){var e="undefined"==typeof b?[]:b;if(void 0===a)return"";if(null===a||Number.isInteger(a)||void 0===D||null===D||"object"!=typeof D)return a;if("string"===typeof a)return S(a);M--;if(0>M)return M++,alert("Stackoverflow protection triggered"),M=10,a;var h=!1;Array.isArray(e)&&0<e.length&&(h=!0);for(var d in a)if(void 0!==a[d]&&null!==a[d]&&!Number.isInteger(a[d]))if(Array.isArray(a[d])||
"object"==typeof a[d])R(a[d],e);else if("string"===typeof a[d]||a[d]instanceof String)h?c(e,d,!0)&&(a[d]=S(a[d])):a[d]=S(a[d]);M++;return a}function S(a){if(void 0===a)return"";if(void 0===D||null===D||"object"!=typeof D)return a;var b,c;if(0>a.length-7)return a;for(var e,d=a.indexOf("@str."),f=300;-1!=d;){f--;if(0>f){alert("Loop protection: JS template library");break}c=d+5;a:{b=c;e=a;var m,k,n=-1,g=e.length;for(m=0;41>m;m++){n=b+m;if(n>=g){b=g;break a}k=e.charCodeAt(n);if(!(48<=k&&57>=k||65<=k&&
90>=k||97<=k&&122>=k||95==k)){b=n;break a}}b=n}e=b-c;2<e||40>e?(c=a.substr(c,e),void 0!==D[c]?(a=a.replace("@str."+c,D[c]),d=a.indexOf("@str.",d+1)):(console.log('No translation for key: "'+c+'"'),d=a.indexOf("@str.",b))):d=a.indexOf("@str.",b)}return a}var G=!1,z=["[*","*]"],A=["[!","!]"],B=["{{","}}"],I="",T=Math.floor(999*Math.random()+1),L=0,H=0;if(void 0!==jQuery)try{jQuery.fn.serializeHtmlForm=function(){return V(this[0])},jQuery.fn.injectJSON=function(a,b){var c=x(a,b);this.each(function(){jQuery(this).html(c);
n(jQuery(this)[0])});return this}}catch(a){}var X=0,K={},ba=Math.round(1E4*Math.random()+1E4),M=10,D=null;return{inject:x,inject2DOM:function(a,b,c){var e=null;try{e=document.querySelectorAll(c)}catch(d){}if(void 0===e||null==e)return"";a=x(a,b);for(b=0;b<e.length;++b)c=e[b],"innerHTML"in c&&(c.innerHTML=a,n(c));return a},getJSON:function(a,b){"fetch"in window?P("get","json",a,null,b):Q("get","json",a,null,b)},postJSON:function(a,b,c){"fetch"in window?P("post","json",a,b,c):Q("post","json",a,b,c)},
loadTemplatesArray:function(a,b,c){c="undefined"==typeof c?!0:c;1>H||alert("Critical error.\nTrying to load templates before previous templates request is completed");c&&(K={});X=b;H++;for(b=0;b<a.length;b++)aa(K,a[b],W);H--;W()},setTranslationArray:function(a){void 0===a?console.log("Translation array is undefined"):(D=a,0==Object.keys(D).length&&(D=null))},translate:R,executeJS:n,printObject:J,setDebug:function(a){G=a},serializeHtmlForm:function(a){a=document.querySelector(a);return void 0===a||
null==a?{}:V(a)}}}(),jth=json2html;

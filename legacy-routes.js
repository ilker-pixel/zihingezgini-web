(() => {
  const hash = window.location.hash || "";
  const summaries = {"1":"/kitap-ozetleri/1-zamanin-kisa-tarihi/","3":"/kitap-ozetleri/3-fizik-uzerine-yedi-kisa-ders/","4":"/kitap-ozetleri/4-evrenin-dokusu/","5":"/kitap-ozetleri/5-kaos-yeni-bir-bilim-teorisi/","6":"/kitap-ozetleri/6-sarhos-yuruyusu/","11":"/kitap-ozetleri/11-ucuncu-sempanze-insan-turunun-evrimi-ve-gelecegi/","13":"/kitap-ozetleri/13-buyuk-tarih/","90":"/kitap-ozetleri/90-sisifos-soyleni/","130":"/kitap-ozetleri/130-yargi-gucunun-elestirisi/","179":"/kitap-ozetleri/179-risk-toplumu/","224":"/kitap-ozetleri/224-oryantalizm/","248":"/kitap-ozetleri/248-yapay-zeka-dusunen-insanlar-icin-bir-rehber/","277":"/kitap-ozetleri/277-karisini-sapka-sanan-adam/"};
  let target = null;
  if (hash.startsWith("#/post/")) target = "/yazilar/" + hash.slice(7) + "/";
  else if (hash === "#/roadmap") target = "/okuma-haritasi/";
  else if (hash === "#/library") target = "/arastirma-arsivi/";
  else if (hash === "#/about") target = "/zihin-odasi/";
  else if (hash === "#/random") target = "/rastgele/";
  else {
    const match = hash.match(/^#\/book\/(\d+)\/summary$/);
    if (match && summaries[match[1]]) target = summaries[match[1]];
  }
  if (target) window.location.replace(target);
})();

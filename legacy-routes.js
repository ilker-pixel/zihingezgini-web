(() => {
  const hash = window.location.hash || "";
  const summaries = {"1":"/kitap-ozetleri/1-zamanin-kisa-tarihi/","2":"/kitap-ozetleri/2-kozmos/","3":"/kitap-ozetleri/3-fizik-uzerine-yedi-kisa-ders/","4":"/kitap-ozetleri/4-evrenin-dokusu/","5":"/kitap-ozetleri/5-kaos-yeni-bir-bilim-teorisi/","6":"/kitap-ozetleri/6-sarhos-yuruyusu/","7":"/kitap-ozetleri/7-turlerin-kokeni/","8":"/kitap-ozetleri/8-gen-bencildir/","11":"/kitap-ozetleri/11-ucuncu-sempanze-insan-turunun-evrimi-ve-gelecegi/","13":"/kitap-ozetleri/13-buyuk-tarih/","18":"/kitap-ozetleri/18-sessiz-bahar/","31":"/kitap-ozetleri/31-nicin-uyuruz/","34":"/kitap-ozetleri/34-beden-kayit-tutar/","36":"/kitap-ozetleri/36-hizli-ve-yavas-dusunme/","38":"/kitap-ozetleri/38-dil-icgudusu/","60":"/kitap-ozetleri/60-sevme-sanati/","61":"/kitap-ozetleri/61-kendime-dusunceler/","70":"/kitap-ozetleri/70-tao-te-ching/","81":"/kitap-ozetleri/81-kahramanin-bin-yuzu/","88":"/kitap-ozetleri/88-insanin-anlam-arayisi/","90":"/kitap-ozetleri/90-sisifos-soyleni/","92":"/kitap-ozetleri/92-mukaddime/","95":"/kitap-ozetleri/95-prens/","99":"/kitap-ozetleri/99-ozgurluk-uzerine/","121":"/kitap-ozetleri/121-meditasyonlar/","130":"/kitap-ozetleri/130-yargi-gucunun-elestirisi/","138":"/kitap-ozetleri/138-bilimsel-devrimlerin-yapisi/","142":"/kitap-ozetleri/142-karanlik-bir-dunyada-bilimin-mum-isigi/","143":"/kitap-ozetleri/143-siyah-kugu/","151":"/kitap-ozetleri/151-uluslarin-zenginligi/","157":"/kitap-ozetleri/157-borc-ilk-5000-yil/","179":"/kitap-ozetleri/179-risk-toplumu/","182":"/kitap-ozetleri/182-felsefi-sorusturmalar/","185":"/kitap-ozetleri/185-metaforlarla-yasamak/","195":"/kitap-ozetleri/195-televizyon-olduruyor/","211":"/kitap-ozetleri/211-fotograf-uzerine/","213":"/kitap-ozetleri/213-gorme-bicimleri/","216":"/kitap-ozetleri/216-ikinci-cins/","224":"/kitap-ozetleri/224-oryantalizm/","238":"/kitap-ozetleri/238-hapishanenin-dogusu/","243":"/kitap-ozetleri/243-yorgunluk-toplumu/","244":"/kitap-ozetleri/244-sapiens-hayvanlardan-tanrilara/","248":"/kitap-ozetleri/248-yapay-zeka-dusunen-insanlar-icin-bir-rehber/","266":"/kitap-ozetleri/266-boyle-buyurdu-zerdust/","277":"/kitap-ozetleri/277-karisini-sapka-sanan-adam/","284":"/kitap-ozetleri/284-ezilenlerin-pedagojisi/","287":"/kitap-ozetleri/287-aydinlanma-simdi/","294":"/kitap-ozetleri/294-algi-kapilari/"};
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

#!/usr/bin/env python3
"""Replace source URLs confirmed as permanently unavailable in the 2026 audit."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPLACEMENTS = {
    "https://www.nature.com/scitable/knowledge/library/kin-selection-13216114/": ("https://plato.stanford.edu/entries/altruism-biological/", "Stanford Encyclopedia of Philosophy - Biological Altruism"),
    "https://www.ucl.ac.uk/biosciences/people/dr-nick-lane": ("https://nick-lane.net/about/", "Nick Lane - About and research"),
    "https://www.jareddiamond.org/guns-germs-and-steel": ("https://www.penguin.co.uk/books/355771/guns-germs-and-steel-by-jared-diamond/9780099302780", "Penguin - Guns, Germs and Steel"),
    "https://iep.utm.edu/lucretius/": ("https://plato.stanford.edu/entries/lucretius/", "Stanford Encyclopedia of Philosophy - Lucretius"),
    "https://www.who.int/publications/i/item/9789241572415": ("https://www.who.int/publications/i/item/ddt-in-indoor-residual-spraying-human-health-aspects", "WHO - DDT in Indoor Residual Spraying"),
    "https://dornsife.usc.edu/bci/antonio-damasio/": ("https://dornsife.usc.edu/profile/antonio-damasio/", "USC Dornsife - Antonio Damasio"),
    "https://www.mpi.nl/research/research-databases": ("https://www.mpi.nl/", "Max Planck Institute for Psycholinguistics"),
    "https://stevenpinker.com/publications/blank-slate-modern-denial-human-nature": ("https://www.penguinrandomhouse.com/books/290730/the-blank-slate-by-steven-pinker/", "Penguin Random House - The Blank Slate"),
    "https://psychology.ucsd.edu/people/profiles/vsramachandran.html": ("https://psychology.ucsd.edu/people/profiles/vramachandran.html", "UC San Diego - V. S. Ramachandran"),
    "https://thomasmetzinger.com/books/the-ego-tunnel/": ("https://www.hachettebookgroup.com/titles/thomas-metzinger/the-ego-tunnel/9780465020690/", "Basic Books - The Ego Tunnel"),
    "https://cogs.indiana.edu/directory/faculty/hofstadter-douglas.html": ("https://cogs.indiana.edu/directory/faculty/profile.php?faculty=dughof", "Indiana University - Douglas Hofstadter"),
    "https://iep.utm.edu/nagel/": ("https://www.britannica.com/biography/Thomas-Nagel", "Encyclopaedia Britannica - Thomas Nagel"),
    "https://iep.utm.edu/eliade/": ("https://www.britannica.com/biography/Mircea-Eliade", "Encyclopaedia Britannica - Mircea Eliade"),
    "https://iep.utm.edu/thucydides/": ("https://www.britannica.com/biography/Thucydides-Greek-historian", "Encyclopaedia Britannica - Thucydides"),
    "https://iep.utm.edu/ibn-khaldun/": ("https://www.britannica.com/biography/Ibn-Khaldun", "Encyclopaedia Britannica - Ibn Khaldun"),
    "https://oll.libertyfund.org/title/democracy-in-america-historical-critical-edition-vol-1": ("https://oll.libertyfund.org/titles/schleifer-democracy-in-america-historical-critical-edition-vol-1", "Online Library of Liberty - Democracy in America, Vol. 1"),
    "https://iep.utm.edu/sci-change/": ("https://plato.stanford.edu/entries/scientific-revolutions/", "Stanford Encyclopedia of Philosophy - Scientific Revolutions"),
    "https://www.versobooks.com/products/1908-against-method": ("https://www.versobooks.com/en-gb/products/1041-against-method", "Verso - Against Method"),
    "https://iep.utm.edu/feyerabe/": ("https://plato.stanford.edu/entries/feyerabend/", "Stanford Encyclopedia of Philosophy - Paul Feyerabend"),
    "https://guides.library.cornell.edu/carl_sagan": ("https://www.loc.gov/news/2012/12-104.html", "Library of Congress - Carl Sagan Papers"),
    "https://www.cornell.edu/video/playlist/richard-feynman-messenger-lectures": ("https://www.feynmanlectures.caltech.edu/messenger.html", "Caltech - Feynman's Messenger Lectures"),
    "https://press.princeton.edu/books/paperback/9780307719225/why-nations-fail": ("https://news.mit.edu/2012/why-nations-fail-0323", "MIT News - Why Nations Fail"),
    "https://iep.utm.edu/wittgenstein/": ("https://plato.stanford.edu/entries/wittgenstein/", "Stanford Encyclopedia of Philosophy - Wittgenstein"),
    "https://www.seuil.com/ouvrage/mythologies-roland-barthes/9782757841846": ("https://us.macmillan.com/books/9780809071944/mythologies/", "Macmillan - Mythologies"),
    "https://iep.utm.edu/barthes/": ("https://www.britannica.com/biography/Roland-Gerard-Barthes", "Encyclopaedia Britannica - Roland Barthes"),
    "https://www.cambridge.org/core/books/interpretation-and-overinterpretation/": ("https://www.cambridge.org/core/books/interpretation-and-overinterpretation/1E7557106821FE18EA4D741F9342D3F2", "Cambridge University Press - Interpretation and Overinterpretation"),
    "https://plato.stanford.edu/entries/eco/": ("https://www.britannica.com/biography/Umberto-Eco", "Encyclopaedia Britannica - Umberto Eco"),
    "https://www.mit.edu/people/sturkle/": ("https://sherryturkle.mit.edu/", "MIT - Sherry Turkle"),
    "https://www.wiley.com/en-us/The+Ideology+of+the+Aesthetic-p-9780631163028": ("https://books.google.com/books/about/The_Ideology_of_the_Aesthetic.html?id=QzYDaoaUyLYC", "Google Books - The Ideology of the Aesthetic"),
    "https://www.versobooks.com/products/1548-critique-of-everyday-life": ("https://www.versobooks.com/products/1353-critique-of-everyday-life-vol-1", "Verso - Critique of Everyday Life"),
    "https://www.bl.uk/collection-guides/john-berger-archive": ("https://searcharchives.bl.uk/?per_page=50&q=032-002358665&sort=hierarchy", "British Library - John Berger Archive"),
    "https://www.bbc.co.uk/programmes/p00hqlvs": ("https://www.penguin.co.uk/books/261355/ways-of-seeing-by-john-berger/9780141035796", "Penguin - Ways of Seeing"),
    "https://www.brooklyn.edu/faculty-staff/silvia-federici/": ("https://www.unimi.it/en/ugov/person/silvia-federici", "University of Milan - Silvia Federici"),
    "https://www.versobooks.com/products/2259-imagined-communities": ("https://www.versobooks.com/products/1126-imagined-communities", "Verso - Imagined Communities"),
    "https://government.cornell.edu/benedict-anderson": ("https://news.cornell.edu/stories/2015/12/benedict-anderson-who-wrote-imagined-communities-dies", "Cornell Chronicle - Benedict Anderson"),
    "https://www.versobooks.com/products/99-the-black-atlantic": ("https://www.versobooks.com/en-gb/products/1418-the-black-atlantic", "Verso - The Black Atlantic"),
    "https://plato.stanford.edu/entries/bachelard/": ("https://www.britannica.com/biography/Gaston-Bachelard", "Encyclopaedia Britannica - Gaston Bachelard"),
    "https://www.nature.com/scitable/knowledge/library/the-development-of-agriculture-10026280/": ("https://www.penn.museum/research/publications/publication/743", "Penn Museum - Origins of Agriculture"),
    "https://futureoflife.org/ai-safety/": ("https://futureoflife.org/our-position-on-ai/", "Future of Life Institute - Our Position on AI"),
    "https://melaniemitchell.me/books/": ("https://melaniemitchell.me/", "Melanie Mitchell - Official site"),
    "https://cyberlaw.stanford.edu/content/files/images/4/44/heidegger_martin_the_question_concerning_technology_and_other_essays.pdf": ("https://plato.stanford.edu/entries/technology/", "Stanford Encyclopedia of Philosophy - Philosophy of Technology"),
    "https://www.caltech.edu/about/news/sean-carroll-joins-caltech-faculty": ("https://physics-astronomy.jhu.edu/directory/sean-carroll/", "Johns Hopkins University - Sean Carroll"),
    "https://uis.unesco.org/sites/default/files/documents/a-place-to-learn-lessons-from-research-on-learning-environments-2012-en.pdf": ("https://www.unicef.org/innocenti/reports/learning-everyone-global-report", "UNICEF - Learning is for Everyone"),
}


def main() -> int:
    replaced = 0
    for path in sorted((ROOT / "data" / "summaries").glob("*.json"), key=lambda item: int(item.stem)):
        summary = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for source in summary.get("sources", []):
            replacement = REPLACEMENTS.get(source.get("url"))
            if replacement:
                source["url"], source["title"] = replacement
                changed = True
                replaced += 1
        if changed:
            path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Replaced {replaced} permanently unavailable source links.")
    return 0 if replaced == len(REPLACEMENTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())

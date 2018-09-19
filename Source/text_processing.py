from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk import *
import re
import string

list_of_oss_license = {
                        "BSD": ["2-clause BSD License", "BSD-2-Clause", "3-clause BSD License", "BSD-3-Clause", "BSD+Patent", "BSD-2-Clause-Patent"],
                        "AFL": ["Academic Free License 3.0", "AFL-3.0"],
                        "APL": ["Adaptive Public License", "APL-1.0"], 
                        "Apache": ["Apache License 2.0", "Apache-2.0"], 
                        "APSL": ["Apple Public Source License", "APSL-2.0"], 
                        "Artistic": ["Artistic License 2.0", "Artistic-2.0"], 
                        "AAL": ["Attribution Assurance License"], 
                        "BSL": ["Boost Software License", "BSL-1.0"],
                        "CECILL": ["CeCILL License 2.1", "CECILL-2.1"], 
                        "CATOSL": ["Computer Associates Trusted Open Source License 1.1", "CATOSL-1.1"],
                        "MIT": ["MIT License"],
                        "AGPL": ["GNU Affero General Public License version 3", "AGPL-3.0"],
                        "GPL": ["GNU General Public License", "General Public License", "GNU General Public License version 2", "GPL-2.0",
                        "GNU General Public License version 3", "GPL-3.0"],
                        "LGPL": ["GNU Lesser General Public License", "Lesser General Public License", "GNU Lesser General Public License version 2.1",
                        "LGPL-2.1", "GNU Lesser General Public License version 3", "LGPL-3.0"],
                        "Zlib": ["zlib/libpng license", "libpng license", "Zlib license"],
                        "CDDL": ["Common Development and Distribution License 1.0", "CDDL-1.0"],
                        "CPAL": ["Common Public Attribution License 1.0", "CPAL-1.0"],
                        "CUA-OPL": ["CUA Office Public License Version 1.0", "CUA-OPL-1.0"],
                        "EUDatagrid": ["EU DataGrid Software License"],
                        "EPL": ["Eclipse Public License 1.0", "EPL-1.0", "Eclipse Public License 2.0", "EPL-2.0"],
                        "eCos": ["eCos License", "eCos License version 2.0"],
                        "ECL": ["Educational Community License, Version 2.0 ", "ECL-2.0"],
                        "EFL": ["Eiffel Forum License V2.0", "EFL-2.0"],
                        "Entessa": ["Entessa Public License", "Entessa"],
                        "EUPL": ["European Union Public License Version 1.1", "EUPL-1.1"],
                        "EUPL": ["European Union Public License Version 1.1", "EUPL-1.1"], 
                        "Fair": ["Fair License", "Fair"],
                        "Frameworx": ["Frameworx License", "Frameworx-1.0"],
                        "Public": ["Free Public License"],
                        "HPND": ["Historical Permission Notice and Disclaimer", "HPND"],
                        "IPL": ["IBM Public License 1.0", "IPL-1.0"],
                        "IPA": ["IPA Font License"],
                        "ISC": ["ISC License"],
                        "LPPL": ["LaTeX Project Public License 1.3c", "LPPL-1.3c"],
                        "LiLiQ-P": ["Licence Libre du Québec – Permissive", "LiLiQ-P version 1.1"],
                        "LiLiQ-R": ["Licence Libre du Québec – Réciprocité", "LiLiQ-R version 1.1"],
                        "LiLiQ-R+": ["Licence Libre du Québec – Réciprocité forte", "LiLiQ-R+ version 1.1"],
                        "LPL": ["Lucent Public License Version 1.02", "LPL-1.02"],
                        "MirOS": ["MirOS Licence"],
                        "MS-PL": ["Microsoft Public License"],
                        "MS-RL": ["Microsoft Reciprocal License"],
                        "Motosoto": ["Motosoto License"], 
                        "MPL": ["Mozilla Public License 1.0", "MPL-1.0", "Mozilla Public License 1.1", "MPL-1.1", "Mozilla Public License 2.0", "MPL-2.0"],
                        "Multics": ["Multics License"], 
                        "NASA": ["NASA Open Source Agreement 1.3", "NASA-1.3"],
                        "NTP": ["NTP License"],
                        "Naumen": ["Naumen Public License"],
                        "NGPL": ["Nethack General Public License"],
                        "Nokia": ["Nokia Open Source License"],
                        "NPOSL": ["Non-Profit Open Software License 3.0", "NPOSL-3.0"],
                        "OCLC": ["OCLC Research Public License 2.0", "OCLC-2.0"],
                        "OGTSL": ["Open Group Test Suite License"],
                        "OSL": ["Open Software License 3.0", "OSL-3.0"],
                        "OSET": ["OSET Public License version 2.1"],
                        "PHP": ["PHP License 3.0", "PHP-3.0"],
                        "PostgreSQL": ["The PostgreSQL License"],
                        "Python": ["Python License", "Python-2.0"],
                        "CNRI": ["CNRI Python license", "CNRI-Python"], 
                        "QPL": ["Q Public License", "QPL-1.0"],
                        "RPSL": ["RealNetworks Public Source License V1.0", "RPSL-1.0"],
                        "RPL": ["Reciprocal Public License 1.5", "RPL-1.5"],
                        "RSCPL": ["Ricoh Source Code Public License"],
                        "OFL": ["SIL Open Font License 1.1", "OFL-1.1"],
                        "SimPL": ["Simple Public License 2.0", "SimPL-2.0"],
                        "Sleepycat": ["Sleepycat License"],
                        "SPL": ["Sun Public License 1.0", "SPL-1.0"],
                        "Watcom": ["Sybase Open Watcom Public License 1.0", "Watcom-1.0"],
                        "NCSA": ["University of Illinois/NCSA Open Source License", "University of Illinois", "NCSA Open Source License"],
                        "UPL": ["Universal Permissive License"],
                        "Upstream": ["Upstream Compatibility License v1.0"],
                        "VSL": ["Vovida Software License v. 1.0", "VSL-1.0"],
                        "W3C": ["W3C License"],
                        "WXwindows": ["wxWindows Library License"],
                        "Xnet": ["X.Net License"],
                        "0BSD": ["Zero Clause BSD License"],
                        "ZPL": ["Zope Public License 2.0", "ZPL-2.0"]
                        }


def _cleanText(text):

    text = re.sub('\n+', ' ', text)
    #text = re.sub(r'http?:\/\/.*', ' ', text)
    text = re.sub(' +', " ", text)
    text = bytes(text, "UTF-8")
    text = text.decode("ascii", "ignore")

    cleanText = []
    text = text.split(' ')

    for word in text:
        word = word.strip(string.punctuation)
        if len(word)>1:
            cleanText.append(word)
    return ' '.join(cleanText)
    #return cleanText



def _getBrowserData(url):    
    browser_data = urlopen(url)
    bsObj_text = BeautifulSoup(browser_data, 'lxml').text
    return _cleanText(bsObj_text)


def _get_all_phrases_containing_tar_wrd(target_word, url, left_margin = 10, right_margin = 10):
    """
        Function to get all the phases that contain the target word in a text/passage tar_passage.
        Workaround to save the output given by nltk Concordance function
         
        str target_word, str tar_passage int left_margin int right_margin --> list of str
        left_margin and right_margin allocate the number of words/pununciation before and after target word
        Left margin will take note of the beginning of the text
    """

    tar_passage = _getBrowserData(url)
    
    ## Create list of tokens using nltk function
    tokens = word_tokenize(tar_passage)
     
    ## Create the text of tokens
    text = Text(tokens)
    
    ## Collect all the index or offset position of the target word
    c = ConcordanceIndex(text.tokens, key = lambda s: s.lower())

    
    ## Collect the range of the words that is within the target word by using text.tokens[start;end].
    ## The map function is use so that when the offset position - the target range < 0, it will be default to zero
    concordance_txt = ([text.tokens[list(map(lambda x: x-5 if (x-left_margin)>0 else 0,[offset]))[0]:offset+1] for offset in c.offsets(target_word)])

    if len(concordance_txt) == 0:
        missed_license_names = []
        for t in tokens:
            if re.search('( |-|_|\/)license', t.lower()) != None:
                missed_license_names.append(t)
        return missed_license_names
    
    ## join the sentences for each of the target phrase and return it
    return [''.join([x+' ' for x in con_sub]) for con_sub in concordance_txt]
    #return True


def getLicenseNames(url_list):
    
    license_names = []
    is_public_license = False
    
    for url in url_list:

        results = _get_all_phrases_containing_tar_wrd('license', url)
        
        for result in results:
            
            for key, val in list_of_oss_license.items():
                
                l = [v for v in val if (result.lower().find(v.lower()) != -1 and (len(license_names)>0 and val not in license_names))]
                results = None
                
                if len(l) > 0 or result.find(key) != -1:
                    results = key+" "+"License"

                if results != None and results not in license_names:
                    if results == "Public License":
                        is_public_license = True
                    license_names.append(results)

    if is_public_license and any(re.search("GPL|LGPL", val, re.IGNORECASE) != None for val in license_names):
        
        try:
            index = license_names.index("Public License")
        except ValueError:
            pass
        else:
            del license_names[index]

        if "GPL License" in license_names and "LGPL License" in license_names:
            try:
                index = license_names.index("LGPL License")
            except ValueError:
                pass
            else:
                del license_names[index]

    if len(license_names) == 0:
        return ["Unlicensed"]
    return license_names


#TODO: Extract license which are not given in the above dictionary.


if __name__ == "__main__":

    url_list = ['https://github.com/Marak/asciimo/blob/master/MIT-LICENSE.txt', \
        'https://github.com/Marak/asciimo/blob/master/GPL-LICENSE.txt', \
        'https://github.com/Marak/asciimo']
    
    print(getLicenseNames(url_list))

import re
from collections import defaultdict


class _HashPrefixRemover:
    PREFIXES_TO_REMOVE = ['OPEN', 'RES', 'LNK', 'IND', 'CAP', 'TRN', 'TRP', 'MOS', 'DIO', 'ZEN', 'LED', 'TRC', 'TRF']

    def __init__(self):
        self.prefixesByLength = defaultdict(set)
        for p in self.PREFIXES_TO_REMOVE:
            self.prefixesByLength[len(p)].add(p)
            
        self.lengths = sorted(self.prefixesByLength.keys(), reverse=True)

    def clean(self, text:str) -> str:
        textLen = len(text)
        
        for length in self.lengths:
            if textLen < length:
                continue
                
            if text[:length] in self.prefixesByLength[length]:
                return text[length:].strip()
                
        return text
    
    

class TracebilityFailsParser:
    def __init__(self):
        self.prefixRemover = _HashPrefixRemover()

    def parse(self, texts:list[str]) -> list[str]:
        testPointsPatetrn = r'^(SHO|FLOAT|LNK2TP)'
        
        componentsSet = set()
        for text in texts:
            if re.search(testPointsPatetrn, text):
                subResult = self._getTestPoints(text)
            else:
                sanitizedText = self._sanitizeToAlphaNumeric(text)
                subResult = self._getComponentsFromSanitizedString(sanitizedText)
            
            if subResult:
                componentsSet.update(subResult)

        return list(componentsSet)
    
    def _getTestPoints(self, text:str) -> list[str]:
        # SHO NET GND (TP 22) (TP 6-2,42,55,162-163) (1.0000 -> ['22', '6', '2', '42', '55', '162', '163']
        preixedGroupsPattern = r'\([A-Z]+\s*([\d\s,-]+)\)'
        prefixedBlocks = re.findall(preixedGroupsPattern, text)
        if prefixedBlocks:
            result = []
            for block in prefixedBlocks:
                result.extend(re.findall(r'\d+', block))
            return result

        # 'FLOAT (303)' -> ['303'] and 'SHO-HighRes-LowCap (298 256)' -> ['298', '256']
        testPointsInLastBracketPattern = r'\(([\d\s]+)\)'
        bracketGroup = re.search(testPointsInLastBracketPattern, text)
        if bracketGroup:
            return bracketGroup.group(1).split()
        
        # 'LNK2TP 3.6V 305-37' -> ['305', '37']
        testPointsHyphenPattern = r'\b(\d+)-(\d+)\s*$'
        hyphenGroup = re.search(testPointsHyphenPattern, text)
        if hyphenGroup:
            return list(hyphenGroup.groups())
        

    def _sanitizeToAlphaNumeric(self, text:str) -> str:
        sanitized = ''
        for char in text:
            char = char.upper() if char.isalnum() else ' '
            sanitized += char
        
        sanitized = sanitized.strip()
        sanitized = ' '.join(sanitized.split())
        return sanitized

    def _getComponentsFromSanitizedString(self, text:str) -> list[str]:
        componentPattern = r'^[A-Z]+\d+$'
        rawComponents = [item for item in text.split(' ') if re.search(componentPattern, item)]
        return [self.prefixRemover.clean(item) for item in rawComponents]

        
if __name__ == '__main__':
    fails = [
        'CAP C138/C139 10.1u 20% -20%', 
        'CAP C200/C229/C76/C77/C115/C117/C208/C75/C114/C116', 
        'CAPC32 1u 10% -10%', 
        'CAPC35 1u 10% -10%', 
        'JSCAN D26-E'
    ]

    parser = TracebilityFailsParser()
    print(parser.parse(fails))
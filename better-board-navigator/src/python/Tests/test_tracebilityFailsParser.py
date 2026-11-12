import pytest
from tracebilityFailsParser import TracebilityFailsParser

@pytest.fixture
def parser():
    return TracebilityFailsParser()

@pytest.mark.parametrize('inputText, expectedOutput', [
    ('FLOAT (303)', 'FLOAT 303'),
    ('SHO-HighRes-LowCap (298 256)', 'SHO HIGHRES LOWCAP 298 256'),
    ('SHO NET GND (TP 22) (TP 6-2,42,55,162-163) (1.0000', 'SHO NET GND TP 22 TP 6 2 42 55 162 163 1 0000'),
    ('LNK2TP 3.6V 305-37', 'LNK2TP 3 6V 305 37'),
    ('LNK2TP +12V 325-341', 'LNK2TP 12V 325 341'),
    ('OPENSW1-1 (TP 3-50)', 'OPENSW1 1 TP 3 50'),
    ('OPENJ6 (TP 193-197) Do Not Mount!', 'OPENJ6 TP 193 197 DO NOT MOUNT'),
    ('RESR122 150K 1%', 'RESR122 150K 1'),
    ('LNKR16 182-183', 'LNKR16 182 183'),
    ('RESRB1-1-8 10K 5%', 'RESRB1 1 8 10K 5'),
    ('RES R142/R143 50 1%', 'RES R142 R143 50 1'),
    ('RESNTC1 4.7 20%', 'RESNTC1 4 7 20'),
    ('LNK R169 + RESR154 220K 5%', 'LNK R169 RESR154 220K 5'),
    ('RES TR42-RBE/TR48-RBE 25.85K 30%', 'RES TR42 RBE TR48 RBE 25 85K 30'),
    ('RESR270 // R275+C151 6.96K 10%', 'RESR270 R275 C151 6 96K 10'),
    ('CAPC144 100n 10% -10%', 'CAPC144 100N 10 10'),
    ('CAP C161/C165 13.6n 10% -10%', 'CAP C161 C165 13 6N 10 10'),
    ('CAP C175/C193/C201/C202/C226/C227/C228/C187/C192/C176/ 72.1001uF 11% -11%', 
        'CAP C175 C193 C201 C202 C226 C227 C228 C187 C192 C176 72 1001UF 11 11'),
    ('CAP EC1/C45/C63/C69/C97/C145/C154/C146/C147/C152/C153/ 89.8uF 15% -15%', 
        'CAP EC1 C45 C63 C69 C97 C145 C154 C146 C147 C152 C153 89 8UF 15 15'),
    ('CAPC2\\C46\\C47\\C4\\C5\\C6\\C42\\C23\\C24\\C25\\C26\\C27\\C28\\C29\\C17\\C10\\C11\\C21\\C13\\C14\\C18 320.22uF +20% -20%', 
        'CAPC2 C46 C47 C4 C5 C6 C42 C23 C24 C25 C26 C27 C28 C29 C17 C10 C11 C21 C13 C14 C18 320 22UF 20 20'),
    ('DSC-C30', 'DSC C30'),
    ('DSC-CP[C58]', 'DSC CP C58'),
    ('DSC-CP[C58, C85]', 'DSC CP C58 C85'),
    ('CAP.EC2 Reversed!', 'CAP EC2 REVERSED'),
    ('JSCAN U10-23', 'JSCAN U10 23'),
    ('CAPC26+C28 69pF 5% -5%', 'CAPC26 C28 69PF 5 5'),
    ('INDL1 10u 10% -10%', 'INDL1 10U 10 10'),
    ('TRNQ1 BC847B', 'TRNQ1 BC847B'),
    ('TRPQ37 BC857B', 'TRPQ37 BC857B'),
    ('MOSQ8 2N7002ET1G', 'MOSQ8 2N7002ET1G'),
    ('TRNTR1 BC847B', 'TRNTR1 BC847B'),
    ('DIOD1-D1 !BAV170_D', 'DIOD1 D1 BAV170 D'),
    ('ZENZ1 GWMMSZ5232B', 'ZENZ1 GWMMSZ5232B'),
    ('TVS D11', 'TVS D11'),
    ('TVS DD2-Z2 !CDSOT23-SM712', 'TVS DD2 Z2 CDSOT23 SM712'),
    ('LEDLD2 LHRF12243/F139/A', 'LEDLD2 LHRF12243 F139 A'),
    ('VDR1 PRESENT?', 'VDR1 PRESENT'),
    ('RELAY RL1 HF170F12-2H1DTF', 'RELAY RL1 HF170F12 2H1DTF'),
    ('OPTC OC3 K10104A', 'OPTC OC3 K10104A'),
    ('TRCTY1 BTP16-700BWRG', 'TRCTY1 BTP16 700BWRG'),
    ('T1 5-7 Presence test', 'T1 5 7 PRESENCE TEST'),
    ('TRFVT1-1', 'TRFVT1 1'),
    ('D13-01 ', 'D13 01'),
    ('C303', 'C303'),
    ('UNKNOWN FORMAT 123', 'UNKNOWN FORMAT 123')
])
def test__sanitizeToAlphaNumeric(parser, inputText, expectedOutput):
    assert parser._sanitizeToAlphaNumeric(inputText) == expectedOutput

@pytest.mark.parametrize('inputText, expectedOutput', [
    ('FLOAT (303)', ['303']),
    ('SHO-HighRes-LowCap (298 256)', ['298', '256']),
    ('LNK2TP 3.6V 305-37', ['305', '37']),
    ('LNK2TP +12V 325-341', ['325', '341']),
    ('SHO NET GND (TP 22) (TP 6-2,42,55,162-163) (1.0000', ['22', '6', '2', '42', '55', '162', '163'])
])
def test__getTestPoints(parser, inputText, expectedOutput):
    assert parser._getTestPoints(inputText) == expectedOutput


@pytest.mark.parametrize('inputText, expectedOutput', [
    ('FLOAT (303)', []),
    ('SHO-HighRes-LowCap (298 256)', []),
    ('LNK2TP 3.6V 305-37', []),
    ('LNK2TP +12V 325-341', []),
    ('SHO NET GND (TP 22) (TP 6-2,42,55,162-163) (1.0000', []),
    ('OPENSW1-1 (TP 3-50)', ['SW1']),
    ('OPENJ6 (TP 193-197) Do Not Mount!', ['J6']),
    ('RESR122 150K 1%', ['R122']),
    ('LNKR16 182-183', ['R16']),
    ('RESRB1-1-8 10K 5%', ['RB1']),
    ('RES R142/R143 50 1%', ['R142', 'R143']),
    ('RESNTC1 4.7 20%', ['NTC1']),
    ('LNK R169 + RESR154 220K 5%', ['R169', 'R154']),
    ('RES TR42-RBE/TR48-RBE 25.85K 30%', ['TR42', 'TR48']),
    ('RESR270 // R275+C151 6.96K 10%', ['R270', 'R275', 'C151']),
    ('CAPC144 100n 10% -10%', ['C144']),
    ('CAP C161/C165 13.6n 10% -10%', ['C161', 'C165']),
    ('CAP C175/C193/C201/C202/C226/C227/C228/C187/C192/C176/ 72.1001uF 11% -11%', ['C175', 'C193', 'C201', 'C202', 'C226', 'C227', 'C228', 'C187', 'C192', 'C176']),
    ('CAP EC1/C45/C63/C69/C97/C145/C154/C146/C147/C152/C153/ 89.8uF 15% -15%', ['EC1', 'C45', 'C63', 'C69', 'C97', 'C145', 'C154', 'C146', 'C147', 'C152', 'C153']),
    ('CAPC2\\C46\\C47\\C4\\C5\\C6\\C42\\C23\\C24\\C25\\C26\\C27\\C28\\C29\\C17\\C10\\C11\\C21\\C13\\C14\\C18 320.22UF +20% -20%', ['C2', 'C46', 'C47', 'C4', 'C5', 'C6', 
        'C42', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C17', 'C10', 'C11', 'C21', 'C13', 'C14', 'C18']),  
    ('DSC-C30', ['C30']),
    ('DSC-CP[C58]', ['C58']),
    ('DSC-CP[C58, C85]', ['C58', 'C85']),
    ('CAP.EC2 Reversed!', ['EC2']),
    ('JSCAN U10-23', ['U10']),
    ('CAPC26+C28 69pF 5% -5%', ['C26', 'C28']),
    ('INDL1 10u 10% -10%', ['L1']),
    ('TRNQ1 BC847B', ['Q1']),
    ('TRPQ37 BC857B', ['Q37']),
    ('MOSQ8 2N7002ET1G', ['Q8']),
    ('TRNTR1 BC847B', ['TR1']),
    ('DIOD1-D1 !BAV170_D', ['D1','D1', 'BAV170']),
    ('ZENZ1 GWMMSZ5232B', ['Z1']),
    ('TVS D11', ['D11']),
    ('TVS DD2-Z2 !CDSOT23-SM712', ['DD2', 'Z2', 'CDSOT23', 'SM712']),
    ('LEDLD2 LHRF12243/F139/A', ['LD2', 'LHRF12243', 'F139']),
    ('VDR1 PRESENT?', ['VDR1']),
    ('RELAY RL1 HF170F12-2H1DTF', ['RL1']),
    ('OPTC OC3 K10104A', ['OC3']),
    ('TRCTY1 BTP16-700BWRG', ['TY1', 'BTP16']),
    ('T1 5-7 Presence test', ['T1']),
    ('TRFVT1-1', ['VT1']),
    ('D13-01 ', ['D13']),
    ('C303', ['C303']),
    ('UNKNOWN FORMAT 123', [])
])
def test__getComponentsFromSanitizedString(parser, inputText, expectedOutput):
    sanitized = parser._sanitizeToAlphaNumeric(inputText)
    assert parser._getComponentsFromSanitizedString(sanitized) == expectedOutput


def test_parse(parser):
    inputData = [
        'LNKR16 182-183',
        'RESRB1-1-8 10K 5%',
        'RES R142/R143 50 1%',
        'RESNTC1 4.7 20%',
        'LNK R169 + RESR154 220K 5%', 
        'RES TR42-RBE/TR48-RBE 25.85K 30%', 
        'RESR270 // R275+C151 6.96K 10%',
        'CAP EC1/C45/C63/C69/C97/C145/C154/C146/C147/C152/C153/ 89.8uF 15% -15%',
        'C303-3',
        'CAPC26+C28 69pF 5% -5%',
        'DIOD1-D1 !BAV170_D'
    ]
    expected = sorted(['R16', 'RB1', 'R142', 'R143', 'NTC1', 'R169', 'R154', 'TR42', 'TR48', 'R270', 'R275', 'C151',
        'EC1', 'C45', 'C63', 'C69', 'C97', 'C145', 'C154', 'C146', 'C147', 'C152', 'C153', 'C303', 'C26', 'C28', 'D1', 'BAV170'
    ])

    result = sorted(parser.parse(inputData))
    assert expected == result
    

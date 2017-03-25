from collections import defaultdict

def natalie(words):
    "Find the best Portmanteau word formed from any two of the list of words."
    # First find all (start, mid, end) triples, then find the best scoring one
    triples = alltriples(words)
    if not triples: return None
    return ''.join(max(triples, key=portman_score))

def alltriples(words):
    """All (start, mid, end) pairs where start+mid and mid+end are in words
    (and all three parts are non-empty)."""
    # First compute all {mid: [end]} pairs, then for each (start, mid) pair,
    # grab the [end...] entries, if any.  This approach make two O(N)
    # passes over the words (and O(number of letters) for each word), but is
    # much more efficient than the naive O(N^2) algorithm of looking at all
    # word pairs.
    ends = compute_ends(words)
    return [(start, mid, end)
            for w in words
            for start, mid in splits(w)
            for end in ends[mid]
            if w != mid+end]

def splits(w):
    "Return a list of splits of the word w into two non-empty pieces."
    return [(w[:i], w[i:]) for i in range(1, len(w))]

def compute_ends(words):
    "Return a dict of {mid: [end, ...]} entries."
    ends = defaultdict(list)
    for w in words:
        for mid, end in splits(w):
            ends[mid].append(end)
    return ends

def portman_score(triple):
    "Return the numeric score for a (start, mid, end) triple."
    S, M, E = map(len, triple)
    T = S+M+E
    return T - abs(S-T/4.) - abs(M-T/2.) - abs(E-T/4.) 

def test_natalie():
    "Some test cases for natalie"
    assert (natalie(['eskimo', 'escort', 'kimchee', 'kimono', 'cheese'])
            == 'eskimono')
    assert (natalie(['kimono', 'kimchee', 'cheese', 'serious', 'us', 'usage'])
            == 'kimcheese')
    assert (natalie(['circus', 'elephant', 'lion', 'opera', 'phantom'])
            == 'elephantom')
    assert (natalie(['adolescent', 'scented', 'centennial', 'always',
                    'ado', 'centipede'])
            in ( 'adolescented', 'adolescentennial', 'adolescentipede'))
    assert (natalie(['programmer', 'coder', 'partying', 'merrymaking'])
            == 'programmerrymaking')
    assert (natalie(['int', 'intimate', 'hinter', 'hint', 'winter'])
            == 'hintimate')
    assert (natalie(['morass', 'moral', 'assassination'])
            == 'morassassination')
    assert (natalie(['entrepreneur', 'academic', 'doctor',
                     'neuropsychologist', 'neurotoxin', 'scientist', 'gist'])
            in ('entrepreneuropsychologist', 'entrepreneurotoxin'))
    assert (natalie(['perspicacity', 'cityslicker', 'capability', 'capable'])
            == 'perspicacityslicker')
    assert (natalie(['backfire', 'fireproof', 'backflow', 'flowchart',
                     'background', 'groundhog'])
            == 'backgroundhog')
    assert (natalie(['streaker', 'nudist', 'hippie', 'protestor',
                     'disturbance', 'cops'])
            == 'nudisturbance')
    assert (natalie(['night', 'day']) == None)
    assert (natalie(['dog', 'dogs']) == None)
    assert (natalie(['test']) == None)
    assert (natalie(['']) ==  None)
    assert (natalie(['ABC', '123']) == None)
    assert (natalie([]) == None)
    assert (natalie(['pedestrian', 'pedigree', 'green', 'greenery'])
            == 'pedigreenery')
    assert (natalie(['armageddon', 'pharma', 'karma', 'donald', 'donut'])
            == 'pharmageddon')
    assert (natalie(['lagniappe', 'appendectomy', 'append', 'lapin'])
            == 'lagniappendectomy')
    assert (natalie(['angler', 'fisherman', 'boomerang', 'frisbee', 'rangler',
                     'ranger', 'rangefinder'])
            in ('boomerangler', 'boomerangefinder'))
    assert (natalie(['freud', 'raelian', 'dianetics', 'jonestown', 'moonies'])
            == 'freudianetics')
    assert (natalie(['atheist', 'math', 'athlete', 'psychopath'])
            in ('psychopatheist', 'psychopathlete'))
    assert (natalie(['hippo', 'hippodrome', 'potato', 'dromedary'])
            == 'hippodromedary')
    assert (natalie(['taxi', 'taxicab', 'cabinet', 'cabin',
                     'cabriolet', 'axe'])
            in ('taxicabinet', 'taxicabriolet'))
    assert (natalie(['pocketbook', 'bookmark', 'bookkeeper', 'goalkeeper'])
            in ('pocketbookmark', 'pocketbookkeeper'))
    assert (natalie(['athlete', 'psychopath', 'athletic', 'axmurderer'])
            in ('psychopathlete', 'psychopathletic'))
    assert (natalie(['info', 'foibles', 'follicles'])
            == 'infoibles')
    assert (natalie(['moribund', 'bundlers', 'bundt'])
            == 'moribundlers')
test_natalie()
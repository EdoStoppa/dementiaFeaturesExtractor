BOY       = ['boy', 'son', 'brother', 'male child']
GIRL      = ['girl', 'daughter', 'sister', 'female child']
WOMAN     = ['woman', 'mom', 'mother', 'lady', 'parent', 'female', 'adult', 'grownup']
KITCHEN   = ['kitchen', 'room']
EXTERIOR  = ['exterior', 'outside', 'garden', 'yard', 'outdoors', 'backyard', 'driveway', 'path', 'tree', 'bush']
COOKIE    = ['cookie', 'biscuit', 'cake', 'treat']
JAR       = ['jar', 'container', 'crock', 'pot']
STOOL     = ['stool', 'seat', 'chair', 'ladder']
SINK      = ['sink', 'basin', 'washbasin', 'washbowl', 'washstand', 'tap']
PLATE     = ['plate']
DISHCLOTH = ['dishcloth', 'dishrag', 'rag', 'cloth', 'napkin', 'towel']
WATER     = ['water', 'dishwater', 'liquid']
WINDOW    = ['window', 'frame', 'glass']
CUPBOARD  = ['cupboard', 'closet', 'shelf']
DISHES    = ['dish', 'dishes', 'cup', 'cups', 'counter']
CURTAINS  = ['curtain', 'curtains', 'drape', 'drapes', 'drapery', 'drapery', 'blind', 'blinds', 'screen', 'screens']
STEAL     = ['take', 'steal', 'taking', 'stealing']
FALL      = ['fall', 'falling', 'slip', 'slipping']
WASH      = ['wash', 'dry', 'clean', 'washing', 'drying', 'cleaning']
OVERFLOW  = ['overflow', 'spill', 'overflowing', 'spilling']


############################## KEYWORDS BY PHOTO SPLIT ############################

# ----------------------
# Divide image in half
# ----------------------

def get_leftside_keyword_set():
    return  BOY + GIRL + COOKIE + JAR + STOOL + CUPBOARD + STEAL + FALL + KITCHEN


def get_rightside_keyword_set():
    return  (WOMAN + EXTERIOR + SINK + PLATE + DISHCLOTH + WATER + WINDOW + DISHES + CURTAINS
            + WASH + OVERFLOW + CUPBOARD + KITCHEN)


# ----------------------
# Divide image in 4 vertical strips
# ----------------------

def get_farleft_keyword_set():
    return  GIRL + COOKIE + JAR + STOOL + CUPBOARD + STEAL + KITCHEN + CUPBOARD


def get_centerleft_keyword_set():
    return  BOY + COOKIE + STOOL + STEAL + FALL + KITCHEN + CUPBOARD 


def get_farright_keyword_set():
    return  (WOMAN + EXTERIOR + SINK + PLATE + DISHCLOTH + WATER + WINDOW + DISHES + CURTAINS + WASH
            + OVERFLOW + KITCHEN + CUPBOARD)


def get_centerright_keyword_set():
    return EXTERIOR + WINDOW + DISHES + CURTAINS + KITCHEN + CUPBOARD


# ----------------------
# Divide image in 4 quadrants
# ----------------------

def get_NW_keyword_set():
    return GIRL + COOKIE + JAR + CUPBOARD + STEAL + BOY + COOKIE + KITCHEN


def get_NE_keyword_set():
    return WOMAN + EXTERIOR + PLATE + DISHCLOTH + WASH + WINDOW + CURTAINS + KITCHEN


def get_SE_keyword_set():
    return WOMAN + SINK + WATER + DISHES + OVERFLOW + CUPBOARD + KITCHEN


def get_SW_keyword_set():
    return GIRL + STOOL + FALL + CUPBOARD + KITCHEN

############################## KEYWORDS ENDED ############################

# Extract all the words from the interview
def get_all_words_from_interview(interview):
    words = []
    for uttr in interview:
        words += [word.lower() for word in uttr["token"] if word.isalpha()]
    return words

# Return the list of keywords uttered during the conversation
def get_keywords(words, keyword_set):
    return [w for w in words if w in keyword_set]

# Raw count keywords
# (proxy for the 'keyword count' features)
def count_of_general_keyword(words, keywords):
    if not words or not keywords:
        return 0
    else:
        return len(keywords)

# Keywords / all words uttered
# (this is a measure of how 'relevant' the speech is)
def general_keyword_to_non_keyword_ratio(words, keywords):
    if not words or not keywords:
        return 0
    else:
        return len(keywords) / float(len(words))

# Unique keywords uttered / total set of possible keywords
# (proxy for the 'binary count' features)
def percentage_of_general_keywords_mentioned(words, keywords, len_keyword_set):
    if not words or not keywords:
        return 0
    else:
        return len(set(keywords)) / float(len_keyword_set)

# Unique keywords uttered / total_keywords_uttered
# (Measure of the diversity of keywords uttered)
def general_keyword_type_to_token_ratio(words, keywords):
    if not words or not keywords:
        return 0
    else:
        return len(set(keywords)) / float(len(keywords))

# Compute all the features for each section provided
def compute_features_by_section(words, section_keyset_pairs):
    feat_dict = {}
    for section, keyword_set in section_keyset_pairs:
            keywords = get_keywords(words, keyword_set)

            feat_dict[f"{section}_count"] = count_of_general_keyword(words, keywords)
            feat_dict[f"{section}_ty_to_tok_ratio"] = general_keyword_type_to_token_ratio(words, keywords)
            feat_dict[f"{section}_kw_to_w_ratio"]  = general_keyword_to_non_keyword_ratio(words, keywords)
            feat_dict[f"prcnt_{section}_uttered"] = percentage_of_general_keywords_mentioned(words, keywords, len(keyword_set))
            
    return feat_dict

# Main function that extract the features based on the photo split provided
def get_spatial_features(interview, photo_split):
    # First, check if the 
    divisions = ['halves', 'strips', 'quadrants']
    if photo_split not in divisions:
        raise ValueError("'photo_split' must be one of 'halves', 'quadrants' or 'strips', not: %s" % photo_split)

    # Get all the words uttered in the interview
    words = get_all_words_from_interview(interview)

    if photo_split == 'halves':

        # This will extract:
        #    1) leftside_keywords
        #       (These are keywords which only appear on the left side of the image)
        #    2) rightside_keywords
        #       (These are keywords which only appear on the right side of the image)
        section_keyset_pairs = [('ls', get_leftside_keyword_set()), ('rs', get_rightside_keyword_set())]

        feat_dict = compute_features_by_section(words, section_keyset_pairs)

        return feat_dict


    if photo_split == 'strips':

        # This will extract:
        #    1) farleft_keywords
        #       (These are keywords which only appear on the farleft side of the image)
        #    2) centerleft_keywords
        #       (These are keywords which only appear on the centerleft side of the image)
        #    3) farright_keywords
        #       (These are keywords which only appear on the farright side of the image)
        #    4) centerright_keywords
        #       (These are keywords which only appear on the centerright side of the image)
        section_keyset_pairs = [('farleft', get_farleft_keyword_set()), ('centerleft', get_centerleft_keyword_set()),
                                ('farright', get_farright_keyword_set()), ('centerright', get_centerright_keyword_set())]

        feat_dict = compute_features_by_section(words, section_keyset_pairs)

        return feat_dict


    if photo_split == 'quadrants':

         # This will extract:
        #    1) NW_keywords
        #       (These are keywords which only appear in the North-West quadrant of the image)
        #    2) NE_keywords
        #       (These are keywords which only appear in the North-East quadrant of the image)
        #    3) SE_keywords
        #       (These are keywords which only appear in the South-East quadrant of the image)
        #    4) SW_keywords
        #       (These are keywords which only appear in the South-West quadrant of the image)
        section_keyset_pairs = [('NW', get_NW_keyword_set()), ('NE', get_NE_keyword_set()),
                                ('SE', get_SE_keyword_set()), ('SW', get_SW_keyword_set())]

        feat_dict = compute_features_by_section(words, section_keyset_pairs)

        return feat_dict
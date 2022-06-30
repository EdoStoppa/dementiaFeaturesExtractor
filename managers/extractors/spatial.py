# Extended keyword set
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

# Action words
STEAL    = ['take', 'steal', 'taking', 'stealing']
FALL     = ['fall', 'falling', 'slip', 'slipping']
WASH     = ['wash', 'dry', 'clean', 'washing', 'drying', 'cleaning']
OVERFLOW = ['overflow', 'spill', 'overflowing', 'spilling']

# =====================================
# Feature sets
# =====================================
def get_keyword_set():
    return BOY + GIRL + WOMAN + KITCHEN + EXTERIOR + COOKIE + JAR + STOOL + SINK + PLATE + DISHCLOTH + WATER + WINDOW + CUPBOARD + DISHES + CURTAINS + STEAL + FALL + WASH + OVERFLOW

# ----------------------
# Divide image in half
# ----------------------


def get_leftside_keyword_set():
    return BOY + GIRL + COOKIE + JAR + STOOL + CUPBOARD + STEAL + FALL + KITCHEN


def get_rightside_keyword_set():
    return WOMAN + EXTERIOR + SINK + PLATE + DISHCLOTH + WATER + WINDOW + DISHES + CURTAINS + WASH + OVERFLOW + CUPBOARD + KITCHEN
# ----------------------

# ----------------------
# Divide image in 4 vertical strips
# ----------------------


def get_farleft_keyword_set():
    return GIRL + COOKIE + JAR + STOOL + CUPBOARD + STEAL + KITCHEN + CUPBOARD


def get_centerleft_keyword_set():
    return BOY + COOKIE + STOOL + STEAL + FALL + KITCHEN + CUPBOARD 


def get_farright_keyword_set():
    return WOMAN + EXTERIOR + SINK + PLATE + DISHCLOTH + WATER + WINDOW + DISHES + CURTAINS + WASH + OVERFLOW + KITCHEN + CUPBOARD


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


# # -------------------------------------
# # LS/RS switch
# # -------------------------------------
def count_ls_rs_switches(interview):
    leftside  = get_leftside_keyword_set()
    rightside = get_rightside_keyword_set()
    words = getAllWordsFromInterview(interview)

    last_side    = None
    current      = None
    switch_count = 0

    for word in words:
        if word in leftside:
            current = 'left'
        if word in rightside:
            current = 'right'

        if last_side is None and current:
            last_side = current
        else:
            if current and last_side and (current != last_side):
                switch_count += 1
                last_side = current

    return switch_count


def getAllWordsFromInterview(interview):
    words = []
    for uttr in interview:
        words += [word.lower() for word in uttr["token"] if word.isalpha()]
    return words

# Raw count keywords
# (proxy for the 'keyword count' features)
def count_of_general_keyword(interview, keyword_set):
    words = getAllWordsFromInterview(interview)
    keywords = [w for w in words if w in keyword_set]
    if not words or not keywords:
        return 0
    else:
        return len(keywords)


# Keywords / all words uttered
# (this is a measure of how 'relevant' the speech is)
def general_keyword_to_non_keyword_ratio(interview, keyword_set):
    words = getAllWordsFromInterview(interview)
    keywords = [w for w in words if w in keyword_set]
    if not words or not keywords:
        return 0
    else:
        return len(keywords) / float(len(words))


# unique keywords uttered / total set of possible keywords
# (proxy for the 'binary count' features)
def percentage_of_general_keywords_mentioned(interview, keyword_set):
    words = getAllWordsFromInterview(interview)
    keywords = [w for w in words if w in keyword_set]
    if not words or not keywords:
        return 0
    else:
        return len(set(keywords)) / float(len(keyword_set))


# unique keywords uttered / total_keywords_uttered
# (Measure of the diversity of keywords uttered)
def general_keyword_type_to_token_ratio(interview, keyword_set):
    words = getAllWordsFromInterview(interview)
    keywords = [w for w in words if w in keyword_set]
    if not words or not keywords:
        return 0
    else:
        return len(set(keywords)) / float(len(keywords))


def get_spatial_features(interview, photo_split):
    divisions = ['halves', 'strips', 'quadrants']

    if photo_split not in divisions:
        raise ValueError("'photo_split' must be one of 'halves', 'quadrants' or 'strips', not: %s" % photo_split)

    feat_dict = {}

    if photo_split == 'halves':
        # leftside_keywords
        # (These are keywords which only appear on the left side of the image)
        leftside_keywords = get_leftside_keyword_set()
        feat_dict["ls_count"] = count_of_general_keyword(interview, leftside_keywords)
        feat_dict["ls_ty_to_tok_ratio"] = general_keyword_type_to_token_ratio(
            interview, leftside_keywords)
        feat_dict["ls_kw_to_w_ratio"]  = general_keyword_to_non_keyword_ratio(
            interview, leftside_keywords)
        feat_dict["prcnt_ls_uttered"] = percentage_of_general_keywords_mentioned(
            interview, leftside_keywords)

        # rightside_keywords
        # (These are keywords which only appear on the right side of the image)
        rightside_keywords = get_rightside_keyword_set()
        feat_dict["rs_count"] = count_of_general_keyword(interview, rightside_keywords)
        feat_dict["rs_ty_to_tok_ratio"] = general_keyword_type_to_token_ratio(
            interview, rightside_keywords)
        feat_dict["rs_kw_to_w_ratio"]  = general_keyword_to_non_keyword_ratio(
            interview, rightside_keywords)
        feat_dict["prcnt_rs_uttered"] = percentage_of_general_keywords_mentioned(
            interview, rightside_keywords)

        # feat_dict["count_ls_rs_switches"] = count_ls_rs_switches(interview)
        return feat_dict

    if photo_split == 'strips':
        # farleft_keywords
        # (These are keywords which only appear on the farleft side of the image)
        farleft_keywords = get_farleft_keyword_set()
        feat_dict["farleft_count"] = count_of_general_keyword(interview, farleft_keywords)
        feat_dict["farleft_ty_to_tok_ratio"] = general_keyword_type_to_token_ratio(
            interview, farleft_keywords)
        feat_dict["farleft_kw_to_w_ratio"]  = general_keyword_to_non_keyword_ratio(
            interview, farleft_keywords)
        feat_dict["prcnt_farleft_uttered"] = percentage_of_general_keywords_mentioned(
            interview, farleft_keywords)

        # centerleft_keywords
        # (These are keywords which only appear on the centerleft side of the image)
        centerleft_keywords = get_centerleft_keyword_set()
        feat_dict["centerleft_count"] = count_of_general_keyword(interview, centerleft_keywords)
        feat_dict["centerleft_ty_to_tok_ratio"] = general_keyword_type_to_token_ratio(
            interview, centerleft_keywords)
        feat_dict["centerleft_kw_to_w_ratio"]  = general_keyword_to_non_keyword_ratio(
            interview, centerleft_keywords)
        feat_dict["prcnt_centerleft_uttered"] = percentage_of_general_keywords_mentioned(
            interview, centerleft_keywords)

        # farright_keywords
        # (These are keywords which only appear on the farright side of the image)
        farright_keywords = get_farright_keyword_set()
        feat_dict["farright_count"] = count_of_general_keyword(interview, farright_keywords)
        feat_dict["farright_ty_to_tok_ratio"] = general_keyword_type_to_token_ratio(
            interview, farright_keywords)
        feat_dict["farright_kw_to_w_ratio"]  = general_keyword_to_non_keyword_ratio(
            interview, farright_keywords)
        feat_dict["prcnt_farright_uttered"] = percentage_of_general_keywords_mentioned(
            interview, farright_keywords)

        # centerright_keywords
        # (These are keywords which only appear on the centerright side of the image)
        centerright_keywords = get_centerright_keyword_set()
        feat_dict["centerright_count"] = count_of_general_keyword(interview, centerright_keywords)
        feat_dict["centerright_ty_to_tok_ratio"] = general_keyword_type_to_token_ratio(
            interview, centerright_keywords)
        feat_dict["centerright_kw_to_w_ratio"]  = general_keyword_to_non_keyword_ratio(
            interview, centerright_keywords)
        feat_dict["prcnt_centerright_uttered"] = percentage_of_general_keywords_mentioned(
            interview, centerright_keywords)

        return feat_dict

    if photo_split == 'quadrants':
        # NW_keywords
        # (These are keywords which only appear on the centerright side of the image)
        NW_keywords = get_NW_keyword_set()
        feat_dict["NW_count"] = count_of_general_keyword(interview, NW_keywords)
        feat_dict["NW_ty_to_tok_ratio"] = general_keyword_type_to_token_ratio(
            interview, NW_keywords)
        feat_dict["NW_kw_to_w_ratio"]  = general_keyword_to_non_keyword_ratio(
            interview, NW_keywords)
        feat_dict["prcnt_NW_uttered"] = percentage_of_general_keywords_mentioned(
            interview, NW_keywords)

        # NE_keywords
        # (TheNE are keywords which only appear on the centerright side of the image)
        NE_keywords = get_NE_keyword_set()
        feat_dict["NE_count"] = count_of_general_keyword(interview, NE_keywords)
        feat_dict["NE_ty_to_tok_ratio"] = general_keyword_type_to_token_ratio(
            interview, NE_keywords)
        feat_dict["NE_kw_to_w_ratio"]  = general_keyword_to_non_keyword_ratio(
            interview, NE_keywords)
        feat_dict["prcnt_NE_uttered"] = percentage_of_general_keywords_mentioned(
            interview, NE_keywords)

        # SE_keywords
        # (TheNE are keywords which only appear on the centerright side of the image)
        SE_keywords = get_SE_keyword_set()
        feat_dict["SE_count"] = count_of_general_keyword(interview, SE_keywords)
        feat_dict["SE_ty_to_tok_ratio"] = general_keyword_type_to_token_ratio(
            interview, SE_keywords)
        feat_dict["SE_kw_to_w_ratio"]  = general_keyword_to_non_keyword_ratio(
            interview, SE_keywords)
        feat_dict["prcnt_SE_uttered"] = percentage_of_general_keywords_mentioned(
            interview, SE_keywords)

        # SW_keywords
        # (TheNE are keywords which only appear on the centerright side of the image)
        SW_keywords = get_SW_keyword_set()
        feat_dict["SW_count"] = count_of_general_keyword(interview, SW_keywords)
        feat_dict["SW_ty_to_tok_ratio"] = general_keyword_type_to_token_ratio(
            interview, SW_keywords)
        feat_dict["SW_kw_to_w_ratio"]  = general_keyword_to_non_keyword_ratio(
            interview, SW_keywords)
        feat_dict["prcnt_SW_uttered"] = percentage_of_general_keywords_mentioned(
            interview, SW_keywords)

        return feat_dict
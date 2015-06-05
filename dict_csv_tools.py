def public(mydict):
    return_me = {}
    for k, v in mydict.iteritems():
        if k[0] == "_":
            continue
        return_me[k] = v
    return return_me

